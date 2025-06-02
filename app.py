from flask import Flask, request, jsonify
import json
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Permitir requests desde cualquier origen

# Para Railway: usar variable de entorno para el puerto
PORT = int(os.environ.get("PORT", 5000))

# Archivo para persistir los datos entre ejecuciones
DATA_FILE = 'rankings_data.json'

def load_data():
    """Carga los datos del archivo JSON"""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_data(data):
    """Guarda los datos en el archivo JSON"""
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2)

# Cargar datos al iniciar
rankings_data = load_data()

@app.route('/api/doce/<codigo_grupo>', methods=['GET'])
def get_rankings(codigo_grupo):
    """
    GET: Obtiene los rankings de jugadores para el código de grupo
    """
    try:
        if codigo_grupo not in rankings_data:
            # Si el grupo no existe, devuelve array vacío
            return jsonify([])
        
        # Convertir el formato interno a formato de respuesta
        result = []
        for nombre, ganadas in rankings_data[codigo_grupo].items():
            result.append({
                "nombreJugador": nombre,
                "cantidadPartidasGanadas": ganadas
            })
        
        # Ordenar por cantidad de partidas ganadas (descendente)
        result.sort(key=lambda x: x["cantidadPartidasGanadas"], reverse=True)
        
        return jsonify(result), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/api/doce', methods=['POST'])
def save_ranking():
    """
    POST: Guarda jugadores y sus puntajes en el grupo especificado
    """
    try:
        data = request.get_json()
        
        # Validar formato de entrada
        if not data or 'CodigoGrupo' not in data or 'jugador' not in data:
            return jsonify({"error": "Formato de datos inválido"}), 400
        
        codigo_grupo = data['CodigoGrupo']
        jugador = data['jugador']
        
        if 'nombre' not in jugador or 'vencedor' not in jugador:
            return jsonify({"error": "Datos del jugador incompletos"}), 400
        
        nombre = jugador['nombre']
        vencedor = jugador['vencedor']
        
        # Inicializar grupo si no existe
        if codigo_grupo not in rankings_data:
            rankings_data[codigo_grupo] = {}
        
        # Inicializar jugador si no existe
        if nombre not in rankings_data[codigo_grupo]:
            rankings_data[codigo_grupo][nombre] = 0
        
        # Si ganó (vencedor = 1), incrementar contador
        if vencedor == 1:
            rankings_data[codigo_grupo][nombre] += 1
        
        # Guardar datos
        save_data(rankings_data)
        
        return '', 204  # No Content
        
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/api/doce/<codigo_grupo>', methods=['DELETE'])
def reset_group(codigo_grupo):
    """
    DELETE: Elimina todos los rankings de un grupo específico
    """
    try:
        if codigo_grupo in rankings_data:
            del rankings_data[codigo_grupo]
            save_data(rankings_data)
        
        return jsonify({"message": f"Grupo {codigo_grupo} reseteado correctamente"}), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/status', methods=['GET'])
def status():
    """Endpoint para verificar que la API está funcionando"""
    return jsonify({
        "status": "API Mock funcionando",
        "grupos_activos": len(rankings_data),
        "total_jugadores": sum(len(grupo) for grupo in rankings_data.values())
    })

if __name__ == '__main__':
    print("=== API Mock para Juego UNO ===")
    print("Endpoints disponibles:")
    print("GET    /api/doce/<codigo_grupo>  - Obtener rankings")
    print("POST   /api/doce                 - Guardar resultado")
    print("DELETE /api/doce/<codigo_grupo>  - Resetear grupo")
    print("GET    /status                   - Estado de la API")
    print(f"\nEjecutándose en puerto: {PORT}")
    print("=====================================")
    
    app.run(debug=False, host='0.0.0.0', port=PORT)