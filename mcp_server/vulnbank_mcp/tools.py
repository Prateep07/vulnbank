from pydantic import BaseModel, Field

from nitrostack import (
    ExecutionContext,
    injectable,
    tool,
    use_interceptors,
    widget,
)

from .exploit_service import ExploitService
from .interceptors import LoggingInterceptor
from .service import VulnBankService


class EmptyInput(BaseModel):
    pass


class AuthenticateInput(BaseModel):
    api_key: str = Field(
        description="VulnBank MCP API key"
    )


class LoginInput(BaseModel):
    username: str
    password: str


class AccountInput(BaseModel):
    account_id: int


class TransferInput(BaseModel):
    to_account: int
    amount: float


class RunExploitInput(BaseModel):
    name: str = Field(
        description=(
            "Exploit name such as "
            "01_sqli, 02_idor, 03_bruteforce"
        )
    )


@injectable(
    deps=[
        VulnBankService,
        ExploitService
    ]
)
class VulnBankTools:

    def __init__(
        self,
        service: VulnBankService,
        exploit_service: ExploitService
    ):
        self.service = service
        self.exploit_service = exploit_service

    @tool(
        name="authenticate",
        description="Authenticate with the VulnBank MCP server",
        input_schema=AuthenticateInput
    )
    @use_interceptors(LoggingInterceptor)
    async def authenticate(
        self,
        input: AuthenticateInput,
        context: ExecutionContext
    ) -> dict:

        return self.service.authenticate(
            input.api_key
        )

    @tool(
        name="list_vulnerabilities",
        description="List the OWASP vulnerabilities available in VulnBank",
        input_schema=EmptyInput
    )
    @widget("vuln-list")
    @use_interceptors(LoggingInterceptor)
    async def list_vulnerabilities(
        self,
        input: EmptyInput,
        context: ExecutionContext
    ) -> dict:

        self.service.require_auth()

        vulnerabilities = [
            {
                "id": "A01",
                "name": "Broken Access Control"
            },
            {
                "id": "A02",
                "name": "Cryptographic Failures"
            },
            {
                "id": "A03",
                "name": "SQL Injection"
            },
            {
                "id": "A04",
                "name": "Insecure Design"
            },
            {
                "id": "A05",
                "name": "Security Misconfiguration"
            },
            {
                "id": "A06",
                "name": "Vulnerable Components"
            },
            {
                "id": "A07",
                "name": "Authentication Failures"
            },
            {
                "id": "A08",
                "name": "Insecure Deserialization"
            },
            {
                "id": "A09",
                "name": "Logging Failures"
            },
            {
                "id": "A10",
                "name": "SSRF"
            }
        ]

        return {
            "vulnerabilities": vulnerabilities,
            "total": len(vulnerabilities)
        }

    @tool(
        name="login",
        description="Login to the VulnBank application",
        input_schema=LoginInput
    )
    @use_interceptors(LoggingInterceptor)
    async def login(
        self,
        input: LoginInput,
        context: ExecutionContext
    ) -> dict:

        return self.service.login(
            input.username,
            input.password
        )

    @tool(
        name="get_dashboard",
        description="Retrieve the VulnBank dashboard",
        input_schema=EmptyInput
    )
    @use_interceptors(LoggingInterceptor)
    async def get_dashboard(
        self,
        input: EmptyInput,
        context: ExecutionContext
    ) -> dict:

        return self.service.get_dashboard()

    @tool(
        name="get_account",
        description="Retrieve a VulnBank account by account ID",
        input_schema=AccountInput
    )
    @use_interceptors(LoggingInterceptor)
    async def get_account(
        self,
        input: AccountInput,
        context: ExecutionContext
    ) -> dict:

        return self.service.get_account(
            input.account_id
        )

    @tool(
        name="transfer_funds",
        description="Transfer funds between VulnBank accounts",
        input_schema=TransferInput
    )
    @use_interceptors(LoggingInterceptor)
    async def transfer_funds(
        self,
        input: TransferInput,
        context: ExecutionContext
    ) -> dict:

        return self.service.transfer_funds(
            input.to_account,
            input.amount
        )

    @tool(
        name="get_admin_panel",
        description="Retrieve the VulnBank admin panel",
        input_schema=EmptyInput
    )
    @use_interceptors(LoggingInterceptor)
    async def get_admin_panel(
        self,
        input: EmptyInput,
        context: ExecutionContext
    ) -> dict:

        return self.service.get_admin_panel()

    @tool(
        name="run_exploit",
        description="Run an authorized VulnBank security lab exploit",
        input_schema=RunExploitInput,
        task_support="optional",
    )
    @use_interceptors(LoggingInterceptor)
    async def run_exploit(
        self,
        input: RunExploitInput,
        context: ExecutionContext
    ) -> dict:

        self.service.require_auth()

        def on_progress(line: str) -> None:
            if context.task:
                context.task.update_progress(line)

        return await self.exploit_service.run(
            input.name,
            on_progress=on_progress,
        )