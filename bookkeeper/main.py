import sys
from PySide6.QtWidgets import QApplication

from repository.database import DatabaseConnection
from view.view import MainWindow
from view.connector import Connector

db = DatabaseConnection()
conn = Connector(db)
app = QApplication(sys.argv)

main_window = MainWindow(db, conn)
main_window.show()

app.exec()
# db.close_connection()