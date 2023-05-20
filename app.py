from flask import Flask, render_template, request, url_for
from flask_migrate import Migrate
from werkzeug.utils import redirect


from database import db
from forms import PersonaForm
from models import Persona

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

db.init_app(app)

#Configurar flask-migrate
migrate =Migrate()
migrate.init_app(app, db)

#configuracion de flask-wtf
app.config['SECRET_KEY']='llave_secreta'


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

@app.route('/ver/<int:id>')
def ver_detalle(id):
    #Recuperamos la persona segun el id proporcionado
    persona = Persona.query.get_or_404(id)
    app.logger.debug(f'Ver persona: {persona}')
    return render_template('detalle.html', personaId_HTML = persona )

@app.route('/agregar', methods=['GET','POST'])
def agregar():
    #Creacion de objeto Persona
    persona = Persona()
    #Creacion de objeto PersonaForm
    personaForm = PersonaForm(obj = persona)
    #Si el tipo de envio es POST
    if request.method == 'POST':
        #Validamos si el formulario es valido
        if personaForm.validate_on_submit():
            #
            personaForm.populate_obj(persona)
            #Imprimimos a nivel  debug la persona a insertar
            app.logger.debug(f'Persona insertar: {persona}')
            #Guardamos informacion eb BBDD
            db.session.add(persona)
            #Hacemos commit de la transaccion
            db.session.commit()
            #Redireccionamos a la pagina de inicio para ver el listado de personas
            return redirect(url_for('inicio'))
    return render_template('agregar.html', personaFormHTML = personaForm)
