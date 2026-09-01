import asyncio
import logging

from aiohttp import ClientError, ClientSession, web

from config.config import LINEAS, PARADAS
from utils.common import client_session, get_json, health


logger = logging.getLogger(__name__)


def closest_bus(line_detail: dict, stop_location: int) -> dict:
    arrivals = [bus["ubicacion"] - stop_location for bus in line_detail["colectivos"]]
    if not arrivals:
        raise ValueError("The line has no buses")
    return {"linea": line_detail["linea"], "tiempoDeLlegada": min(arrivals)}


async def session_context(app: web.Application):
    app["http"] = client_session()
    yield
    await app["http"].close()


async def get_line_details(session: ClientSession, lines: list) -> list:
    """Obtiene el detalle de todas las lineas en forma concurrente."""
    # - crear una corutina get_json por cada linea;
    # - ejecutarlas concurrentemente (asyncio.gather es suficiente);
    # - devolver los resultados en el mismo orden que ``lines``.
    #
    # No resolverlo con un ``for`` que haga await en cada iteracion: con tres
    # lineas lentas los tiempos se acumularian.
    raise NotImplementedError("Completar las consultas concurrentes")


async def arrival_times(request: web.Request) -> web.Response:
    try:
        # TODO: ejecutar la corutina que consulta la parada y guardar su
        # resultado en ``stop``. Recordar que llamar una async function no la
        # ejecuta por si solo.
        stop = get_json(
            request.app["http"], PARADAS, f"/paradas/{request.match_info['parada']}"
        )
        details = await get_line_details(request.app["http"], stop["lineas"])
        states = [closest_bus(detail, stop["ubicacion"]) for detail in details]
        states.sort(key=lambda state: state["tiempoDeLlegada"])
        return web.json_response({"estados": states})
    except web.HTTPException:
        raise


def create_app() -> web.Application:
    app = web.Application()
    app.cleanup_ctx.append(session_context)
    app.router.add_get("/health", health)
    app.router.add_get("/cuando-viene/{parada}", arrival_times)
    return app


if __name__ == "__main__":
    web.run_app(create_app(), host="0.0.0.0", port=3002)
