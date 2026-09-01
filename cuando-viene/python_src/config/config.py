import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Service:
    name: str
    host: str
    port: int

    @property
    def base_url(self) -> str:
        return f"http://{self.host}:{self.port}"


PARADAS = Service("PARADAS", os.getenv("PARADAS_HOST", "cuando-viene-paradas"), 3000)
LINEAS = Service("LINEAS", os.getenv("LINEAS_HOST", "cuando-viene-lineas"), 3001)
CUANDO_VIENE = Service(
    "CUANDO-VIENE", os.getenv("CUANDO_VIENE_HOST", "cuando-viene-main"), 3002
)
MONITOREO = Service("MONITOREO", os.getenv("MONITOREO_HOST", "cuando-viene-monitoreo"), 3003)
