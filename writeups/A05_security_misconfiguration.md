# A05 — Security Misconfiguration

## What it is

Security misconfiguration covers a broad class of issues where insecure
default settings, exposed debug interfaces, or missing access controls
make a system vulnerable. VulnBank has two: an unauthenticated admin
panel and Flask debug mode enabled in production.

## Vulnerable code

```python
# No auth check on admin route
@app.route("/admin")
def admin():
    users = db.execute("SELECT id, username, role FROM users").fetchall()
    accounts = db.execute("SELECT * FROM accounts").fetchall()
    return render_template("admin.html", users=users, accounts=accounts)

# Debug mode exposes interactive Python shell
app.run(debug=True)
```

## Exploit

### Unauthenticated admin access

Visit /admin with no session cookie. Server returns full user and
account data with HTTP 200.

### Debug mode RCE

Flask's Werkzeug debugger is accessible at /**debugger** and provides
an interactive Python console that executes on the server. While it
requires a PIN in newer versions, the PIN is derivable from server
properties exposed in the error pages.

Running `python -m exploits.05_misconfig`:

## Proof
