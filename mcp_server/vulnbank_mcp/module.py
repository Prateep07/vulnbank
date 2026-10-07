from nitrostack import module

from vulnbank_mcp.exploit_service import ExploitService
from vulnbank_mcp.resources import VulnBankResources
from vulnbank_mcp.service import VulnBankService
from vulnbank_mcp.tools import VulnBankTools


@module(
    name="vulnbank",
    controllers=[
        VulnBankTools,
        VulnBankResources,
    ],
    providers=[
        VulnBankService,
        ExploitService,
    ],
)
class VulnBankModule:
    pass


@module(
    name="app",
    imports=[
        VulnBankModule
    ],
)
class AppModule:
    pass