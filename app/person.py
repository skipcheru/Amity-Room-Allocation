
""" Amity models"""


class Person(object):
    """docstring for Person."""

    def __init__(self, first_name, last_name, gender):
        self.first_name = first_name
        self.last_name = last_name
        self.gender = gender

    def __str__(self):
        return '{} {}'.format(self.first_name, self.last_name)


class Fellow(Person):
    """docstring for Fellow."""

    def __init__(self, *args, **kwargs):
        super(Fellow, self).__init__(*args, **kwargs)
        self.person_type = 'FELLOW'
        self.fellow_id = None

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        return False

    def __ne__(self, other):
        if isinstance(other, self.__class__):
            return not self.__eq__(other)
        return False

    @property
    def details(self):
        return '{} {}'.format(self.first_name, self.last_name)


class Staff(Person):
    """docstring for Staff."""

    def __init__(self, *args, **kwargs):
        super(Staff, self).__init__(*args, **kwargs)
        self.person_type = 'STAFF'
        self.staff_id = None

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        return False

    def __ne__(self, other):
        if isinstance(other, self.__class__):
            return not self.__eq__(other)
        return False
