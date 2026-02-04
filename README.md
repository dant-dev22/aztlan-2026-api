# API REST Aztlan 26 (Flask)

API REST en Python Flask para registro de participantes, comprobantes y dashboard.

## Requisitos

- Python 3.10+
- Opcional: MySQL (por defecto se usa **modo mock** con SQLite en memoria)

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
| `DB_USE_MOCK` | Si es `true`, usa SQLite en memoria (no requiere MySQL) | `true` |
| `DB_HOST`, `DB_PORT`, `DB_USER`, `DB_PASSWORD`, `DB_NAME` | Conexión MySQL (cuando `DB_USE_MOCK=false`) | - |
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

- Con **DB_USE_MOCK=true** (por defecto): SQLite en memoria. No necesitas MySQL; los modelos son compatibles con MySQL para cuando lo configures.
- Con **DB_USE_MOCK=false**: se usa MySQL con la URI construida a partir de `DB_HOST`, `DB_PORT`, `DB_USER`, `DB_PASSWORD`, `DB_NAME`. Crear la base `aztlan26` (o la que uses) y las tablas se crean al arrancar (`db.create_all()`).
