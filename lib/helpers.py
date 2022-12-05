"""A class for modelling tasks"""


class Task:
    """
    A class that contains the basic building blocks of a Task. Name, priority and an id.
    """

    def __init__(self, name: str, priority: int, the_id: int):
        self.name = name
        self.priority = priority
        self.the_id = the_id

    def __str__(self):
        return f"Task: {self.name} \tPriority: {self.priority}"

    @property
    def name(self) -> str:
        """
        :param self: The object
        :type self: Task
        :return: The name property
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name: str):
        """
        :param self: The object
        :type self: Task
        :param name: The name description of the task
        :type name: str
        """
        self._name = name

    @property
    def priority(self) -> int:
        """
        :param self: The object
        :type self: Task
        :return: The priority property
        :rtype: int
        """
        return self._priority

    @priority.setter
    def priority(self, priority: int):
        """
        :param self: The object
        :type self: Task
        :param name: The priority of the task
        :type name: int
        """
        self._priority = priority

    @property
    def the_id(self) -> int:
        """
        :param self: The object
        :type self: Task
        :return: The id property
        :rtype: int
        """
        return self._the_id

    @the_id.setter
    def the_id(self, the_id: int):
        """
        :param self: The object
        :type self: Task
        :param name: The priority of the task
        :type name: int
        """
        self._the_id = the_id
