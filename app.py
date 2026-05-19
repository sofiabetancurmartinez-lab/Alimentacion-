import streamlit as st
from bokeh.models.widgets import Button
from bokeh.models import CustomJS
from streamlit_bokeh_events import streamlit_bokeh_events
import paho.mqtt.client as mqtt
import time

# ---------------- MQTT CONFIG ----------------
BROKER = "broker.hivemq.com"
PORT = 1883
TOPIC = "petbuddy_sofia_2026/feed"

# Este TOPIC debe ser IGUAL en Wokwi:
# const char* topic = "petbuddy_sofia_2026/feed";

def on_publish(client, userdata, mid):
    print("Comando publicado correctamente")

def enviar_comando_mqtt(comando):
    try:
        client = mqtt.Client()
        client.on_publish = on_publish
        client.connect(BROKER, PORT, 60)
        client.publish(TOPIC, comando)
        client.disconnect()
        return True
    except Exception as e:
        st.error(f"Error conectando con Wokwi: {e}")
        return False

# ---------------- STREAMLIT UI ----------------
st.set_page_config(
    page_title="PetBuddy - Control por voz",
    page_icon="🐾",
    layout="centered"
)

st.title("🐾 PetBuddy")
st.subheader("Control de alimentación por voz 🎙️")

st.write(
    "Presiona el botón, di un comando como **alimentar**, **dar comida** "
    "o **servir comida**, y PetBuddy activará el dispensador en Wokwi."
)

st.divider()

st.markdown("### 🎙️ Habla con PetBuddy")

stt_button = Button(label="🎙️ Iniciar reconocimiento de voz", width=300)

stt_button.js_on_event("button_click", CustomJS(code="""
    var recognition = new webkitSpeechRecognition();
    recognition.continuous = false;
    recognition.interimResults = false;
    recognition.lang = "es-ES";

    recognition.onresult = function (e) {
        var value = "";
        for (var i = e.resultIndex; i < e.results.length; ++i) {
            if (e.results[i].isFinal) {
                value += e.results[i][0].transcript;
            }
        }

        if (value != "") {
            document.dispatchEvent(new CustomEvent("GET_TEXT", {detail: value}));
        }
    }

    recognition.start();
"""))

result = streamlit_bokeh_events(
    stt_button,
    events="GET_TEXT",
    key="listen",
    refresh_on_update=False,
    override_height=80,
    debounce_time=0
)

if result and "GET_TEXT" in result:
    texto_voz = result.get("GET_TEXT").strip().lower()

    st.success(f"Comando escuchado: {texto_voz}")

    comandos_validos = [
        "alimentar",
        "dar comida",
        "servir comida",
        "comida",
        "dale comida",
        "darle comida",
        "alimenta a mi mascota",
        "alimentar mascota",
        "petbuddy alimentar"
    ]

    comando_reconocido = any(comando in texto_voz for comando in comandos_validos)

    if comando_reconocido:
        enviado = enviar_comando_mqtt("alimentar")

        if enviado:
            with st.spinner("Sirviendo comida..."):
                time.sleep(1)

            st.balloons()
            st.success("¡Comida servida! 🐶🍖")
    else:
        st.warning("No reconocí ese comando. Intenta decir: alimentar, dar comida o servir comida.")

st.divider()

st.markdown("### 🧪 Prueba manual")

if st.button("Alimentar manualmente 🦴", use_container_width=True):
    enviado = enviar_comando_mqtt("alimentar")

    if enviado:
        st.success("Comando enviado manualmente a Wokwi 🐾")

st.divider()

st.info("Recuerda: primero debes darle Play a Wokwi y luego probar el comando desde Streamlit.")
