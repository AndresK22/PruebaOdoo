from odoo import models, fields
from datetime import datetime, timedelta

class EstateTag(models.Model):
    _name = "estate_tag"
    _description = "Modelo de tags de propiedades"
    _order = "name"

    name = fields.Char(
        string = 'Tag de propiedad',
        required=True)

    color = fields.Integer(string = 'Color del tag')

    #Constraints de SQL
    _sql_constraints = [
        ('check_unique_tag_name', 'unique(name)', 'Cada etiqueta debe ser unica.')
    ]