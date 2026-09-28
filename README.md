# 📊 SRE Observability Stack

Entorno local de observabilidad diseñado bajo la filosofía SRE (Site Reliability Engineering) para monitorear las **Golden Signals** (Latencia, Tráfico y Errores) de una API en Python utilizando **Prometheus** y **Grafana** sobre contenedores Docker.

---

## 🏗️ Arquitectura del Stack

```
+-------------------------------------------------------------------+
|                        Rocky Linux Host                           |
|                                                                   |
|   +---------------+       +------------------+       +--------+   |
|   |  Flask App    | <---- |    Prometheus    | <---- |Grafana |   |
|   | (Puerto 5000) |       |  (Scrape /metrics|       | (Dash) |   |
|   +---------------+       |   Puerto 9090)   |       +--------+   |
|                           +------------------+                    |
+-------------------------------------------------------------------+
```

---

## 📋 Requisitos Previos (Rocky Linux 9/10)

Antes de iniciar, asegúrate de contar con un sistema **Rocky Linux** actualizado y con acceso a `sudo`.

### 1. Actualización del Sistema
```bash
sudo dnf update -y
```

### 2. Instalación de Docker y Docker Compose Plugin
Rocky Linux utiliza `dnf` como gestor de paquetes. Para instalar la versión oficial de Docker Engine:

```bash
# Instalar utilidades del sistema
sudo dnf install -y dnf-utils

# Agregar el repositorio oficial de Docker
sudo dnf config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo

# Instalar Docker Engine, CLI y Docker Compose Plugin
sudo dnf install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

# Habilitar e iniciar el servicio de Docker
sudo systemctl enable --now docker
```

### 3. Configuración de Permisos de Usuario (Opcional pero Recomendado)
Para ejecutar comandos de Docker sin anteponer `sudo`:

```bash
sudo usermod -aG docker $USER
newgrp docker
```

---

## 🛡️ Ajustes Específicos para Rocky Linux (SELinux y Firewall)

### A. Configuración de SELinux
Rocky Linux ejecuta **SELinux** en modo `Enforcing` por defecto. Si montas volúmenes locales en contenedores Docker y obtienes errores de permisos (`Permission Denied`), aplica las etiquetas de seguridad correspondientes a los directorios del proyecto:

```bash
# Asignar el contexto de seguridad SELinux para contenedores
sudo chcon -Rt svirt_sandbox_file_t prometheus/
```

*Nota: Alternativamente, en el archivo `docker-compose.yml` se puede agregar el sufijo `:z` a los volúmenes montados.*

### B. Configuración de `firewalld`
Para acceder a las interfaces web desde fuera del servidor local (o tu red de laboratorio), abre los puertos requeridos en el cortafuegos de Rocky Linux:

```bash
# Abrir puertos para la App (5000), Prometheus (9090) y Grafana (3000)
sudo firewall-cmd --permanent --add-port={5000,9090,3000}/tcp
sudo firewall-cmd --reload
```

---

## 🚀 Despliegue del Proyecto

### 1. Clonar el Repositorio
```bash
git clone https://github.com/mcastilloc/sre-observability-stack.git
cd sre-observability-stack
```

### 2. Construir y Levantar los Contenedores
```bash
docker compose up -d --build
```

### 3. Verificar el Estado de los Servicios
```bash
docker compose ps
```

---

## 🌐 Servicios y Verificación

Una vez levantados los servicios, estarán disponibles en las siguientes rutas:

| Servicio | URL | Descripción |
| :--- | :--- | :--- |
| **Flask App** | `http://localhost:5000` | Endpoint principal de la aplicación (Genera métricas/errores simulados) |
| **App Metrics**| `http://localhost:5000/metrics` | Endpoint expuesto con métricas en formato Prometheus |
| **Prometheus** | `http://localhost:9090` | Consola de métricas y consultas PromQL |
| **Grafana** | `http://localhost:3000` | Paneles de monitoreo (Credenciales: `admin` / `admin`) |

---

## 🧪 Pruebas de Carga (Simulación de Tráfico)

Para generar datos en vivo y visualizar la latencia y la tasa de errores en Grafana, ejecuta un bucle de peticiones HTTP en Bash desde la terminal de tu Rocky Linux:

```bash
while true; do curl -s http://localhost:5000/ > /dev/null; sleep 0.3; done
```

---

## 🧹 Detención y Limpieza del Entorno

Para detener la ejecución de los contenedores sin borrar los volúmenes:
```bash
docker compose stop
```

Para remover los contenedores y las redes creadas:
```bash
docker compose down
```

![alt text](image.png)