import json
from myvector import MyVector
from student import Student

class StudentDataBase:
    def __init__(self):
        self.students = MyVector()
        self.modified = False

    def add_student(self, student_data):
        """Добавление студента - упрощенная версия"""
        print(f"DEBUG: add_student вызван с данными: {student_data}")
        
        # Генерируем ID если None
        if student_data[0] is None:
            # Находим максимальный ID
            max_id = 0
            for student in self.students:
                try:
                    sid = int(student.student_id)
                    if sid > max_id:
                        max_id = sid
                except:
                    continue
            new_id = str(max_id + 1)
        else:
            new_id = student_data[0]
        
        # Создаем студента
        student = Student(
            student_id=new_id,
            surname=student_data[1],
            name=student_data[2],
            group=student_data[3],
            age=student_data[4],
            avg_score=student_data[5]
        )
        
        # Добавляем в вектор
        self.students.push_back(student)
        self.modified = True
        
        print(f"DEBUG: Студент создан: {student}")
        print(f"DEBUG: Всего студентов: {len(self.students)}")

    def remove_student(self, index: int):
        if 0 <= index < len(self.students):
            self.students.erase(index)
            self.modified = True

    def clear(self):
        self.students.clear()
        self.modified = False

    def save(self, filename: str):
        try:
            data = []
            for student in self.students:
                data.append({
                    "ID": student.student_id,
                    "Фамилия": student.surname,
                    "Имя": student.name,
                    "Группа": student.group,
                    "Возраст": student.age,
                    "Средний балл": student.avg_score
                })
            
            with open(filename, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            self.modified = False
            return True
        except Exception as e:
            print(f"Ошибка сохранения: {e}")
            return False

    def load(self, filename: str):
        try:
            with open(filename, "r", encoding="utf-8") as f:
                data = json.load(f)
            
            self.students.clear()
            for item in data:
                student = Student(
                    student_id=item["ID"],
                    surname=item["Фамилия"],
                    name=item["Имя"],
                    group=item["Группа"],
                    age=item["Возраст"],
                    avg_score=item["Средний балл"]
                )
                self.students.push_back(student)
            
            self.modified = False
            return True
        except Exception as e:
            print(f"Ошибка загрузки: {e}")
            return False