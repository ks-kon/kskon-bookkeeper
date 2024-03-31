"""
main
"""
import sys
from PySide6.QtWidgets import QApplication

from bookkeeper.bookkeeper.repository.database import DatabaseConnection
from bookkeeper.bookkeeper.repository.memory_repository import MemoryRepository

from bookkeeper.bookkeeper.view.view import MainWindow
from bookkeeper.bookkeeper.repository.connector import Connector

from bookkeeper.bookkeeper.models.category import Category
from bookkeeper.bookkeeper.models.budget import Budget


if __name__ == '__main__':
    db = DatabaseConnection()
    conn = Connector(db)
    budg = Budget(db, 1000, 5000, 100000)
    cat_mem_repo = MemoryRepository[Category]()
    cat_tree = [('Продукты', None), ('Электроника', None)]
    Category.create_from_tree(tree=cat_tree, repo=cat_mem_repo)
    print(Category.make_tree_from_repo(Category, repo=cat_mem_repo))
    conn.send_categories_to_db()

    app = QApplication(sys.argv)
    main_window = MainWindow(db, conn, budg, cat_mem_repo)
    main_window.show()

    app.exec()
