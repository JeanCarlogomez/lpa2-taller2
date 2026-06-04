# Generador de Facturas

| Código | Nombre | Correo |
| --- | --- | --- |
| 1005707675 | Jean Carlo Gomez Ortiz | jean.gomez.7675@miremington.edu.co |

---

## Descripción del Proyecto

Sistema completo de generación de facturas, utilizando [FastAPI](https://fastapi.tiangolo.com/) para el backend que genera datos sintéticos con [Faker](https://faker.readthedocs.io/), y proporciona un frontend web con [Flask](https://flask.palletsprojects.com/) para generar PDFs de las facturas con [ReportLab](https://docs.reportlab.com/reportlab/userguide/ch1_intro/).

Este proyecto consta de dos servicios principales:

- **Backend API**: FastAPI que genera datos sintéticos de facturas utilizando Faker
- **Frontend Web**: Aplicación web que consume el API y genera PDFs descargables de las facturas

## Arquitectura
┌────────────────┐          ┌───────────────┐
│  Frontend Web  │ ───────> │  Backend API  │
│  puerto 3000   │   HTTP   │  puerto 8000  │
│  Flask + RLab  │ <─────── │  FastAPI      │
└────────────────┘          └───────────────┘
## Estructura del Proyecto
lpa2-taller2/
├── docker-compose.yml
├── README.md
├── backend/
│   ├── Dockerfile
│   └── app/
│       ├── main.py
│       └── requirements.txt
└── frontend/
├── Dockerfile
└── app/
├── main.py
├── requirements.txt
├── static/
│   ├── css/
│   │    └── style.css
│   └── js/
│        └── app.js
└── templates/
└── index.html

## Prerrequisitos

- Docker instalado
- Docker Compose instalado
- Git instalado

## Cómo ejecutar

**1. Clonar el repositorio**
```bash
git clone https://github.com/JeanCarlogomez/lpa2-taller2.git
cd lpa2-taller2
```

**2. Construir y levantar los servicios**
```bash
docker-compose up --build
```

**3. Acceder a la aplicación**

| Servicio | URL |
| --- | --- |
| Frontend | http://localhost:3000 |
| Backend API | http://localhost:8000 |
| Documentación Swagger | http://localhost:8000/docs |
| Documentación ReDoc | http://localhost:8000/redoc |

**4. Detener los servicios**
```bash
docker-compose down
```

## Uso de la Aplicación

1. Abrir el navegador en `http://localhost:3000`
2. Ingresar un número de factura (ej: FAC-2025-001, INV-2024-123)
3. Hacer clic en **"Generar Factura"**
4. Ver la vista previa de la factura
5. Descargar el PDF haciendo clic en **"Descargar PDF"**

## Endpoints del Backend

**Endpoint principal:** `GET /facturas/v1/{numero_factura}`

```bash
curl http://localhost:8000/facturas/v1/FAC-2025-001
```

**Ejemplo de respuesta:**
```json
{
  "numero_factura": "FAC-2025-001",
  "fecha_emision": "2025-08-15",
  "empresa": {
    "nombre": "Tech Solutions S.L.",
    "direccion": "Calle Mayor 123, Madrid",
    "telefono": "+34 912 345 678",
    "email": "contacto@techsolutions.es"
  },
  "cliente": {
    "nombre": "Industrias López",
    "direccion": "Av. Libertad 456, Barcelona",
    "telefono": "+34 933 456 789"
  },
  "subtotal": 1250.00,
  "impuesto": 262.50,
  "total": 1512.50
}
```

## Comandos Docker útiles

```bash
# Levantar en segundo plano
docker-compose up -d

# Ver logs
docker-compose logs -f

# Ver logs de un servicio específico
docker-compose logs -f backend
docker-compose logs -f frontend

# Reiniciar un servicio
docker-compose restart backend

# Detener y eliminar volúmenes
docker-compose down -v
```
