from flask import Blueprint, render_template, request, redirect, url_for
from database import db 

empleados_bp = Blueprint('empleados', __name__)
col = db['empleados']

@empleados_bp.route("/")
def ver_empleados():
    lista = list(col.find({}, {'_id': 0}))
    return render_template('empleados.html', empleados=lista)

@empleados_bp.route("/nuevo")
def formulario(): 
    return render_template('empleados-form.html')

@empleados_bp.route("/guardar", methods=["POST"])
def guardar():
    ultimo = col.find_one({"id_empleado": {"$type": "int"}}, sort=[("id_empleado", -1)])
    nuevo_id = (ultimo["id_empleado"] + 1) if ultimo else 1

    col.insert_one({
        "id_empleado": nuevo_id,
        "Nombre":                  request.form.get("Nombre"),
        "Apellidos":               request.form.get("Apellidos"),
        "Puesto":                  request.form.get("Puesto"),
        "Fecha de Nacimiento":     request.form.get("Fecha_de_Nacimiento"),
        "Fecha de Contratación":   request.form.get("Fecha_de_Contratación"), 
        "RFC":                     request.form.get("RFC"),                  
        "Teléfono":                request.form.get("Telefono"),
        "Correo electrónico":      request.form.get("Correo_electronico"),
        "Numero de seguro social": request.form.get("Numero_de_seguro_social"),
        "Certificaciones":         request.form.get("Certificaciones"),
        "Horarios":                request.form.get("Horarios"),
        "CURP":                    request.form.get("CURP"),                 
        "Cédula Profesional":      request.form.get("Cédula_Profesional"),   
    })
    return redirect(url_for('empleados.ver_empleados'))

@empleados_bp.route("/eliminar/<int:id_empleado>")
def eliminar(id_empleado):
    col.delete_one({"id_empleado": id_empleado})
    return redirect(url_for('empleados.ver_empleados'))

@empleados_bp.route("/editar/<int:id_empleado>")
def editar_formulario(id_empleado):
    empleado_encontrado = col.find_one({"id_empleado": id_empleado}, {"_id": 0})
    return render_template('empleados-form.html', empleado=empleado_encontrado)

@empleados_bp.route("/actualizar", methods=["POST"])
def actualizar():
    id_empleado = int(request.form.get("id_empleado"))
    
    col.update_one(
        {"id_empleado": id_empleado},
        {"$set": {
            "Nombre":                  request.form.get("Nombre"),
            "Apellidos":               request.form.get("Apellidos"),
            "Puesto":                  request.form.get("Puesto"),
            "Fecha de Nacimiento":     request.form.get("Fecha_de_Nacimiento"),
            "Fecha de Contratación":   request.form.get("Fecha_de_Contratación"), 
            "RFC":                     request.form.get("RFC"),                  
            "Teléfono":                request.form.get("Telefono"),
            "Correo electrónico":      request.form.get("Correo_electronico"),
            "Numero de seguro social": request.form.get("Numero_de_seguro_social"),
            "Certificaciones":         request.form.get("Certificaciones"),
            "Horarios":                request.form.get("Horarios"),
            "CURP":                    request.form.get("CURP"),                 
            "Cédula Profesional":      request.form.get("Cédula_Profesional"), 
        }}
    )
    return redirect(url_for('empleados.ver_empleados'))