from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = 'sale.order.line'

    price_subtotal = fields.Monetary(readonly=False)

    @api.depends('product_id', 'product_uom', 'product_uom_qty', 'price_subtotal')
    def _compute_price_unit(self):
        super()._compute_price_unit()
        for rec in self:
            rec.price_unit = rec.price_subtotal / rec.product_uom_qty
