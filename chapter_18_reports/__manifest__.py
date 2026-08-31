{
    "name": "Bibliothèque",
    "version": "19.0.1.0.0",
    "category": "Bibliothèque",
    "summary": "Gérer une bibliothèque de livres et ses emprunts",
    "author": "Your Name, Another Co-Author",
    "website": "https://github.com/your-repo/odoo-library",
    "license": "LGPL-3",
    "depends": ["base", "mail"],
    "data": [
        "security/library_security.xml",
        "security/ir.model.access.csv",
        # Chargée avant library_book_views.xml : ce fichier définit l'action
        # action_library_book_borrow_wizard référencée par %(...)d dans son bouton "Emprunter"
        # — l'id externe doit déjà exister au moment où cette référence est résolue.
        "wizards/library_book_borrow_wizard_views.xml",
        "views/library_book_views.xml",
        "views/library_book_category_views.xml",
        "views/res_partner_views.xml",
        "data/library_category_data.xml",
        "report/library_book_templates.xml",
        "report/library_book_report_actions.xml",
        "mail/library_book_mail_template.xml",
    ],
    "demo": [
        "demo/library_book_demo.xml",
    ],
    "installable": True,
}
