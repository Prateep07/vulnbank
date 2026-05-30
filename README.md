# VulnBank — OWASP Top 10 Vulnerable Web App

A deliberately vulnerable Flask banking application demonstrating all
10 OWASP Top 10 vulnerabilities (2021 edition), with working exploit
scripts and fix documentation for each.

Built as a cybersecurity portfolio project. Every vulnerability is
intentional, documented, and accompanied by a Python exploit that
demonstrates the attack programmatically.

> **Warning:** This application is intentionally insecure. Run it
> only on localhost, never expose it to a network.

---

## Vulnerabilities covered

| ID  | Vulnerability                  | Location              | Exploit script                       |
| --- | ------------------------------ | --------------------- | ------------------------------------ |
| A01 | Broken Access Control (IDOR)   | `GET /account/<id>`   | `exploits/02_idor.py`                |
| A02 | Cryptographic Failures (MD5)   | `database.py`         | `exploits/08_crack_hashes.py`        |
| A03 | SQL Injection                  | `POST /login`         | `exploits/01_sqli.py`                |
| A04 | Insecure Design (logic flaw)   | `POST /transfer`      | `exploits/04_logic_flaw.py`          |
| A05 | Security Misconfiguration      | `/admin` + debug mode | `exploits/05_misconfig.py`           |
| A06 | Vulnerable Components          | `requirements.txt`    | `pip install safety && safety check` |
| A07 | Auth Failures (brute force)    | `POST /login`         | `exploits/03_bruteforce.py`          |
| A08 | Insecure Deserialisation (RCE) | `GET /restore`        | `exploits/06_pickle_rce.py`          |
| A09 | Logging Failures               | all routes            | (absence of logs — see writeup)      |
| A10 | SSRF                           | `POST /import`        | `exploits/07_ssrf.py`                |

---

## Setup

```bash
git clone https://github.com/YOURUSERNAME/vulnbank
cd vulnbank
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
python database.py
python app.py
```

App runs at `http://localhost:5000`

**Test accounts:**
| Username | Password | Role |
|----------|----------|------|
| admin | admin123 | admin |
| alice | password1 | user |
| bob | qwerty | user |

---

## Running the exploits

In a second terminal (with the app running):

```bash
# Run all exploits
python -m exploits.run_all

# Or run individually
python -m exploits.01_sqli
python -m exploits.02_idor
python -m exploits.03_bruteforce
python -m exploits.04_logic_flaw
python -m exploits.05_misconfig
python -m exploits.06_pickle_rce
python -m exploits.07_ssrf
python -m exploits.08_crack_hashes
```

---

## Project structure

```
vulnbank/
├── app.py                  # Vulnerable Flask app
├── database.py             # DB init with weak password hashing
├── requirements.txt        # Intentionally outdated dependencies (A06)
├── templates/              # Jinja2 HTML templates
├── exploits/               # Python attack scripts (one per vuln)
└── writeups/               # Markdown documentation per vulnerability
```

---

## Writeups

Detailed breakdown of each vulnerability — vulnerable code, exploit
walkthrough, proof of concept output, and the fix:

- [A01 — Broken Access Control](writeups/A01_broken_access_control.md)
- [A02 — Cryptographic Failures](writeups/A02_cryptographic_failures.md)
- [A03 — SQL Injection](writeups/A03_injection.md)
- [A04 — Insecure Design](writeups/A04_insecure_design.md)
- [A05 — Security Misconfiguration](writeups/A05_security_misconfiguration.md)
- [A07 — Auth Failures](writeups/A07_auth_failures.md)
- [A08 — Insecure Deserialisation](writeups/A08_insecure_deserialisation.md)
- [A10 — SSRF](writeups/A10_ssrf.md)

---

## What I learned

- How each OWASP Top 10 vulnerability works at the code level
- How to exploit them programmatically using Python's `requests` library
- The minimal code change required to fix each one
- Why secure defaults (parameterised queries, bcrypt, session rotation)
  exist and what breaks without them
