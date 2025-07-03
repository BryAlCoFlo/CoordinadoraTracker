# CoordinadoraTracker

**CoordinadoraTracker** es un script en Python que monitorea automáticamente el estado de un envío en la empresa de transporte **Coordinadora** (Colombia), extrayendo datos directamente desde su sitio web.

El script consulta periódicamente el estado del paquete y emite una alerta sonora (y opcionalmente vía WhatsApp) si detecta un cambio, ideal para no perder actualizaciones importantes como "En reparto" o "Entregado".

> Este proyecto es de uso personal y educativo. No está afiliado a Coordinadora.

---

## 🚀 Características

- 🕵️‍♂️ Obtención automática del token CSRF sin autenticación
- 📦 Seguimiento por número de guía vía API JSON de Coordinadora
- 🔔 Alerta sonora en tiempo real si el estado cambia
- 📲 Notificación opcional por WhatsApp usando [CallMeBot](https://www.callmebot.com/blog/free-api-whatsapp-messages/)
- ⚡ Totalmente local, sin navegador ni scraping visual
- 🧪 Simple, rápido y fácil de ejecutar en cualquier entorno

---

## 🛠️ Requisitos

- Python 3.8 o superior

### 📦 Paquetes de Python

- `requests`
- `python-dotenv`
- `sounddevice`
- `scipy`
- `soundfile`

### 🐧 Requisito adicional en Linux

En sistemas Linux (como Ubuntu), también necesitas instalar la siguiente librería del sistema:

```bash
sudo apt install libportaudio2
```


### 📥 Instalación

Instala todos los paquetes de Python necesarios con:

```bash
sudo apt install libportaudio2
```

