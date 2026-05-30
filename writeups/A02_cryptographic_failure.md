# A02 — Cryptographic Failures (Weak Password Hashing)

## What it is

The application stores passwords hashed with MD5 — an algorithm designed
for fast checksums, not password storage. MD5 has no salt and runs in
nanoseconds, making offline brute-force trivial with a GPU.

## Vulnerable code

```python
import hashlib
def md5(p):
    return hashlib.md5(p.encode()).hexdigest()

db.execute("INSERT INTO users (username, password) VALUES (?,?)",
           (username, md5(password)))
```

## Exploit

After reading hashes from vulnbank.db, we crack all three with a
15-word wordlist in milliseconds because MD5 is instantaneous to compute.

Running `python -m exploits.08_crack_hashes`:

## Proof
