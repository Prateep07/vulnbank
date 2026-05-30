# A01 — Broken Access Control (IDOR)

## What it is
Broken access control means the application fails to enforce restrictions
on what authenticated users are allowed to do. In VulnBank, this appears
as an Insecure Direct Object Reference (IDOR) — account IDs are exposed
in the URL and the server never checks ownership before returning data.

## Vulnerable code
```python
@app.route("/account/<int:account_id>")
def view_account(account_id):
    if "user_id" not in session:
        return redirect(url_for("login"))
    account = db.execute(
        "SELECT * FROM accounts WHERE id=?", (account_id,)
    ).fetchone()
    return render_template("dashboard.html", accounts=[account])
```
The route checks that the user is logged in, but never checks that
the account belongs to the logged-in user.

## Exploit
Logged in as alice (user_id=2, account_id=2), visit /account/1.
The server returns admin's account data with no error.

Running `python -m exploits.02_idor` confirms HTTP 200 is returned
for all three accounts regardless of who is logged in.

## Proof