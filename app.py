from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

#Configuramos nuestra conexion a base de datos
USER_DB = 'postgres'
PASS_DB ='admin'
URL_DB = 'localhost'
NAME_DB = 'sap_flask_db_mayo_2023'
FULL_URL_DB = f'postgresql://{USER_DB}:{PASS_DB}@{URL_DB}/{NAME_DB}'


#Indicar la configuracion
app.config['SQLALCHEMY_DATABASE_URI'] = FULL_URL_DB
#Para rastrear las modifcaciones de los objetos
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#Incicializacion del objeto db de sqlalchemy
db = SQLAlchemy(app)