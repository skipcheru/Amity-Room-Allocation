from app.room import Room, Office, LivingSpace
from app.person import Fellow, Staff
from abc import abstractmethod

class Amity(object):
    """docstring for Amity."""
    def __init__(self):
        self.rooms = []
        self.staff = []
        self.fellows = []
    # create room and add to the list of rooms
    # use randomness to create offices and LivingSpaces --immplement later
    def create_room(self, *args):
        self.args = args
        for arg in self.args:
            room = Room(arg)
            self.rooms.append(room)

    # rename room if entered incorrectly
    def rename_room(self, name, new_name):
        self.name = name
        self.new_name = new_name

        for room in self.rooms:
            if self.name == room.name:
                room.name = self.new_name

    # number of rooms in amity
    def no_of_rooms(self):
        return len(self.rooms)

    # add person to system
    def add_person(self, first_name, last_name, person_type, gender):
        self.first_name = first_name
        self.last_name = last_name
        self.person_type = person_type
        self.gender = gender

        if self.person_type == 'FELLOW':
            fellow = Fellow(self.first_name, self.last_name, self.gender)
            return fellow

        elif self.person_type == 'STAFF':
            staff = Staff(self.first_name, self.last_name, self.gender)
            return staff
