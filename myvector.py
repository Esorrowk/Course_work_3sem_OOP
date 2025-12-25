class MyVector:
    """Пользовательский класс-вектор для хранения объектов"""
    
    def __init__(self):
        self.data = []
    
    def append(self, item):
        """Добавление элемента в конец вектора"""
        self.data.append(item)
    
    def remove_at(self, index):
        """Удаление элемента по индексу"""
        if 0 <= index < len(self.data):
            return self.data.pop(index)
        raise IndexError("Индекс вне диапазона")
    
    def clear(self):
        """Очистка вектора"""
        self.data.clear()
    
    def __len__(self):
        """Возвращает количество элементов"""
        return len(self.data)
    
    def __getitem__(self, index):
        """Получение элемента по индексу"""
        return self.data[index]
    
    def __setitem__(self, index, value):
        """Установка элемента по индексу"""
        self.data[index] = value
    
    def __iter__(self):
        """Итератор по элементам вектора"""
        return iter(self.data)
    
    def __str__(self):
        """Строковое представление"""
        return str(self.data)