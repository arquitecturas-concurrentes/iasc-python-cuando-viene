import asyncio
import json
import random
from pathlib import Path


MAX_UBICACION = 200
INTERVALO_SEGUNDOS = 2


def actualizar_ubicaciones(lineas: dict) -> None:
    """Move every bus forward and restart its route after location defined in MAX_UBICACION."""
    for detalle in lineas.values():
        for colectivo in detalle["colectivos"]:
            nueva_ubicacion = colectivo["ubicacion"] + random.randint(3, 8)
            colectivo["ubicacion"] = 0 if nueva_ubicacion >= MAX_UBICACION else nueva_ubicacion


def guardar_lineas(path: Path, lineas: dict) -> None:
    # Replacing a complete temporary file prevents readers from seeing partial JSON.
    temporary_path = path.with_suffix(path.suffix + ".tmp")
    with temporary_path.open("w", encoding="utf-8") as database:
        json.dump(lineas, database, ensure_ascii=False, indent=2)
        database.write("\n")
    temporary_path.replace(path)


async def ejecutar_actualizaciones(path: Path, lineas: dict, lock: asyncio.Lock) -> None:
    while True:
        async with lock:
            actualizar_ubicaciones(lineas)
            await asyncio.to_thread(guardar_lineas, path, lineas)
        await asyncio.sleep(INTERVALO_SEGUNDOS)
