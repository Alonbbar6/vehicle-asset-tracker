

# models.py
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Vehicle(db.Model):
    __tablename__ = 'vehicles'  # your table name

    id = db.Column(db.String, primary_key=True, name="ID del vehículo")
    grupo_familia = db.Column(db.String, name="Grupo de Familia")
    subfamilia = db.Column(db.String, name="Subfamilia")
    marca_modelo = db.Column(db.String, name="Marca/Modelo")
    anio_adquisicion = db.Column(db.Integer, name="Año de adquisición")
    costo_adquisicion = db.Column(db.Float, name="Costo de adquisición")
    vida_util = db.Column(db.Integer, name="Vida útil estimada (años)")
    valor_residual = db.Column(db.Float, name="Valor residual")
    metodo_depreciacion = db.Column(db.String, name="Método de depreciación")
    justificacion_tecnica = db.Column(db.String, name="Justificación técnica")
    fecha_revision = db.Column(db.String, name="Fecha de revisión")
    depreciacion_anual = db.Column(db.Float, name="Depreciación anual")







# cd ~/Desktop/zoilas_project
# python3 models.py
