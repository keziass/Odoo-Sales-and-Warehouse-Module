# -*- coding: utf-8 -*-
from odoo import http

# class SwWh(http.Controller):
#     @http.route('/sw_wh/sw_wh/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/sw_wh/sw_wh/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('sw_wh.listing', {
#             'root': '/sw_wh/sw_wh',
#             'objects': http.request.env['sw_wh.sw_wh'].search([]),
#         })

#     @http.route('/sw_wh/sw_wh/objects/<model("sw_wh.sw_wh"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('sw_wh.object', {
#             'object': obj
#         })