# API REST Aztlan 26 (Flask)

API REST en Python Flask para registro de participantes, comprobantes y dashboard.

## Requisitos

- Python 3.10+
- MySQL (base de datos real)

## Instalación

```bash
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Variables de entorno

Copia `env.example` a `.env` y ajusta:

| Variable | Descripción | Por defecto |
|----------|-------------|-------------|
| `PORT` | Puerto del servidor | `5000` |
| `DB_HOST`, `DB_PORT`, `DB_USER`, `DB_PASSWORD`, `DB_NAME` | Conexión MySQL | ver `env.example` |
| `UPLOAD_FOLDER` | Carpeta para guardar comprobantes | `uploads/comprobantes` |

## Ejecución

```bash
python app.py
```

La API quedará en `http://localhost:5000` (o el `PORT` configurado).

## Documentación OpenAPI / Swagger

Con el servidor en marcha:

- **Raíz** → redirige a Swagger: [http://localhost:5000](http://localhost:5000) → [http://localhost:5000/apidocs/](http://localhost:5000/apidocs/)
- **Swagger UI**: [http://localhost:5000/apidocs/](http://localhost:5000/apidocs/)
- **Especificación OpenAPI (JSON)**: [http://localhost:5000/apispec.json](http://localhost:5000/apispec.json)

## Endpoints

### 1. Registro

- **POST /registro**  
  Recibe formularios de registro. Body JSON según `tipoRegistro`:
  - **Común**: `tipoRegistro` (`juvenil` \| `adultos` \| `masters`), `nombreCompleto`, `email`, `timestamp` (ISO).
  - **juvenil**: además `sexo`, `cinta`, `nivelExperiencia`, `categoriaEdad`, `categoriaPeso`.
  - **adultos / masters**: además `edad`, `sexo`, `nivelExperiencia`, `categoriaPeso`, `categoriaPesoTipo` (`varonil` \| `femenil`).
  - Respuesta **201**: `{ nombreParticipante, mensaje, statusCode: 200, aztlan_id }`.

### 2. Comprobante

- **POST /comprobante**  
  Body: `aztlan_id`, `comprobante` (base64), `comprobante_filename`, `comprobante_media_type`, `comprobante_size_bytes`, `timestamp`.  
  Asocia el comprobante al registro y lo deja pendiente de aprobación.  
  Respuesta **200**: `{ success, message, referencia?, timestamp }`. **404** si no existe el registro.

### 3. Dashboard (usuarios)

- **GET /usuarios**  
  Lista todos los registros con todos los campos (incl. `comprobanteAprobado`, `comprobanteUrl`).
- **PATCH /usuarios/:id**  
  Body: `{ comprobanteAprobado: boolean }`. Solo actualiza aprobación del comprobante.
- **DELETE /usuarios/:id**  
  Elimina el registro. Respuesta **204**.

## CORS

CORS está habilitado para todos los orígenes (`*`) para permitir llamadas desde el front.

## Base de datos

- La API usa **MySQL**. Configura en el servidor un archivo `.env` con `DB_HOST`, `DB_PORT`, `DB_USER`, `DB_PASSWORD` y `DB_NAME` (ver `env.example` y la guía en `docs/VPS_HOSTINGER_DATABASE.md`).
- Las tablas se crean al arrancar si no existen (`db.create_all()`). En producción suele crearse antes la base y la tabla `registros` con el script SQL de la documentación.
