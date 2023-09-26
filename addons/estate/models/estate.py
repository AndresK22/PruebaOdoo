from odoo import api, models, fields
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
    living_area = fields.Float(
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
    garden_area = fields.Float(
        string = 'Area de jardin (m^2)',
        required=True)
    garden_orientation = fields.Selection(
        string='Orientacion del jardin',
        selection=[('north','Norte'), ('south','Sur'), ('east','Este'), ('west','Oeste')],
        help="Orientacion del jardin")
    active = fields.Boolean(
        string = 'Activo',
        required=True,
        default = True)
    state = fields.Selection(
        string='Estado de la propiedad',
        selection=[('new','Nueva'), ('offer_received','Oferta recibida'), ('offer_accepted','Oferta aceptada'), ('sold','Vendida'), ('canceled','Cancelada')],
        help="Estado de la propiedad",
        required = True,
        default = 'new')
    
    #Muchos estates tienen un tipo, un comprador y un vendedor
    property_type_id = fields.Many2one(
        "estate_type",
        string="Tipo de propiedad")
    partner_id = fields.Many2one(
        "res.partner",
        string="Comprador",
        copy=False)
    users_id = fields.Many2one(
        "res.users",
        string="Vendedor",
        default=lambda self: self.env.user)

    #Muchos estates tienen muchos tags
    property_tag_id = fields.Many2many(
        "estate_tag",
        string="Tags")

    #Un estado puede tener muchas ofertas. En el modelo de estate_offer esta el contrario: Muchas ofertas esta en un estate
    offer_ids = fields.One2many(
        "estate_offer",
        "property_id",
        string="Ofertas")

    #Campos calculados
    total_area = fields.Float(
        compute="_calcular_area_total",
        string="Area total",
        store=True)

    @api.depends('living_area', 'garden_area')
    def _calcular_area_total(self):
        for registro in self:
            registro.total_area = registro.living_area + registro.garden_area


    best_price = fields.Float(
        compute="_calcular_mejor_oferta",
        string="Mejor oferta",
        store=True)

    #Campo calculado de otra tabla
    @api.depends("offer_ids.price")
    def _calcular_mejor_oferta(self):
        for record in self:
            record.best_price = max(record.mapped('offer_ids.price'), default=None)

    #Campos onChange
    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden == True:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = 0
            self.garden_orientation = ""