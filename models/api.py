from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import pandas as pd
import joblib
import os

# Criação da API com descrição
app = FastAPI(
    title="API Previsão Clínica Veterinária",
    description="Prevê o desfecho clínico e os dias de internação com base nos dados do paciente.",
    version="1.0.0"
)

# Carrega modelos e features
modelo_desfecho = joblib.load(os.path.join('models', 'modelo_desfecho.pkl'))
modelo_dias = joblib.load(os.path.join('models', 'modelo_dias.pkl'))
features_treinadas = joblib.load(os.path.join('models', 'features.pkl'))
le_y = joblib.load(os.path.join('models', 'label_encoder_y.pkl'))

# Define entrada
class DadosEntrada(BaseModel):
    FC: Optional[float]
    FR: Optional[float]
    PAS: Optional[float]
    Temp: Optional[float]
    Hematocrito: Optional[float]

# Rota de predição
@app.post("/prever", tags=["Previsão"], summary="Predição de desfecho e dias de internação")
def prever(dados: DadosEntrada):
    entrada = pd.DataFrame([{
        "FC": dados.FC or 0,
        "FR": dados.FR or 0,
        "PAS": dados.PAS or 0,
        "Temp": dados.Temp or 0,
        "Hematocrito": dados.Hematocrito or 0
    }])

    # Garante consistência com features do modelo
    for col in features_treinadas:
        if col not in entrada.columns:
            entrada[col] = 0
    entrada = entrada[features_treinadas]

    # Faz predição
    desfecho_cod = modelo_desfecho.predict(entrada)[0]
    desfecho = le_y.inverse_transform([desfecho_cod])[0]
    dias = modelo_dias.predict(entrada)[0]

    # Salva previsão para análise posterior
    os.makedirs("logs", exist_ok=True)
    entrada['previsao_desfecho'] = desfecho
    entrada['previsao_dias'] = dias
    entrada.to_csv("logs/previsoes.csv", mode="a", header=not os.path.exists("logs/previsoes.csv"), index=False)

    return {
        "desfecho_previsto": desfecho.capitalize(),
        "dias_previstos_internacao": round(dias, 2)

    }
    
from fastapi import UploadFile, File
from sklearn.metrics import accuracy_score, mean_absolute_error

@app.post("/validar", tags=["Validação"], summary="Valida previsões com dados reais")
def validar(arquivo: UploadFile = File(...)):
    df = pd.read_csv(arquivo.file)

    if 'previsao_desfecho' not in df.columns or 'real_desfecho' not in df.columns:
        raise HTTPException(status_code=400, detail="Colunas 'previsao_desfecho' e 'real_desfecho' são obrigatórias")
    if 'previsao_dias' not in df.columns or 'real_dias' not in df.columns:
        raise HTTPException(status_code=400, detail="Colunas 'previsao_dias' e 'real_dias' são obrigatórias")

    acc = accuracy_score(df['real_desfecho'], df['previsao_desfecho'])
    erro_medio = mean_absolute_error(df['real_dias'], df['previsao_dias'])

    return {
        "acuracia_desfecho": round(acc, 4),
        "erro_medio_dias_internacao": round(erro_medio, 2)
    }