# A04 — Insecure Design (Business Logic Flaw)

## What it is

Insecure design refers to missing or ineffective controls at the
architecture level, not just at the code level. VulnBank's transfer
endpoint performs no business logic validation — amounts, direction,
and limits are completely unchecked.

## Vulnerable code

```python
amount = float(request.form["amount"])
to_acc = int(request.form["to_account"])
db.execute("UPDATE accounts SET balance = balance - ? WHERE id=?", (amount, from_acc))
db.execute("UPDATE accounts SET balance = balance + ? WHERE id=?", (amount, to_acc))
```

## Exploit

Submitting amount=-99999 with to_account pointing to your own account:

- Server executes: `balance = balance - (-99999)` on source account
- Server executes: `balance = balance + (-99999)` on destination
- Net result: the "destination" (your own account) gains $99,999

Running `python -m exploits.04_logic_flaw`:

## Proof
