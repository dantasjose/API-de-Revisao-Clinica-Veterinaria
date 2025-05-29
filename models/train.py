import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, GradientBoostingRegressor
from sklearn.preprocessing import LabelEncoder
import joblib
import os
import json

# Caminhos relativos
base_dir = os.path.dirname(__file__)
dataset_dir = os.path.join(base_dir, '..', 'dataset')  # Volta uma pasta

# Criar pasta models
os.makedirs(os.path.join(base_dir, 'models'), exist_ok=True)

# === 1. Carregar datasets ===
df_evolucao = pd.read_csv(os.path.join(dataset_dir, 'evolucao_tabela.csv'))
df_evolucao['ID_PET'] = df_evolucao['Animal']

df_dados = pd.read_excel(os.path.join(dataset_dir, 'dados_veterinarios.xlsx'))
df_dados['ID_PET'] = df_dados['paciente']

# === 2. Carregar JSON ===
with open(os.path.join(dataset_dir, 'dados_veterinarios_estruturados.json'), encoding='utf-8') as f:
    data = json.load(f)

lista = []
for nome, conteudo in data.items():
    registro = {'ID_PET': nome}
    registro.update(conteudo.get('info', {}))
    registro.update(conteudo.get('hematologia', {}))
    lista.append(registro)
df_json = pd.DataFrame(lista)

# === 3. Merge ===
df_merge = df_evolucao.merge(df_dados, on='ID_PET', how='outer')
df_merge = df_merge.merge(df_json, on='ID_PET', how='outer')

print("✅ Datasets unificados!")

# === 4. Tratar valores ausentes ===
df_merge = df_merge.fillna(0)

# === 5. Separar features e alvos ===
try:
    X = df_merge.drop(columns=['desfecho', 'data_inicio', 'data_fim', 'ID_PET'], errors='ignore')
    y_class = df_merge['desfecho'].astype(str)
    y_reg = (pd.to_datetime(df_merge['data_fim']) - pd.to_datetime(df_merge['data_inicio'])).dt.days
except KeyError as e:
    print(f"⚠️ Erro: Coluna ausente - {e}")
    exit()

# === 5.1. Codificar features ===
label_encoders_X = {}
for column in X.select_dtypes(include=['object']).columns:
    le = LabelEncoder()
    X[column] = le.fit_transform(X[column].astype(str))
    label_encoders_X[column] = le

# Salvar label encoders
joblib.dump(label_encoders_X, os.path.join(base_dir, 'models', 'label_encoders_X.pkl'))

# === 5.2. Codificar variável alvo ===
le_y = LabelEncoder()
y_class_encoded = le_y.fit_transform(y_class)
joblib.dump(le_y, os.path.join(base_dir, 'models', 'label_encoder_y.pkl'))

# ✅ Salvar features usadas
features_treinadas = list(X.columns)
joblib.dump(features_treinadas, os.path.join(base_dir, 'models', 'features.pkl'))
print(f"✅ Features salvas: {features_treinadas}")

# === 6. Split ===
X_train, X_test, y_train, y_test = train_test_split(X, y_class_encoded, test_size=0.2, random_state=42)

# === 7. Treinar classificação ===
clf = RandomForestClassifier(n_estimators=100, random_state=42)
clf.fit(X_train, y_train)
joblib.dump(clf, os.path.join(base_dir, 'models', 'modelo_desfecho.pkl'))
print("✅ Modelo de desfecho salvo!")

# === 8. Treinar regressão ===
X_train_reg, X_test_reg, y_train_reg, y_test_reg = train_test_split(X, y_reg, test_size=0.2, random_state=42)
reg = GradientBoostingRegressor()
reg.fit(X_train_reg, y_train_reg)
joblib.dump(reg, os.path.join(base_dir, 'models', 'modelo_dias.pkl'))
print("✅ Modelo de dias de internação salvo!")

print("✅ Todos os modelos e recursos prontos!")
