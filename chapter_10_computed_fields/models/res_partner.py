from odoo import fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    borrowed_book_ids = fields.Many2many(
        comodel_name="library.book", string="Livres empruntés"
    )
