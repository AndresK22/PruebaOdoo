from odoo import models, api, fields
from odoo.tools.float_utils import float_compare
from odoo.exceptions import ValidationError

from datetime import datetime, timedelta

class Estate(models.Model):
    _name = "estate"
    _description = "Modelo de las propiedades"
    _order = "id desc"

    name = fields.Char(
        string = 'Nombre',
        default = "Unknown",
        required=True)
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

    
    #Acciones de botones
    def cambiar_a_vender(self):
        for record in self:
            if (record.state == "canceled"):
                raise ValidationError("No puede establecer una propiedad cancelada como vendida")
            else:
                record.state = "sold"
        return True

    def cambiar_a_cancelar(self):
        for record in self:
            if (record.state == "sold"):
                raise ValidationError("No puede establecer una propiedad vendida como cancelada")
            else:
                record.state = "canceled"
        return True


    #Constraints de SQL
    _sql_constraints = [
        ('check_expected_price', 'CHECK(expected_price > 0)', 'El precio esperado debe ser estrictamente positivo.'),
        ('check_selling_price', 'CHECK(selling_price >= 0)', 'El precio de venta debe ser positivo')
    ]


    #Constraints de Python
    @api.constrains('selling_price', 'expected_price')
    def _check_selling_price2(self):
        for record in self:
            for offer in record.offer_ids:
                if offer.status == 'refused':
                    pass
                elif offer.status == 'accepted':
                    for off in record.offer_ids:
                        resultado = float_compare(off.price, (record.expected_price * 0.9), precision_digits=2)
                        if resultado == -1:
                            raise ValidationError("El precio de venta no puede ser menor al 90 por ciento del precio esperado")
                else:
                    pass         
        # all records passed the test, don't return anything



    #Metodos heredados y sobrecargados

    #Evitar que se borre si el estado no es "Nuevo" o "Cancelado"
    @api.ondelete(at_uninstall=False)
    def _delete_estate(self):
        for reg in self:
            if reg.state in ('offer_received', 'offer_accepted', 'sold'):
                raise ValidationError("No se puede eliminar un inmueble a menos que sea nuevo o cancelado")