from flask import Flask, request, jsonify
import utils
import mysql.connector


# Configura la conexión a la base de datos
db = mysql.connector.connect(
    host='localhost',
    user='root',
    password='password',
    database='mezumo'
)
cursor = db.cursor()


# Crear una instancia con FastAPI
app = Flask(__name__)


@app.route('/ruletas', methods=['POST'])
def crear_ruleta():

    '''
    Esta funcion se encarga de generar un id y agregarlo a la base de datos.

    '''
    
    # Crear el id
    ruleta_id = utils.generar_id()
    
    # Almacenar la nueva ruleta en la base de datos
    query = "INSERT INTO ruletas (id, estado) VALUES (%s, %s)"
    values = (ruleta_id, 0)
    cursor.execute(query, values)
    db.commit()
    
    return jsonify({'ruleta_id': ruleta_id})




# Iniciar el servidor de desarrollo uvicorn
if __name__ == "__main__":
    app.run(debug=True, port=3006)