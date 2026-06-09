from flask import Blueprint, render_template, request, redirect, url_for
from database import db

pacientes_bp = Blueprint('pacientes', __name__)
col = db['pacientes'] 

@pacientes_bp.route("/")
def ver_pacientes():
    lista = list(col.find({}, {"_id": 0}))
    return render_template('pacientes.html', pacientes=lista)

@pacientes_bp.route("/nuevo")
def formulario():
    return render_template('pacientes-form.html')

# --- NUEVA RUTA DE BÚSQUEDA RÁPIDA ---
@pacientes_bp.route("/buscar", methods=["GET"])
def buscar_paciente():
    criterio = request.args.get("criterio", "").strip()
    
    if not criterio:
        return redirect(url_for('pacientes.formulario'))
    
    # Buscamos en MongoDB Atlas por coincidencia parcial en RFC o Nombre
    query = {
        "$or": [
            {"RFC": {"$regex": criterio, "$options": "i"}},
            {"Nombre": {"$regex": criterio, "$options": "i"}}
        ]
    }
    
    paciente_encontrado = col.find_one(query, {"_id": 0})
    
    if paciente_encontrado:
        # Si encuentra al paciente, recarga el formulario pasándole los datos para editar
        return render_template('pacientes-form.html', paciente=paciente_encontrado)
    else:
        # Si no lo encuentra, regresa al formulario con una alerta
        return render_template('pacientes-form.html', error_busqueda=f"No se encontró ningún paciente con '{criterio}'")

@pacientes_bp.route("/guardar", methods=["POST"])
def guardar():
    ultimo = col.find_one({"id_paciente": {"$type": "int"}}, sort=[("id_paciente", -1)])
    nuevo_id = (ultimo["id_paciente"] + 1) if ultimo else 1

    col.insert_one({
        "id_paciente": nuevo_id,
        "Nombre": request.form.get("Nombre"),
        "Apellidos": request.form.get("Apellidos"),
        "Fecha_de_nacimiento": request.form.get("Fecha_de_nacimiento"),
        "Sexo": request.form.get("Sexo"),
        "Edad": request.form.get("Edad"),
        "Aseguranza": request.form.get("Aseguranza"), # Guardado unificado como Aseguranza
        "Telefono": request.form.get("Telefono"),
        "Contacto_de_emergencia": request.form.get("Contacto_de_emergencia"),
        "Domicilio": request.form.get("Domicilio"),
        "Correo_electronico": request.form.get("Correo_electronico"),
        "Alergias": request.form.get("Alergias"),
        "RFC": request.form.get("RFC")
    })
    return redirect(url_for('pacientes.ver_pacientes'))

@pacientes_bp.route("/eliminar/<int:id_paciente>")
def eliminar(id_paciente):
    col.delete_one({"id_paciente": id_paciente}) 
    return redirect(url_for('pacientes.ver_pacientes')) 

@pacientes_bp.route("/editar/<int:id_paciente>")
def editar_formulario(id_paciente):
    paciente_encontrado = col.find_one({"id_paciente": id_paciente}, {"_id": 0})
    return render_template('pacientes-form.html', paciente=paciente_encontrado)

@pacientes_bp.route("/actualizar", methods=["POST"])
def actualizar():
    id_paciente = int(request.form.get("id_paciente"))
    
    col.update_one(
        {"id_paciente": id_paciente},
        {"$set": {
            "Nombre": request.form.get("Nombre"),
            "Apellidos": request.form.get("Apellidos"),
            "Fecha_de_nacimiento": request.form.get("Fecha_de_nacimiento"),
            "Sexo": request.form.get("Sexo"),
            "Edad": request.form.get("Edad"),
            "Aseguranza": request.form.get("Aseguranza"), # Actualizado unificado como Aseguranza
            "Telefono": request.form.get("Telefono"),
            "Contacto_de_emergencia": request.form.get("Contacto_de_emergencia"),
            "Domicilio": request.form.get("Domicilio"),
            "Correo_electronico": request.form.get("Correo_electronico"),
            "Alergias": request.form.get("Alergias"),
            "RFC": request.form.get("RFC")
        }}
    )
    return redirect(url_for('pacientes.ver_pacientes'))