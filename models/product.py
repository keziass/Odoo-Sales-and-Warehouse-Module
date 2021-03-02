# -*- coding: utf-8 -*-
import datetime

from odoo import models, fields, api
from odoo.exceptions import UserError


class product(models.Model):
    _name = 'sw_wh.product'
    _rec_name = 'name'

    product_id = fields.Char(string="Code", default="New", readonly=True)

    name = fields.Char("Product Name", help="Isi dengan nama product")
    image = fields.Binary("Image", attachment="true", help="Select image here")
    desc = fields.Text("Description")
    price = fields.Monetary("Price")
    qty = fields.Float("Jumlah", readonly=True, default=0)
    qty_in = fields.Float("Jumlah Barang Masuk", default=0)
    qty_out = fields.Float("Jumlah Barang Defect", default=0)
    currency_id = fields.Many2one('res.currency', 'Currency',
                                  default=lambda self: self.env.user.company_id.currency_id)


    @api.model
    def create(self, vals_list):
        vals_list.update({
            'product_id': self.env["ir.sequence"].with_context().next_by_code('sw_wh.product')
        })
        return super(product, self).create(vals_list)

    @api.multi
    def name_get(self):
        data = []
        for rec in self:
            data.append((rec.id, rec.name))  # .id harus ada di depan.
        return data

    @api.multi
    def write(self, vals):
        new_qty=self.qty
        if 'qty_in' in vals:
            new_qty = new_qty + vals['qty_in']
        if 'qty_out' in vals:
            if vals['qty_out'] < new_qty:
                new_qty = new_qty - vals['qty_out']
            else:
                raise UserError("Stock tidak ADA")
        if new_qty < 0:
            new_qty = 0
        vals.update({'qty': new_qty})

        return super(product, self).write(vals)

    @api.model
    def alert_qty(self):
        end_date = datetime.date.today().replace(day=1) - datetime.timedelta(days=1)
        start_date = end_date.replace(day=1)
        print("START", start_date, "END", end_date)
        detail_bulan_lalu = self.env["swalayan_sales.detail_order"].sudo().search([("tanggal", "<=", end_date)])
        # str = "Harap ingatkan member di bawah ini untuk mengembalikan buku:\n"
        product = []
        for rec in detail_bulan_lalu:
            jum = 0
            temp = {
                "id": 0,
                "qty": 0
            }
            rec.tanggal
            for rec2 in product:
                if rec.product_id.id == rec2["id"]:
                    product[jum]["qty"] = product[jum]["qty"] + rec.qty
                else:
                    jum = jum + 1

            if jum == len(product):
                temp["id"] = rec.product_id.id
                temp["qty"] = rec.qty
                product.append(temp)
        stri = "Stock Hampir HABIS! Segera Pesan! \n"
        for x in product:
            products = self.env["sw_wh.product"].sudo().search([("id", "=", x['id'])])
            x["qty"] = x["qty"] / 4
            if products.qty <= x["qty"]:
                stri = stri + products.name + " - Minimum Stock : " + str(x["qty"]) + "\n"
        print(stri)
        return stri

