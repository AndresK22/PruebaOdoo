from odoo import api, models, fields
from odoo.exceptions import ValidationError
from datetime import datetime, timedelta

class EstateOffer(models.Model):
    _name = "estate_offer"
    _description = "Modelo de ofertas de propiedades"
    _order = "price desc"

    price = fields.Float(
        string = 'Oferta $')
    status = fields.Selection(
        string = 'Estado de la oferta',
        selection=[('accepted','Aceptado'), ('refused','Rechazado')],
        copy=False)
    partner_id = fields.Many2one(
        "res.partner",
        string="Comprador",
        required=True)
    property_id = fields.Many2one(
        "estate",
        string="Propiedad",
        required=True)

    #Campo relacionado a otro
    property_type_id = fields.Many2one(
        string="Tipo de propiedad",
        related="property_id.property_type_id",
        store=True)

    #Campo para encontrar el estado del inmueble
    #property_state = fields.Selection(
     #   related='property_id.state',
      #  string='Estado de la Propiedad')
    
    #Campo calculado, incluyendo inverse
    validity = fields.Integer(
        string='Validez',
        default='7',
        store=True)

    date_deadline = fields.Datetime(
        string='Fecha limite',
        compute='_calcular_fecha_final',
        inverse='_inverse_calcular_fecha_final',
        store=True)


    #Una mouseherramienta misteriosa
    def _es_datetime_valido(self, dt):
        if isinstance(dt, datetime):
            try:
                datetime(dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second, dt.microsecond)
                return True
            except ValueError:
                return False

    @api.depends('validity')
    def _calcular_fecha_final(self):
        for record in self:
            if record._es_datetime_valido(record.create_date):
                record.date_deadline = (record.create_date + timedelta(days=record.validity)).strftime('%Y-%m-%d')
            else:
                record.date_deadline = (datetime.today() + timedelta(days=record.validity)).strftime('%Y-%m-%d')

    def _inverse_calcular_fecha_final(self):
        for record in self:
            if record._es_datetime_valido(record.create_date):
                record.validity = (record.date_deadline - record.create_date).days
            else:
                pass

    #Acciones de botones
    def aceptar_oferta(self):
        for record in self:
            if not record.property_id.partner_id:
                record.status = "accepted"
                record.property_id.state = "offer_accepted"
                record.property_id.selling_price = record.price
                record.property_id.partner_id = record.partner_id
            else:
                raise ValidationError("No puede aceptar mas de una oferta")
        return True

    def rechazar_oferta(self):
        for record in self:
            record.status = "refused"
            record.property_id.selling_price = None
            record.property_id.partner_id = None
        return True

    
    #Constraints de SQL
    _sql_constraints = [
        ('check_price', 'CHECK(price > 0)', 'El precio ofertado debe ser estrictamente positivo.')
    ]
