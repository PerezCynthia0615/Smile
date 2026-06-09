from flask import Blueprint, render_template, request, redirect, url_for
from database import db 

citas_bp = Blueprint('citas', __name__)
col = db['citas']

@citas_bp.route("/")
def ver_citas():
    lista = list(col.find({}, {'_id': 0}))
    return render_template('citas.html', citas=lista)

@citas_bp.route("/nueva")
def formulario(): 
    return render_template('citas-form.html')

@citas_bp.route("/guardar", methods=["POST"])
def guardar():
    ultimo = col.find_one({"id_cita": {"$type": "int"}}, sort=[("id_cita", -1)])
    nuevo_id = (ultimo["id_cita"] + 1) if ultimo else 1

    col.insert_one({
        "id_cita": nuevo_id,
        "Paciente": request.form.get("Paciente"),
        "Tratamiento": request.form.get("Tratamiento"),
        "Fecha y Hora": request.form.get("Fecha_y_Hora"),
        "Estado": request.form.get("Estado"),
        "Medico": request.form.get("Medico"),
        "Duracion": int(request.form.get("Duracion")),
        "Notas": request.form.get("Notas"),
    })
    return redirect(url_for('citas.ver_citas'))

@citas_bp.route("/eliminar/<int:id_cita>")
def eliminar(id_cita):
    col.delete_one({"id_cita": id_cita})
    return redirect(url_for('citas.ver_citas'))

@citas_bp.route("/editar/<int:id_cita>")
def editar_formulario(id_cita):
    cita_encontrada = col.find_one({"id_cita": id_cita}, {"_id": 0})
    return render_template('citas-form.html', cita=cita_encontrada)

@citas_bp.route("/actualizar", methods=["POST"])
def actualizar():
    id_cita = int(request.form.get("id_cita"))
    
    col.update_one(
        {"id_cita": id_cita},
        {"$set": {
            "Paciente": request.form.get("Paciente"),
            "Tratamiento": request.form.get("Tratamiento"),
            "Fecha y Hora": request.form.get("Fecha_y_Hora"),
            "Estado": request.form.get("Estado"),
            "Medico": request.form.get("Medico"),
            "Duracion": int(request.form.get("Duracion")),
            "Notas": request.form.get("Notas"),
        }}
    )
    return redirect(url_for('citas.ver_citas'))