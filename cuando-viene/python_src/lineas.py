import asyncio
import json
from contextlib import suppress
from pathlib import Path

from aiohttp import web

from utils.actualizacion_lineas import ejecutar_actualizaciones
from utils.common import health


DB_PATH = Path(__file__).parent / "db" / "lineas.db.json"


def read_lines() -> dict:
    with DB_PATH.open(encoding="utf-8") as database:
        return json.load(database)


async def get_line(request: web.Request) -> web.Response:
    line_number = request.match_info["linea"]
    async with request.app["lines_lock"]:
        detail = request.app["lines"].get(line_number)
        if detail is None:
            raise web.HTTPNotFound()
        return web.json_response({"linea": line_number, **detail})


async def updater_context(app: web.Application):
    try:
        app["lines"] = await asyncio.to_thread(read_lines)
    except (OSError, json.JSONDecodeError) as error:
        raise RuntimeError(f"Could not load {DB_PATH}") from error

    app["lines_lock"] = asyncio.Lock()
    updater = asyncio.create_task(
        ejecutar_actualizaciones(DB_PATH, app["lines"], app["lines_lock"])
    )
    yield
    updater.cancel()
    with suppress(asyncio.CancelledError):
        await updater


def create_app() -> web.Application:
    app = web.Application()
    app.cleanup_ctx.append(updater_context)
    app.router.add_get("/health", health)
    app.router.add_get("/lineas/{linea}", get_line)
    return app


if __name__ == "__main__":
    web.run_app(create_app(), host="0.0.0.0", port=3001)
