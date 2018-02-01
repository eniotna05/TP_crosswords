<h1 align='center'> Optimisation TD1 </h1>
<p align='center'>
<i>Option ISIA - Centrale Paris <br>
Janvier 2017 <hr></i></p>

__Auteur__ : Eymard Houdeville, Antoine Aubay<br>

## Index
1. [Description](#description)
2. [Première solution](#init)
3. [Seconde solution](#bool)

Pour lancer le projet il suffit de git clone le repo et de lancer l'un des scripts main en ligne de commande:

"""
python mot_croise.py
"""

## <a name="description"></a>1. Première solution

Nos variables sont dans cette première solution les "segments" c'est à dire les mots que nous cherchons (caractérisés par leur longueur).

Nous avons commencé par poser trois contraintes:
- Chaque mot doit être différent
- Chaque mot qui occupe un segment doit avoir la même longueur que celui-ci
- Le choix des mots doit respecter la contrainte d'intersection

Cette solution était néanmoins extrêmement gourmande en énergie et en temps: il fallait poser la contrainte d'intersection pour tous les croisements et cette contrainte portait sur tous les mots au carré.

Cette solution permet de résoudre les problèmes simples comme la grille 1.

## <a name="init"></a>2. Seconde solution

La seconde solution que nous livrons dans ce repo repose sur une idée simple: il suffit de considérer les cases d'intersection de segments comme eux mêmes des segments et imposer que ces dernières soient des lettres uniques, communes aux mots verticaux et horizontaux.

**Solution**: 0.0906 secondes

Les valeurs de segments que nous trouvons:

1: 'analyzable', 2: 'ammonia', 3: 'arena', 4: 'lots', 5: 'playmate', 6: 'yellow', 7: 'studio', 8: 'amending', 9: 'lace', 10: 'drama', 11: 'unaware', 12: '
identified', 13: 'Talleyrand', 14: 'admit', 15: 'leeward', 16: 'aunt', 17: 'Woodlawn', 18: 'yearly', 19: 'annuli', 20: 'analysts', 21: 'taxi', 22: 'leeward
', 23: 'award', 24: 'anemometer'
