from odoo import models, fields, api
import datetime

from odoo.exceptions import UserError


class vendor(models.Model):
    _name = 'sw_wh.vendor'

    code = fields.Char("Code", default="Vendor Code", required=True, readonly=True)
    name = fields.Char("Name", required=True)
    alamat = fields.Char("Alamat", required=True)
    no_telp = fields.Char("No Telp", required=True)
    desc = fields.Text("Deskripsi")
    purchase_ids = fields.One2many("sw_wh.purchase", "vendor_id", string="Purchase")

    @api.model
    def create(self, vals_list):
        vals_list.update({
            'code': self.env["ir.sequence"].with_context().next_by_code('sw_wh.vendor')
        })
        return super(vendor, self).create(vals_list)

    @api.multi
    def name_get(self):
        data = []
        for rec in self:
            data.append((rec.id, rec.name))  # .id harus ada di depan.
        return data