from flask import Flask, render_template, request, redirect, session, url_for, flash
import os
from werkzeug.utils import secure_filename
from datetime import datetime
import mysql.connector

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Conexión a la base de datos
database = mysql.connector.connect(
    host="leben.mysql.pythonanywhere-services.com",
    user="leben",
    passwd="nattgo.21",
    db="leben$default"
)

# Rutas adicionales
@app.route('/')
def index():
    return render_template('index.html')
@app.route('/index_urs')
def index_urs():
     if 'user_id' not in session:
         return redirect(url_for('inicioSesion'))

     user_name = session['user_name']
     return render_template('/clients/index_urs.html', user_name=user_name)
@app.route('/productos')
def productos():
    productos = obtener_productos()

    for producto in productos:
        if isinstance(producto['imgproductos'], bytes):
            producto['imgproductos'] = producto['imgproductos'].decode('utf-8')

    return render_template('productos.html', productos=productos)

def obtener_productos():
    cursor = database.cursor(dictionary=True)
    cursor.execute("SELECT * FROM productos")
    productos = cursor.fetchall()
    cursor.close()
    return productos

@app.route('/productos_urs')
def productos_urs():
    return render_template('/clients/productos_urs.html')

@app.route('/nosotros')
def nosotros():
    return render_template('nosotros.html')

@app.route('/nosotros_urs')
def nosotros_urs():
    return render_template('/clients/nosotros_urs.html')

@app.route('/contacto')
def contacto():
    return render_template('contacto.html')

@app.route('/contacto_urs')
def contacto_urs():
    return render_template('/clients/contacto_urs.html')

@app.route('/inicioSesion', methods=['GET', 'POST'])
def inicioSesion():
    if request.method == 'POST':
        usuario = request.form['usuario']
        contrasena = request.form['contrasena']

        cursor = database.cursor()
        sql = "SELECT idusuario, contraseñausuario, idrol, nombreusuario FROM usuarios WHERE emailusuario = %s"
        cursor.execute(sql, (usuario,))
        user = cursor.fetchone()
        cursor.close()

        if user and user[1] == contrasena:
            session['user_id'] = user[0]
            session['user_name'] = user[3]  

            if user[2] == 2:  
                return redirect(url_for('dashboard'))
            else:
                return redirect(url_for('index_urs'))
        else:
            return render_template('inicioSesion.html', error="Usuario o contraseña incorrectos")
        
    return render_template('inicioSesion.html')

@app.route('/registrarse', methods=['GET', 'POST'])
def registrar():

    if request.method == 'POST':
        
        idciudad = request.form['id_ciudad']
        correo = request.form['correo']
        contraseña = request.form['password']
        nombre_usuario = request.form['nombres']  
        fechanacimientousuario = request.form['fechanacimientousuario']
        apellidos_usuario = request.form['apellidos']
        telefono_usuario = request.form['telefono']
        id_rol = 1

        cursor = database.cursor()
        sql = "INSERT INTO usuarios (nombreusuario, apellidousuario, telefonousuario, emailusuario, fechanacimientousuario, contraseñausuario, idrol, idciudad) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        data = (nombre_usuario, apellidos_usuario, telefono_usuario, correo, fechanacimientousuario, contraseña, id_rol, idciudad)
        cursor.execute(sql, data)
        database.commit()
        cursor.close()

        return render_template('iniciosesion.html')  
    else:
        cursor = database.cursor()
        cursor.execute("SELECT idciudad, nombreciudad FROM ciudades")
        ciudades = cursor.fetchall()

        cursor.close()
    return render_template('registrar.html', ciudades=ciudades)



@app.route('/contraseña')
def contraseña():
    return render_template('contraseña.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/ventas')
def ventas():
    return render_template('ventas.html')



