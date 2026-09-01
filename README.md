# Práctica grupal: _Cuando Viene_ con corutinas

**Duración máxima:** 2 horas 30 minutos.

**Modalidad:** grupal.

## Dominio

Estamos a cargo de el desarrollo y mantenimiento de un sistema que nos permite saber cuál 
es el próximo colectivo de cada línea que va a pasar por mi parada.

Contamos con varios servicios que se encargan de distintos concerns: `lineas`, `paradas` y `cuando-viene`. Este último es el único que va a estar de cara a los usuarios, exponiendo una API REST.

Existe un cuarto componente, `monitoreo`, que nos sirve para conocer el estado del resto de los servicios. Éste expone una página web para ser visualizada por el equipo de infraestructura.
La misma utiliza [websockets](https://en.wikipedia.org/wiki/WebSocket) para ser notificada ante cambios en los estados. Debería poder soportar varias pestañas abiertas. 

## Implementación

Los servicios se encuentran en `cuando-viene/python_src` y usan Python, `asyncio` y
`aiohttp` para HTTP, llamadas concurrentes y WebSockets. Las solicitudes entre servicios
incluyen timeouts, reintentos y manejo de errores.

El objetivo es practicar el uso de corutias, esperas no bloqueantes, concurrencia de este tipo de contextos de ejecucion y cancelación de
tareas. La persistencia y actualización periódica de las líneas ya están resueltas
y **no deben modificarse** (`lineas.py` y `utils/actualizacion_lineas.py`).

## Consigna

Completen los cuatro `TODO` presentes en el código:

1. **Espera no bloqueante (`paradas.py`, 20 min):** completen el middleware para
   que uno de cada dos pedidos (excepto `/health`) demore 5 segundos sin bloquear
   el event loop.
2. **Consultas concurrentes (`cuando_viene.py`, 50 min):** implementen
   `get_line_details` para consultar todas las líneas a la vez. Los resultados
   deben conservar el orden de entrada. No hagan los pedidos secuencialmente.
3. **Ejecución de una corutina (`cuando_viene.py`, 20 min):** corrijan la consulta
   de la parada en `arrival_times` para trabajar con el resultado y no con el
   objeto corutina.
4. **Monitoreo periódico (`monitoreo.py`, 45 min):** implementen `monitor` para
   consultar los tres servicios concurrentemente, enviar sus estados por el
   WebSocket una vez por segundo y terminar limpiamente al cerrar la conexión.

Los 15 minutos restantes están previstos para integración y prueba. Se puede usar
`asyncio.gather` en los puntos de concurrencia; no es necesario incorporar
`TaskGroup` ni modificar el manejo de sesiones HTTP ya provisto.

### Criterios de aceptación

- El código no contiene `time.sleep` ni crea una sesión HTTP por pedido.
- Una petición lenta a `paradas` no impide que `/health` responda inmediatamente.
- Las consultas a varias líneas se inician concurrentemente y el endpoint
  `/cuando-viene/{parada}` devuelve los estados ordenados por tiempo de llegada.
- Cada pestaña de monitoreo recibe actualizaciones independientes y periódicas.
- Al cerrar una pestaña no quedan tareas de monitoreo ejecutándose.
- No se modifican `lineas.py` ni `utils/actualizacion_lineas.py`.

### Pistas

- Una función declarada con `async def` devuelve una corutina al invocarla; para
  obtener su resultado hay que esperarla.
- `asyncio.sleep` cede el control al event loop; mientras que `time.sleep` lo bloquea.
- `asyncio.gather` acepta varias corutinas y devuelve sus resultados en el orden
  en que fueron pasadas.
- El alta y la cancelación de la tarea de monitoreo ya están resueltas en
  `index_or_websocket`; el trabajo pendiente está dentro de `monitor`.

### Comprobación manual sugerida

Con los cuatro servicios levantados, prueben los endpoints indicados debajo. Abran
además dos pestañas en `http://localhost:3003/`, verifiquen que ambas se actualicen
y cierren una para confirmar que la otra continúe funcionando. Ejecuten dos veces
seguidas el endpoint de paradas y, mientras la segunda llamada espera, consulten
`/health` desde otra terminal.

Para ejecutar los cuatro servicios con Docker:

```sh
docker compose up --build
```

Endpoints:

- `http://localhost:3000/paradas/0`
- `http://localhost:3001/lineas/15`
- `http://localhost:3002/cuando-viene/0`
- `http://localhost:3003/` (monitoreo por WebSocket)

## Desarrollo local

```sh
python -m venv .venv
source .venv/bin/activate
pip install -r cuando-viene/requirements.txt
```

Desde `cuando-viene/python_src`, inicie cada servicio en una terminal independiente:

```sh
python paradas.py
python lineas.py
PARADAS_HOST=localhost LINEAS_HOST=localhost python cuando_viene.py
PARADAS_HOST=localhost LINEAS_HOST=localhost CUANDO_VIENE_HOST=localhost python monitoreo.py
```
