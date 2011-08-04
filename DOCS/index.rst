.. Algorithme de réordonnancement d'une table 0/1 (CURSES) master file, created by
   sphinx-quickstart on Fri Jul 29 01:20:12 2011.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.


.. toctree::
   :maxdepth: 1
   

Table de matières
==================
* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`


Quick start
===========

Version CURSES de l'algorithme de réordonnancement d'une table 0/1

#. On commence par préciser la table qu'on veut dans le fichier *curses_version.py* (ligne 114):

    * On indique pour celà les variables *table*, *labels_lignes*, *labels_colonnes* ::
    
        table = [[0, 0, 1], [1, 1, 1], [1, 0, 0], [1, 1, 0]]
        labels_lignes = ["ligne0", "ligne1", "ligne2"]
        labels_colonnes = ["col1", "col2", "col3", "col4"]
        
    * Ou encore on importe une table depuis un fichier texte ::
    
        table, labels_lignes, labels_colonnes =  imporTable_generique(open('./Examples/table_10_20.txt'), False, False)
    
#. Puis on exécute le script *curses_version.py* ::

    python curses_version.py
    
Touches Clavier
===============

===========     ===============================================
  Touche                              Action      
===========     ===============================================
  Espace        Choix de la ligne
    i           Déplacement en haut parmi les lignes autorisées
    k           Déplacement en bas parmi les lignes autorisées
===========     ===============================================

Documentation
=============
.. automodule:: ordonancement
   :members:
   
.. automodule:: import_export
   :members:
   
.. automodule:: utils
   :members:


