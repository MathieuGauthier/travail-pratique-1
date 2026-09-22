import json
import sys
import os
from PySide6.QtWidgets import QApplication, QHBoxLayout, QLineEdit,QMessageBox, QPushButton, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QLabel
from PySide6.QtCore import Qt


#-------------------------------------- Files -------------------------------------------------------
#C:\Users\User\Desktop\NAD\Python\TP1\data_small.json
#C:\Users\User\Desktop\NAD\Python\TP1\data_large.json

#----------------------------------- Les Fonctions --------------------------------------------------
# Function to load a JSON file and handle errors
def load_json_file(file_path):

    # Le try me permet de tester si le fichier existe et si le JSON est correct -------------------------------------
    try:

        #Le open me permet d'ouvrir le fichier en mode lecture et de le lire avec l'encodage UTF-8 pour les accents.
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data

    # Le except me permet de gérer les erreurs si le fichier n'existe pas ou si le JSON est incorrect.
    except FileNotFoundError:
        QMessageBox.critical(None, "Error", "Error: The file was not found. Please check the file path and try again.")
        return None

    except json.JSONDecodeError:
        QMessageBox.critical(None, "Error", "Error: The file JSON has incorrect data.")
        return None


# Fonction pour le tri croissant ou decroissant des données du tableau -----------------------------------------------
def tri(sortingtype):
    if sortingtype == "Croissant":
        table.sortItems(0, Qt.AscendingOrder)
    elif sortingtype == "Décroissant":
        table.sortItems(0, Qt.DescendingOrder)

# Fonction pour la barre de recherche --------------------------------------------------------------------------------
def researching(search_text):

    # Ici la premiere boucle est pour regarder les ROWS et les initialiser à False.
    for row in range(table.rowCount()):
        match = False

        # Ici la deuxieme boucle est pour regarder si le texte dans la COLUNM est identique a la recherche.
        for column in range(table.columnCount()):
            item = table.item(row, column)
            if item and search_text.lower() in item.text().lower():
                match = True
                break

        table.setRowHidden(row, not match)

#----------------------------------------------- L'interface ----------------------------------------------------------

app = QApplication(sys.argv)

# Le input me permet de demander à l'utilisateur de saisir le chemin du fichier JSON.
#Je conserve le chemin du ficher dans une variable pour afficher les informations plus tard.
file_path = input()
data = load_json_file(file_path)

# Les setRowCount et setColumnCount me permettent de définir le nombre de lignes et de colonnes du tableau
table = QTableWidget()
table.setRowCount(len(data))
table.setColumnCount(len(data[0]))
table.setHorizontalHeaderLabels(data[0].keys())


# Double boucle qui permet de remplir le tableau avec les données du JSON (itération).
for row, jsonitem in enumerate(data):
    for columns, (key, value) in enumerate(jsonitem.items()):
        table.setItem(row, columns, QTableWidgetItem(str(value)))


# Ici je set mes variables pour créer l'interface graphique.
interface = QLabel()
interface.setWindowTitle("Tableau de données JSON")
interface.setFixedSize(800,600)


# Ici je set ma variable pour la barre de recherche.
recherche = QLineEdit()
recherche.setPlaceholderText("Rechercher :")
recherche.textChanged.connect(lambda text: researching(text))


# Ici je set les varibles pour des bouttons.
bouton_c = QPushButton("Croissant")
bouton_d = QPushButton("Décroissant")
bouton_c.clicked.connect(lambda: tri("Croissant"))
bouton_d.clicked.connect(lambda: tri("Décroissant"))


# Ici pour afficher les données du fichier JSON.
file_name = os.path.basename(file_path)
file_size = os.path.getsize(file_path)
number_elements = len(data)
file_data = QLabel()
file_data.setText(f"Name : {file_name}\n"f"Size : {file_size} bytes\n" f"Number of elements : {number_elements}")


# Ici Je set ma varible pour la disposition mes bottons dans l'interface.
layout_v = QVBoxLayout(interface) 
layout_h = QHBoxLayout() 
layout_v.addLayout(layout_h) # addition les 2 layouts pour let set une fois.

layout_v.addWidget(file_data)
layout_v.addWidget(bouton_c)
layout_v.addWidget(bouton_d)
layout_v.addWidget(recherche)
layout_v.addWidget(table)


interface.setLayout(layout_h)
interface.show()
sys.exit(app.exec())