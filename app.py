
from flask import Flask, g, render_template_string, request
import sqlite3
from flask import redirect, url_for
from flask import Flask, render_template, request, redirect, url_for
from models import db, Vehicle
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'  # your DB
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False



app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE = os.path.join(BASE_DIR, "mydatabase.db")

import os

basedir = os.path.abspath(os.path.dirname(__file__))  # directory of your app

app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{os.path.join(basedir, 'mydatabase.db')}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

#with app.app_context():
 #  db.create_all()



def get_db():
    db = sqlite3.connect(DATABASE)
    db.row_factory = sqlite3.Row
    print("Connected to DB at:", DATABASE)
    return db

@app.teardown_appcontext
def close_db(exception):
    db = g.pop("db", None)
    if db is not None:
        db.close()

@app.route("/")
def home():
    return redirect(url_for('vehicles'))


from flask import render_template

from flask import request

@app.route("/vehicles")
def vehicles():
    # Get filter values from query parameters
    anio = request.args.get("anio")
    grupo_familia = request.args.get("grupo_familia")
    costo_max = request.args.get("costo_max")

    # Start SQLAlchemy query
    query = Vehicle.query

    # Apply filters if they exist
    if anio:
        query = query.filter(Vehicle.anio_adquisicion == int(anio))
    if grupo_familia:
        query = query.filter(Vehicle.grupo_familia.ilike(f"%{grupo_familia}%"))
    if costo_max:
        query = query.filter(Vehicle.costo_adquisicion <= float(costo_max))

    # Execute query
    vehicles = query.all()

    # Optional: debug
    print("Filtered Vehicles IDs:", [v.id for v in vehicles])

    # Convert to list of dicts for your current template
    rows = []
    for v in vehicles:
        rows.append({
            "ID del vehículo": v.id,
            "Grupo de Familia": v.grupo_familia,
            "Subfamilia": v.subfamilia,
            "Marca/Modelo": v.marca_modelo,
            "Año de adquisición": v.anio_adquisicion,
            "Costo de adquisición": v.costo_adquisicion,
            "Vida útil estimada (años)": v.vida_util,
            "Valor residual": v.valor_residual,
            "Método de depreciación": v.metodo_depreciacion,
            "Justificación técnica": v.justificacion_tecnica,
            "Fecha de revisión": v.fecha_revision,
            "Depreciación anual": v.depreciacion_anual
        })

    return render_template("vehicles.html", rows=rows)




@app.route('/vehicles/edit/<string:id>', methods=['GET', 'POST'])
def edit_vehicle(id):
    vehicle = Vehicle.query.get(id)

    if request.method == 'POST':

        vehicle = Vehicle.query.get(id)
  # or however you fetch it

        if not vehicle:
            print("DEBUG: Asset not found for ID:", id)
        else:
            print("DEBUG: Found asset:", vehicle)

        vehicle.grupo_familia = request.form['grupo_familia']

        
        vehicle.subfamilia = request.form['subfamilia']
        vehicle.marca_modelo = request.form['marca_modelo']
        vehicle.anio = request.form['anio']
        vehicle.costo = request.form['costo']

        # new fields
        vehicle.vida_util = request.form['vida_util']
        vehicle.valor_residual = request.form['valor_residual']
        vehicle.metodo_depreciacion = request.form['metodo_depreciacion']
        vehicle.justificacion_tecnica = request.form['justificacion_tecnica']
        vehicle.fecha_revision = request.form['fecha_revision']
        vehicle.depreciacion_anual = request.form['depreciacion_anual']

        db.session.commit()
        return redirect('/vehicles')

    return render_template('edit_vehicle.html', vehicle=vehicle)




@app.route("/add_vehicle", methods=["GET", "POST"])
def add_vehicle():
    if request.method == "POST":
        # Get form data
        id_vehiculo = request.form["ID_del_vehiculo"]
        grupo_familia = request.form["Grupo_de_Familia"]
        subfamilia = request.form["Subfamilia"]
        marca_modelo = request.form["Marca_Modelo"]
        anio_adquisicion = request.form["Anio_de_adquisicion"]
        costo_adquisicion = request.form["Costo_de_adquisicion"]
        vida_util = request.form["Vida_util"]
        valor_residual = request.form["Valor_residual"]
        metodo_depreciacion = request.form["Metodo_depreciacion"]
        justificacion_tecnica = request.form["Justificacion_tecnica"]
        fecha_revision = request.form["Fecha_revision"]
        depreciacion_anual = request.form["Depreciacion_anual"]

        # Insert into database
        db = get_db()
        db.execute(
            """INSERT INTO vehicles 
            ("ID del vehículo","Grupo de Familia","Subfamilia","Marca/Modelo",
            "Año de adquisición","Costo de adquisición","Vida útil estimada (años)",
            "Valor residual","Método de depreciación","Justificación técnica",
            "Fecha de revisión","Depreciación anual")
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (id_vehiculo, grupo_familia, subfamilia, marca_modelo, anio_adquisicion,
             costo_adquisicion, vida_util, valor_residual, metodo_depreciacion,
             justificacion_tecnica, fecha_revision, depreciacion_anual)
        )
        db.commit()
        return redirect("/vehicles")

    # GET request: show form
    html = """
    <h1>Add Vehicle</h1>
    <form method="POST">
        ID del vehículo: <input type="text" name="ID_del_vehiculo" required><br>
        Grupo de Familia: <input type="text" name="Grupo_de_Familia"><br>
        Subfamilia: <input type="text" name="Subfamilia"><br>
        Marca/Modelo: <input type="text" name="Marca_Modelo"><br>
        Año de adquisición: <input type="text" name="Anio_de_adquisicion"><br>
        Costo de adquisición: <input type="text" name="Costo_de_adquisicion"><br>
        Vida útil estimada (años): <input type="text" name="Vida_util"><br>
        Valor residual: <input type="text" name="Valor_residual"><br>
        Método de depreciación: <input type="text" name="Metodo_depreciacion"><br>
        Justificación técnica: <input type="text" name="Justificacion_tecnica"><br>
        Fecha de revisión: <input type="text" name="Fecha_revision"><br>
        Depreciación anual: <input type="text" name="Depreciacion_anual"><br>
        <input type="submit" value="Add Vehicle">

        
        
    </form>
    <a href="/vehicles">Back to list</a>
    
    
    """
    return render_template_string(html)



@app.route('/vehicles/delete/<string:id>', methods=['POST'])
def delete_vehicle(id):
    # Get the vehicle by ID
    vehicle = Vehicle.query.get(id)
    if vehicle:
        db.session.delete(vehicle)
        db.session.commit()
        return redirect('/vehicles')
    else:
        return "Vehicle not found", 404





if __name__ == "__main__":
    app.run(debug=True)

  

 # debug
# show exactly what each row contains


#cd ~/Desktop/zoilas_project
# source venv/bin/activate

