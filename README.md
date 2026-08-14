# 🏨 daHotel — PMS & Motor de Reservas Web

[![Python](https://img.shields.io/badge/Python-3.9%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Flet](https://img.shields.io/badge/UI-Flet-007ACC?style=for-the-badge)](https://flet.dev/)
[![Flask](https://img.shields.io/badge/Web-Flask-000000?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![SQLite](https://img.shields.io/badge/Database-SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white)](https://www.sqlite.org/)

**daHotel** es una solución integral ligera para la gestión de pequeños y medianos establecimientos hoteleros. Combina un **Panel de Control de Escritorio (PMS)** en tiempo real para recepción con un **Motor de Reservas Web** para clientes finales, compartiendo una arquitectura de base de datos unificada en SQLite.

---

## 🚀 Características Principales

### 🖥️ Panel Administrativo de Recepción (`Flet`)
* **Configuración Inicial Dinámica:** Permite establecer pisos, número de habitaciones y tarifa base por noche.
* **Mapa Interactivo de Habitaciones:** Estado visual codificado por colores:
  * 🟢 **LIBRE** (`FREE`)
  * 🔴 **OCUPADA** (`OCCUPIED`)
  * 🔵 **RESERVADA** (`RESERVED`)
  * 🟠 **MANTENIMIENTO** (`MAINTENANCE`)
* **Gestión de Estancias:** Módulo de Check-in, Check-out y cobro directo.
* **Cargos Extra:** Añadido rápido de servicios adicionales (minibar, lavandería, room service) con actualización instantánea de la factura.
* **Modo Oscuro / Claro:** Alternancia rápida de tema visual.

### 🌐 Motor de Reservas Web (`Flask` + `Jinja2`)
* **Búsqueda de Disponibilidad:** Consulta por fecha de entrada y número de noches.
* **Selección de Habitación:** Muestra las opciones disponibles organizadas por planta y precio.
* **Confirmación Directa:** Registro de datos del huésped y cálculo automático del total a pagar.
* **Sincronización Total:** Las reservas realizadas vía web se reflejan automáticamente en el panel de recepción como estado `RESERVED`.

---

## 🛠️ Arquitectura del Proyecto

```text
daHotel/
├── main.py        # Punto de entrada de la app de escritorio (Flet)
├── web.py         # Servidor web y endpoints del motor de reservas (Flask)
├── db.py          # Capa de persistencia y lógica de datos (SQLite3)
├── ui.py          # Wrappers y componentes reutilizables de UI en Flet
├── templates/
│   └── index.html # Plantilla HTML/Jinja2 para el proceso de reserva web
└── requirements.txt