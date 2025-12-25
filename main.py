import sys
from PyQt6.QtWidgets import *
from PyQt6.QtCore import Qt
from database import StudentDataBase
from dialogs import StudentDialog
from student import Student


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("База данных студентов")
        self.resize(900, 600)

        self.db = StudentDataBase()
        self.current_file = None

        # Создаем таблицу ПЕРЕД использованием
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(
            ["ID", "Фамилия", "Имя", "Группа", "Возраст", "Средний балл"]
        )
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table.setSortingEnabled(True)
        
        # Устанавливаем таблицу как центральный виджет
        central_widget = QWidget()
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        # Панель поиска
        search_widget = QWidget()
        search_layout = QHBoxLayout(search_widget)
        search_layout.addWidget(QLabel("Поиск:"))
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Поиск по всем полям...")
        self.search_input.textChanged.connect(self.update_table)
        search_layout.addWidget(self.search_input)
        
        main_layout.addWidget(search_widget)
        main_layout.addWidget(self.table)
        
        self.setCentralWidget(central_widget)
        
        # Создаем тулбар
        self.create_toolbar()
        
        # Создаем меню
        self.create_menu()
        
        # Статус бар
        self.status_bar = self.statusBar()
        self.status_bar.showMessage("Готово к работе")
        
        # Добавляем несколько тестовых записей для проверки
        print("Инициализация базы данных...")
        print(f"Количество студентов в базе: {len(self.db.students)}")
        
        # Обновляем таблицу
        self.update_table()
        
        print("Главное окно инициализировано")

    def create_menu(self):
        """Создание меню"""
        menubar = self.menuBar()
        
        # Меню Файл
        file_menu = menubar.addMenu("Файл")
        file_menu.addAction("Создать", self.new_db)
        file_menu.addAction("Открыть", self.load_db)
        file_menu.addAction("Сохранить", self.save_db)
        file_menu.addAction("Сохранить как", self.save_as_db)
        file_menu.addSeparator()
        file_menu.addAction("Выход", self.close)
        
        # Меню Действия
        action_menu = menubar.addMenu("Действия")
        action_menu.addAction("Добавить студента", self.add_student)
        action_menu.addAction("Редактировать студента", self.edit_student)
        action_menu.addAction("Удалить студента", self.delete_student)

    def create_toolbar(self):
        """Создание панели инструментов"""
        toolbar = self.addToolBar("Инструменты")
        
        # Добавляем кнопки на тулбар
        toolbar.addAction("➕ Добавить", self.add_student)
        toolbar.addAction("✏️ Редактировать", self.edit_student)
        toolbar.addAction("🗑️ Удалить", self.delete_student)
        toolbar.addSeparator()
        toolbar.addAction("💾 Сохранить", self.save_db)
        toolbar.addAction("📂 Открыть", self.load_db)
        toolbar.addAction("🆕 Новая БД", self.new_db)

    def update_table(self):
        """Обновление таблицы с данными студентов"""
        try:
            print("Обновление таблицы...")
            
            # Получаем текст для поиска
            search_text = self.search_input.text().strip().lower()
            print(f"Текст поиска: '{search_text}'")
            
            # Получаем всех студентов из базы
            all_students = []
            for i in range(len(self.db.students)):
                all_students.append(self.db.students[i])
            
            print(f"Всего студентов в базе: {len(all_students)}")
            
            # Фильтруем студентов по поисковому запросу
            filtered_students = []
            if search_text:
                for student in all_students:
                    # Проверяем все поля студента на совпадение
                    student_data = [
                        str(student.student_id).lower(),
                        student.surname.lower(),
                        student.name.lower(),
                        student.group.lower(),
                        str(student.age).lower(),
                        str(student.avg_score).lower()
                    ]
                    
                    # Если хотя бы одно поле содержит поисковый запрос
                    if any(search_text in field for field in student_data):
                        filtered_students.append(student)
            else:
                filtered_students = all_students
            
            print(f"Отфильтровано студентов: {len(filtered_students)}")
            
            # Устанавливаем количество строк в таблице
            self.table.setRowCount(len(filtered_students))
            
            # Заполняем таблицу данными
            for row_index, student in enumerate(filtered_students):
                # Столбец 0: ID
                id_item = QTableWidgetItem(str(student.student_id))
                id_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.table.setItem(row_index, 0, id_item)
                
                # Столбец 1: Фамилия
                surname_item = QTableWidgetItem(student.surname)
                self.table.setItem(row_index, 1, surname_item)
                
                # Столбец 2: Имя
                name_item = QTableWidgetItem(student.name)
                self.table.setItem(row_index, 2, name_item)
                
                # Столбец 3: Группа
                group_item = QTableWidgetItem(student.group)
                self.table.setItem(row_index, 3, group_item)
                
                # Столбец 4: Возраст
                age_item = QTableWidgetItem(str(student.age))
                age_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.table.setItem(row_index, 4, age_item)
                
                # Столбец 5: Средний балл
                avg_item = QTableWidgetItem(str(student.avg_score))
                avg_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.table.setItem(row_index, 5, avg_item)
            
            # Обновляем статус бар
            self.status_bar.showMessage(
                f"Записей в базе: {len(all_students)} | " +
                f"Отображено: {len(filtered_students)} | " +
                f"Изменения: {'Да' if self.db.modified else 'Нет'}"
            )
            
            print("Таблица обновлена успешно")
            
        except Exception as e:
            print(f"Ошибка при обновлении таблицы: {e}")
            import traceback
            traceback.print_exc()
            self.status_bar.showMessage(f"Ошибка: {str(e)}")

    def add_student(self):
        """Добавление нового студента"""
        print("Нажата кнопка 'Добавить'")
        
        try:
            # Создаем диалог для добавления студента
            dialog = StudentDialog(self)
            print("Диалог создан")
            
            # Показываем диалог и ждем результат
            result = dialog.exec()
            print(f"Результат диалога: {result}")
            
            if result == QDialog.DialogCode.Accepted:
                # Получаем данные из диалога
                data = dialog.get_data()
                print(f"Получены данные из диалога: {data}")
                
                if data:
                    # Добавляем студента в базу данных
                    print("Добавляем студента в базу...")
                    self.db.add_student(data)
                    print(f"Студент добавлен. Всего студентов: {len(self.db.students)}")
                    
                    # Обновляем таблицу
                    self.update_table()
                    
                    # Показываем сообщение об успехе
                    QMessageBox.information(
                        self, 
                        "Успех", 
                        f"Студент {data[1]} {data[2]} успешно добавлен!"
                    )
                else:
                    print("Данные не получены из диалога")
                    QMessageBox.warning(self, "Ошибка", "Не удалось получить данные студента")
            else:
                print("Диалог отменен пользователем")
                
        except Exception as e:
            print(f"Ошибка при добавлении студента: {e}")
            import traceback
            traceback.print_exc()
            QMessageBox.critical(self, "Ошибка", f"Не удалось добавить студента: {str(e)}")

    def edit_student(self):
        """Редактирование выбранного студента"""
        print("Нажата кнопка 'Редактировать'")
        
        # Получаем выбранную строку
        selected_row = self.table.currentRow()
        print(f"Выбранная строка: {selected_row}")
        
        if selected_row < 0:
            QMessageBox.warning(self, "Ошибка", "Выберите студента для редактирования")
            return
        
        try:
            # Получаем ID студента из выбранной строки
            id_item = self.table.item(selected_row, 0)
            if not id_item:
                QMessageBox.warning(self, "Ошибка", "Не удалось получить ID студента")
                return
            
            student_id = id_item.text()
            print(f"ID студента для редактирования: {student_id}")
            
            # Ищем студента в базе данных
            student_to_edit = None
            for i in range(len(self.db.students)):
                student = self.db.students[i]
                if str(student.student_id) == student_id:
                    student_to_edit = student
                    break
            
            if not student_to_edit:
                QMessageBox.warning(self, "Ошибка", "Студент не найден в базе данных")
                return
            
            print(f"Найден студент: {student_to_edit.surname} {student_to_edit.name}")
            
            # Создаем диалог редактирования с данными студента
            dialog = StudentDialog(self, student_to_edit)
            print("Диалог редактирования создан")
            
            # Показываем диалог
            result = dialog.exec()
            print(f"Результат диалога редактирования: {result}")
            
            if result == QDialog.DialogCode.Accepted:
                # Получаем обновленные данные
                new_data = dialog.get_data()
                print(f"Получены обновленные данные: {new_data}")
                
                if new_data:
                    # Обновляем студента в базе данных
                    for i in range(len(self.db.students)):
                        student = self.db.students[i]
                        if str(student.student_id) == new_data[0]:
                            # Обновляем данные студента
                            self.db.students[i] = Student(*new_data)
                            self.db.modified = True
                            print(f"Студент с ID {new_data[0]} обновлен")
                            break
                    
                    # Обновляем таблицу
                    self.update_table()
                    
                    # Сообщение об успехе
                    QMessageBox.information(
                        self,
                        "Успех",
                        f"Данные студента {new_data[1]} {new_data[2]} успешно обновлены!"
                    )
                    
        except Exception as e:
            print(f"Ошибка при редактировании студента: {e}")
            import traceback
            traceback.print_exc()
            QMessageBox.critical(self, "Ошибка", f"Не удалось отредактировать студента: {str(e)}")

    def delete_student(self):
        """Удаление выбранного студента"""
        print("Нажата кнопка 'Удалить'")
        
        # Получаем выбранную строку
        selected_row = self.table.currentRow()
        print(f"Выбранная строка для удаления: {selected_row}")
        
        if selected_row < 0:
            QMessageBox.warning(self, "Ошибка", "Выберите студента для удаления")
            return
        
        try:
            # Получаем ID студента из таблицы
            id_item = self.table.item(selected_row, 0)
            if not id_item:
                QMessageBox.warning(self, "Ошибка", "Не удалось получить ID студента")
                return
            
            student_id = id_item.text()
            print(f"ID студента для удаления: {student_id}")
            
            # Получаем имя студента для подтверждения
            surname_item = self.table.item(selected_row, 1)
            name_item = self.table.item(selected_row, 2)
            student_name = f"{surname_item.text()} {name_item.text()}" if surname_item and name_item else "студента"
            
            # Запрос подтверждения
            reply = QMessageBox.question(
                self,
                "Подтверждение удаления",
                f"Вы уверены, что хотите удалить {student_name} (ID: {student_id})?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No
            )
            
            if reply == QMessageBox.StandardButton.Yes:
                print("Пользователь подтвердил удаление")
                
                # Ищем и удаляем студента из базы данных
                for i in range(len(self.db.students)):
                    student = self.db.students[i]
                    if str(student.student_id) == student_id:
                        self.db.remove_student(i)
                        print(f"Студент с ID {student_id} удален")
                        break
                
                # Обновляем таблицу
                self.update_table()
                
                # Сообщение об успехе
                self.status_bar.showMessage(f"Студент {student_name} удален")
                print("Студент успешно удален")
                
        except Exception as e:
            print(f"Ошибка при удалении студента: {e}")
            import traceback
            traceback.print_exc()
            QMessageBox.critical(self, "Ошибка", f"Не удалось удалить студента: {str(e)}")

    def new_db(self):
        """Создание новой базы данных"""
        print("Создание новой базы данных")
        
        # Проверяем, есть ли несохраненные изменения
        if self.db.modified and len(self.db.students) > 0:
            reply = QMessageBox.question(
                self,
                "Несохраненные изменения",
                "Есть несохраненные изменения. Создать новую базу без сохранения?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No
            )
            
            if reply != QMessageBox.StandardButton.Yes:
                return
        
        # Очищаем базу данных
        self.db.clear()
        self.current_file = None
        self.search_input.clear()
        
        # Обновляем таблицу
        self.update_table()
        
        self.status_bar.showMessage("Новая база данных создана")
        QMessageBox.information(self, "Успех", "Новая база данных создана")
        print("Новая база данных создана")

    def save_db(self):
        """Сохранение базы данных"""
        print("Сохранение базы данных")
        
        if self.current_file:
            try:
                if self.db.save(self.current_file):
                    self.status_bar.showMessage(f"База данных сохранена: {self.current_file}")
                    QMessageBox.information(self, "Успех", "База данных успешно сохранена")
                    print(f"База данных сохранена в {self.current_file}")
                else:
                    QMessageBox.warning(self, "Ошибка", "Не удалось сохранить базу данных")
            except Exception as e:
                print(f"Ошибка при сохранении: {e}")
                QMessageBox.critical(self, "Ошибка", f"Ошибка при сохранении: {str(e)}")
        else:
            self.save_as_db()

    def save_as_db(self):
        """Сохранение базы данных под новым именем"""
        print("Сохранение базы данных как...")
        
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Сохранить базу данных",
            "",
            "JSON файлы (*.json);;Все файлы (*)"
        )
        
        if file_path:
            # Добавляем расширение .json если его нет
            if not file_path.lower().endswith('.json'):
                file_path += '.json'
            
            self.current_file = file_path
            self.save_db()

    def load_db(self):
        """Загрузка базы данных из файла"""
        print("Загрузка базы данных")
        
        # Проверяем, есть ли несохраненные изменения
        if self.db.modified and len(self.db.students) > 0:
            reply = QMessageBox.question(
                self,
                "Несохраненные изменения",
                "Есть несохраненные изменения. Загрузить новую базу без сохранения?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No
            )
            
            if reply != QMessageBox.StandardButton.Yes:
                return
        
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Открыть базу данных",
            "",
            "JSON файлы (*.json);;Все файлы (*)"
        )
        
        if file_path:
            try:
                if self.db.load(file_path):
                    self.current_file = file_path
                    self.search_input.clear()
                    self.update_table()
                    
                    self.status_bar.showMessage(f"База данных загружена: {file_path}")
                    QMessageBox.information(
                        self,
                        "Успех",
                        f"База данных успешно загружена. Загружено {len(self.db.students)} записей."
                    )
                    print(f"База данных загружена из {file_path}")
                else:
                    QMessageBox.warning(self, "Ошибка", "Не удалось загрузить базу данных")
            except Exception as e:
                print(f"Ошибка при загрузке: {e}")
                QMessageBox.critical(self, "Ошибка", f"Ошибка при загрузке: {str(e)}")

    def closeEvent(self, event):
        """Обработка закрытия окна"""
        if self.db.modified:
            reply = QMessageBox.question(
                self,
                "Несохраненные изменения",
                "Есть несохраненные изменения. Выйти без сохранения?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No
            )
            
            if reply != QMessageBox.StandardButton.Yes:
                event.ignore()
                return
        
        print("Приложение закрывается")
        event.accept()
    def create_menu(self):
        """Создание меню"""
        menubar = self.menuBar()
        
        # Меню Файл
        file_menu = menubar.addMenu("Файл")
        file_menu.addAction("Создать", self.new_db)
        file_menu.addAction("Открыть", self.load_db)
        file_menu.addAction("Сохранить", self.save_db)
        file_menu.addAction("Сохранить как", self.save_as_db)
        file_menu.addAction("Объединить с...", self.merge_db)  # НОВОЕ
        file_menu.addSeparator()
        file_menu.addAction("Выход", self.close)
        
        # Меню Действия
        action_menu = menubar.addMenu("Действия")
        action_menu.addAction("Добавить студента", self.add_student)
        action_menu.addAction("Редактировать студента", self.edit_student)
        action_menu.addAction("Удалить студента", self.delete_student)

    def create_toolbar(self):
        """Создание панели инструментов"""
        toolbar = self.addToolBar("Инструменты")
        
        # Добавляем кнопки на тулбар
        toolbar.addAction("➕ Добавить", self.add_student)
        toolbar.addAction("✏️ Редактировать", self.edit_student)
        toolbar.addAction("🗑️ Удалить", self.delete_student)
        toolbar.addSeparator()
        toolbar.addAction("💾 Сохранить", self.save_db)
        toolbar.addAction("📂 Открыть", self.load_db)
        toolbar.addAction("🔄 Объединить", self.merge_db)  # НОВОЕ
        toolbar.addAction("🆕 Новая БД", self.new_db)
    def merge_db(self):
        """Объединение текущей базы данных с другой"""
        print("Начало объединения баз данных...")
        
        # Проверяем, есть ли студенты в текущей базе
        if len(self.db.students) == 0:
            reply = QMessageBox.question(
                self,
                "Пустая база данных",
                "Текущая база данных пуста. Хотите просто загрузить другую базу?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No
            )
            
            if reply == QMessageBox.StandardButton.Yes:
                self.load_db()
                return
        
        # Открываем диалог выбора файла для объединения
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Выберите базу данных для объединения",
            "",
            "JSON файлы (*.json);;Все файлы (*)"
        )
        
        if not file_path:
            print("Объединение отменено: файл не выбран")
            return
        
        try:
            # Создаем временную базу данных для загрузки другой БД
            temp_db = StudentDataBase()
            
            # Загружаем данные из выбранного файла
            if not temp_db.load(file_path):
                QMessageBox.warning(self, "Ошибка", f"Не удалось загрузить базу данных из файла: {file_path}")
                return
            
            print(f"Загружено {len(temp_db.students)} записей из файла {file_path}")
            
            if len(temp_db.students) == 0:
                QMessageBox.information(self, "Информация", "Выбранная база данных пуста. Объединение не требуется.")
                return
            
            # Запрашиваем у пользователя стратегию объединения
            strategy = self.ask_merge_strategy()
            if strategy is None:
                print("Объединение отменено пользователем")
                return
            
            # Определяем количество записей до объединения
            before_merge = len(self.db.students)
            
            # Выполняем объединение
            added, updated, skipped = self.db.merge_with(temp_db, strategy)
            
            # Определяем количество записей после объединения
            after_merge = len(self.db.students)
            
            # Обновляем таблицу
            self.update_table()
            
            # Показываем результаты
            result_message = (
                f"Объединение завершено!\n\n"
                f"Исходное количество записей: {before_merge}\n"
                f"Записей для объединения: {len(temp_db.students)}\n"
                f"Добавлено новых: {added}\n"
                f"Обновлено существующих: {updated}\n"
                f"Пропущено: {skipped}\n"
                f"Итоговое количество записей: {after_merge}"
            )
            
            self.status_bar.showMessage(f"Базы объединены. Добавлено: {added}, Обновлено: {updated}")
            QMessageBox.information(self, "Результат объединения", result_message)
            
            print(f"Объединение завершено. Добавлено: {added}, Обновлено: {updated}, Пропущено: {skipped}")
            
        except Exception as e:
            print(f"Ошибка при объединении баз данных: {e}")
            import traceback
            traceback.print_exc()
            QMessageBox.critical(self, "Ошибка", f"Не удалось объединить базы данных: {str(e)}")

    def ask_merge_strategy(self):
        """Запрашивает у пользователя стратегию объединения"""
        dialog = QDialog(self)
        dialog.setWindowTitle("Стратегия объединения")
        dialog.resize(400, 250)
        
        layout = QVBoxLayout(dialog)
        
        # Текст объяснения
        label = QLabel(
            "Выберите стратегию объединения записей с одинаковыми ID:\n\n"
            "1. <b>Заменить</b> - заменить существующие записи новыми\n"
            "2. <b>Пропустить</b> - сохранить существующие записи\n"
            "3. <b>Сохранить обе</b> - создать новые записи с уникальными ID"
        )
        label.setWordWrap(True)
        layout.addWidget(label)
        
        # Группа радиокнопок
        group_box = QGroupBox("Стратегия объединения")
        group_layout = QVBoxLayout()
        
        self.replace_radio = QRadioButton("Заменить существующие записи")
        self.skip_radio = QRadioButton("Пропустить существующие записи")
        self.both_radio = QRadioButton("Сохранить обе записи (создать новые ID)")
        
        # Устанавливаем значение по умолчанию
        self.replace_radio.setChecked(True)
        
        group_layout.addWidget(self.replace_radio)
        group_layout.addWidget(self.skip_radio)
        group_layout.addWidget(self.both_radio)
        group_box.setLayout(group_layout)
        layout.addWidget(group_box)
        
        # Кнопки
        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        button_box.accepted.connect(dialog.accept)
        button_box.rejected.connect(dialog.reject)
        layout.addWidget(button_box)
        
        # Показываем диалог
        result = dialog.exec()
        
        if result == QDialog.DialogCode.Accepted:
            if self.replace_radio.isChecked():
                return "replace"
            elif self.skip_radio.isChecked():
                return "skip"
            elif self.both_radio.isChecked():
                return "both"
        
        return None

if __name__ == "__main__":
    print("Запуск приложения...")
    
    app = QApplication(sys.argv)
    
    # Устанавливаем стиль приложения
    app.setStyle("Fusion")
    
    window = MainWindow()
    window.show()
    
    print("Приложение запущено")
    
    sys.exit(app.exec())