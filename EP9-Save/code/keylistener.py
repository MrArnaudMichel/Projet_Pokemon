class KeyListener:
    """
    KeyListener class to manage the keys
    """
    def __init__(self) -> None:
        """
        Initialize the keys list
        """
        self.keys: list[int] = []

    def add_key(self, key: int) -> None:
        """
        Add a key to the keys list
        :param key:
        :return:
        """
        if key not in self.keys:
            self.keys.append(key)

    def remove_key(self, key: int) -> None:
        """
        Remove a key from the keys list
        :param key:
        :return:
        """
        if key in self.keys:
            self.keys.remove(key)

    def key_pressed(self, key: int) -> bool:
        """
        Check if a key is pressed
        :param key:
        :return:
        """
        return key in self.keys

    def clear(self) -> None:
        """
        Clear the keys list
        :return:
        """
        self.keys.clear()
