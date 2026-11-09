
import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QLabel,
    QPushButton, QLineEdit, QComboBox, QSpinBox,
    QListWidget, QVBoxLayout, QHBoxLayout,
    QFormLayout, QGroupBox
)
from PyQt6.QtCore import pyqtSignal


class MovieForm(QWidget):
    movie_added = pyqtSignal(str, int, str)

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()

        group = QGroupBox("Додавання фільму")
        form = QFormLayout()

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Введіть назву фільму")

        self.year_input = QSpinBox()
        self.year_input.setRange(1900, 2026)
        self.year_input.setValue(2020)

        self.genre_input = QComboBox()
        self.genre_input.addItems([
            "Комедія",
            "Фантастика",
            "Бойовик",
            "Драма",
            "Пригоди"
        ])

        form.addRow("Назва:", self.name_input)
        form.addRow("Рік:", self.year_input)
        form.addRow("Жанр:", self.genre_input)

        group.setLayout(form)
        layout.addWidget(group)

        self.add_button = QPushButton("Додати фільм")
        self.reset_button = QPushButton("Очистити поля")

        layout.addWidget(self.add_button)
        layout.addWidget(self.reset_button)

        self.setLayout(layout)

        self.add_button.clicked.connect(self.add_movie)
        self.reset_button.clicked.connect(self.reset_form)

    def add_movie(self):
        name = self.name_input.text().strip()
        year = self.year_input.value()
        genre = self.genre_input.currentText()

        if not name:
            return

        self.movie_added.emit(name, year, genre)
        self.reset_form()

    def reset_form(self):
        self.name_input.clear()
        self.year_input.setValue(2020)
        self.genre_input.setCurrentIndex(0)


class MovieList(QWidget):
    movie_selected = pyqtSignal(int, str)

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()

        title = QLabel("Список фільмів")
        title.setStyleSheet("font-size: 17px; font-weight: bold;")

        self.list_widget = QListWidget()
        self.info_label = QLabel("Оберіть фільм зі списку")
        self.info_label.setWordWrap(True)

        layout.addWidget(title)
        layout.addWidget(self.list_widget)
        layout.addWidget(self.info_label)

        self.setLayout(layout)

        self.list_widget.currentRowChanged.connect(
            self.select_movie
        )

    def add_movie(self, name, year, genre):
        self.list_widget.blockSignals(True)

        self.list_widget.addItem(
            name + " (" + str(year) + ")"
        )

        self.list_widget.blockSignals(False)

        self.movies = getattr(self, "movies", [])
        self.movies.append((name, year, genre))

    def select_movie(self, index):
        if index >= 0 and index < len(self.movies):
            movie = self.movies[index]

            info = (
                "Назва: " + movie[0] + "\n"
                + "Рік: " + str(movie[1]) + "\n"
                + "Жанр: " + movie[2]
            )

            self.info_label.setText(info)
            self.movie_selected.emit(index, movie[0])


class MovieApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Колекція фільмів")
        self.setMinimumSize(750, 450)

        widget = QWidget()
        self.setCentralWidget(widget)

        main_layout = QVBoxLayout()
        content_layout = QHBoxLayout()

        self.form = MovieForm()
        self.movie_list = MovieList()

        content_layout.addWidget(self.form)
        content_layout.addWidget(self.movie_list)

        main_layout.addLayout(content_layout)

        self.status_label = QLabel("Готово до роботи")
        main_layout.addWidget(self.status_label)

        widget.setLayout(main_layout)

        self.form.movie_added.connect(self.add_movie)
        self.movie_list.movie_selected.connect(
            self.show_movie
        )

    def add_movie(self, name, year, genre):
        self.movie_list.add_movie(name, year, genre)

        count = self.movie_list.list_widget.count()

        self.status_label.setText(
            "Фільм додано. Кількість фільмів: " + str(count)
        )

    def show_movie(self, index, name):
        self.status_label.setText(
            "Обрано фільм: " + name
        )


app = QApplication(sys.argv)
window = MovieApp()
window.show()
sys.exit(app.exec())
