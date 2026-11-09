
import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QLabel,
    QPushButton, QLineEdit, QComboBox, QCheckBox,
    QSpinBox, QSlider, QVBoxLayout, QHBoxLayout,
    QFormLayout, QGroupBox
)
from PyQt6.QtCore import Qt


class StudentApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Реєстрація студента")
        self.setMinimumSize(450, 500)

        widget = QWidget()
        self.setCentralWidget(widget)

        main_layout = QVBoxLayout()
        widget.setLayout(main_layout)

        title = QLabel("Реєстрація студента")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 20px; font-weight: bold;")
        main_layout.addWidget(title)

        form_group = QGroupBox("Інформація про студента")
        form_layout = QFormLayout()

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Введіть ім'я та прізвище")

        self.group_input = QLineEdit()
        self.group_input.setPlaceholderText("Наприклад, БІКСб-1-25-40")

        self.course_input = QSpinBox()
        self.course_input.setRange(1, 6)
        self.course_input.setValue(1)

        self.specialty_input = QComboBox()
        self.specialty_input.addItems([
            "Кібербезпека",
            "Комп'ютерні науки",
            "Інженерія програмного забезпечення",
        ])

        form_layout.addRow("ПІБ:", self.name_input)
        form_layout.addRow("Група:", self.group_input)
        form_layout.addRow("Курс:", self.course_input)
        form_layout.addRow("Спеціальність:", self.specialty_input)

        form_group.setLayout(form_layout)
        main_layout.addWidget(form_group)

        attendance_group = QGroupBox("Відвідуваність")
        attendance_layout = QVBoxLayout()

        self.attendance_label = QLabel("Відвідуваність: 50%")
        self.attendance_slider = QSlider(Qt.Orientation.Horizontal)
        self.attendance_slider.setRange(0, 100)
        self.attendance_slider.setValue(50)

        attendance_layout.addWidget(self.attendance_label)
        attendance_layout.addWidget(self.attendance_slider)

        attendance_group.setLayout(attendance_layout)
        main_layout.addWidget(attendance_group)

        self.scholarship_check = QCheckBox("Отримує стипендію")
        main_layout.addWidget(self.scholarship_check)

        self.confirm_check = QCheckBox(
            "Підтверджую правильність введених даних"
        )
        main_layout.addWidget(self.confirm_check)

        self.result_label = QLabel("Заповніть форму")
        self.result_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.result_label.setWordWrap(True)
        main_layout.addWidget(self.result_label)

        button_layout = QHBoxLayout()

        self.confirm_button = QPushButton("Зареєструвати")
        self.reset_button = QPushButton("Скинути")

        self.confirm_button.setEnabled(False)

        button_layout.addWidget(self.confirm_button)
        button_layout.addWidget(self.reset_button)

        main_layout.addLayout(button_layout)

        self.name_input.textChanged.connect(self.update_name)

        self.attendance_slider.valueChanged.connect(
            lambda value: self.attendance_label.setText(
                "Відвідуваність: " + str(value) + "%"
            )
        )

        def update_specialty(specialty):
            self.result_label.setText(
                "Обрана спеціальність: " + specialty
            )

        self.specialty_input.currentTextChanged.connect(
            update_specialty
        )

        self.confirm_check.toggled.connect(
            self.confirm_button.setEnabled
        )

        self.confirm_button.clicked.connect(self.confirm_data)
        self.reset_button.clicked.connect(self.reset_form)

    def update_name(self, name):
        if name:
            self.result_label.setText("Студент: " + name)
        else:
            self.result_label.setText("Заповніть форму")

    def validate_data(self):
        name = self.name_input.text().strip()
        group = self.group_input.text().strip()

        if not name:
            return "Помилка: введіть ПІБ студента"

        if not group:
            return "Помилка: введіть назву групи"

        if not self.confirm_check.isChecked():
            return "Підтвердіть правильність даних"

        return ""

    def confirm_data(self):
        error = self.validate_data()

        if error:
            self.result_label.setText(error)
            return

        name = self.name_input.text()
        group = self.group_input.text()
        course = self.course_input.value()
        specialty = self.specialty_input.currentText()
        attendance = self.attendance_slider.value()

        if self.scholarship_check.isChecked():
            scholarship = "Так"
        else:
            scholarship = "Ні"

        self.result_label.setText(
            "Студента зареєстровано!\n"
            + "ПІБ: " + name + "\n"
            + "Група: " + group + "\n"
            + "Курс: " + str(course) + "\n"
            + "Спеціальність: " + specialty + "\n"
            + "Відвідуваність: " + str(attendance) + "%\n"
            + "Стипендія: " + scholarship
        )

    def reset_form(self):
        self.name_input.clear()
        self.group_input.clear()
        self.course_input.setValue(1)
        self.specialty_input.setCurrentIndex(0)
        self.attendance_slider.setValue(50)
        self.scholarship_check.setChecked(False)
        self.confirm_check.setChecked(False)
        self.result_label.setText("Форму очищено")


app = QApplication(sys.argv)
window = StudentApp()
window.show()
sys.exit(app.exec())
