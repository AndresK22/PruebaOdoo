from odoo import api, models, fields
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

    #Campo relacionado
    offer_ids = fields.One2many(
        "estate_offer",
        "property_type_id",
        string="Ofertas")

    #Campo calculado que cuenta el numero de ofertas para un tipo de propiedad determinado
    offer_count = fields.Integer(
        string="Cantidad de ofertas",
        compute="_calcular_cant_ofertas")


    @api.depends('offer_ids')
    def _calcular_cant_ofertas(self):
        for registro in self:
            for off in registro.offer_ids:
                registro.offer_count = off.property_type_id

    #Acciones de botones
    def cambiar_a_vender(self):
        for record in self:
            if (record.state == "canceled"):
                raise ValidationError("No puede establecer una propiedad cancelada como vendida")
            else:
                record.state = "sold"
        return True

    #Constraints de SQL
    _sql_constraints = [
        ('check_unique_name_type', 'unique(name)', 'Cada tipo debe ser unico.')
    ]