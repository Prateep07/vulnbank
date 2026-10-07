import asyncio

from nitrostack import McpApplicationFactory

from vulnbank_mcp.module import AppModule


async def main():
    app = await McpApplicationFactory.create(AppModule)
    await app.start()


if __name__ == "__main__":
    asyncio.run(main())