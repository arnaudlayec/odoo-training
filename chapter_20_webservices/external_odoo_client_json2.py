# You MUST store this key securely. Place it in an
# environment variable or in in a file outside of
# git (e.g. your home directory).
api_key = "4fb0311b842344307e833b93297baaac7cda49f1"

import requests
response = requests.post(
    "http://training_19-0.localhost/json/2/library.book/search_read",
    headers={
        "Authorization": f"Bearer {api_key}",
        # "X-Odoo-Database": "...",
    },
    json={
        "domain": [
            [
                "display_name",
                "ilike",
                "a%"
            ]
        ],
        "fields": [
            "display_name"
        ],
        "limit": 20
    },
)
response.raise_for_status()
data = response.json()

from pprint import pprint
pprint(data)
