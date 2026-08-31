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
        "security/ir.model.access.csv",
        "views/library_book_views.xml",
    ],
    "installable": True,
}
