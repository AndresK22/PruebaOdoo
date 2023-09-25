from odoo import models, fields
from datetime import datetime, timedelta

class Estate(models.Model):
    _name = "estate"
    _description = "Modelo de las propiedades"

    name = fields.Char(
        string = 'Nombre',
        default = "Unknown",
        required=True)
    last_seen = fields.Datetime(
        string="Visto por ultima vez",
        default=lambda self: fields.Datetime.now())
    description = fields.Text(
        string = 'Descripcion',
        required=True)
    postcode = fields.Char(
        string = 'Codigo postal',
        required=True)
    date_availability = fields.Date(
        string = 'Disponibilidad desde',
        required=True,
        default = lambda self: (datetime.today() + timedelta(days=90)).strftime('%Y-%m-%d'),
        copy=False)
    expected_price = fields.Float(
        string = 'Precio esperado',
        required=True)
    selling_price = fields.Float(
        string = 'Precio de venta',
        readonly=True,
        copy = False)
    bedrooms = fields.Integer(
        string = 'Habitaciones',
        required=True,
        default = 2)
    living_area = fields.Integer(
        string = 'Area de la vivienda (m^2)',
        required=True)
    facades = fields.Integer(
        string = 'Fachada',
        required=True)
    garage = fields.Boolean(
        string = 'Cochera',
        required=True)
    garden = fields.Boolean(
        string = 'Jardin',
        required=True)
    garden_area = fields.Integer(
        string = 'Area de jardin (m^2)',
        required=True)
    garden_orientation = fields.Selection(
        string='Orientacion del jardin',
        selection=[('north','Norte'), ('south','Sur'), ('east','Este'), ('west','Oeste')],
        help="Orientacion del jardin"
    )
    active = fields.Boolean(
        string = 'Activo',
        required=True,
        default = True)
    state = fields.Selection(
        string='Estado de la propiedad',
        selection=[('new','Nueva'), ('offer_received','Oferta recibida'), ('offer_accepted','Oferta aceptada'), ('sold','Vendida'), ('canceled','Cancelada')],
        help="Estado de la propiedad",
        required = True,
        default = 'new'
    )