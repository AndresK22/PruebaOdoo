from odoo import models, fields
from datetime import datetime, timedelta

class EstateTag(models.Model):
    _name = "estate_tag"
    _description = "Modelo de tags de propiedades"

    name = fields.Char(
        string = 'Tag de propiedad',
        required=True)