from flask import Flask, request, session, redirect, url_for, render_template, abort
import hashlib, sqlite3, pickle, base64, requests as req
from database import get_db

app = Flask(__name__)
app.secret_key = "secret"           # A07 - weak hardcoded key

# ─── A02: MD5 helper ───────────────────────────────────────────────────────────
def md5(p):
    return hashlib.md5(p.encode()).hexdigest()

# ─── A03: SQL Injection — login ────────────────────────────────────────────────
@app.route("/", methods=["GET", "POST"])
@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        # VULNERABLE: string interpolation in SQL query
        query = f"SELECT * FROM users WHERE username='{username}' AND password='{md5(password)}'"
        db = get_db()
        user = db.execute(query).fetchone()
        if user:
            session["user_id"] = user["id"]
            session["username"] = user["username"]
            session["role"] = user["role"]
            return redirect(url_for("dashboard"))
        error = "Invalid credentials"
    return render_template("login.html", error=error)

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

# ─── A01: Broken Access Control — IDOR ─────────────────────────────────────────
@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect(url_for("login"))
    db = get_db()
    # Shows only your accounts — but /account/<id> has IDOR
    accounts = db.execute(
        "SELECT * FROM accounts WHERE user_id=?", (session["user_id"],)
    ).fetchall()
    return render_template("dashboard.html", accounts=accounts)

@app.route("/account/<int:account_id>")
def view_account(account_id):
    if "user_id" not in session:
        return redirect(url_for("login"))
    db = get_db()
    # VULNERABLE: no ownership check
    account = db.execute(
        "SELECT * FROM accounts WHERE id=?", (account_id,)
    ).fetchone()
    txns = db.execute(
        "SELECT * FROM transactions WHERE from_account=? OR to_account=?",
        (account_id, account_id)
    ).fetchall()
    if not account:
        abort(404)
    return render_template("dashboard.html", accounts=[account], txns=txns)

# ─── A04: Insecure Design — no limit/validation on transfers ───────────────────
@app.route("/transfer", methods=["GET", "POST"])
def transfer():
    if "user_id" not in session:
        return redirect(url_for("login"))
    msg = None
    if request.method == "POST":
        try:
            amount = float(request.form["amount"])
            to_acc = int(request.form["to_account"])
            db = get_db()
            # VULNERABLE: no balance check, no rate limit, negative amounts allowed
            from_acc = db.execute(
                "SELECT id FROM accounts WHERE user_id=?", (session["user_id"],)
            ).fetchone()["id"]
            db.execute("UPDATE accounts SET balance = balance - ? WHERE id=?", (amount, from_acc))
            db.execute("UPDATE accounts SET balance = balance + ? WHERE id=?", (amount, to_acc))
            db.execute("INSERT INTO transactions (from_account, to_account, amount) VALUES (?,?,?)",
                       (from_acc, to_acc, amount))
            db.commit()
            msg = f"Transferred ${amount} to account #{to_acc}"
        except Exception as e:
            msg = f"Error: {e}"
    return render_template("transfer.html", msg=msg)

# ─── A05: Security Misconfiguration — unprotected admin panel ──────────────────
@app.route("/admin")
def admin():
    # VULNERABLE: no role check whatsoever
    db = get_db()
    users = db.execute("SELECT id, username, role FROM users").fetchall()
    accounts = db.execute("SELECT * FROM accounts").fetchall()
    return render_template("admin.html", users=users, accounts=accounts)

# ─── A08: Insecure Deserialisation — pickle via URL param ──────────────────────
@app.route("/restore")
def restore():
    if "user_id" not in session:
        return redirect(url_for("login"))
    data = request.args.get("data", "")
    if data:
        try:
            # VULNERABLE: deserialising untrusted user input with pickle
            prefs = pickle.loads(base64.b64decode(data))
            return f"Restored preferences: {prefs}"
        except Exception as e:
            return f"Error: {e}", 400
    return "No data provided", 400

# ─── A10: SSRF — user-supplied URL fetched server-side ─────────────────────────
@app.route("/import", methods=["GET", "POST"])
def import_statement():
    if "user_id" not in session:
        return redirect(url_for("login"))
    result = None
    if request.method == "POST":
        url = request.form["url"]
        try:
            # VULNERABLE: fetches any URL including internal ones
            resp = req.get(url, timeout=3)
            result = resp.text[:2000]
        except Exception as e:
            result = f"Error: {e}"
    return render_template("import.html", result=result)

# ─── A09: No logging anywhere in this app (intentional) ────────────────────────

if __name__ == "__main__":
    app.run(debug=True)      # A05: debug mode exposes Werkzeug shell at /__debugger__