from flask import Flask, request, jsonify
import utils
import mysql.connector
import json


# Configura la conexión a la base de datos
db = mysql.connector.connect(
    host='localhost',
    user='root',
    password='password',
    database='mezumo'
)

cursor = db.cursor()


# Crear una instancia con Flask
app = Flask(__name__)

##########################################################################

# Endpoint de creacion de ruleta
@app.route('/ruletas', methods=['POST'])
def crear_ruleta():

    '''
    Esta funcion se encarga de generar un id y agregarlo a la base de datos.

    '''
    
    # Crear el id.
    ruleta_id = utils.generar_id()
    
    # Almacenar la nueva ruleta en la base de datos.
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

    # Buscar el id en la tabla ruletas.
    query = "SELECT estado FROM ruletas WHERE id = %s"
    cursor.execute(query, (ruleta_id,))
    ruleta = cursor.fetchone()

    # Generar la apertura de la ruleta si es que existe y que este en estado igual a 0.
    if ruleta and ruleta[0] == 0:

        # Update al estado de la ruleta.
        query_estado = "UPDATE ruletas SET estado = 1 WHERE id = %s"
        cursor.execute(query_estado, (ruleta_id,))
        db.commit()

        return jsonify({'estado': 'Apertura exitosa'})
    
    else:

        return jsonify({'estado': 'Apertura denegada'})

##########################################################################

# Endpoint de apuesta a un numero o color.
@app.route('/ruletas/<ruleta_id>/apuesta', methods=['POST'])
def realizar_apuesta(ruleta_id):

    '''
    Esta funcion se encarga de realizar la apuesta de un numero o un color.

    '''

    # Buscar el id en la tabla ruletas.
    query = "SELECT estado FROM ruletas WHERE id = %s"
    cursor.execute(query, (ruleta_id,))
    ruleta = cursor.fetchone()

    # Generar la apertura de la ruleta si es que existe y que este en estado igual a 0.
    if ruleta and ruleta[0] == 1:

        # Obtener los headers y guardarlos en variables.
        usuario_id = request.headers.get('User')
        apuesta =  json.loads(request.headers.get('Apuesta')) 
        tipo = apuesta['tipo']
        valor = apuesta['valor']
        color = apuesta['color'] 
        numero = apuesta['numero'] 

        # Verificar si es un numero o un color y que el valor de la apuesta no supere los 10000.
        if tipo in ['numero', 'color'] and valor <= 10000:
            
            # Si el tipo de apuesta es un numero.
            if tipo == 'numero': 

                    # Verificar que el numero este en el rango (0,36)
                    if numero >= 0 and numero <= 36:

                        # Insertar apuesta
                        quere_apuesta = "INSERT INTO apuestas(id_apuesta,id_ruleta, valor, tipo, numero, id_usuario) VALUES(%s, %s, %s, %s, %s, %s)"
                        cursor.execute(quere_apuesta,(utils.generar_id(),ruleta_id, valor, tipo, numero, usuario_id,))
                        db.commit()

                        return jsonify({'estado':'Apuesta realizada'})
                    
                    else:

                        return jsonify({'mensaje':'El numero a apostar es incorrecto'})

            # Si el tipo de apuesta es un color.
            elif tipo == 'color':

                # Si el color es negro o rojo.
                if color in ['rojo','negro']:

                    # Insertar apuesta
                    quere_apuesta = "INSERT INTO apuestas(id_apuesta,id_ruleta, valor, tipo, color, id_usuario) VALUES(%s, %s, %s, %s, %s, %s)"
                    cursor.execute(quere_apuesta,(utils.generar_id(),ruleta_id, valor, tipo, color, usuario_id,))
                    db.commit()

                    return jsonify({'estado':'Apuesta realizada'})
            
                else:

                    return jsonify({'mensaje':'El color ingresado es incorrecto'})

        else:

            return jsonify({'mensaje':'Tipo de apuesta o valor de la apuesta invalidos.'})
        
##########################################################################

# Endpoint de cierre de apuestas.
@app.route('/ruletas/<int:ruleta_id>/cierre', methods=['POST'])
def cerrar_apuestas(ruleta_id):

    '''
    Esta funcion se engarga de cerrar la ruleta.

    '''

    # Crear numero ganador.
    numero_ganador = utils.numero_ganador()

    # Crear color ganador.
    color_ganador = utils.color_ganador(numero_ganador)

    # Obtener las apuestas de la ruleta
    query = "SELECT * FROM apuestas WHERE id_ruleta = %s"
    cursor.execute(query, (ruleta_id,))
    apuestas = cursor.fetchall()

    # Variable para guardar resultados
    Ganancia = 0

    # Calcular resultados
    for apuesta in apuestas:

        apuesta_id = apuesta[0]
        usuario_id = apuesta[6]
        valor_apuesta = apuesta[2]
        tipo_apuesta = apuesta[3]

        if tipo_apuesta == 'numero':

            if apuesta[4] == numero_ganador:

                Ganancia = valor_apuesta * 5

        elif tipo_apuesta == 'color':

            if apuesta[5] == color_ganador:

                Ganancia = valor_apuesta * 1.8


    # Marcar la ruleta como cerrada
    cursor.execute("UPDATE ruletas SET estado = 0 WHERE id = %s", (ruleta_id,))
    
    # Confirmar los cambios en la base de datos
    db.commit()
    cursor.close()
    
    return jsonify({'mensaje': 'Apuestas cerradas', 'numero_ganador' : numero_ganador, 'color_ganador' : color_ganador,'Usuario' : usuario_id ,'Apuesta' : apuesta_id,'Valor apostado' : valor_apuesta,'Ganancia' :  Ganancia})


# Iniciar el servidor
if __name__ == "__main__":
    app.run(debug=True, port=3007)