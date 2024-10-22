# -*- coding: utf-8 -*-
# from odoo import http


# class Scm(http.Controller):
#     @http.route('/scm/scm', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/scm/scm/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('scm.listing', {
#             'root': '/scm/scm',
#             'objects': http.request.env['scm.scm'].search([]),
#         })

#     @http.route('/scm/scm/objects/<model("scm.scm"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('scm.object', {
#             'object': obj
#         })

