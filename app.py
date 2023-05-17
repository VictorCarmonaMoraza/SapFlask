from flask import Flask, render_template
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

#Configuramos nuestra conexion a base de datos
USER_DB = 'postgres'
PASS_DB ='Vcarmona32'
URL_DB = 'localhost'
NAME_DB = 'sap_flask_db_mayo_2023'
FULL_URL_DB = f'postgresql://{USER_DB}:{PASS_DB}@{URL_DB}/{NAME_DB}'


#Indicar la configuracion
app.config['SQLALCHEMY_DATABASE_URI'] = FULL_URL_DB
#Para rastrear las modifcaciones de los objetos
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#Incicializacion del objeto db de sqlalchemy
db = SQLAlchemy(app)

#Configurar flask-migrate
migrate =Migrate()
migrate.init_app(app, db)

#Esto va a representar kla tabla en base de datos con sus columnas
class Persona(db.Model):
    #atributos
    id =db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(250))
    apellido = db.Column(db.String(250))
    email = db.Column(db.String(250))

    def __str__(self):
        return (
            f'Id: {self.id}, '
            f'Nombre: {self.nombre}, '
            f'Apellido: {self.apellido}, '
            f'Email: {self.email}'
        )

@app.route('/')
@app.route('/index')
@app.route('/index.html')
def inicio():
    #Listado de personas
    personas = Persona.query.all()
    #Obtenemos numero de persona de BBDD
    total_personas =Persona.query.count()
    app.logger.debug(f'Listado personas: {personas}')
    app.logger.debug(f'Total de personas: {total_personas}')
    return render_template('index.html',personasHTML = personas, total_personasHTML = total_personas)