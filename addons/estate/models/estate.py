from odoo import models, fields

class Estate(models.Model):
    _name = "estate"
    _description = "Modelo de las propiedades"

    name = fields.Char(
        string = 'Nombre',
        required=True)
    description = fields.Text(required=True)
    postcode = fields.Char(required=True)
    date_availability = fields.Date(required=True)
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(required=True)
    bedrooms = fields.Integer(Required=True)
    living_area = fields.Integer(Required=True)
    facades = fields.Integer(Required=True)
    garage = fields.Boolean(Required=True)
    garden = fields.Boolean(Required=True)
    garden_area = fields.Integer(Required=True)
    garden_orientation = fields.Selection(
        string='Orientacion del jardin',
        selection=[('north','North'), ('south','South'), ('east','East'), ('west','West')],
        help="Orientacion del jardin"
    )