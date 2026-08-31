# Correction des exercices

## Installer le module `web_responsive`

1. Modifier `spec.yaml` (voir le fichier)

**Note** : une convention veut que les répertoires et modules soient listés en ordre alphabétique.

2. Relancer un `ak build`

```bash
cd ~/.../training/odoo # (!) Bien se placer dans le dossier 'odoo'
ak build
```

3. Activer le mode développeur
Ouvrir l'URL : http://training_19-0.localhost/odoo/apps?debug=1

4. Actionner le bouton **Mettre à jour la liste des Apps**

5. Chercher et installer `web_responsive`. Vous devrez retirer le filtre *Apps*.

**Note** : le `__manifest__.py` d'un module Odoo permet de déclarer certains modules en tant que "Application", d'où ce filtre *Apps*.
