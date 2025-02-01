from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///historias.db'
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

db = SQLAlchemy(app)

# Modelo de Historia Clínica
class HistoriaClinica(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    anio = db.Column(db.Integer, nullable=False)
    codigo = db.Column(db.String(50), nullable=False)
    dni = db.Column(db.String(20), nullable=True)
    archivos = db.relationship('Archivo', backref='historia', lazy=True)

# Modelo de Archivos
class Archivo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    historia_id = db.Column(db.Integer, db.ForeignKey('historia_clinica.id'), nullable=False)
    ruta = db.Column(db.String(200), nullable=False)


@app.route('/lista', methods=['GET'])
def list():
    historias = HistoriaClinica.query.all()
    return render_template('lista.html', historias=historias)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        nombre = request.form['nombre']
        anio = request.form['anio']
        codigo = request.form['codigo']
        dni = request.form.get('dni')

        nueva_historia = HistoriaClinica(nombre=nombre, anio=anio, codigo=codigo, dni=dni)
        db.session.add(nueva_historia)
        db.session.commit()

        # Guardar imágenes
        from logging import getLogger
        log = getLogger("dev")
        archivos = request.files
        for keyarch in archivos:
            archivo = request.files.get(keyarch)
            if archivo and archivo.filename:
                filename = secure_filename(archivo.filename)
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                archivo.save(filepath)

                nuevo_archivo = Archivo(historia_id=nueva_historia.id, ruta=filepath)
                db.session.add(nuevo_archivo)

        db.session.commit()
        return redirect(url_for('index'))
    return render_template('index.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host="0.0.0.0", port=8000)

