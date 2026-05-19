import streamlit as st
import paho.mqtt.client as mqtt
import time

# ---------- CONFIG ----------
BROKER = "broker.hivemq.com"
PORT = 1883
TOPIC = "petbuddy/sofia/alimentar"

# ---------- FUNCIÓN MQTT ----------
def enviar_comando(comando):
    client = mqtt.Client()
    client.connect(BROKER, PORT, 60)
    client.publish(TOPIC, comando)
    client.disconnect()

# ---------- INTERFAZ ----------
st.set_page_config(page_title="PetBuddy - Alimentación", page_icon="🐾")

st.title("🐾 PetBuddy")
st.subheader("Página 1: Alimentación inteligente")

st.write(
    "Controla la alimentación de tu mascota usando botones o comandos de texto."
)

st.image(
    "https://cdn-icons-png.flaticon.com/512/616/616408.png",
    width=150
)

st.divider()

st.markdown("### 🍽️ Alimentación automática")

if st.button("Alimentar ahora 🦴"):
    enviar_comando("alimentar")
    st.success("Comando enviado: alimentando a la mascota...")
    st.balloons()

st.divider()

st.markdown("### 💬 Comando por texto")

comando_texto = st.text_input(
    "Escribe un comando",
    placeholder="Ej: alimentar, dar comida, comida"
)

if st.button("Enviar comando"):
    comando = comando_texto.lower().strip()

    if comando in ["alimentar", "dar comida", "comida", "feed"]:
        enviar_comando("alimentar")
        st.success("Comando reconocido. Alimentando mascota 🐶")
    else:
        st.warning("Comando no reconocido. Intenta con: alimentar o dar comida.")

st.divider()

st.markdown("### 📋 Estado del sistema")

estado = st.empty()

estado.info("Sistema listo para recibir comandos.")

with st.expander("¿Qué pasa en Wokwi?"):
    st.write(
        "Cuando envías el comando, el ESP32 recibe la señal por MQTT, "
        "enciende un LED y mueve un servo simulando el dispensador de comida."
    )
