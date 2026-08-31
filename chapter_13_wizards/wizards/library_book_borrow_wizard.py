from odoo import api, fields, models


class LibraryBookBorrowWizard(models.TransientModel):
    # TransientModel : comme un Model classique (mêmes champs, mêmes méthodes), mais ses
    # enregistrements sont temporaires — nettoyés automatiquement par un cron (quelques
    # heures/jours), pas destinés à être conservés comme historique.
    _name = "library.book.borrow.wizard"
    _description = "Emprunter un livre"

    book_id = fields.Many2one(comodel_name="library.book", string="Livre", required=True)
    partner_id = fields.Many2one(comodel_name="res.partner", string="Emprunteur", required=True)
    loan_date = fields.Date(string="Date d'emprunt", default=fields.Date.context_today)

    @api.model
    def default_get(self, fields_list):
        # Bonus : pré-remplissage intelligent — si l'utilisateur courant est lié à un
        # partenaire (cas fréquent), on le propose directement comme emprunteur.
        defaults = super().default_get(fields_list)
        if "partner_id" in fields_list and not defaults.get("partner_id"):
            defaults["partner_id"] = self.env.user.partner_id.id
        return defaults

    def action_confirm(self):
        self.ensure_one()
        self.book_id.write(
            {
                "borrower_id": self.partner_id.id,
                "loan_date": self.loan_date,
                "state": "borrowed",
            }
        )
