import time
from nitrostack import ExecutionContext

class LoggingInterceptor:
    async def intercept(self, context: ExecutionContext, next_fn):
        started = time.monotonic()
        context.logger.info(
            f"-> {context.tool_name} called",
            {"request_id": context.request_id},
        )
        try:
            result = await next_fn()
            duration_ms = round((time.monotonic() - started) * 1000, 1)
            context.logger.info(
                f"<- {context.tool_name} completed in {duration_ms}ms"
            )
            return result
        except Exception as exc:
            duration_ms = round((time.monotonic() - started) * 1000, 1)
            context.logger.error(
                f"<- {context.tool_name} failed after {duration_ms}ms: {exc}"
            )
            raise