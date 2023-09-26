from odoo import models, fields
from datetime import datetime, timedelta

class EstateType(models.Model):
    _name = "estate_type"
    _description = "Modelo del tipo de propiedades"

    name = fields.Char(
        string = 'Tipo de propiedad',
        required=True)