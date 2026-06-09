from flask import Blueprint, render_template, request, redirect, url_for
from database import db 

inventario_bp = Blueprint('inventario', __name__)
col = db['inventario']

@inventario_bp.route("/")
def ver_inventario():
    lista = list(col.find({}, {'_id': 0}))
    return render_template('inventario.html', inventario=lista)

@inventario_bp.route("/nuevo")
def formulario(): 
    return render_template('inventario-form.html')

@inventario_bp.route("/guardar", methods=["POST"])
def guardar():
    ultimo = col.find_one({"id_inventario": {"$type": "int"}}, sort=[("id_inventario", -1)])
    nuevo_id = (ultimo["id_inventario"] + 1) if ultimo else 1

    col.insert_one({
        "id_inventario": nuevo_id,
        "Nombre": request.form.get("Nombre"),
        "Cantidad": int(request.form.get("Cantidad")),
        "Unidad de Medida": request.form.get("Unidad_de_Medida"),
        "Proveedor": request.form.get("Proveedor"),
        "Fecha de caducidad": request.form.get("Fecha_de_caducidad"),
        "Costo unitario": float(request.form.get("Costo_unitario")),
        "Ubicación en almacén": request.form.get("Ubicacion_en_almacen"),
        "Notas Adicionales": request.form.get("Notas_adicionales"),
    })
    return redirect(url_for('inventario.ver_inventario'))

@inventario_bp.route("/eliminar/<int:id_inventario>")
def eliminar(id_inventario):
    col.delete_one({"id_inventario": id_inventario})
    return redirect(url_for('inventario.ver_inventario'))

@inventario_bp.route("/editar/<int:id_inventario>")
def editar_formulario(id_inventario):
    material_encontrado = col.find_one({"id_inventario": id_inventario}, {"_id": 0})
    return render_template('inventario-form.html', material=material_encontrado)

@inventario_bp.route("/actualizar", methods=["POST"])
def actualizar():
    id_inventario = int(request.form.get("id_inventario"))
    
    col.update_one(
        {"id_inventario": id_inventario},
        {"$set": {
            "Nombre": request.form.get("Nombre"),
            "Cantidad": int(request.form.get("Cantidad")),
            "Unidad de Medida": request.form.get("Unidad_de_Medida"),
            "Proveedor": request.form.get("Proveedor"),
            "Fecha de caducidad": request.form.get("Fecha_de_caducidad"),
            "Costo unitario": float(request.form.get("Costo_unitario")),
            "Ubicación en almacén": request.form.get("Ubicacion_en_almacen"),
            "Notas Adicionales": request.form.get("Notas_adicionales"),
        }}
    )
    return redirect(url_for('inventario.ver_inventario'))