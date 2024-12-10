from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash
import os
from datetime import datetime


# Inicialización de la aplicación
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///events.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'static/images'  # Carpeta donde se almacenarán las imágenes
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}  # Extensiones permitidas

# Inicialización de las extensiones
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Definición de las tablas (modelos)
class Usuario(db.Model):
    id_usuario = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    contraseña = db.Column(db.String(100), nullable=False)
    
    # Relación con la tabla Entrada
    entradas = db.relationship('Entrada', backref='usuario', lazy=True)

class Ciudad(db.Model):
    id_ciudad = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    
    # Relación con la tabla Evento
    eventos = db.relationship('Evento', backref='ciudad', lazy=True)

class Evento(db.Model):
    id_evento = db.Column(db.Integer, primary_key=True)
    nombre_evento = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.String(200), nullable=True)
    fecha = db.Column(db.DateTime, nullable=False)
    imagen = db.Column(db.String(200), nullable=True)
    categoria = db.Column(db.String(50), nullable=False)  # Nueva columna de categoría

    # Relación con la tabla Ciudad
    id_ciudad = db.Column(db.Integer, db.ForeignKey('ciudad.id_ciudad'), nullable=False)

    # Relación con la tabla Entrada
    entradas = db.relationship('Entrada', backref='evento', lazy=True)

class Entrada(db.Model):
    id_entrada = db.Column(db.Integer, primary_key=True)
    id_evento = db.Column(db.Integer, db.ForeignKey('evento.id_evento'), nullable=False)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuario.id_usuario'), nullable=False)
    precio = db.Column(db.Float, nullable=False)
    fecha_compra = db.Column(db.DateTime, nullable=False)

# Función para verificar si el archivo tiene una extensión permitida
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

# Ruta para el login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        contraseña = request.form['contraseña']
        
        # Buscar al usuario en la base de datos
        usuario = Usuario.query.filter_by(email=email).first()
        
        if usuario and check_password_hash(usuario.contraseña, contraseña):
            session['user_id'] = usuario.id_usuario  # Guardar ID de usuario en la sesión
            flash('¡Has iniciado sesión exitosamente!', 'success')
            return redirect(url_for('tu_evento'))  # Redirigir a la página de 'Tu Evento'
        else:
            flash('Credenciales incorrectas. Intenta de nuevo.', 'danger')
    
    return render_template('login.html')

# Ruta para el registro
@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        nombre = request.form['nombre']
        email = request.form['email']
        contraseña = request.form['contraseña']
        confirm_contraseña = request.form['confirm_contraseña']
        
        if contraseña != confirm_contraseña:
            flash('Las contraseñas no coinciden.', 'danger')
            return redirect(url_for('registro'))
        
        # Verificar si el email ya está registrado
        if Usuario.query.filter_by(email=email).first():
            flash('Este correo electrónico ya está registrado.', 'danger')
            return redirect(url_for('registro'))
        
        # Registrar al nuevo usuario
        nuevo_usuario = Usuario(
            nombre=nombre,
            email=email,
            contraseña=generate_password_hash(contraseña)
        )
        
        db.session.add(nuevo_usuario)
        db.session.commit()
        flash('¡Te has registrado exitosamente! Ahora puedes iniciar sesión.', 'success')
        return redirect(url_for('login'))

    return render_template('registro.html')


# Ruta para "Tu Evento"
@app.route('/tu_evento', methods=['GET', 'POST'])
def tu_evento():
    if 'user_id' not in session:
        flash('Debes iniciar sesión para acceder a esta página.', 'danger')
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        nombre_evento = request.form['nombre_evento']
        descripcion = request.form['descripcion']
        fecha_str = request.form['fecha']
        id_ciudad = request.form['id_ciudad']

        # Convertir la fecha del formulario a un objeto datetime
        try:
            fecha = datetime.strptime(fecha_str, '%Y-%m-%dT%H:%M')  # Formato: 'YYYY-MM-DDTHH:MM'
        except ValueError:
            flash('El formato de la fecha es incorrecto. Usa el formato YYYY-MM-DDTHH:MM.', 'danger')
            return redirect(url_for('tu_evento'))
        
        # Obtener el archivo de la imagen
        imagen = request.files['imagen']
        if imagen and allowed_file(imagen.filename):
            # Guardar la imagen en la carpeta estática
            imagen_filename = os.path.join(app.config['UPLOAD_FOLDER'], imagen.filename)
            imagen.save(imagen_filename)
        
            # Crear un nuevo evento con la imagen
            evento = Evento(
                nombre_evento=nombre_evento,
                descripcion=descripcion,
                fecha=fecha,  # Usamos la fecha convertida
                id_ciudad=id_ciudad,
                imagen=imagen.filename  # Solo guardamos el nombre del archivo en la base de datos
            )
            
            # Agregar el evento a la base de datos
            db.session.add(evento)
            db.session.commit()

            flash('Evento creado exitosamente.', 'success')
            return redirect(url_for('index'))  # Redirigir al índice después de agregar el evento
    
    # Obtener las ciudades para el formulario
    ciudades = Ciudad.query.all()
    return render_template('tu_evento.html', ciudades=ciudades)

# Ruta para el índice
@app.route('/')
def index():
    eventos_destacados = Evento.query.order_by(Evento.fecha.desc()).limit(2).all()
    return render_template('index.html', eventos=eventos_destacados)

# Ruta para cerrar sesión
@app.route('/logout')
def logout():
    session.pop('user_id', None)  # Eliminar el ID del usuario de la sesión
    flash('Has cerrado sesión exitosamente.', 'info')
    return redirect(url_for('index'))  # Redirigir al índice después de cerrar sesión

# Ejecutar la aplicación
if __name__ == '__main__':
    app.run(debug=True)
