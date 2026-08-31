# Correction des exercices

## 1. Modèle depuis l'UI — mini-exercice

1. **Paramètres > Technique > Structure de la base de données > Modèles**, chercher "Contact".
2. Ouvrir la fiche, cliquer sur l'icône "bug" (mode debug) > **Voir les métadonnées**.

**Réponse** : XML ID `base.model_res_partner`.

**Note** : tout modèle Python génère automatiquement un `ir.model` dont l'External ID suit la
convention `<module>.model_<nom_du_modèle_avec_underscores>`. `res.partner` étant
défini dans le module `base`, on obtient `base.model_res_partner`.

## 2. Menus — mini-exercice

**Réponse** : XML ID `account.action_move_out_invoice`.

Pour la retrouver soi-même : mode debug actif, cliquer sur le menu "Facturation" (niveau 1),
puis l'icône bug de la page chargée > **Action**. Le  External ID est l'autre nom du XML ID.

## 3. Bonus — vues liste et formulaire manuelles

1. Architecture de vue liste simple

```xml
<list>
   <field name="x_name"/>
</list>
```

2. Architecture de vue liste avec d'autres champs

```xml
<list>
   <field name="x_name"/>
   <field name="create_date"/>
   <field name="write_date"/>
</list>
```

3. Vue formulaire avec nouveaux champs custom

```xml
<form>
      <sheet>
         <group>
            <field name="x_name"/>
            <field name="x_is_done"/>
            <field name="x_deadline"/>
         </group>
      </sheet>
</form>
```