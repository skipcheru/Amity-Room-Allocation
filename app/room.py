from app.person import Fellow, Staff


class Room(object):

    def __init__(self, name):
        self.name = name
        self.occupants = []
        self.capacity = None

    # check if room is vacant
    def is_vacant(self):
        return len(self.occupants) != self.capacity

    def add_occupant(self, person):
        self.person = person
        # check if room is vacant and person is occupant before adding
        if not self.is_vacant() or self.is_occupant(self.person):
            return False
        # add person to list of occupants
        self.occupants.append(self.person)
        return True

    # remove person if reallocated to another room
    def remove_occupant(self, person):
        # check if occupant
        if self.is_occupant(person):
            self.occupants.remove(person)

    # check if person is occupant
    def is_occupant(self, person):
        occupant = [occupant for occupant in self.occupants if occupant == person]

        return occupant != []


class Office(Room):

    def __init__(self, *args, **kwargs):
        super(Office, self).__init__(*args, **kwargs)
        self.capacity = 6

    def __eq__(self, other):
        if isinstance(other, self):
            return self.__dict__ == other.__dict__
        return False


class LivingSpace(Room):

    def __init__(self, *args, **kwargs):
        super(LivingSpace, self).__init__(*args, **kwargs)
        self.capacity = 4