# Directorio donde se guardarán las imágenes
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/inventario', methods=['GET', 'POST'])
def inventario():
    cursor = database.cursor(dictionary=True)

    if request.method == 'POST':
        form_data = request.form
        # file = request.files['imgproductos']  # No se utiliza en este formulario

        try:
            if 'nombreproducto' in form_data:
                nombreproducto = form_data['nombreproducto']
                valorproducto = form_data['valorproducto']
                idproveedor = form_data['proveedor']
                idcategoria = form_data['categoria']
                idtalla = form_data['talla']

                cursor.execute("START TRANSACTION")

                # Insertar producto
                cursor.execute("""
                    INSERT INTO productos (nombreproducto, valorproducto, idproveedor, idcategoria, idtalla) 
                    VALUES (%s, %s, %s, %s, %s)
                """, (nombreproducto, valorproducto, idproveedor, idcategoria, idtalla))

                idproducto = cursor.lastrowid

                 # Insertar inventario
                cursor.execute("""
                    INSERT INTO inventario (idproducto, stockinventario, fechastock) 
                    VALUES (%s, %s, NOW())
                """, (idproducto, 0))

                idinventario = cursor.lastrowid
                
                # Insertar entrada con cantidad inicial 0
                cursor.execute("""
                    INSERT INTO entrada (cantidadentrada, fechaentrada, idinventario) 
                    VALUES (%s, NOW(), %s)
                """, (0, idinventario))
                
                database.commit()
                flash('Producto, inventario y entrada creados con éxito')
            
            elif 'producto' in form_data:
                idproducto = form_data['producto']
                cantidadentrada = form_data['cantidadentrada']
                fechaentrada = form_data['fechaentrada']
                
                # Actualizar stock del inventario
                cursor.execute("""
                    UPDATE inventario 
                    SET stockinventario = stockinventario + %s, fechastock = %s 
                    WHERE idproducto = %s
                """, (cantidadentrada, fechaentrada, idproducto))
                
                # Insertar nueva entrada
                cursor.execute("""
                    INSERT INTO entrada (cantidadentrada, fechaentrada, idinventario) 
                    VALUES (%s, %s, (SELECT idinventario FROM inventario WHERE idproducto = %s))
                """, (cantidadentrada, fechaentrada, idproducto))
                
                database.commit()
                flash('Entrada de inventario agregada con éxito')
        
        except mysql.connector.IntegrityError as e:
            database.rollback()
            flash(f'Error al agregar: {str(e)}')
        except KeyError as e:
            flash(f'Campo faltante en el formulario: {str(e)}')
        finally:
            cursor.close()
        
        return redirect(url_for('inventario'))

    cursor.execute("SELECT * FROM proveedor")
    proveedores = cursor.fetchall()
    cursor.execute("SELECT * FROM categorias")
    categorias = cursor.fetchall()
    cursor.execute("SELECT * FROM tallas")
    tallas = cursor.fetchall()
    cursor.execute("SELECT * FROM productos")
    productos = cursor.fetchall()

    cursor.execute("""
        SELECT 
            i.idinventario,
            i.stockinventario,
            i.fechastock,
            p.idproducto,
            p.nombreproducto,
            p.valorproducto,
            c.idcategoria,
            c.nombrecategoria,
            t.numerotalla,
            t.letratalla,
            e.fechaentrada
        FROM 
            inventario i
        JOIN 
            productos p ON i.idproducto = p.idproducto
        LEFT JOIN 
            categorias c ON p.idcategoria = c.idcategoria
        LEFT JOIN 
            tallas t ON p.idtalla = t.idtalla
        LEFT JOIN 
            entrada e ON i.idinventario = e.idinventario
        INNER JOIN (
            SELECT idinventario, MAX(fechaentrada) as max_fecha
            FROM entrada
            GROUP BY idinventario
        ) latest_entrada ON e.idinventario = latest_entrada.idinventario AND e.fechaentrada = latest_entrada.max_fecha;
    """)
    inventario = cursor.fetchall()
    cursor.close()

    return render_template('inventario.html', data=inventario, proveedores=proveedores, categorias=categorias, tallas=tallas, productos=productos)

if __name__ == '__main__':
    app.run(debug=True, port=4000)
