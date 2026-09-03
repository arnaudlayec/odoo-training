import xmlrpc.client

url, db, username = "http://training_19-0.localhost", "db", "admin"
api_key = "4fb0311b842344307e833b93297baaac7cda49f1" # password-like
common = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/common")
uid = common.authenticate(db, username, api_key, {})

models = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/object")
books = models.execute_kw(
    db, uid, api_key,
    "library.book", "search",
    [()]
)

from pprint import pprint
pprint(books)
