# 🏨 daHotel — PMS & Motor de Reservas Web

[![Python](https://img.shields.io/badge/Python-3.9%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Flet](https://img.shields.io/badge/UI-Flet-007ACC?style=for-the-badge)](https://flet.dev/)
[![Flask](https://img.shields.io/badge/Web-Flask-000000?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![SQLite](https://img.shields.io/badge/Database-SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white)](https://www.sqlite.org/)

**daHotel** es una solución integral ligera para la gestión de pequeños y medianos establecimientos hoteleros. Combina un **Panel de Control de Escritorio (PMS)** en tiempo real para recepción con un **Motor de Reservas Web** para clientes finales, compartiendo una arquitectura de base de datos unificada en SQLite.

---
## 📸 Galería del Sistema

### 🌐 Motor de Reservas Web y Flujo de Gestión (Flask)

<p align="center">
  <img width="850" alt="Vista del Sistema 3" src="https://github.com/user-attachments/assets/6f998eb5-7a04-4e24-8147-38ccbc1d8406" />
  <br><br>
  <img width="850" alt="Vista del Sistema 2" src="https://github.com/user-attachments/assets/11e146c4-612a-4393-8bd5-390edaf99875" />
  <br><br>
  <img width="850" alt="Vista del Sistema 1" src="https://github.com/user-attachments/assets/8a1d5fb3-dbd7-4110-9837-76f466771c20" />
  <br><br>
</p>

### 🖥️ Panel Administrativo de Recepción (Flet)

  <p align="center">
    <img width="850" alt="Vista del Sistema 9" src="https://github.com/user-attachments/assets/aa101bf2-deac-4e17-ae67-281ff25abbe1" />
    <br><br>
    <img width="850" alt="Vista del Sistema 8" src="https://github.com/user-attachments/assets/c510c829-fa0e-4c1e-8927-5e5185f901f4" />
    <br><br>
    <img width="850" alt="Vista del Sistema 7" src="https://github.com/user-attachments/assets/331584e6-da0f-4bf2-ac9d-077d21a1e12d" />
    <br><br>
    <img width="850" alt="Vista del Sistema 6" src="https://github.com/user-attachments/assets/360ca89b-aaef-4c6c-b8b6-c43e36645c74" />
    <br><br>
    <img width="850" alt="Vista del Sistema 4" src="https://github.com/user-attachments/assets/08a1efce-f35a-46da-94e3-f31ecc33a800" />
    <br><br>
    <img width="850" alt="Vista del Sistema 5" src="https://github.com/user-attachments/assets/c4ec1121-5690-4538-ab8b-a8764c272d01" />
    <br><br>
  </p>

---

## 🚀 Características Principales

### 🖥️ Panel Administrativo de Recepción (`Flet`)
- **Configuración Inicial Dinámica:** Permite establecer pisos, número de habitaciones y tarifa base por noche.
- **Mapa Interactivo de Habitaciones:** Estado visual codificado por colores:
  * 🟢 **LIBRE** (`FREE`)
  * 🔴 **OCUPADA** (`OCCUPIED`)
  * 🔵 **RESERVADA** (`RESERVED`)
  * 🟠 **MANTENIMIENTO** (`MAINTENANCE`)
- **Gestión de Estancias:** Módulo de Check-in, Check-out y cobro directo.
- **Cargos Extra:** Añadido rápido de servicios adicionales (minibar, lavandería, room service) con actualización instantánea de la factura.
- **Modo Oscuro / Claro:** Alternancia rápida de tema visual.

### 🌐 Motor de Reservas Web (`Flask` + `Jinja2`)
- **Búsqueda de Disponibilidad:** Consulta por fecha de entrada y número de noches.
- **Selección de Habitación:** Muestra las opciones disponibles organizadas por planta y precio.
- **Confirmación Directa:** Registro de datos del huésped y cálculo automático del total a pagar.
- **Sincronización Total:** Las reservas realizadas vía web se reflejan automáticamente en el panel de recepción como estado `RESERVED`.

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
