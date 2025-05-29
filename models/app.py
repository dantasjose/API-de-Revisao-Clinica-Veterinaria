
import streamlit as st
import requests
from pyngrok import ngrok  # Adicione esta linha

st.title("Diagnóstico Veterinário Automatizado")

# Inputs
FC = st.number_input("Frequência Cardíaca", 0, 300, 100)
FR = st.number_input("Frequência Respiratória", 0, 100, 20)
PAS = st.number_input("Pressão Arterial Sistólica", 0, 300, 120)
Temp = st.number_input("Temperatura", 30.0, 42.0, 38.5)
Hematocrito = st.number_input("Hematócrito", 0.0, 100.0, 40.0)

# Botão de previsão
if st.button("Prever Desfecho e Dias de Internação"):
    entrada = {
        "FC": FC,
        "FR": FR,
        "PAS": PAS,
        "Temp": Temp,
        "Hematocrito": Hematocrito
    }
    
    try:
        response = requests.post("http://localhost:8000/prever", json=entrada)
        if response.status_code == 200:
            resultado = response.json()
            st.success(f"**Desfecho:** {resultado['desfecho_previsto']}")
            st.info(f"**Dias estimados de internação:** {resultado['dias_previstos_internacao']:.1f}")
        else:
            st.error("Erro ao obter previsão. Verifique se a API está rodando.")
    except Exception as e:
        st.error(f"Erro ao conectar com a API: {e}")
