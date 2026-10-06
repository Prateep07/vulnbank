import subprocess
import sys
from pathlib import Path
import httpx

try:    
    from mcp.server.fastmcp import FastMCP  # mcp < 2.0
except ModuleNotFoundError:
    from mcp.server.mcpserver import MCPServer as FastMCP  # mcp >= 2.0

VULNBANK_BASE_URL = "http://localhost:5000"
VULNBANK_REPO_PATH = Path(__file__).resolve().parent.parent
EXPLOITS_DIR = VULNBANK_REPO_PATH / "exploits"
mcp = FastMCP("vulnbank-mcp")
client = httpx.Client(base_url=VULNBANK_BASE_URL, follow_redirects=True, timeout=10)

@mcp.tool()
def list_vulnerabilities():
    return [
        "Broken Access Control",
        "Cryptographic Failures",
        "SQL Injection",
        "Insecure Design",
        "Security Misconfiguration",
        "Vulnerable Components",
        "Authentication Failures",
        "Insecure Deserialization",
        "Logging Failures",
        "SSRF"
    ]

@mcp.tool()
def login(username: str, password: str) -> dict:
    resp = client.post("/login", data={"username": username, "password": password})
    logged_in = "login" not in resp.url.path
    return {"status_code": resp.status_code, "logged_in": logged_in, "body": resp.text[:1000]}


@mcp.tool()
def get_dashboard() -> dict:
    resp = client.get("/dashboard")
    return {"status_code": resp.status_code, "body": resp.text[:3000]}

@mcp.tool()
def get_account(account_id: int) -> dict:
    resp = client.get(f"/account/{account_id}")
    return {"status_code": resp.status_code, "body": resp.text[:3000]}

@mcp.tool()
def transfer_funds(to_account: int, amount: float) -> dict:
    resp = client.post("/transfer", data={"to_account": to_account, "amount": amount})
    return {"status_code": resp.status_code, "body": resp.text[:1000]}


@mcp.tool()
def get_admin_panel() -> dict:
    resp = client.get("/admin")
    return {"status_code": resp.status_code, "body": resp.text[:3000]}

ALLOWED_EXPLOITS = {
    "01_sqli",
    "02_idor",
    "03_bruteforce",
    "04_logic_flaw",
    "05_misconfig",
    "06_pickle_rce",
    "07_ssrf",
    "08_crack_hashes",
}

@mcp.tool()
def run_exploit(name: str) -> dict:
    """01_sqli, 02_idor, 03_bruteforce,
    04_logic_flaw, 05_misconfig, 06_pickle_rce, 07_ssrf,
    08_crack_hashes.
    """
    if name not in ALLOWED_EXPLOITS:
        return {"error": f"Unknown exploit '{name}'. Must be one of: {sorted(ALLOWED_EXPLOITS)}"}

    script_path = EXPLOITS_DIR / f"{name}.py"
    if not script_path.exists():
        return {"error": f"Script not found at {script_path}"}

    result = subprocess.run(
        [sys.executable, str(script_path)],
        capture_output=True,
        text=True,
        timeout=30,
    )
    return {
        "exit_code": result.returncode,
        "stdout": result.stdout,
        "stderr": result.stderr,
    }

if __name__ == "__main__":
    mcp.run(transport="stdio")