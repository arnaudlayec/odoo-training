from psycopg2.errors import UniqueViolation

from odoo.tests import Form, TransactionCase, tagged
from odoo.tests.common import new_test_user
from odoo.tools import mute_logger


@tagged("post_install", "-at_install")
class TestLibraryBook(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.category = cls.env["library.book.category"].create({"name": "Roman (test)"})

    def test_create_book_defaults(self):
        book = self.env["library.book"].create(
            {"name": "1984", "category_id": self.category.id}
        )
        self.assertEqual(book.state, "new")
        self.assertTrue(book.active)
        self.assertEqual(book.sequence, 10)
        self.assertEqual(book.currency_id, self.env.company.currency_id)

    @mute_logger("odoo.sql_db")
    def test_isbn_unique_constraint(self):
        self.env["library.book"].create(
            {"name": "Livre A", "isbn": "9780000000002", "category_id": self.category.id}
        )
        with self.assertRaises(UniqueViolation):
            self.env["library.book"].create(
                {"name": "Livre B", "isbn": "9780000000002", "category_id": self.category.id}
            )

    def test_ir_rule_reader_hides_archived_books(self):
        book = self.env["library.book"].create(
            {"name": "Livre archivé", "category_id": self.category.id, "active": False}
        )
        reader = new_test_user(
            self.env, login="library_reader_test", groups="library.group_library_reader"
        )
        librarian = new_test_user(
            self.env, login="library_librarian_test", groups="library.group_library_librarian"
        )
        Book = self.env["library.book"].with_context(active_test=False)
        self.assertFalse(
            Book.with_user(reader).search([("id", "=", book.id)]),
            "La règle ir.rule doit cacher les livres archivés au Lecteur",
        )
        self.assertTrue(
            Book.with_user(librarian).search([("id", "=", book.id)]),
            "Le Bibliothécaire doit voir les livres archivés (règle de groupe permissive, cf. chapitre 15)",
        )

    # ----------------------------------------------------------------
    # Bonus
    # ----------------------------------------------------------------
    def test_borrow_wizard_action_confirm(self):
        book = self.env["library.book"].create(
            {"name": "Livre à emprunter", "category_id": self.category.id, "state": "available"}
        )
        partner = self.env["res.partner"].create({"name": "Emprunteur Test"})

        wizard_form = self.env["library.book.borrow.wizard"].create({

        }).with_context(default_book_id=book.id)
        wizard_form.partner_id = partner
        wizard = wizard_form.save()
        wizard.action_confirm()

        self.assertEqual(book.state, "borrowed")
        self.assertEqual(book.borrower_id, partner)
