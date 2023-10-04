from odoo import api, models, fields

class AmbienteDestino(models.Model):
    _name = "facturas.ambiente_destino"
    _description = "Catalogo de ambiente de destino"
    _order = "codigo desc"

    name = fields.Char(
        required = False,
        compute = "_nombrar",
        store = True
    )

    codigo = fields.Char(
        string = 'Codigo',
        required = True,
        copy = False,
        size = 2
    )
    valor = fields.Text(
        string = 'Valor',
        required = True
    )
    state = fields.Boolean(
        string = 'Estado',
        required = True,
        default = True
    )

    #Validaciones
    #Constraints de SQL
    _sql_constraints = [
        ('check_amb_dest_unique', 'UNIQUE(codigo)', 'El codigo no puede repetirse.')
    ]


    #Campos calculados
    @api.depends('valor')
    def _nombrar(self):
        for reg in self:
            reg.name = reg.valor