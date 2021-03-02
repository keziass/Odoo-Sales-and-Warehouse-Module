from odoo import models, fields, api
import datetime

from odoo.exceptions import UserError


class cycle(models.Model):
    _name = 'sw_wh.cycle'

    name = fields.Char("Code", default="Cycle Code", required=True, readonly=True)
    tanggal = fields.Date("Tanggal", default=datetime.date.today())
    product_id = fields.Many2one("sw_wh.product", string="Product", required=True)
    qty = fields.Float("Jumlah", default=0, required=True)
    state = fields.Selection(selection=[("in", "Penyesuaian Barang"),("out", "Pengurangan Barang")],
                             string="Jenis", default="out")
    desc = fields.Text("Keterangan")

    @api.model
    def create(self, vals_list):
        vals_list.update({
            'name': self.env["ir.sequence"].with_context().next_by_code('sw_wh.cycle')
        })
        update_new = self.env['sw_wh.product'].sudo().search([('id', '=', vals_list['product_id'])])
        if vals_list["state"]=="in":
            update_new.write({'qty_in': vals_list['qty']})
        else:
            update_new.write({'qty_out': vals_list['qty']})
        return super(cycle, self).create(vals_list)

    @api.multi
    def write(self, vals_list):
        self.ensure_one()
        state = self.state
        if 'state' in vals_list:
            state = vals_list["state"]
            if vals_list['state'] == 'out':
                self.product_id.write({'qty_out': self.qty})
            else:
                self.product_id.write({'qty_in': self.qty})
        if 'qty' in vals_list:
            new_qty = vals_list['qty']
            old_qty = self.qty
            if 'product_id' in vals_list:
                if state == 'out':
                    update_new = self.env['sw_wh.product'].search([('id', '=', vals_list['product_id'])])
                    update_new.write({'qty_out': new_qty})
                    self.product_id.write({'qty_in': old_qty})
                else:
                    update_new = self.env['sw_wh.product'].search([('id', '=', vals_list['product_id'])])
                    update_new.write({'qty_in': new_qty})
                    self.product_id.write({'qty_out': old_qty})
            else:
                if state == 'out':
                    self.product_id.write({'qty_out': new_qty})
                else:
                    self.product_id.write({'qty_in': new_qty})
        else:
            if 'product_id' in vals_list:
                if state == 'out':
                    update_new = self.env['sw_wh.product'].search([('id', '=', vals_list['product_id'])])
                    update_new.write({'qty_out': self.qty})
                    self.product_id.write({'qty_in': self.qty})
                else:
                    update_new = self.env['sw_wh.product'].search([('id', '=', vals_list['product_id'])])
                    update_new.write({'qty_in': self.qty})
                    self.product_id.write({'qty_out': self.qty})
            elif 'state' in vals_list:
                if vals_list['state'] == 'out':
                    self.product_id.write({'qty_out': self.qty})
                else:
                    self.product_id.write({'qty_in': self.qty})
        res = super(cycle, self).write(vals_list)
        return res

