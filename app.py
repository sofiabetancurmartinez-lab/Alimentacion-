import os
import streamlit as st
from bokeh.models.widgets import Button
from bokeh.models import CustomJS
from streamlit_bokeh_events import streamlit_bokeh_events
from PIL import Image
import time
import glob
import paho.mqtt.client as paho
import json
from gtts import gTTS
from googletrans import Translator

def on_publish(client,userdata,result):
    print("Comando enviado correctamente \n")
    pass

def on_message(client, userdata, message):
    global message_received
    time.sleep(2)
    message_received=str(message.payload.decode("utf-8"))
    st.write(message_received)

broker="broker.mqttdashboard.com"
port=1883
client1 = paho.Client(client_id="petbuddy_sofia")
client1.on_message = on_message

st.title("🐾 PETBUDDY")
st.subheader("CONTROL DE ALIMENTACIÓN POR VOZ")

image = Image.open('voice_ctrl.jpg')

st.image(image, width=200)

st.write("Toca el botón y di: alimentar, dar comida o servir comida")

stt_button = Button(label="🎙️ Iniciar", width=200)

stt_button.js_on_event("button_click", CustomJS(code="""
    var recognition = new webkitSpeechRecognition();
    recognition.continuous = true;
    recognition.interimResults = true;
 
    recognition.onresult = function (e) {
        var value = "";
        for (var i = e.resultIndex; i < e.results.length; ++i) {
            if (e.results[i].isFinal) {
                value += e.results[i][0].transcript;
            }
        }
        if ( value != "") {
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
    override_height=75,
    debounce_time=0)

if result:
    if "GET_TEXT" in result:

        comando = result.get("GET_TEXT").strip().lower()

        st.write("Comando escuchado:", comando)

        comandos_validos = [
            "alimentar",
            "dar comida",
            "servir comida",
            "comida",
            "dale comida"
        ]

        if comando in comandos_validos:

            client1.on_publish = on_publish
            client1.connect(broker,port)

            message = json.dumps({"Act1":"alimentar"})

            ret = client1.publish("petbuddy_sofia_2026/feed", message)

            st.success("🐶🍖 ¡Comida servida!")

        else:
            st.warning("Comando no reconocido")

try:
    os.mkdir("temp")
except:
    pass
