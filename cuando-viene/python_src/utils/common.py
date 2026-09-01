import asyncio
from typing import Any

from aiohttp import ClientError, ClientSession, ClientTimeout, web

from config.config import Service


async def health(_: web.Request) -> web.Response:
    return web.json_response({"status": "UP"})


async def get_json(
    session: ClientSession,
    service: Service,
    path: str,
    *,
    attempts: int = 2,
) -> Any:
    """GET JSON with a bounded timeout and a small linear retry."""
    last_error: Exception | None = None
    for attempt in range(attempts):
        try:
            async with session.get(f"{service.base_url}{path}") as response:
                if response.status != 200:
                    raise RuntimeError(
                        f"Request to {service.name}{path} returned {response.status}"
                    )
                return await response.json()
        except (ClientError, asyncio.TimeoutError, RuntimeError, ValueError) as error:
            last_error = error
            if attempt + 1 < attempts:
                await asyncio.sleep(0.1 * (attempt + 1))
    assert last_error is not None
    raise last_error


def client_session() -> ClientSession:
    return ClientSession(timeout=ClientTimeout(total=2.0, connect=0.5))
