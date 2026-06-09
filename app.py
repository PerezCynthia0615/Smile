from flask import Flask

from database import db

app = Flask(__name__)

#Vamos a crear una carpeta llamada "routes" donde vamos a almacenar los documentos.py de cada una de nuestras colecciones.
from routes.index import index_bp
from routes.pacientes import pacientes_bp
from routes.empleados import empleados_bp
from routes.inventario import inventario_bp
from routes.tratamientos import tratamientos_bp
from routes.citas import citas_bp

app.register_blueprint(index_bp)
app.register_blueprint(pacientes_bp, url_prefix='/pacientes')
app.register_blueprint(empleados_bp, url_prefix='/empleados')
app.register_blueprint(inventario_bp, url_prefix='/inventario')
app.register_blueprint(tratamientos_bp, url_prefix='/tratamientos')
app.register_blueprint(citas_bp, url_prefix='/citas')

if __name__ == "__main__":
    app.run(debug=True)
