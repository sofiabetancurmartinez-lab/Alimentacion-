import streamlit as st
import paho.mqtt.client as mqtt
import time

BROKER = "broker.hivemq.com"
PORT = 1883
TOPIC = "petbuddy/sofia/alimentar"

def enviar_comando(comando):
    try:
        client = mqtt.Client()
        client.connect(BROKER, PORT, 60)
        client.publish(TOPIC, comando)
        client.disconnect()
        return True
    except Exception as e:
        st.error(f"Error enviando comando: {e}")
        return False

st.set_page_config(
    page_title="PetBuddy",
    page_icon="🐾",
    layout="centered"
)

st.title("🐾 PetBuddy")
st.subheader("Página 1: Alimentación inteligente")

st.write(
    "Controla la alimentación de tu mascota desde una interfaz multimodal "
    "usando botones y comandos de texto."
)

st.divider()

st.markdown("## 🍽️ Alimentar mascota")

st.image(
    "https://cdn-icons-png.flaticon.com/512/616/616408.png",
    width=150
)

if st.button("Alimentar ahora 🦴", use_container_width=True):
    enviado = enviar_comando("alimentar")

    if enviado:
        with st.spinner("Enviando comida..."):
            time.sleep(1)

        st.success("¡Comida servida! 🐶🍖")
        st.balloons()

st.divider()

st.markdown("## 💬 Comando por texto")

comando_texto = st.text_input(
    "Escribe un comando",
    placeholder="Ej: alimentar, dar comida, comida"
)

if st.button("Enviar comando", use_container_width=True):
    comando = comando_texto.lower().strip()

    comandos_validos = [
        "alimentar",
        "dar comida",
        "comida",
        "servir comida",
        "feed"
    ]

    if comando in comandos_validos:
        enviado = enviar_comando("alimentar")

        if enviado:
            st.success("Comando reconocido. Alimentando a tu mascota 🐾")
    else:
        st.warning("Comando no reconocido. Intenta escribir: alimentar o dar comida.")

st.divider()

st.markdown("## 📋 Estado del sistema")

st.info("Sistema conectado a PetBuddy. Listo para enviar comandos al dispensador.")

with st.expander("¿Qué hace esta página?"):
    st.write(
        "Esta página permite controlar un dispensador inteligente de comida "
        "para mascotas. Al presionar el botón o escribir un comando válido, "
        "Streamlit envía una señal por MQTT al ESP32 simulado en Wokwi."
    )
