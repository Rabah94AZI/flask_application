from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Mon Application")
        
        self.label = QLabel("Bonjour, bienvenue dans l'application !", self)
        self.label.move(50, 50)
        
        self.bouton = QPushButton("Cliquez ici", self)
        self.bouton.move(50, 100)
        self.bouton.clicked.connect(self.on_bouton_clicked)

    def on_bouton_clicked(self):
        self.label.setText("Vous avez cliqué sur le bouton !")

if __name__ == "__main__":
    app = QApplication([])
    
    fenetre = MainWindow()
    fenetre.show()

    app.exec_()
