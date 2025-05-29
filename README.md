# API de Previsão Clínica Veterinária

Esta API fornece recursos para prever o desfecho clínico e estimar a duração de internação de pacientes veterinários com base em sinais vitais e exames laboratoriais.

---

## 📚 Tecnologias e Dependências

* **Python 3.13**
* **FastAPI**: framework web para criação de APIs rápidas e modernas
* **scikit-learn**: treinamento e inferência de modelos de Machine Learning (RandomForestClassifier e GradientBoostingRegressor)
* **pandas**: manipulação e processamento de dados
* **joblib**: serialização de modelos e encoders
* **python-multipart**: necessário para endpoints que recebem arquivos via `UploadFile`

Instale as dependências com:

```bash
pip install -r requirements.txt
```

Arquivo `requirements.txt` sugerido:

```
fastapi
uvicorn
scikit-learn
pandas
joblib
python-multipart
```

---

## 📂 Estrutura do Projeto

```
/Apiweb
├── dataset/                    # Dados brutos (CSV, Excel, JSON)
├── models/                     # Modelos e encoders salvos (*.pkl)
├── src/                        # Código-fonte da aplicação
│   ├── api.py                  # Roteiros FastAPI e rotas
│   ├── train.py                # Script de treinamento e salvamento de modelos
│   └── test_api.py             # Testes automatizados da API
├── logs/                       # Histórico de previsões geradas
├── .gitignore                  # Arquivos e pastas a serem ignorados pelo Git
├── README.md                   # Documentação do projeto
└── requirements.txt            # Dependências do projeto
```

---

## 🚀 Como executar

1. **Treinar os modelos** (gera arquivos `.pkl` em `models/`):

   ```bash
   cd src
   python train.py
   ```

2. **Iniciar a API**:

   ```bash
   uvicorn models.api:app --reload --port 8000
   ```

3. **Acessar a documentação interativa**:

   Abra no navegador: `http://127.0.0.1:8000/docs`

4. **Exemplo de requisição**:

   ```bash
   curl -X POST "http://127.0.0.1:8000/prever" \
     -H "Content-Type: application/json" \
     -d '{
       "FC": 80.0,
       "FR": 20.0,
       "PAS": 120.0,
       "Temp": 38.5,
       "Hematocrito": 42.0
     }'
   ```

---

## 📊 Rotas Disponíveis

* **POST /prever**

  * Recebe JSON com sinais vitais e retorna:

    * `desfecho_previsto`: Alta, Óbito ou Eutanásia
    * `dias_previstos_internacao`: número estimado de dias

* **POST /validar**

  * Recebe um arquivo CSV via `multipart/form-data` com colunas: `previsao_desfecho`, `real_desfecho`, `previsao_dias`, `real_dias`
  * Retorna métricas de performance:

    * `acuracia_desfecho`
    * `erro_medio_dias_internacao`

---

## 🤝 Contribuições

Contribuições são bem-vindas!

1. Abra uma issue descrevendo o problema ou sugestão.
2. Faça um fork do projeto.
3. Crie uma branch com a feature ou correção (`git checkout -b feature/nome-da-feature`).
4. Faça commit das suas alterações (`git commit -m 'feat: descrição'`).
5. Faça push para a branch (`git push origin feature/nome-da-feature`).
6. Abra um Pull Request.

---

## 📄 Licença

Este projeto está licenciado sob a [MIT License](LICENSE).
