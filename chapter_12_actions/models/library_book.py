from odoo import api, fields, models
from odoo.exceptions import ValidationError
from odoo.fields import Domain

TAX_RATE = 5.5 / 100


class LibraryBook(models.Model):
    _name = "library.book"
    _description = "Livre de bibliothèque"
    _order = "sequence, id"

    _isbn_unique = models.Constraint(
        "UNIQUE(isbn)",
        "L'ISBN doit être unique.",
    )
    _category_index = models.Index("(category_id)")

    name = fields.Char(string="Titre", required=True)
    isbn = fields.Char(string="ISBN", size=13)
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
    # Onchange & constrains
    # ----------------------------------------------------------------
    @api.onchange("isbn")
    def _onchange_isbn(self):
        # Ne vérifie qu'une fois l'ISBN-13 complet (13 caractères, la taille max du champ) —
        # inutile d'alerter à chaque frappe intermédiaire.
        if len(self.isbn or "") != 13:
            return
        # Le warning d'un onchange s'affiche toujours en orange (style "warning"), jamais
        # en vert/rouge : contrairement au bouton "Vérifier l'ISBN" ci-dessous, impossible
        # de déclencher ici un display_notification coloré, seul ce mécanisme natif existe.
        res = self.action_check_isbn()
        return {
            "warning": dict(res["params"], type="notification")
        }

    @api.constrains("date_release")
    def _check_date_release(self):
        if self.env.context.get("skip_date_release_check"): # Bonus
            return
        today = fields.Date.context_today(self)
        for book in self:
            if book.date_release and book.date_release > today:
                raise ValidationError("La date de sortie ne peut pas être dans le futur.")

    # ----------------------------------------------------------------
    # Actions & business logics
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

    @api.model
    def _check_isbn_format(self, isbn):
        # Norme ISBN-13 : 13 chiffres, le dernier (clé de contrôle) est calculé à partir des
        # 12 premiers avec des poids alternés 1/3, de sorte que la somme pondérée soit un
        # multiple de 10.
        digits = isbn or ""
        if len(digits) != 13 or not digits.isdigit():
            return False
        checksum = sum(int(d) * (1 if i % 2 == 0 else 3) for i, d in enumerate(digits))
        return checksum % 10 == 0

    def action_check_isbn(self):
        """Méthode PUBLIQUE (pas de préfixe `_`) : appelée depuis un bouton de vue, donc
        potentiellement accessible en RPC — jamais de préfixe `_` sur ce genre de méthode."""
        self.ensure_one()
        action = {
            "type": "ir.actions.client",
            "tag": "display_notification",
            "params": {
                "title": "Bibliothèque",
                "message": "ISBN valide.",
                "type": "success",
            },
        }
        if not self._check_isbn_format(self.isbn):
            action["params"] = dict(
                action["params"],
                message="ISBN invalide.",
                type="danger",
            )
        return action
