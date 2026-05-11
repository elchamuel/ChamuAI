import groq 
from groq import Groq
import streamlit as st 

# CONFIGURACION INICIAL ------------------

def config_inicial():
    st.set_page_config(
        page_title="ChamuAI", 
        page_icon="🤖"
    )

# API -----------------------------------

api_key = st.secrets.get("CLAVE_API")

def obtener_cliente():
    if api_key :
        return Groq(api_key = api_key) 
    else:
        st.error("❌No se encontró la API Key revisa que esté todo bien configurado.")
        st.stop()

# MODELOS ------------------------------

modelos = {
    "Groq": "groq/compound",
    "Groq Mini": "groq/compound-mini", 
    "Llama": "llama-3.1-8b-instant"
}

# ESTADO -------------------------------

def inicializar_estado():
    if "mensajes" not in st.session_state:
        st.session_state.mensajes = [
            {
                "role": "assistant",
                "content": "¡Hola! soy ChamuAI, en que puedo ayudarte?"
            }
        ]

# IA ----------------------------------

def obtener_respuesta(cliente, modelo, mensajes):
    response = cliente.chat.completions.create(
        model=modelo,
        messages=mensajes
    )
    return response.choices[0].message.content

# MAIN ---------------------------------

def main():
    config_inicial()
    st.title("ChamuAI")
    cliente = obtener_cliente()
    inicializar_estado()

    st.sidebar.title("Opciones de Configuracion")
    modelo_nombre = st.sidebar.selectbox(
        "Elegi el modelo a usar: ", 
        list(modelos.keys())
    )
    modelo = modelos[modelo_nombre]
    for mensaje in st.session_state.mensajes:
        with st.chat_message(mensaje["role"]):
            st.write(mensaje["content"])
    #input del usuario
    if prompt := st.chat_input("Pregunta a ChamuAI..."):
        #agrego prompt a la lista de mensajes
        st.session_state.mensajes.append(
            {
                "role": "user",
                "content": prompt
            }
        )
        #mensaje del usuario
        with st.chat_message("user"):
            st.write(prompt)
        #respuesta de la IA
        with st.chat_message("assistant"):
            with st.spinner("Elaborando respuesta..."):
                respuesta = obtener_respuesta(cliente, modelo, st.session_state.mensajes)
                st.write(respuesta)
        #agrego respuesta de la IA a lista de mensajes
        st.session_state.mensajes.append(
            {
                "role": "assistant",
                "content": respuesta
            }
        )

if __name__ == "__main__":
    main()