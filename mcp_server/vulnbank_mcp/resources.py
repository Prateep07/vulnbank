from pathlib import Path
from nitrostack import ExecutionContext, injectable, resource

@injectable(deps=[])
class VulnBankResources:
    def __init__(self):
        self.repo_path = Path(__file__).resolve().parents[2]

    @resource(
        uri="vulnbank://readme",
        name="VulnBank README",
        description="VulnBank project README",
        mime_type="text/markdown"
    )
    async def get_readme(self, context: ExecutionContext):
        path = self.repo_path / "README.md"

        if not path.exists():
            text = "No README.md found in the repo."
        else:
            text = path.read_text(encoding="utf-8")

        return {
            "contents": [
                {
                    "uri": "vulnbank://readme",
                    "mimeType": "text/markdown",
                    "text": text
                }
            ]
        }

    @resource(
    uri="writeup://{vuln_id}",
    name="Vulnerability Writeup",
    description="VulnBank vulnerability writeup",
    mime_type="text/markdown"
)
    async def get_writeup(
        self,
        vuln_id: str,
        context: ExecutionContext
    ):
        writeups_dir = self.repo_path / "writeups"
    
        if not writeups_dir.exists():
            text = f"No writeups/ folder found at {writeups_dir}"
        else:
            matches = list(writeups_dir.glob(f"{vuln_id}_*.md"))
    
            if not matches:
                text = f"No writeup found for {vuln_id}"
            else:
                text = matches[0].read_text(encoding="utf-8")
    
        return {
            "contents": [
                {
                    "uri": f"writeup://{vuln_id}",
                    "mimeType": "text/markdown",
                    "text": text
                }
            ]
        }