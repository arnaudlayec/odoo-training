from odoo import fields, models


class LibraryBookCategory(models.Model):
    _name = "library.book.category"
    _description = "Catégorie de livre"

    name = fields.Char(string="Nom", required=True)
    book_ids = fields.One2many(
        comodel_name="library.book",
        inverse_name="category_id",
        string="Livres"
    )
