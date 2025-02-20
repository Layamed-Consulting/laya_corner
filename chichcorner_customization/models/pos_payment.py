from odoo import fields, models,api

class PosPayment(models.Model):
    _inherit = 'pos.payment'

    stan = fields.Char(
        string='STAN Number',
        related='pos_order_id.stan',
        readonly=True,
        help='System Trace Audit Number from the associated POS order.'
    )
    identite_number = fields.Char(
        string='CIN',
        related='pos_order_id.identite_number',
        readonly=True,
        help='System Trace Audit Number from the associated POS order.'
    )
    cheque_number = fields.Char(
        string='Check number',
        related='pos_order_id.cheque_number',
        readonly=True,
        help='System Trace Audit Number from the associated POS order.'
    )
    banque = fields.Selection(
        string='Banque',
        related='pos_order_id.banque',
        readonly=True,
        help='System Trace Audit Number from the associated POS order.'
    )
    cheque_date = fields.Date(
        string='Date du chèque',
        related='pos_order_id.cheque_date',
        readonly=True,
        help='The date associated with the cheque payment from the POS order.'
    )

    @api.depends('payment_method_id')
    def _compute_field_visibility(self):
        for record in self:
            method = record.payment_method_id.name
            record.show_stan = method == 'Carte Bancaire'
            record.show_cheque_fields = method in ['Chèque', 'Chèque MDC']
            record.show_date = method == 'Chèque MDC'
            record.show_identite = method in ['Chèque MDC', 'Chèque']

    show_stan = fields.Boolean(compute='_compute_field_visibility')
    show_cheque_fields = fields.Boolean(compute='_compute_field_visibility')
    show_date = fields.Boolean(compute='_compute_field_visibility')
    show_identite = fields.Boolean(compute='_compute_field_visibility')


