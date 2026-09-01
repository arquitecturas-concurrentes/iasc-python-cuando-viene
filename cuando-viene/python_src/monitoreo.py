import asyncio
from contextlib import suppress
from pathlib import Path

from aiohttp import WSMsgType, web

from config.config import CUANDO_VIENE, LINEAS, PARADAS
from utils.common import client_session, get_json


INDEX_PATH = Path(__file__).with_name("index.html")
SERVICES = (("paradas", PARADAS), ("cuando-viene", CUANDO_VIENE), ("lineas", LINEAS))


async def session_context(app: web.Application):
    app["http"] = client_session()
    yield
    await app["http"].close()


async def service_status(app: web.Application, name, service) -> dict:
    try:
        await get_json(app["http"], service, "/health", attempts=1)
        status = "UP"
    except Exception:
        status = "DOWN"
    return {"servicio": name, "status": status}


async def monitor(ws: web.WebSocketResponse, app: web.Application) -> None:
    """Envia periodicamente el estado de los servicios por el WebSocket."""
    # TODO:
    # - mientras el WebSocket siga abierto, consultar todos los SERVICES de
    #   manera concurrente usando service_status;
    # - enviar {"msg": {"estados": states}, "type": "estados"};
    # - esperar un segundo entre actualizaciones sin bloquear el event loop;
    # - finalizar normalmente ante CancelledError o ConnectionError.
    raise NotImplementedError("Completar el monitoreo periodico")


async def index_or_websocket(request: web.Request) -> web.StreamResponse:
    ws = web.WebSocketResponse()
    if not ws.can_prepare(request).ok:
        return web.FileResponse(INDEX_PATH)

    await ws.prepare(request)
    await ws.send_json({"msg": "¡Conectado al monitoreo de servicios!", "type": "texto"})
    task = asyncio.create_task(monitor(ws, request.app))
    try:
        async for message in ws:
            if message.type == WSMsgType.ERROR:
                break
    finally:
        task.cancel()
        with suppress(asyncio.CancelledError):
            await task
    return ws


def create_app() -> web.Application:
    app = web.Application()
    app.cleanup_ctx.append(session_context)
    app.router.add_get("/", index_or_websocket)
    return app


if __name__ == "__main__":
    web.run_app(create_app(), host="0.0.0.0", port=3003)
