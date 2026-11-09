
import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QLabel,
    QPushButton, QLineEdit, QTextEdit, QComboBox,
    QCheckBox, QRadioButton, QSlider, QSpinBox,
    QProgressBar, QVBoxLayout, QHBoxLayout,
    QFormLayout, QGroupBox
)
from PyQt6.QtCore import Qt


class FootballApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Реєстрація футбольної команди")
        self.setMinimumSize(600, 650)

        main_widget = QWidget()
        self.setCentralWidget(main_widget)

        main_layout = QVBoxLayout()
        main_widget.setLayout(main_layout)

        title = QLabel("Реєстрація футбольної команди")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 20px; font-weight: bold;")
        title.setToolTip("Головний заголовок програми")

        main_layout.addWidget(title)

        form_group = QGroupBox("Інформація про команду")
        form_layout = QFormLayout()

        self.team_name = QLineEdit()
        self.team_name.setPlaceholderText("Введіть назву команди")

        self.coach_name = QLineEdit()
        self.coach_name.setPlaceholderText("Введіть ім'я тренера")

        self.league = QComboBox()
        self.league.addItems([
            "Прем'єр-ліга",
            "Перша ліга",
            "Друга ліга",
            "Аматорська ліга"
        ])
        self.league.setToolTip("Оберіть лігу команди")

        self.players = QSpinBox()
        self.players.setRange(1, 30)
        self.players.setValue(11)
        self.players.setToolTip("Кількість гравців у команді")

        form_layout.addRow("Назва команди:", self.team_name)
        form_layout.addRow("Тренер:", self.coach_name)
        form_layout.addRow("Ліга:", self.league)
        form_layout.addRow("Кількість гравців:", self.players)

        form_group.setLayout(form_layout)
        main_layout.addWidget(form_group)

        position_group = QGroupBox("Додаткова інформація")
        position_layout = QVBoxLayout()

        self.captain = QRadioButton("Призначити капітана")
        self.captain.setChecked(True)

        self.uniform = QCheckBox("Потрібна нова футбольна форма")
        self.uniform.setToolTip("Позначте, якщо команді потрібна форма")

        position_layout.addWidget(self.captain)
        position_layout.addWidget(self.uniform)

        position_group.setLayout(position_layout)
        main_layout.addWidget(position_group)

        level_layout = QHBoxLayout()

        level_label = QLabel("Рівень команди:")
        self.level_slider = QSlider(Qt.Orientation.Horizontal)
        self.level_slider.setRange(1, 10)
        self.level_slider.setValue(5)

        self.level_value = QLabel("5")

        self.level_slider.valueChanged.connect(
            lambda value: self.level_value.setText(str(value))
        )

        level_layout.addWidget(level_label)
        level_layout.addWidget(self.level_slider)
        level_layout.addWidget(self.level_value)

        main_layout.addLayout(level_layout)

        main_layout.addWidget(QLabel("Опис команди:"))

        self.description = QTextEdit()
        self.description.setPlaceholderText(
            "Напишіть коротку інформацію про команду..."
        )
        self.description.setMaximumHeight(100)
        main_layout.addWidget(self.description)

        self.progress = QProgressBar()
        self.progress.setRange(0, 100)
        self.progress.setValue(50)
        self.progress.setFormat("Заповнення анкети: %p%")
        main_layout.addWidget(self.progress)

        button_layout = QHBoxLayout()

        self.save_button = QPushButton("Зберегти")
        self.clear_button = QPushButton("Очистити")

        self.save_button.setToolTip("Зберегти інформацію про команду")
        self.clear_button.setToolTip("Очистити всі поля")

        self.save_button.clicked.connect(self.save_data)
        self.clear_button.clicked.connect(self.clear_data)

        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.clear_button)

        main_layout.addLayout(button_layout)

    def save_data(self):
        self.progress.setValue(100)
        self.save_button.setText("Збережено!")

    def clear_data(self):
        self.team_name.clear()
        self.coach_name.clear()
        self.description.clear()
        self.players.setValue(11)
        self.league.setCurrentIndex(0)
        self.captain.setChecked(True)
        self.uniform.setChecked(False)
        self.level_slider.setValue(5)
        self.progress.setValue(0)
        self.save_button.setText("Зберегти")


app = QApplication(sys.argv)
window = FootballApp()
window.show()
sys.exit(app.exec())
