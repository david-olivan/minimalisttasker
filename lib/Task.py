class Task:
    def __init__(self, name: str, priority: int, the_id: int):
        self.name = name
        self.priority = priority
        self.the_id = the_id

    def __str__(self):
        return f"Task: {self.name} \tPriority: {self.priority}"

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name: str):
        self._name = name

    @property
    def priority(self):
        return self._priority

    @priority.setter
    def priority(self, priority: int):
        self._priority = priority

    @property
    def the_id(self):
        return self._the_id

    @the_id.setter
    def the_id(self, the_id: int):
        self._the_id = the_id
