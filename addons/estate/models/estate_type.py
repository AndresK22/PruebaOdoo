from odoo import models, fields
from datetime import datetime, timedelta

class EstateType(models.Model):
    _name = "estate_type"
    _description = "Modelo del tipo de propiedades"
    _order = "sequence, name"

    name = fields.Char(
        string = 'Tipo de propiedad',
        required=True)

    sequence = fields.Integer(
        'Sequence',
        default=1,
        help="Usado para ordenar los tipos. Lower is better.")

    property_ids = fields.One2many(
        "estate",
        "property_type_id",
        string="Propiedades")

    #Constraints de SQL
    _sql_constraints = [
        ('check_unique_name_type', 'unique(name)', 'Cada tipo debe ser unico.')
    ]