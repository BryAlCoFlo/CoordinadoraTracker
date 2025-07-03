import requests, re, time, os
from dotenv import load_dotenv
from urllib.parse import quote
import sounddevice as sd
from scipy.io.wavfile import read


load_dotenv(override=True)

apiKey = os.getenv("API_KEY")
apiUrl = os.getenv("API_URL")
phoneNumber = os.getenv("PHONE_NUMBER")
usarWhatsapp = all([apiKey, apiUrl, phoneNumber])

def validarNumeroCallmebot():
    if not usarWhatsapp:
        return False
    print("📲 Verificando si el número está registrado en CallMeBot...")
    try:
        url = f"{apiUrl}?phone={phoneNumber}&text=Test+message&apikey={apiKey}"
        r = requests.get(url, timeout=10)
        if "Message queued" in r.text or "Message successfully sent" in r.text:
            print("✅ Número validado en CallMeBot.")
            return True
    except Exception as e:
        print(f"❌ Error al validar número en CallMeBot: {e}")
    
    print("⚠️ No se pudo validar CallMeBot, se ignorará el envío por WhatsApp.")
    return False

def enviarAlertaWhatsapp(mensaje):
    if not usarWhatsapp:
        return
    texto = quote(mensaje)
    url = f"{apiUrl}?phone={phoneNumber}&text={texto}&apikey={apiKey}"
    try:
        r = requests.get(url, timeout=10)
        print(f"📲 WhatsApp enviado: {r.text}")
    except Exception as e:
        print(f"❌ Error al enviar WhatsApp: {e}")

def beep(numberOfBeep=3):
    try:
        samplerate, data = read("dialogWarning.wav")
        for _ in range(numberOfBeep):
            sd.play(data, samplerate)
            sd.wait()
    except Exception as e:
        print(f"❌ Error al reproducir sonido: {e}")

def obtenerToken(remisionCode):
    try:
        html = requests.get(f"https://coordinadora.com/seguimiento/?guia={remisionCode}", timeout=10).text
        match = re.search(r"data-csrf='([^']+)'", html)
        return match.group(1) if match else None
    except Exception as e:
        print(f"❌ Error al obtener token: {e}")
        return None

def obtenerEstado(token, remisionCode):
    try:
        r = requests.get(
            f"https://www.coordinadora.com/wp-json/rgc/v1/detail_tracking?remission_code={remisionCode}",
            headers={"Authorization": f"Bearer {token}", "Accept": "application/json"},
            timeout=10
        )
        return r.json()
    except Exception as e:
        print(f"❌ Error al obtener estado: {e}")
        return {}

# 🚀 Entradas del usuario
remisionCode = input("🔢 Ingresa el número de guía (remission code): ").strip()
try:
    minutos = int(input("⏱️ ¿Cada cuántos minutos quieres verificar el estado? "))
    intervalo = minutos * 60
except ValueError:
    print("❌ Error: Ingresa un número entero para los minutos.")
    exit()

# 🛡️ Validación previa
validarNumeroCallmebot()

estadoAnterior = None
beep(1)  # Beep al inicio

validarNumeroCallmebot()
while True:
    token = obtenerToken(remisionCode)
    if not token:
        print("❌ Token inválido. Reintentando en 1 minuto...")
        time.sleep(60)
        continue

    datos = obtenerEstado(token, remisionCode)
    estadoActual = datos.get("current_state_text", "DESCONOCIDO")

    if estadoAnterior is None:
        estadoAnterior = estadoActual
        print(f"🔄 Estado inicial: {estadoActual}")
    elif estadoActual != estadoAnterior:
        print(f"📦 ¡Estado cambiado! Nuevo estado: {estadoActual}")
        estadoAnterior = estadoActual
        beep()
        enviarAlertaWhatsapp(f"📦 ¡Nuevo estado de tu paquete! -> {estadoActual}")
    else:
        print(f"✅ Sin cambios. Estado: {estadoActual}")

    time.sleep(intervalo)
