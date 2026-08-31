from odoo import fields, models


class LibraryBook(models.Model):
    _name = "library.book"
    _description = "Livre de bibliothèque"

    name = fields.Char(string="Titre", required=True)
    isbn = fields.Char() # Argument 'string' optionnel : auto-determiné par le nom de la variable
    date_release = fields.Date(string="Date de sortie")
    page_count = fields.Integer(string="Nombre de pages")
    notes = fields.Text(string="Notes internes")
    cover = fields.Image(string="Couverture")
    active = fields.Boolean(
        # Argument 'string' optionnel : déjà défini dans `models.Models` (puis traduit)
        default=True, # Optionel : True est la valeur par défaut des Boolean
    )
    price = fields.Monetary(
        string="Prix",
        currency_field="currency_id", # Optionel ici car suit la convention
    )
    currency_id = fields.Many2one(
        comodel_name="res.currency",
        string="Devise",
        default=lambda self: self.env.company.currency_id,
    )
