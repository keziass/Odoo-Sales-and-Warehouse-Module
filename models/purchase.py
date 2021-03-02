# -*- coding: utf-8 -*-

from odoo import models, fields, api
import datetime

class purchase(models.Model):
    _name = 'sw_wh.purchase'

    purchase_id = fields.Char("Code", default="New", required=True, readonly=True)
    vendor_id = fields.Many2one("sw_wh.vendor", string="Vendor", required=True)
    tanggal = fields.Date("Order Date", default=datetime.date.today())
    total = fields.Monetary("Total Amount", compute='get_total', default=0, readonly="True")
    detail_order_ids = fields.One2many("sw_wh.detail_order", "purchase_id",
                                              string="Detail Order")
    currency_id = fields.Many2one('res.currency', 'Currency',
                                  default=lambda self: self.env.user.company_id.currency_id)

    # employee_id = fields.Many2one("hr.employees", string="Yang bertugas") // ini kalau mau nyambung ke modul lain (depends pada manifest)
    # employee_id = fields.Many2one('res.users', string='Yang bertugas', index=True,
    #                               track_visibility='onchange', default=lambda self: self.env.user, readonly=True)


    @api.model  # UNTUK CRUD -> bawaan odoo
    def create(self, vals_list):
        vals_list.update({
            'purchase_id': self.env["ir.sequence"].with_context().next_by_code('sw_wh.purchase')
        })
        return super(purchase, self).create(vals_list)

    @api.multi
    @api.onchange("detail_order_ids")
    @api.depends("detail_order_ids")
    def get_total(self):
        for rec in self:
            jumlah = 0
            for x in rec.detail_order_ids:
                jumlah = jumlah + x.subtotal
            rec.total = jumlah


        # self.alertbooktelat()
    #
    # @api.multi
    # def print_transaksi_buku(self):
    #     return self.env.ref('books.action_report_transaksi_buku') \
    #         .with_context({'discard_logo_check': True}).report_action(self)