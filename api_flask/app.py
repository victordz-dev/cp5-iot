from flask import Flask, request, jsonify
import json
import os
from datetime import datetime

app = Flask(__name__)

DATA_FILE = 'dados.json'

def init_db():
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'w') as f:
            json.dump([], f)

@app.route('/api/dados_re', methods=['POST'])
def receber_dados():
    try:
        dados = request.get_json()
        
        if not dados:
            return jsonify({"erro": "Nenhum dado fornecido"}), 400
            
        distancia = dados.get('distancia')
        timestamp = dados.get('timestamp')
        
        if not timestamp:
            timestamp = datetime.now().isoformat()
            
        if distancia is None:
            return jsonify({"erro": "O campo 'distancia' é obrigatório"}), 400
            
        registro = {
            "distancia": distancia,
            "timestamp": timestamp
        }
        
        with open(DATA_FILE, 'r') as f:
            historico = json.load(f)
            
        historico.append(registro)
        
        with open(DATA_FILE, 'w') as f:
            json.dump(historico, f, indent=4)
            
        return jsonify({"mensagem": "Dados recebidos e armazenados com sucesso!", "registro": registro}), 201

    except Exception as e:
        return jsonify({"erro": str(e)}), 500

@app.route('/api/dados_re', methods=['GET'])
def listar_dados():
    try:
        if not os.path.exists(DATA_FILE):
            return jsonify([]), 200
            
        with open(DATA_FILE, 'r') as f:
            historico = json.load(f)
        return jsonify(historico), 200
    except Exception as e:
        return jsonify({"erro": str(e)}), 500

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=True)
