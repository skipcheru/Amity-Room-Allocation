from abc import abstractmethod
from app.person import Fellow, Staff

class Room(object):
    """docstring for Room."""
    def __init__(self, name):
        self.name = name

    # to be implemented by all sub classes
    @abstractmethod
    def is_vacant(self):
        pass

class Office(Room):
    """docstring for Office."""
    def __init__(self, *args, **kwargs):
        super(Office, self).__init__(*args, **kwargs)
        self.capacity = 4
        self.occupants = []

    def __eq__(self, other):
        if isinstance(other, self):
            return self.__dict__ == other.__dict__
        return False

    def add_occupant(self, person):
        self.person = person
        # check if room is vacant
        if self.is_vacant():
            # check if person has already been allocated this room
            if self.is_person_an_occupant(self.person):
                return 'The person is an occupant of this rooom'
            else:
                self.occupants.append(self.person)
                return 'person added sucessfully'
        else:
            return 'Sorry! The office is Not Vacant'

    # remove fellow if reallocated to another room
    def remove_occupant(self, person):
        self.person = person
        # check if fellow is allocated this room
        if self.is_person_an_occupant(self.person):
            self.occupants.remove(self.person)
            return True
        else:
            return False

    # check if room is vacant
    def is_vacant(self):
        if len(self.occupants) is 4:
            return False
        else:
            return True

    def is_person_an_occupant(self, person):
        self.person = person
        office_occupant = [occupant for occupant in self.occupants if
                            occupant == self.person]
        #debug ...print(office_occupant)
        if not office_occupant:
            return False
        else:
            return True

class LivingSpace(Room):
    """docstring for Office."""
    def __init__(self, *args, **kwargs):
        super(LivingSpace, self).__init__(*args, **kwargs)
        self.capacity = 6
        self.occupants = []

    # allocate fellow living space
    def add_occupant(self, fellow):
        self.fellow = fellow
        try:
            if isinstance(self.fellow, Fellow):
                if self.is_vacant():
                    if self.is_fellow_an_occupant(self.fellow):
                        return 'fellow already an occupant'
                    else:
                        self.occupants.append(self.fellow)
                        return 'fellow allocated room sucessfully'
                else:
                    return 'room is full'

        except Exception as e:
            raise TypeError('type not fello')

    # remove fellow if reallocated to another room
    def remove_occupant(self, fellow):
        self.fellow = fellow
        # check if fellow is allocated this room
        if self.is_fellow_an_occupant:
            self.occupants.remove(self.fellow)
            return True
        else:
            return False

    # check if fellow is allocated LivingSpace
    def is_fellow_an_occupant(self, fellow):
        self.fellow = fellow
        try:
            if isinstance(self.fellow, Fellow):
                room_occupant = [occupant for occupant in self.occupants
                                 if occupant == self.fellow]
                #print(room_occupant)
                if not room_occupant:
                    return False
                else:
                    return True
        except Exception as e:
            raise TypeError("Type not fellow")

    # check if LivingSpace is vacant
    def is_vacant(self):
        if len(self.occupants) == 6:
            return False
        else:
            return True
