import asyncio

from aiohttp import web

from utils.common import health


PARADAS = {
    "0": {"ubicacion": 0, "lineas": [15, 60]},
    "3": {"ubicacion": 30, "lineas": [15, 184]},
    "11": {"ubicacion": 110, "lineas": [15, 60, 720]},
}


@web.middleware
async def unstable_network(request: web.Request, handler):
    """Simula una red inestable sin bloquear el event loop."""
    if request.path == "/health":
        return await handler(request)

    request.app["request_count"] += 1
    if request.app["request_count"] % 2 == 0:
        # TODO: esperar 5 segundos de manera no bloqueante.
        # No usar time.sleep(), porque impediria atender otros pedidos.
        raise NotImplementedError("Completar la espera asincronica")

    return await handler(request)

async def registrar_metrica(parada: str):
    await asyncio.sleep(2) # Simula red lenta
    print(f"Métrica registrada para parada {parada}")

async def get_stop(request: web.Request) -> web.Response:
    stop = PARADAS.get(request.match_info["parada"])
    if stop is None:
        raise web.HTTPNotFound()
    return web.json_response(stop)


def create_app() -> web.Application:
    app = web.Application(middlewares=[unstable_network])
    app["request_count"] = 0
    app.router.add_get("/health", health)
    app.router.add_get("/paradas/{parada}", get_stop)
    return app


if __name__ == "__main__":
    web.run_app(create_app(), host="0.0.0.0", port=3000)
