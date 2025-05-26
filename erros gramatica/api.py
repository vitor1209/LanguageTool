import pandas as pd
import requests
import time

df = pd.read_csv('errosConcordância.csv')
url = 'http://localhost:8081/v2/check'  
headers = {
    "Content-Type": "application/x-www-form-urlencoded"
}

resultados = []

for i, linha in df.iterrows():
    payload = {
        "texto": linha['Frase_com_Erro']  
    }

    try:
        data = {
            "text": payload["texto"],
            "language": "pt-BR",
            "disabledRules": "COMMA_PARENTHESIS_WHITESPACE,UPPERCASE_SENTENCE_START,WHITESPACE_RULE"
        }
        response = requests.post(url, headers=headers, data=data)
        matches = response.json().get("matches", [])
        resultados.append({
            "id": linha.get("id", i),
            "resposta": matches
        })
    except Exception as e:
        resultados.append({
            "id": linha.get("id", i),
            "erro": str(e)
        })
    
    time.sleep(0.1) 

import json
with open("respostas.json", "w", encoding="utf-8") as f:
    json.dump(resultados, f, ensure_ascii=False, indent=2)
