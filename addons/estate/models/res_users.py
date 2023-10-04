from odoo import models, fields

class ResUsers(models.Model):
    _inherit = "res.users"

    property_ids = fields.One2many(
        "estate",
        "users_id",
        string = "Propiedades"
    )