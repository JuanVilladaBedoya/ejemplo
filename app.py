from flask import Flask
from flask import render_template, request, redirect, Response, url_for, session
from flask_mysqldb import MySQL,MySQLdb # pip install Flask-MySQLdb


app = Flask(__name__,template_folder='template')

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'salondebelleza'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app)


@app.route('/')
def principal():
    return render_template('index.html')

@app.route('/acceso')
def login():
    return render_template('adm-login.html')


@app.route('/acceso-login', methods= ["GET", "POST"])
def administrador():
   
    if request.method == 'POST' and 'txtCorreo' in request.form and 'txtPassword' in request.form:
       
        _correo = request.form['txtCorreo']
        _password = request.form['txtPassword']

        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM users WHERE correo = %s AND password = %s', (_correo, _password,))
        account = cur.fetchone()
      
        if account:
            session['logueado'] = True
            session['id'] = account['id']
            session['id_rol'] = account['id_rol']
            
            if session['id_rol']==1:
                return render_template("administrador.html")
            elif session['id_rol']==2:
                return render_template("productos.html")
        else:
            return render_template('adm-login.html',mensaje="Usuario O Contraseña Incorrectas")
        
@app.route('/administrador')
def webadminister():
    return render_template('administrador.html')

@app.route('/editarcontenido')
def editarcontenido():
    return render_template('subircontenido-adm.html')
    
@app.route('/productos')
def productos():
    return render_template('productos.html')


@app.route('/decuentos')
def descuentos():
    return render_template('descuentos.html')
    

@app.route('/contacto')
def contacto():
    return render_template('contacto.html')


@app.route('/store', methods=['POST', 'GET'])
def storage():

    nombre= request.form['txtNombre']
    celular= request.form['celular']
    ciudad= request.form['ciudad']
    correo= request.form['correo']

    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO usuarios (IDusuario, nombre, celular, ciudad, correo) VALUES (NULL, %s, %s, %s, %s)",(nombre, celular, ciudad, correo))
    mysql.connection.commit()

    return render_template('contacto.html')

        
@app.route('/usuarios')
def mostrarusuarios():

    cur = mysql.connection.cursor()
    
    cur.execute('SELECT * FROM usuarios')

    usuarios= cur.fetchall()
    cur.close()

    
    print(usuarios)

    
    
    # print(usuarios)

    
    return render_template('adm-registros.html', usuarios=usuarios)

    # # cur = mysql.connection.cursor()
    # # cur.execute('SELECT * FROM usuarios')
    # # usuarios= cur.fetchall()
    # # print(usuarios)
    # # return render_template('adm-registros.html', usuarios=usuarios)

@app.route('/destroy/<int:id>')
def destroy(id):

    conn= mysql.connect()
    cursor=conn.cursor()
    cursor.execute("DELETE FROM usuarios WHERE IDusuario= %s",(id))
    conn.commit()
    return redirect('/usuarios')
    


if __name__ == '__main__':
   app.secret_key = "pinchellave"
   app.run(debug=True, host='0.0.0.0', port=5555, threaded=True)
