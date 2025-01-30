from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///historias_clinicas.db'
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

db = SQLAlchemy(app)

class HistoriaClinica(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    anio = db.Column(db.Integer, nullable=False)
    codigo = db.Column(db.String(50), nullable=False)
    dni = db.Column(db.String(20), nullable=True)
    imagen_frente = db.Column(db.String(200), nullable=False)
    imagen_reverso = db.Column(db.String(200), nullable=False)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        nombre = request.form['nombre']
        anio = request.form['anio']
        codigo = request.form['codigo']
        dni = request.form.get('dni', None)
        
        imagen_frente = request.files['imagen_frente']
        imagen_reverso = request.files['imagen_reverso']
        
        if imagen_frente and imagen_reverso:
            filename_frente = secure_filename(imagen_frente.filename)
            filename_reverso = secure_filename(imagen_reverso.filename)
            path_frente = os.path.join(app.config['UPLOAD_FOLDER'], filename_frente)
            path_reverso = os.path.join(app.config['UPLOAD_FOLDER'], filename_reverso)
            
            imagen_frente.save(path_frente)
            imagen_reverso.save(path_reverso)
            
            historia = HistoriaClinica(nombre=nombre, anio=anio, codigo=codigo, dni=dni,
                                      imagen_frente=path_frente, imagen_reverso=path_reverso)
            db.session.add(historia)
            db.session.commit()
            
            return redirect(url_for('index'))
    
    historias = HistoriaClinica.query.all()
    return render_template('index.html', historias=historias)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0', port=8000)
