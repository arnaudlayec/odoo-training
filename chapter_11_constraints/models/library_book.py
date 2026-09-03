from odoo import api, fields, models
from odoo.exceptions import ValidationError
from odoo.fields import Domain

TAX_RATE = 5.5 / 100


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

    category_count = fields.Integer(
        string="Livres de la catégorie", compute="_compute_category_count"
    )
    price_with_tax = fields.Monetary(
        string="Prix TTC",
        compute="_compute_price_with_tax",
        inverse="_inverse_price_with_tax",
        search="_search_price_with_tax",
    )

    # [V19] Nouvelle syntaxe : un attribut de classe `models.Constraint`, en remplacement de
    # l'ancien `_sql_constraints = [(...)]`. Le nom d'attribut (préfixé `_`) sert d'identifiant
    # technique de la contrainte.
    _isbn_unique = models.Constraint(
        "UNIQUE(isbn)",
        "L'ISBN doit être unique.",
    )
    # Bonus 1 : un index sur un champ souvent filtré (ex. la recherche par catégorie côté
    # vue search/kanban du chapitre 9) accélère ces requêtes sur un gros volume de données.
    _category_index = models.Index("(category_id)")

    # ----------------------------------------------------------------
    # Compute
    # ----------------------------------------------------------------
    @api.depends("category_id.book_ids")
    def _compute_category_count(self):
        rg_result = self.env["library.book"]._read_group(
            domain=Domain("category_id", "in", self.category_id.ids),
            groupby=["category_id"],
            aggregates=["id:count"]
        )
        mapped_data = {categ.id: count for categ, count in rg_result}
        for book in self:
            book.category_count = mapped_data.get(book.category_id.id)

    @api.depends("price")
    def _compute_price_with_tax(self):
        for book in self:
            book.price_with_tax = book.price * (1 + TAX_RATE)

    def _inverse_price_with_tax(self):
        for book in self:
            book.price = book.price_with_tax / (1 + TAX_RATE)

    @api.model
    def _search_price_with_tax(self, operator, value):
        return Domain("price", operator, value / (1 + TAX_RATE))

    # ----------------------------------------------------------------
    # Constrains
    # ----------------------------------------------------------------
    @api.constrains("date_release")
    def _check_date_release(self):
        today = fields.Date.context_today(self)
        for book in self:
            if book.date_release and book.date_release > today:
                raise ValidationError("La date de sortie ne peut pas être dans le futur.")

    # ----------------------------------------------------------------
    # Actions
    # ----------------------------------------------------------------
    def action_view_category_books(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": "Livres de la catégorie",
            "res_model": "library.book",
            "view_mode": "list,form",
            "domain": Domain("category_id", "=", self.category_id.id),
        }
