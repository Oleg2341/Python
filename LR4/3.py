
import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QTextEdit,
    QFileDialog, QMessageBox
)
from PyQt6.QtGui import QAction
from PyQt6.QtCore import Qt


class StudentNotes(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Студентські нотатки")
        self.setMinimumSize(600, 450)

        self.text_edit = QTextEdit()
        self.text_edit.setPlaceholderText(
            "Введіть свої студентські нотатки..."
        )
        self.setCentralWidget(self.text_edit)

        self.create_menu()
        self.create_toolbar()

        self.statusBar().showMessage("Готово до роботи")

        self.text_edit.textChanged.connect(self.update_status)

    def create_menu(self):
        menu = self.menuBar()

        file_menu = menu.addMenu("Файл")

        new_action = QAction("Новий документ", self)
        new_action.setShortcut("Ctrl+N")
        new_action.triggered.connect(self.new_file)

        open_action = QAction("Відкрити", self)
        open_action.setShortcut("Ctrl+O")
        open_action.triggered.connect(self.open_file)

        save_action = QAction("Зберегти", self)
        save_action.setShortcut("Ctrl+S")
        save_action.triggered.connect(self.save_file)

        exit_action = QAction("Вийти", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)

        file_menu.addAction(new_action)
        file_menu.addAction(open_action)
        file_menu.addAction(save_action)
        file_menu.addSeparator()
        file_menu.addAction(exit_action)

        help_menu = menu.addMenu("Довідка")

        about_action = QAction("Про програму", self)
        about_action.triggered.connect(self.show_about)

        info_action = QAction("Інформація", self)
        info_action.triggered.connect(self.show_info)

        help_menu.addAction(about_action)
        help_menu.addAction(info_action)

        self.new_action = new_action
        self.open_action = open_action
        self.save_action = save_action

    def create_toolbar(self):
        toolbar = self.addToolBar("Інструменти")

        toolbar.addAction(self.new_action)
        toolbar.addAction(self.open_action)
        toolbar.addAction(self.save_action)

    def new_file(self):
        self.text_edit.clear()
        self.statusBar().showMessage("Створено новий документ")

    def open_file(self):
        file_name, result = QFileDialog.getOpenFileName(
            self,
            "Відкрити файл",
            "",
            "Текстові файли (*.txt);;Усі файли (*)"
        )

        if file_name:
            try:
                with open(file_name, "r", encoding="utf-8") as file:
                    self.text_edit.setPlainText(file.read())

                self.statusBar().showMessage(
                    "Файл відкрито: " + file_name
                )

            except Exception:
                QMessageBox.warning(
                    self,
                    "Помилка",
                    "Не вдалося відкрити файл"
                )

    def save_file(self):
        file_name, result = QFileDialog.getSaveFileName(
            self,
            "Зберегти файл",
            "",
            "Текстові файли (*.txt);;Усі файли (*)"
        )

        if file_name:
            try:
                with open(file_name, "w", encoding="utf-8") as file:
                    file.write(self.text_edit.toPlainText())

                self.statusBar().showMessage(
                    "Файл збережено: " + file_name
                )

            except Exception:
                QMessageBox.warning(
                    self,
                    "Помилка",
                    "Не вдалося зберегти файл"
                )

    def show_about(self):
        QMessageBox.about(
            self,
            "Про програму",
            "Студентські нотатки\nВерсія 1.0\nДодаток створено на PyQt6"
        )

    def show_info(self):
        QMessageBox.information(
            self,
            "Інформація",
            "Програма призначена для створення та збереження студентських нотаток."
        )

    def update_status(self):
        text = self.text_edit.toPlainText()
        count = len(text)

        self.statusBar().showMessage(
            "Кількість символів: " + str(count)
        )


app = QApplication(sys.argv)
window = StudentNotes()
window.show()
sys.exit(app.exec())
