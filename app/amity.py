from app.room import Room, Office, LivingSpace
from app.person import Fellow, Staff
from abc import abstractmethod
from random import choice, randint
from string import digits, ascii_lowercase

class Amity(object):
    """docstring for Amity."""
    def __init__(self):
        self.offices = []
        self.living_spaces = []
        self.staffs = {}
        self.fellows = {}
    # create room and add to the list of rooms
    # use randomness to create offices and LivingSpaces --immplement later
    def create_room(self, *room_names):
        self.room_names = room_names
        error_list = []
        # add each room to amity room list
        for name in self.room_names:
            if not isinstance(name, str):
                error_list.append(name)
            else:
                if randint(1, 100)%2 == 0:
                    office = Office(name)
                    self.offices.append(office)
                else:
                    livingspace = LivingSpace(name)
                    self.living_spaces.append(livingspace)
                    continue

        # there exists digits ouput error to user
        if error_list:
            print('{} is not a string'.format(error_list))
        else:
            pass

    # list all rooms by name
    def list_rooms(self):
        for office in self.offices:
            print(room.name)

    # add person to system
    def add_person(self, first_name, last_name, person_type, gender, accommodation='N'):
        self.first_name = first_name
        self.last_name = last_name
        self.person_type = person_type
        self.gender = gender
        self.accommodation = accommodation

        person_detail = [self.first_name, self.last_name, self.person_type, self.gender, self.accommodation]

        try:
            if all(isinstance(detail, str) for detail in person_detail):
                if self.person_type.upper() == 'FELLOW':
                    fellow = Fellow(self.first_name, self.last_name, self.gender)
                    self.fellows.append(fellow)
                    return fellow

                elif self.person_type.upper() == 'STAFF':
                    staff = Staff(self.first_name, self.last_name, self.gender)
                    self.staffs.append(staff)
                    return staff
            else:
                raise TypeError
        except TypeError:
            return 'Sorry.All inputs should be string'


    def reallocate_person(self):
        pass

    def load_people(self):
        pass

    def print_allocations(self):
        pass

    def print_unallocated(self):
        pass

    def save_state(self):
        pass

    def load_state(self):
        pass
