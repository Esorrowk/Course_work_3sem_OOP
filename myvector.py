class MyVector:
    def __init__(self):
        self._data = []

    def push_back(self, value):
        self._data.append(value)

    def erase(self, index):
        if 0 <= index < len(self._data):
            del self._data[index]

    def clear(self):
        self._data.clear()

    def __len__(self):
        return len(self._data)

    def __getitem__(self, index):
        return self._data[index]

    def __setitem__(self, index, value):
        self._data[index] = value

    def __iter__(self):
        return iter(self._data)
    
    def __contains__(self, value):
        return value in self._data