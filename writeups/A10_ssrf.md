# A10 — Server-Side Request Forgery (SSRF)

## What it is

SSRF occurs when the server makes HTTP requests to user-supplied URLs.
The request originates from the server itself, giving the attacker
access to internal services that are unreachable from the public internet.

## Vulnerable code

```python
url = request.form["url"]
resp = requests.get(url, timeout=3)
result = resp.text[:2000]
```

## Exploit

### Internal admin panel bypass

Submitting `http://localhost:5000/admin` as the import URL causes the
server to fetch its own admin panel and return the HTML to us — even
though we are logged out and /admin has no auth check.

### Internal network probing

By submitting RFC1918 addresses (10.x.x.x, 192.168.x.x, 172.16.x.x)
we can map internal services: databases, caches, monitoring tools.

### Cloud metadata theft (critical in production)

On AWS, `http://169.254.169.254/latest/meta-data/iam/security-credentials/`
returns temporary AWS access keys for the server's IAM role.

Running `python -m exploits.07_ssrf`:

## Proof
