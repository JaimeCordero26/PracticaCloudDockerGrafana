# Práctica: Entorno Cloud Local con Docker Compose
## Django + Celery + Redis + PostgreSQL + Flower + Grafana + Loki + Vue (Vite)

### 📋 Descripción del Proyecto

Este proyecto implementa un **entorno de nube privada local** utilizando Docker Compose que integra múltiples servicios modernos para demostrar conceptos de arquitectura de servicios web, middleware y observabilidad.

El sistema consiste en:
- **Backend**: Django REST API
- **Base de Datos**: PostgreSQL
- **Cola de Mensajería**: Redis
- **Tareas Asíncronas**: Celery (Worker + Beat)
- **Monitoreo de Tareas**: Flower
- **Observabilidad**: Grafana + Loki
- **Frontend**: Vue 3 con Vite

---

### 🎯 Objetivo Académico

Esta práctica operacionaliza conceptos fundamentales de **Servicios Web y Middleware**:

1. **Arquitectura Cliente-Servidor**: Comunicación HTTP/HTTPS entre Vue (cliente) y Django (servidor)
2. **API RESTful**: Endpoints que siguen principios REST sobre HTTP
3. **Middleware**: Orquestación de peticiones, CORS, serialización
4. **Desacoplamiento**: Uso de colas (Redis) para tareas asíncronas (Celery)
5. **Observabilidad**: Logging centralizado (Loki) y visualización (Grafana)
6. **Containerización**: Todos los servicios orquestados con Docker Compose

---

### 🏗️ Arquitectura del Sistema
```
┌─────────────┐ ┌─────────────┐ ┌─────────────┐
│ Vue 3 │────────▶│ Django │────────▶│ PostgreSQL │
│ (Frontend) │ HTTP │ (Backend) │ │ (DB) │
│ Port 8080 │ │ Port 8000 │ │ Port 5432 │
└─────────────┘ └─────────────┘ └─────────────┘
│
│ Pub/Sub
▼
┌─────────────┐
│ Redis │
│ (Broker) │
│ Port 6379 │
└─────────────┘
│
┌───────────┴───────────┐
▼ ▼
┌──────────┐ ┌──────────┐
│ Celery │ │ Celery │
│ Worker │ │ Beat │
└──────────┘ └──────────┘
│
└──────────▶┌──────────┐
│ Flower │
│ Monitor │
│Port 5555 │
└──────────┘


    ┌─────────────┐         ┌─────────────┐
    │   Grafana   │────────▶│    Loki     │
    │ (Dashboard) │         │   (Logs)    │
    │  Port 3000  │         │  Port 3100  │
    └─────────────┘         └─────────────┘
```


---

### 🔄 Flujo de Funcionamiento

#### 1. **Cliente → Backend (Petición HTTP)**
El frontend Vue realiza peticiones HTTP al endpoint de Django (`/api/hello/`) mediante `fetch()`.

#### 2. **Backend → Base de Datos**
Django procesa la petición y puede consultar/guardar datos en PostgreSQL usando el ORM de Django.

#### 3. **Backend → Cola de Tareas**
Para operaciones asíncronas (envío de emails, procesamiento de imágenes, etc.), Django envía tareas a Redis usando Celery.

#### 4. **Celery Worker → Ejecución**
Los workers de Celery consumen tareas de Redis y las ejecutan en segundo plano.

#### 5. **Celery Beat → Tareas Programadas**
Beat actúa como scheduler para tareas recurrentes (cron jobs).

#### 6. **Flower → Monitoreo**
Flower proporciona una interfaz web para monitorear workers, tareas y estadísticas de Celery.

#### 7. **Grafana + Loki → Observabilidad**
- Loki recolecta logs de todos los contenedores
- Grafana visualiza logs en dashboards para debugging y análisis

---

### 📦 Componentes y Tecnologías
```
| Componente | Tecnología | Puerto | Función |
|------------|------------|--------|---------|
| **Frontend** | Vue 3 + Vite | 8080 | Interfaz de usuario reactiva |
| **Backend** | Django 5.x | 8000 | API REST, lógica de negocio |
| **Base de Datos** | PostgreSQL 16 | 5432 | Persistencia de datos |
| **Broker/Cache** | Redis 7 | 6379 | Cola de mensajes y caché |
| **Task Worker** | Celery | - | Procesamiento asíncrono |
| **Task Scheduler** | Celery Beat | - | Tareas programadas (cron) |
| **Task Monitor** | Flower | 5555 | Dashboard de Celery |
| **Logs** | Loki 2.9.3 | 3100 | Agregación de logs |
| **Visualización** | Grafana 10.4.2 | 3000 | Dashboards y métricas |
```
---

### 🚀 Instalación y Ejecución

#### Prerrequisitos
- Docker Desktop instalado
- Git
- Terminal (PowerShell/Bash/Fish)

#### Pasos de Instalación

1. **Clonar el repositorio**

git clone <tu-repositorio>
cd cloud_practica



2. **Construir y levantar servicios**

docker compose up -d --build



3. **Ejecutar migraciones de Django**

docker compose exec django python manage.py migrate



4. **Crear superusuario (opcional)**

docker compose exec django python manage.py createsuperuser



5. **Verificar servicios**

docker compose ps



---

### 🔍 Verificación de Servicios

#### Backend Django

curl http://localhost:8000/api/hello/
Respuesta esperada: {"message": "¡Hola desde Django API!"}



#### Frontend Vue
Abrir en navegador: `http://localhost:8080`

#### Flower (Monitor Celery)
Abrir en navegador: `http://localhost:5555`

