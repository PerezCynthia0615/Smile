from flask import Blueprint, render_template, request, redirect, url_for
from database import db 

tratamientos_bp = Blueprint('tratamientos', __name__)
col = db['tratamientos']

@tratamientos_bp.route("/")
def ver_tratamientos():
    lista = list(col.find({}, {'_id': 0}))
    return render_template('tratamientos.html', tratamientos=lista)

@tratamientos_bp.route("/nuevo")
def formulario(): 
    return render_template('tratamientos-form.html')

@tratamientos_bp.route("/guardar", methods=["POST"])
def guardar():
    ultimo = col.find_one({"id_tratamiento": {"$type": "int"}}, sort=[("id_tratamiento", -1)])
    nuevo_id = (ultimo["id_tratamiento"] + 1) if ultimo else 1

    col.insert_one({
        "id_tratamiento": nuevo_id,
        "Nombre": request.form.get("Nombre"),
        "Costo": float(request.form.get("Costo")),
        "Duracion(min)": int(request.form.get("Duracion(min)")),
        "Tipo": request.form.get("Tipo"),
        "Descripcion": request.form.get("Descripcion"),
        "Frecuencia": request.form.get("Frecuencia"),
        "Materiales": request.form.get("Materiales"),
        "Instrucciones Post-Tratamiento": request.form.get("Instrucciones_Post_Tratamiento"),
    })
    return redirect(url_for('tratamientos.ver_tratamientos'))

@tratamientos_bp.route("/eliminar/<int:id_tratamiento>")
def eliminar(id_tratamiento):
    col.delete_one({"id_tratamiento": id_tratamiento})
    return redirect(url_for('tratamientos.ver_tratamientos'))

@tratamientos_bp.route("/editar/<int:id_tratamiento>")
def editar_formulario(id_tratamiento):
    tratamiento_encontrado = col.find_one({"id_tratamiento": id_tratamiento}, {"_id": 0}) if 'id_treatment' in locals() else col.find_one({"id_tratamiento": id_tratamiento}, {"_id": 0})
    return render_template('tratamientos-form.html', tratamiento=tratamiento_encontrado)

@tratamientos_bp.route("/actualizar", methods=["POST"])
def actualizar():
    id_tratamiento = int(request.form.get("id_tratamiento"))
    
    col.update_one(
        {"id_tratamiento": id_tratamiento},
        {"$set": {
            "Nombre": request.form.get("Nombre"),
            "Costo": float(request.form.get("Costo")),
            "Duracion(min)": int(request.form.get("Duracion(min)")),
            "Tipo": request.form.get("Tipo"),
            "Descripcion": request.form.get("Descripcion"),
            "Frecuencia": request.form.get("Frecuencia"),
            "Materiales": request.form.get("Materiales"),
            "Instrucciones Post-Tratamiento": request.form.get("Instrucciones_Post_Tratamiento"),
        }}
    )
    return redirect(url_for('tratamientos.ver_tratamientos'))