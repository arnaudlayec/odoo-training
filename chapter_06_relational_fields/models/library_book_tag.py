from odoo import fields, models

# Bonus
class LibraryBookTag(models.Model):
    _name = "library.book.tag"
    _description = "Étiquette de livre"

    name = fields.Char(string="Nom", required=True)
