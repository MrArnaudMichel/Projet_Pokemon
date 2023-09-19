class KeyListener:
    def __init__(self):
        self.keys: list[int] = []

    def add_key(self, key: int) -> None:
        if key not in self.keys:
            self.keys.append(key)

    def remove_key(self, key: int) -> None:
        if key in self.keys:
            self.keys.remove(key)

    def key_pressed(self, key: int) -> bool:
        return key in self.keys

    def clear(self) -> None:
        self.keys.clear()
