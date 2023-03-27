from flask import Flask, render_template,request,flash,redirect,url_for
import requests

import pymysql
import random
import string

HOST="betwimurrau9vuev9jbb-mysql.services.clever-cloud.com"
USERNAME="ucwjmsl59slmoav9"
PASSWORD="8HaZG6bN2qIiR4VF7tke"
DATABASE="betwimurrau9vuev9jbb"

app = Flask(__name__)


@app.before_request
def before_request():
    print('Antes de la petición ')
    return 

@app.after_request
def after_request(response):
    print('Despues de la petición')
    return response

@app.route('/')
def index():
    # query the data
    connection = pymysql.connect(host= HOST, port=3306, user=USERNAME, passwd=PASSWORD, database=DATABASE)
    cursor = connection.cursor()
    query = "SELECT * FROM Rapsberry2 ORDER BY series"
    cursor.execute(query)
    results = cursor.fetchall()
    # close the database connection
    connection.close()

    data ={
        'titulo' :'Algoritmos inteligentes',
        'bienvenida': 'ALGORITMOS INTELIGENTES BASADOS EN COMPORTAMIENTO DE PLANTAS Y ÁRBOLES PARA SU SIMULACIÓN EN MECANISMOS CON IMPACTO EN SALUD DIGITAL',
        'datos': results
    }

    return render_template('index.html', data=data)



@app.route('/contacto/<nombre>/<int:serie>')
# def hello_world():
#     return '<h1>¡Hola, Mundo julio!</h1>'
def conexion(nombre,serie):
    data ={
        'Raspberry' :'Conexion',
        'nombre': nombre,
        'serie': serie
    }
    return render_template('conexion.html', data=data)

@app.route('/on')
def led_on():
   
    return 'LED encendido'

@app.route('/off')
def led_off():
    
    return 'LED apagado'


def query_string():
    print(request)
    print(request.args)
    print(request.args.get('param1'))
    print(request.args.get('param2'))
    return "ok"

@app.route('/add', methods=['GET', 'POST'])
def add_data():
    if request.method == 'POST':
        name = request.form['name']
        series = request.form['series']
        status = request.form['status']

        try:
            connection = pymysql.connect(host=HOST, port=3306, user=USERNAME, passwd=PASSWORD, database=DATABASE)
            cursor = connection.cursor()
            query = f"INSERT INTO Rapsberry2 (name, series, status) VALUES ('{name}', '{series}', '{status}')"
            cursor.execute(query)
            connection.commit()
            connection.close()
            # flash('Data added successfully!', 'success')
        except Exception as e:
            print(e)
            connection.rollback()
            # flash('Error adding data.', 'danger')

    return render_template('add.html')

@app.route('/delete/<int:id>', methods=['POST'])
def delete_data(id):
    # delete the data
    connection = pymysql.connect(host= HOST, port=3306, user=USERNAME, passwd=PASSWORD, database=DATABASE)
    cursor = connection.cursor()
    query = "DELETE FROM Rapsberry2 WHERE id=%s"
    cursor.execute(query, id)
    connection.commit()
    # close the database connection
    connection.close()

    # flash('¡Dato eliminado exitosamente!')

    return redirect(url_for('index'))

@app.route('/edit/<int:id>', methods=['GET','POST'])
def edit_data(id):
    # -----------------------------------------
    url = 'https://332e-2806-2f0-a120-ee14-2747-8013-4dc0-a60c.ngrok.io/'
    if request.method == 'POST':
        status = request.form['status']
        if status == 'Encendido':
                def_url=url+'/on'
                response = requests.get(def_url)
                # Verificar la respuesta del servidor
                if response.status_code == 200:
                    print('LED encendido')
                else:
                    print('Error al enviar la solicitud')
        if status == 'Apagado':
                def_url=url+'/off'
                response = requests.get(def_url)
                # Verificar la respuesta del servidor
                if response.status_code == 200:
                    print('LED apagado')
                else:
                    print('Error al enviar la solicitud')

        connection = pymysql.connect(host=HOST, port=3306, user=USERNAME, passwd=PASSWORD, database=DATABASE)
        cursor = connection.cursor()
        query = f"UPDATE Rapsberry2 SET status='{status}' WHERE id={id}"
        cursor.execute(query)
        connection.commit()
        connection.close()
            # flash('Data updated successfully!', 'success')
    
    return redirect(url_for('index'))

def pag_no_encotrada(error):
    return render_template('404.html'), 404
    # return redirect(url_for('index'))
#the firtly return direct to page no found 
#the second return, return to page index

if __name__ == '__main__':
    app.add_url_rule('/query_string', view_func= query_string)
    
    app.register_error_handler(404,pag_no_encotrada)
    app.run(debug=True, port= 8000)