import json
from student import Student
from myvector import MyVector


class StudentDataBase:
    def __init__(self):
        """Инициализация базы данных"""
        self.students = MyVector()  # Используем кастомный вектор
        self.modified = False
        print("База данных инициализирована")
    
    def add_student(self, data):
        """Добавление нового студента
        
        Args:
            data: список [id, surname, name, group, age, avg_score]
        """
        try:
            # Если ID None, заменяем его на 0
            if data[0] is None:
                data = list(data)
                data[0] = 0
            
            # Создаем объект Student из данных
            student = Student(*data)
            
            # Находим максимальный ID
            max_id = 0
            for existing_student in self.students:
                if existing_student.student_id > max_id:
                    max_id = existing_student.student_id
            
            # Если ID студента 0 или уже существует, генерируем новый
            if student.student_id == 0 or any(s.student_id == student.student_id for s in self.students):
                student.student_id = max_id + 1
            
            # Добавляем студента в вектор
            self.students.append(student)
            self.modified = True
            
            print(f"Студент добавлен: {student.surname} {student.name} (ID: {student.student_id})")
            return True
            
        except Exception as e:
            print(f"Ошибка при добавлении студента: {e}")
            return False
    
    def remove_student(self, index):
        """Удаление студента по индексу"""
        try:
            if 0 <= index < len(self.students):
                student = self.students[index]
                print(f"Удаление студента: {student.surname} {student.name} (ID: {student.student_id})")
                self.students.remove_at(index)
                self.modified = True
                return True
            return False
        except Exception as e:
            print(f"Ошибка при удалении студента: {e}")
            return False
    
    def clear(self):
        """Очистка базы данных"""
        self.students.clear()
        self.modified = False
        print("База данных очищена")
    
    def save(self, filename):
        """Сохранение базы данных в файл"""
        try:
            print(f"Сохранение базы данных в файл: {filename}")
            
            # Преобразуем студентов в список словарей
            data = []
            for student in self.students:
                data.append({
                    'id': student.student_id,
                    'surname': student.surname,
                    'name': student.name,
                    'group': student.group,
                    'age': student.age,
                    'avg_score': student.avg_score
                })
            
            # Сохраняем в JSON файл
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            self.modified = False
            print(f"База данных успешно сохранена. Записей: {len(data)}")
            return True
            
        except Exception as e:
            print(f"Ошибка при сохранении базы данных: {e}")
            return False
    
    def load(self, filename):
        """Загрузка базы данных из файла"""
        try:
            print(f"Загрузка базы данных из файла: {filename}")
            
            # Читаем данные из файла
            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Очищаем текущие данные
            self.clear()
            
            # Загружаем студентов
            for item in data:
                student = Student(
                    item['id'],
                    item['surname'],
                    item['name'],
                    item['group'],
                    item['age'],
                    item['avg_score']
                )
                self.students.append(student)
            
            self.modified = False
            print(f"База данных успешно загружена. Записей: {len(self.students)}")
            return True
            
        except Exception as e:
            print(f"Ошибка при загрузке базы данных: {e}")
            return False

    def merge_with(self, other_db, strategy="replace"):
        """
        Объединяет текущую базу данных с другой
        
        Args:
            other_db: другая база данных StudentDataBase
            strategy: стратегия объединения:
                - "replace": заменить существующие записи
                - "skip": пропустить существующие записи
                - "both": сохранить обе (создать новые ID)
        
        Returns:
            tuple: (добавлено, обновлено, пропущено)
        """
        try:
            print(f"Начало объединения с стратегией: {strategy}")
            added = 0
            updated = 0
            skipped = 0
            
            # Находим максимальный ID в текущей базе
            max_id = 0
            for student in self.students:
                if student.student_id > max_id:
                    max_id = student.student_id
            
            print(f"Максимальный ID в текущей базе: {max_id}")
            print(f"Записей в объединяемой базе: {len(other_db.students)}")
            
            for other_student in other_db.students:
                # Ищем студента с таким же ID в текущей базе
                found = False
                found_index = -1
                
                for i, student in enumerate(self.students):
                    if student.student_id == other_student.student_id:
                        found = True
                        found_index = i
                        break
                
                if found:
                    # Студент с таким ID уже существует
                    print(f"Найден дубликат ID {other_student.student_id}: {other_student.surname} {other_student.name}")
                    
                    if strategy == "replace":
                        # Заменяем существующую запись
                        self.students[found_index] = other_student
                        updated += 1
                        self.modified = True
                        print(f"  → Запись заменена")
                    elif strategy == "skip":
                        # Пропускаем
                        skipped += 1
                        print(f"  → Запись пропущена")
                    elif strategy == "both":
                        # Создаем новую запись с уникальным ID
                        new_id = max_id + 1
                        max_id = new_id
                        new_student = Student(
                            new_id,
                            other_student.surname,
                            other_student.name,
                            other_student.group,
                            other_student.age,
                            other_student.avg_score
                        )
                        self.students.append(new_student)
                        added += 1
                        self.modified = True
                        print(f"  → Создана новая запись с ID {new_id}")
                else:
                    # Студент с таким ID не найден - просто добавляем
                    self.students.append(other_student)
                    added += 1
                    self.modified = True
                    print(f"Добавлен студент ID {other_student.student_id}: {other_student.surname} {other_student.name}")
            
            print(f"Объединение завершено. Добавлено: {added}, Обновлено: {updated}, Пропущено: {skipped}")
            return added, updated, skipped
            
        except Exception as e:
            print(f"Ошибка при объединении баз данных: {e}")
            import traceback
            traceback.print_exc()
            return 0, 0, 0

    def __str__(self):
        """Строковое представление базы данных"""
        result = f"База данных студентов ({len(self.students)} записей):\n"
        for student in self.students:
            result += f"  ID: {student.student_id}, {student.surname} {student.name}, Группа: {student.group}\n"
        return result