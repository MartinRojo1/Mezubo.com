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

##########################################################################

# Endpoint de creacion de ruleta
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

##########################################################################

# Endpoint de apertura de ruleta.
@app.route('/ruletas/<ruleta_id>/apertura', methods=['POST'])
def abrir_ruleta(ruleta_id):
    
    '''
    Esta funcion se encarga de abrir la ruleta y devolver si fue abierta con exito o no.

    '''

    # Buscar el id en la tabla ruletas
    query = "SELECT estado FROM ruletas WHERE id = %s"
    cursor.execute(query, (ruleta_id,))
    ruleta = cursor.fetchone()

    # Generar la apertura de la ruleta si es que existe y que este en estado igual a 0.
    if ruleta and ruleta[0] == 0:

        # Update al estado de la ruleta
        query_estado = "UPDATE ruletas SET estado = 1 WHERE id = %s"
        cursor.execute(query_estado, (ruleta_id,))
        db.commit()

        return jsonify({'estado': 'Apertura exitosa'})
    
    else:

        return jsonify({'estado': 'Apertura denegada'})




# Iniciar el servidor de desarrollo uvicorn
if __name__ == "__main__":
    app.run(debug=True, port=3007)