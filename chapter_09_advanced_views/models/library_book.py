from odoo import fields, models
from odoo.fields import Domain


class LibraryBook(models.Model):
    _name = "library.book"
    _description = "Livre de bibliothèque"
    _order = "sequence, id"

    name = fields.Char(string="Titre", required=True)
    isbn = fields.Char()
    date_release = fields.Date(string="Date de sortie")
    page_count = fields.Integer(string="Nombre de pages")
    notes = fields.Text(string="Notes internes")
    cover = fields.Image(string="Couverture")
    active = fields.Boolean(default=True)
    price = fields.Monetary(string="Prix")
    currency_id = fields.Many2one(
        comodel_name="res.currency",
        string="Devise",
        default=lambda self: self.env.company.currency_id,
    )
    category_id = fields.Many2one(comodel_name="library.book.category", string="Catégorie")
    # Couplé à widget="handle" en vue liste : le glisser-déposer des lignes met à jour ce
    # champ, que _order utilise ensuite pour trier — sans lui, le glisser-déposer n'aurait
    # aucun effet persistant.
    sequence = fields.Integer(string="Séquence", default=10)
    state = fields.Selection(
        selection=[
            ("new", "Nouveau"),
            ("available", "Disponible"),
            ("borrowed", "Emprunté"),
            ("lost", "Perdu"),
        ],
        string="État",
        default="new",
        required=True,
    )
    tag_ids = fields.Many2many(comodel_name="library.book.tag", string="Étiquettes")

    # Bonus
    def action_view_category_books(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": "Livres de la catégorie",
            "res_model": "library.book",
            "view_mode": "list,form",
            "domain": Domain("category_id", "=", self.category_id.id),
        }
