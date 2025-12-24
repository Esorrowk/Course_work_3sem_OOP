class Student:
    def __init__(self, student_id, surname, name, group, age, avg_score):
        self.student_id = student_id
        self.surname = surname
        self.name = name
        self.group = group
        self.age = age
        self.avg_score = avg_score

    def to_dict(self):
        return {
            "ID": self.student_id,
            "Фамилия": self.surname,
            "Имя": self.name,
            "Группа": self.group,
            "Возраст": self.age,
            "Средний балл": self.avg_score
        }
    
    def __str__(self):
        return f"{self.student_id}: {self.surname} {self.name}, {self.group}"
    
    def __repr__(self):
        return f"Student({self.student_id}, {self.surname}, {self.name})"