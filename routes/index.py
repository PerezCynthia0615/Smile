from flask import Blueprint, render_template
from database import db

index_bp = Blueprint('index', __name__)

@index_bp.route("/")
def dashboard():
    total_pacientes = db['pacientes'].count_documents({})
    total_empleados  = db['empleados'].count_documents({})
    total_inventario     = db['inventario'].count_documents({})
    total_tratamientos     = db['tratamientos'].count_documents({})
    total_citas     = db['citas'].count_documents({})
    return render_template('index.html',
        total_pacientes=total_pacientes,
        total_empleados=total_empleados,
        total_inventario=total_inventario,
        total_tratamientos=total_tratamientos,
        total_citas=total_citas
    )