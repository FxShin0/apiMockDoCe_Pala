


# 🃏 API Mock para Rankings del Juego DoCe

Esta es una API sencilla creada con Flask que permite guardar, obtener y resetear los rankings de partidas ganadas por jugadores en grupos identificados por código. Los datos se almacenan en un archivo JSON (`rankings_data.json`) para persistencia local.

- **Deployed in Railway:** https://web-production-c8f19.up.railway.app

## 🚀 Cómo iniciar

Asegurate de tener Python y Flask instalados. Podés instalar las dependencias ejecutando:

```bash
pip install flask flask-cors
````

Luego, simplemente ejecutá el archivo:

```bash
python app.py
```

Por defecto corre en el puerto `5000`, o el definido en la variable de entorno `PORT` (por ejemplo, para Railway).

---

## 📡 Endpoints

### 🔹 `GET /api/doce/PRUEBA`

Devuelve un listado ordenado de los jugadores de un grupo con la cantidad de partidas ganadas.

- https://web-production-c8f19.up.railway.app/api/doce/PRUEBA

**Respuesta:**

```json
[
  {
    "nombreJugador": "Ana",
    "cantidadPartidasGanadas": 3
  },
  ...
]
```

---

### 🔹 `POST /api/doce`

Guarda el resultado de una partida.

- https://web-production-c8f19.up.railway.app/api/doce

**Cuerpo del request:**

```json
{
  "CodigoGrupo": "abc123",
  "jugador": {
    "nombre": "Ana",
    "vencedor": 1
  }
}
```

* `vencedor`: `1` si ganó la partida, `0` si no.

**Respuesta:** `204 No Content` si fue exitoso.

---

### 🔹 `DELETE /api/doce/PRUEBA`

Resetea (borra) todos los rankings.

- https://web-production-c8f19.up.railway.app/api/doce/PRUEBA

**Respuesta:**

```json
{
  "message": "Grupo abc123 reseteado correctamente"
}
```

---

### 🔹 `GET /status`

Devuelve un resumen básico del estado de la API.

- https://web-production-c8f19.up.railway.app/status

**Respuesta:**

```json
{
  "status": "API Mock funcionando",
  "grupos_activos": 2,
  "total_jugadores": 7
}
```

---

## 💾 Persistencia

Los datos se guardan en el archivo `rankings_data.json` para conservar la información entre ejecuciones del servidor.

---

## 🛡️ CORS

Se permite el acceso desde cualquier origen (`CORS` activado globalmente), ideal para pruebas con frontends en desarrollo.

---

