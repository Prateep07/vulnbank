# A07 — Identification and Authentication Failures

## What it is

Authentication failures include weak session secrets, missing brute-force
protection, and insecure session management. VulnBank uses a hardcoded
weak secret key and has no login rate limiting or account lockout.

## Vulnerable code

```python
app.secret_key = "secret"   # Hardcoded, trivially guessable

# No failed attempt tracking, no lockout, no rate limit
@app.route("/login", methods=["POST"])
def login():
    user = db.execute(query).fetchone()
    if user:
        session["user_id"] = user["id"]
    ...
```

## Exploit

With no lockout, we can iterate a password list at full network speed.
A 15-word toy list cracks alice's password in under a second. With
rockyou.txt (14 million entries), any common password falls in minutes.

The weak secret key means session cookies can be forged if the key
is known — and "secret" is the first entry in any key wordlist.

Running `python -m exploits.03_bruteforce`:

## Proof
