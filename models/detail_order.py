from odoo import models, fields, api
import datetime

from odoo.exceptions import UserError


class detail_order(models.Model):
    _name = 'sw_wh.detail_order'

    name = fields.Char("Code", default="Detail Code", required=True, readonly=True)
    product_id = fields.Many2one("sw_wh.product", string="Product", required=True)
    qty = fields.Float("Jumlah", default=0, required=True)
    price = fields.Monetary("Harga Satuan",required=True, default=0)
    subtotal = fields.Monetary("SubTotal", required=True, default=0, compute="hitung_subtotal")
    currency_id = fields.Many2one('res.currency', 'Currency',
                                  default=lambda self: self.env.user.company_id.currency_id)
    purchase_id = fields.Many2one("sw_wh.purchase", string="Purchase Order")

    @api.model
    def create(self, vals_list):
        vals_list.update({
            'name': self.env["ir.sequence"].with_context().next_by_code('sw_wh.detail_order')
        })
        update_new = self.env['sw_wh.product'].sudo().search([('id', '=', vals_list['product_id'])])
        new_price = (update_new.price*update_new.qty + vals_list['price']*vals_list['qty']) / (update_new.qty+vals_list['qty'])
        print(update_new.price, " - ", update_new.qty, " - ", vals_list['price'], " - ", vals_list['qty'])
        update_new.write({'qty_in': vals_list['qty'],
                          'price': new_price})
        return super(detail_order, self).create(vals_list)

    @api.multi
    @api.depends("qty","product_id")
    def hitung_subtotal(self):
        for rec in self:
            subtotal = rec.price*rec.qty
            rec.subtotal = subtotal

    @api.multi
    def write(self, vals_list):
        self.ensure_one()
        if 'qty' in vals_list:
            new_qty = vals_list['qty']
            old_qty = self.qty
            if 'product_id' in vals_list:
                update_new = self.env['sw_wh.product'].search([('id', '=', vals_list['product_id'])])
                self.product_id.write({'qty_out': old_qty})
                update_new.write({'qty_in': new_qty})
            else:
                new_price = (self.product_id.price * self.product_id.qty + vals_list['subtotal']) / (
                            self.product_id.qty + vals_list['qty'])
                self.product_id.write({'qty_out': old_qty,
                                       'qty_in': new_qty,
                                       'price': new_price})
        else:
            if 'product_id' in vals_list:
                qty = self.qty
                pid = vals_list['product_id']
                update_new = self.env['sw_wh.product'].sudo().search([('id', '=', pid)])
                self.product_id.write({'qty_out': qty})
                update_new.write({'qty_in': qty})
                print(update_new)
        res = super(detail_order, self).write(vals_list)
        return res