#### Grafana
Abrir en navegador: `http://localhost:3000`  
Login: `admin` / `admin`

#### PostgreSQL

docker compose exec postgres psql -U myuser -d mydb -c "\dt"



#### Redis

docker compose exec redis redis-cli ping
Respuesta: PONG



---

### 🧪 Probar Tareas Asíncronas con Celery

docker compose exec django python manage.py shell



Dentro del shell de Django:

from app.tasks import ping
result = ping.delay()
print(result.get()) # Debe imprimir: "pong"



Luego verificar en Flower (`http://localhost:5555`) que la tarea se ejecutó correctamente.

---

### 📊 Configuración de Grafana + Loki

1. Acceder a Grafana: `http://localhost:3000`
2. Login: `admin` / `admin`
3. Ir a **Configuration** → **Data Sources** → **Add data source**
4. Seleccionar **Loki**
5. Configurar URL: `http://loki:3100`
6. Click en **Save & Test**
7. Crear un nuevo **Dashboard**
8. Agregar panel con query de Loki para visualizar logs

**Ejemplo de query Loki:**

{container_name="django"}



---

### 📁 Estructura del Proyecto

```
PracticaCloudDockerGrafana/
.
├── backend
│   ├── app
│   ├── backend
│   ├── celerybeat-schedule
│   ├── Dockerfile
│   ├── manage.py
│   └── requirements.txt
├── docker-compose.yml
├── evidences
│   ├── Celery beat.png
│   ├── celery monitor.png
│   ├── Celery worker.png
│   ├── curl.png
│   ├── docker compose build.png
│   ├── docker ps.png
│   ├── evidences.png
│   ├── frontend vue.png
│   ├── Grafana dashboard.png
│   ├── Grafana login.png
│   ├── Logs de django irl.png
│   ├── logs.txt
│   ├── loki conf.png
│   ├── Loki save.png
│   ├── PostgreSQL.png
│   ├── prueba de tarea celery.png
│   ├── Redis.png
│   ├── Screenshot_20251019_095755.png
│   ├── Tarea celery en monitor.png
│   └── tasks monitor.png
├── frontend
│   ├── Dockerfile
│   ├── index.html
│   ├── node_modules
│   ├── package.json
│   ├── public
│   ├── README.md
│   ├── src
│   └── vite.config.js
├── promtail-config.yml
└── README.md
```


---

### 🔧 Comandos Útiles

#### Ver logs de todos los servicios

docker compose logs -f



#### Ver logs de un servicio específico

docker compose logs -f django
docker compose logs -f celery_worker



#### Detener servicios

docker compose down



#### Detener y eliminar volúmenes

docker compose down -v



#### Reconstruir un servicio específico

docker compose up -d --build django



#### Ejecutar comandos en un contenedor

docker compose exec django python manage.py makemigrations
docker compose exec django python manage.py migrate



---

### 🌐 Relación entre Componentes

#### **Vue ↔ Django (HTTP REST)**
- Vue consume la API REST de Django mediante `fetch()`
- Django responde con JSON
- CORS habilitado con `django-cors-headers`

#### **Django ↔ PostgreSQL (ORM)**
- Django usa el ORM para queries SQL
- Conexión configurada en `settings.py`
- Migraciones automáticas con `manage.py migrate`

#### **Django ↔ Redis ↔ Celery (Mensajería)**
- Django envía tareas: `task.delay()`
- Redis actúa como broker (pub/sub)
- Celery Worker consume y ejecuta tareas
- Celery Beat programa tareas recurrentes

#### **Celery ↔ Flower (Monitoreo)**
- Flower se conecta al mismo broker Redis
- Proporciona métricas en tiempo real
- UI web para debugging de tareas

#### **Todos ↔ Loki ↔ Grafana (Observabilidad)**
- Loki recolecta logs de contenedores Docker
- Grafana consulta Loki como data source
- Dashboards para análisis centralizado

---

### 📚 Conceptos Técnicos Clave

#### **RESTful API**
- Endpoints semánticos (`/api/hello/`)
- Métodos HTTP (GET, POST, PUT, DELETE)
- Respuestas en JSON
- Stateless (sin estado entre peticiones)

#### **Middleware**
- CORS: permite peticiones cross-origin
- Autenticación y autorización
- Logging de peticiones
- Manejo de errores centralizado

#### **Arquitectura de Microservicios**
- Cada servicio en su propio contenedor
- Comunicación via red Docker
- Escalabilidad horizontal (más workers)
- Independencia de deploys

#### **Message Queue Pattern**
- Desacoplamiento entre productor (Django) y consumidor (Celery)
- Tolerancia a fallos (retry logic)
- Procesamiento asíncrono
- Escalabilidad de workers

---

### 🎓 Conclusión Académica

Este proyecto demuestra una arquitectura moderna de servicios web que abarca:

1. **Frontend-Backend Separation**: SPA (Vue) consumiendo API REST (Django)
2. **Data Persistence**: Uso de base de datos relacional (PostgreSQL)
3. **Asynchronous Processing**: Tareas en background con Celery/Redis
4. **Observability**: Logs centralizados y visualización con Grafana/Loki
5. **Containerization**: Orquestación multi-contenedor con Docker Compose
6. **Monitoring**: Dashboard de tareas con Flower

Estos patrones son fundamentales en aplicaciones empresariales modernas y sistemas distribuidos.

---

### 👤 Autor

[Alejandro Cordero]  
Universidad: [Universidad Tecnica Nacional]  
Curso: Web III  
Fecha: Octubre 2025

---

### 📄 Licencia

Este proyecto es con fines académicos.
