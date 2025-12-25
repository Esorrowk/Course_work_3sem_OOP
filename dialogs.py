from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QFormLayout,
    QLineEdit, QPushButton, QMessageBox
)


class StudentDialog(QDialog):
    def __init__(self, parent=None, student=None):
        super().__init__(parent)

        self.student = student
        self.data = None

        if student:
            self.setWindowTitle("Редактировать студента")
            self.is_edit = True
        else:
            self.setWindowTitle("Добавить студента")
            self.is_edit = False

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)

        form = QFormLayout()

        self.surname_input = QLineEdit()
        self.name_input = QLineEdit()
        self.group_input = QLineEdit()
        self.age_input = QLineEdit()
        self.avg_input = QLineEdit()

        if self.student:
            self.surname_input.setText(self.student.surname)
            self.name_input.setText(self.student.name)
            self.group_input.setText(self.student.group)
            self.age_input.setText(str(self.student.age))
            self.avg_input.setText(str(self.student.avg_score))

        form.addRow("Фамилия:", self.surname_input)
        form.addRow("Имя:", self.name_input)
        form.addRow("Группа:", self.group_input)
        form.addRow("Возраст:", self.age_input)
        form.addRow("Средний балл:", self.avg_input)

        layout.addLayout(form)

        btn_layout = QHBoxLayout()

        ok_btn = QPushButton("OK")
        cancel_btn = QPushButton("Отмена")

        ok_btn.clicked.connect(self.on_ok)
        cancel_btn.clicked.connect(self.reject)

        btn_layout.addWidget(ok_btn)
        btn_layout.addWidget(cancel_btn)

        layout.addLayout(btn_layout)

    def on_ok(self):
        surname = self.surname_input.text().strip()
        name = self.name_input.text().strip()
        group = self.group_input.text().strip()
        age_text = self.age_input.text().strip()
        avg_text = self.avg_input.text().strip()

        if not all([surname, name, group, age_text, avg_text]):
            QMessageBox.warning(self, "Ошибка", "Заполните все поля")
            return

        try:
            age = int(age_text)
            avg = float(avg_text)
        except ValueError:
            QMessageBox.warning(self, "Ошибка", "Возраст — целое число, балл — число")
            return

        if age < 16 or age > 70:
            QMessageBox.warning(self, "Ошибка", "Возраст от 16 до 70")
            return

        if not (0 <= avg <= 100):
            QMessageBox.warning(self, "Ошибка", "Средний балл от 0 до 100")
            return

        if self.is_edit:
            self.data = (
                self.student.student_id,
                surname,
                name,
                group,
                age,
                avg
            )
        else:
            self.data = (
                None,
                surname,
                name,
                group,
                age,
                avg
            )

        self.accept()

    def get_data(self):
        return self.data