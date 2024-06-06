# Banque analytics

Ce script Python vous permet d'analyser les données de votre banque, comme la Banque Populaire, pour voir vos dépenses par catégories, votre solde à chaque transaction, etc 

Graphiques disponibles :
- Evolution du solde à chaque transaction
- Nombre de transaction par catégories
- Montant des dépenses par catégories
- Comparaison dépenses/revenus par mois

### Utilisation
1. Téléchargez votre fichier d'opérations au format CSV et placez le dans le dossier `compte/` (Pour la banque Populaire : Compte -> Télécharger les opérations -> Format CSV, format de date : JJ/MM/AAAA, séparateur : point-virgule, séparateur décimal : virgule).
    - Si vous avez plusieurs fichiers CSV, le script va automatiquement les lire et les fusionner.
2. Dans `banque.py`, définissez votre solde courant à la ligne 160 (`solde_courant = 1000` par exemple).
3. Lancez le script avec `python banque.py`. Les graphiques seront enregistrés dans le dossier `figures`.

### Autres banques
Si vous souhaitez utiliser les données d'une autre banque, téléchargez votre fichier d'opérations au format CSV et assurez vous que ce dernier contienne les colonnes suivantes :
- `Categorie`
- `Debit`
- `Credit`
- `Date operation`

### Exemple de graphiques
![alt text](figures/evolution_solde.png)
![alt text](figures/depenses_revenus_par_mois.png)