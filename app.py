from flask import Flask, jsonify, request, abort  # importar librerias el jsonify es para convertir un diccionario a un json se retornan los datos
import mysql.connector  # importar libreria de mysql
from mysql.connector import Error  # importar libreria de errores de mysql por si da un error

app = Flask(__name__) # se inicializo flask y se le paso el nombre de la aplicacion
# diccionario de estudiantes
# estudiantes = {}
# identificador_estudiante = 1

# conexion a la base de datos
conexion_bd = {
    'host': 'localhost',
    'database': 'estudiantes_db_api',
    'user': 'adonay',
    'password': '12345',
    'port': 3307  # puerto de la base de datos
}

# metodo crear estudiante
@app.route('/estudiante', methods=['POST'])
def crear_estudiante():  # metodo que sera consumido desde una url
    # global identificador_estudiante #variable global que se puede modificar
    body = request.get_json()  # cuando haga un request lo que se escribio en el body como un json se va a guardar en la variable body

    # id = identificador_estudiante

    # validar que el body tenga los datos necesarios y si no tiene retornar un error
    if not body or 'nombre' not in body or 'apellido' not in body or 'edad' not in body:
        abort(400, "Datos faltantes en el request") # 400 es bad request

    """#coleccion con parametro de identificador_estudiante
    estudiantes[identificador_estudiante] = {
        'id': identificador_estudiante,
        'nombre': body['nombre'],
        'apellido': body['apellido'],
        'edad': body['edad']
    }
    #consumir

    # identificador_estudiante += 1
    # return jsonify(estudiantes[id]), 201 # 201 es created que se creo correctamente """

    try:
        conexion = mysql.connector.connect(**conexion_bd) # conexion a la base de datos
        cursor = conexion.cursor()  # cursor es un objeto que permite ejecutar sentencias sql
        sql = "INSERT INTO estudiante (nombre, apellido, edad) VALUES (%s, %s, %s)"
        valores = (body['nombre'], body['apellido'], body['edad']) # valores que se van a insertar
        cursor.execute(sql, valores) # ejecuta la sentencia sql
        conexion.commit()  # se asegura para que se guarden los datos en la base de datos
        estudiante_id = cursor.lastrowid # obtiene el ultimo id insertado

        # retornar el estudiante creado
        return jsonify({'id': estudiante_id, 'nombre': body['nombre'], 'apellido': body['apellido'], 'edad': body['edad']}), 201 # 201 es created que se creo correctamente

    except Error as e:
        print(f"Error al conectar a MySQL: {e}")  # si hay un error
        abort(500, "Error al conectar a la base de datos") # abortar la conexion

    finally:
        cursor.close()  # cierra el cursor
        conexion.close() # cierra la conexion


# OBTENER estudiante en plural trae todos los estudiantes
@app.route('/estudiante', methods=['GET'])
def obtener_estudiantes():
    try:
        conexion = mysql.connector.connect(**conexion_bd)
        cursor = conexion.cursor(dictionary=True)  # cursor es un objeto que permite ejecutar sentencias sql y devolvera los resultados como un diccionario
        sql = "SELECT * FROM estudiante"
        cursor.execute(sql) # ejecuta la sentencia sql
        estudiantes = cursor.fetchall() # fetchall trae todos los registros

        # retornar los estudiantes
        return jsonify(estudiantes), 200 # 200 es ok que se ejecuto correctamente

    except Error as e:
        print(f"Error al conectar a MySQL: {e}")
        abort(500, "Error al conectar a la base de datos")

    finally:
        cursor.close()  # cerrar el cursor
        conexion.close() # cerrar la conexion


# OBTENER estudiante en singular trae un estudiante
@app.route('/estudiante/<int:id_estudiante>', methods=['GET'])
def obtener_estudiante(id_estudiante):
    try:
        conexion = mysql.connector.connect(**conexion_bd)
        cursor = conexion.cursor(dictionary=True)  # cursor es un objeto que permite ejecutar sentencias sql y devolvera los resultados como un diccionario
        sql = "SELECT * FROM estudiante WHERE id = %s"
        cursor.execute(sql, (id_estudiante,))  # ejecuta la sentencia sql
        estudiante = cursor.fetchone() # fetchone trae un solo registro

        # si no encuentra el estudiante
        if not estudiante:
            abort(404, "Estudiante no encontrado")  # 404 es not found
        return jsonify(estudiante), 200

    except Error as e:
        print(f"Error al conectar a MySQL: {e}")
        abort(500, "Error al conectar a la base de datos")

    finally:
        cursor.close()
        conexion.close()


# Método para eliminar un estudiante
@app.route('/estudiante/<int:id_estudiante>', methods=['DELETE'])
def eliminar_estudiante(id_estudiante):
    try:
        conexion = mysql.connector.connect(**conexion_bd)
        cursor = conexion.cursor() # cursor es un objeto que permite ejecutar sentencias sql
        sql = "DELETE FROM estudiante WHERE id = %s"
        cursor.execute(sql, (id_estudiante,))
        conexion.commit()  # se asegura para que se guarden los datos en la base de datos

        # si no encuentra el estudiante
        if cursor.rowcount == 0:
            abort(404, "Estudiante no encontrado") # 404 es not found
        return '', 204 # 204 es no content

    except Error as e: # si hay un error
        print(f"Error al conectar a MySQL: {e}")
        abort(500, "Error al conectar a la base de datos")

    finally:
        cursor.close()  # cerrar el cursor
        conexion.close() # cerrar la conexion


# Actualizar estudiante todos los campos con put
@app.route('/estudiante/<int:id_estudiante>', methods=['PUT'])
def actualizar_estudiante(id_estudiante):
    body = request.get_json() # cuando haga un request lo que se escribio en el body como un json se va a guardar en la variable body

    if not body or 'nombre' not in body or 'apellido' not in body or 'edad' not in body:
        abort(400, "Datos faltantes en el request") # 400 es bad request

    try:
        conexion = mysql.connector.connect(**conexion_bd)
        cursor = conexion.cursor()
        sql = "UPDATE estudiante SET nombre = %s, apellido = %s, edad = %s WHERE id = %s" # sentencia sql para actualizar
        valores = (body['nombre'], body['apellido'], body['edad'], id_estudiante) # valores que se van a actualizar
        cursor.execute(sql, valores)    # ejecuta la sentencia sql
        conexion.commit()   # se asegura para que se guarden los datos en la base de datos

        # si no encuentra el estudiante
        if cursor.rowcount == 0:
            abort(404, "Estudiante no encontrado") # 404 es not found
            # retornar el estudiante actualizado
        return jsonify({'id': id_estudiante, 'nombre': body['nombre'], 'apellido': body['apellido'], 'edad': body['edad']}), 200   # 200 es ok que se ejecuto correctamente

    except Error as e:
        print(f"Error al conectar a MySQL: {e}")
        abort(500, "Error al conectar a la base de datos")

    finally:
        cursor.close()
        conexion.close()


# metodo principal sea el punto de entrada
if __name__ == '__main__':
    app.run(debug=True)  # corre la aplicacion