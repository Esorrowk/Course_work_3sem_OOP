from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QFormLayout,
    QLineEdit, QPushButton, QLabel, QMessageBox
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
        
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        # Форма
        form_layout = QFormLayout()
        
        # Поля ввода
        self.surname_input = QLineEdit()
        self.name_input = QLineEdit()
        self.group_input = QLineEdit()
        self.age_input = QLineEdit()
        self.avg_input = QLineEdit()
        
        # Если редактируем - заполняем поля
        if self.student:
            self.surname_input.setText(self.student.surname)
            self.name_input.setText(self.student.name)
            self.group_input.setText(self.student.group)
            self.age_input.setText(str(self.student.age))
            self.avg_input.setText(str(self.student.avg_score))
        
        # Добавляем поля в форму
        form_layout.addRow("Фамилия:", self.surname_input)
        form_layout.addRow("Имя:", self.name_input)
        form_layout.addRow("Группа:", self.group_input)
        form_layout.addRow("Возраст:", self.age_input)
        form_layout.addRow("Средний балл:", self.avg_input)
        
        layout.addLayout(form_layout)
        
        # Кнопки
        buttons_layout = QHBoxLayout()
        
        btn_ok = QPushButton("OK")
        btn_ok.clicked.connect(self.on_ok)
        
        btn_cancel = QPushButton("Отмена")
        btn_cancel.clicked.connect(self.reject)
        
        buttons_layout.addWidget(btn_ok)
        buttons_layout.addWidget(btn_cancel)
        
        layout.addLayout(buttons_layout)
        
    def on_ok(self):
        """Обработка нажатия OK"""
        # Получаем данные
        surname = self.surname_input.text().strip()
        name = self.name_input.text().strip()
        group = self.group_input.text().strip()
        age_text = self.age_input.text().strip()
        avg_text = self.avg_input.text().strip()
        
        # Проверяем, что все поля заполнены
        if not surname or not name or not group or not age_text or not avg_text:
            QMessageBox.warning(self, "Ошибка", "Все поля должны быть заполнены!")
            return
        
        # Проверяем возраст
        try:
            age = int(age_text)
            if age < 16 or age > 70:
                raise ValueError
        except ValueError:
            QMessageBox.warning(self, "Ошибка", "Возраст должен быть числом от 16 до 70!")
            self.age_input.setFocus()
            return
        
        # Проверяем средний балл
        try:
            avg = float(avg_text)
            if avg < 0 or avg > 100:
                raise ValueError
        except ValueError:
            QMessageBox.warning(self, "Ошибка", "Средний балл должен быть числом от 0 до 100!")
            self.avg_input.setFocus()
            return
        
        # Формируем данные
        if self.is_edit:
            # Для редактирования берем ID существующего студента
            self.data = (
                self.student.student_id,
                surname,
                name,
                group,
                age,
                avg
            )
        else:
            # Для добавления ID будет None (сгенерируется в БД)
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