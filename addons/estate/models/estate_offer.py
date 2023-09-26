from odoo import api, models, fields
from datetime import datetime, timedelta

class EstateOffer(models.Model):
    _name = "estate_offer"
    _description = "Modelo de ofertas de propiedades"

    price = fields.Float(
        string = 'Precio')
    status = fields.Selection(
        string = 'Tag de propiedad',
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