from room import Room, Office, LivingSpace
from person import Fellow, Staff
from abc import abstractmethod
import random
import string


class Amity(object):
    """docstring for Amity."""

    def __init__(self):
        self.staffs = []
        self.fellows = []
        self.fellows_unallocated_living_space = []
        self.andelans_unallocated_offices = []
        self.offices = []
        self.living_spaces = {'female': [], 'male': []}
        self.set_of_ids = set()

    # create room and add to the list of rooms
    def create_room(self, rooms):
        self.rooms = rooms
        error_list = []
        room_type_error = {'room_type': [], 'living_type': []}

        for room in self.rooms:
            if len(room.split()) <= 1:
                error_list.append(room)

            elif len(room.split()) == 2:

                if all(details.isalpha() for details in room.split()):
                    room_name, room_type = room.split()

                    if room_type.lower() in ('livingspace', 'l'):

                        room_type_error['living_type'].append(room_type)
                        error_list.append(room_type_error)

                    elif room_type.lower() in ('office', 'o'):
                        office = Office(room_name.lower())
                        self.offices.append(office)

                    else:
                        room_type_error['room_type'].append(room_type)
                        error_list.append(room_type_error)

                else:
                    error_list.append(room)

            elif len(room.split()) == 3:
                room_name, room_type, living_type = room.split()

                if all(details.isalpha() for details in room.split()):
                    if room_type.lower() in ('office', 'o'):
                        office = Office(room_name.lower())
                        self.offices.append(office)

                    elif room_type.lower() in ('livingspace', 'l'):
                        living = LivingSpace(room_name.lower())

                        if living_type.lower() in ('male', 'm'):
                            self.living_spaces['male'].append(living)

                        elif living_type.lower() in ('female', 'f'):
                            self.living_spaces['female'].append(living)

                        else:
                            room_type_error['living_type'].append(room_type)
                    else:
                        error_list.append(room)

        print('{} is not a string'.format(error_list))

    # Method to add person to the system and allocate room
    def add_person(self, first_name, last_name, gender, person_type, accommodation='No'):

        self.first_name = first_name
        self.last_name = last_name
        self.person_type = person_type
        self.gender = gender
        self.accommodation = accommodation

        person_details = [self.first_name, self.last_name,
                          self.gender, self.person_type, self.accommodation]

        try:

            if all(isinstance(details, str) for details in person_details):
                # check for null values or digits
                if all(details.isalpha() for details in person_details):

                    if self.person_type.lower() == 'fellow':
                        fellow = Fellow(self.first_name,
                                        self.last_name, self.gender)

                        self.fellows.append({self.generate_id(): fellow})

                        # allocate  fellow livingspace if he/she needs
                        if self.accommodation.lower() in ('y', 'yes'):
                            self.allocate(fellow, accommodation='Yes')

                        elif self.accommodation.lower() in ('n', 'no'):
                            self.allocate(fellow, accommodation='No')

                        else:
                            print('Invalid option. Either Yes or No')

                    elif self.person_type.lower() == 'staff':
                        staff = Staff(self.first_name,
                                      self.last_name, self.gender)

                        self.staffs.append({self.generate_id(): staff})
                        self.allocate(staff, accommodation='No')

                    else:
                        print('Sorry person must be either Staff or Fellow')
                else:
                    print('Null values or digits not accepted')
            else:
                raise TypeError

        except TypeError:
            print("All values must be characters.")

    # Room allocation method.
    def allocate(self, person_type, accommodation='No'):
        self.person_type = person_type
        self.accommodation = accommodation

        # allocate random office to both fellow and staff
        if len(self.offices) == 0:
            self.andelans_unallocated_offices.append(self.person_type)
            return 'No office to allocate you currently.'

        elif any(office for office in self.offices if office.is_vacant()):
            for office in self.offices:
                random_office = random.choice(self.offices)
                if random_office.is_vacant() and not random_office.is_person_an_occupant(self.person_type):
                    random_office.add_occupant(self.person_type)
                    break

        else:
            self.andelans_unallocated_offices.append(self.person_type)
            return 'All offices are full.'

        # allocate random livingspace to fellow
        if isinstance(self.person_type, Fellow) and self.accommodation == 'Yes':

            if len(self.living_spaces['male']) == 0 and self.person_type.gender == 'male':
                self.fellows_unallocated_living_space.append(self.person_type)
                return 'No livingspace to allocate you currently.'

            if len(self.living_spaces['female']) == 0 and self.person_type.gender == 'female':
                self.fellows_unallocated_living_space.append(self.person_type)
                return 'No livingspace to allocate you currently.'

            elif any(living for living in self.living_spaces['male'] if living.is_vacant()):

                if self.person_type.gender == 'male':
                    for living in self.living_spaces['male']:
                        random_living_male = random.choice(
                            self.living_spaces['male'])
                        if random_living_male.is_vacant() and not random_living_male.is_fellow_an_occupant(self.person_type):
                            random_living_male.add_occupant(self.person_type)
                            break

            elif any(living for living in self.living_spaces['female'] if living.is_vacant()):

                if self.person_type.gender == 'female':
                    for living in self.living_spaces['female']:
                        random_living_female = random.choice(
                            self.living_spaces['female'])
                        if random_living_female.is_vacant() and not random_living_female.is_fellow_an_occupant(self.person_type):
                            random_living_female.add_occupant(self.person_type)
                            break

            else:
                self.fellows_unallocated_living_space.append(self.person_type)
                return 'All livingspaces are full.'

    # generate unique id for each Andelan
    def generate_id(self):

        chars = string.ascii_uppercase + string.digits

        andelan_id = ''.join(random.choice(chars) for i in range(4))

        #["{0:03}".format(i) for i in range(121)]

        # check if the id is unique
        while andelan_id not in self.set_of_ids:
            return andelan_id

    '''check if room exists in the system'''

    def check_room(self, room_name):
        self.room_name = room_name
        # check if room exits in offices
        is_office = [
            office for office in amity.offices if self.room_name.lower() in office.name]

        is_male_living_space = [
            living for living in self.living_spaces['male'] if self.room_name.lower() in living.name]

        is_female_living_space = [
            living for living in self.living_spaces['female'] if self.room_name.lower() in living.name]

        if is_office:
            return {'office': is_office}
        elif is_male_living_space:
            return {'male_living_space': is_male_living_space[0]}
        elif is_female_living_space:
            return {'female_living_space': is_female_living_space[0]}
        else:
            return False

    '''check if person exists in the system'''

    def check_person(self, person_id):
        self.person_id = person_id

        is_staff = [
            staff[self.person_id] for staff in self.staffs if self.person_id in staff]

        is_fellow = [
            fellow[self.person_id] for fellow in amity.fellows if self.person_id in fellow]

        if is_staff:
            return {'staff': is_staff[0]}
        elif is_fellow:
            return {'fellow': is_fellow[0]}
        else:
            return False

    '''Realloctes a person from one room to another'''

    def reallocate_person(self, person_id, room_name):
        self.person_id = person_id
        self.room_name = room_name

        # check if both params are correct
        try:
            if isinstance(self.person_id, str) and isinstance(self.room_name, str):
                # check if person and room exists
                person = self.check_person(self.person_id)
                room = self.check_room(self.room_name)

                if person.keys()[0] in ('fellow', 'staff') and room.keys()[0] == 'office':
                    # check if the office is vacant
                    if room['office'][0].is_vacant():
                        room['office'][0].add_occupant(person['fellow'][0])
                    else:
                        print('person cannot be reallocated to {}. Its not vacant'.format(
                            self.room_name))

                elif person.keys()[0] == 'fellow' and room.keys()[0] in ('male_living_space', 'female_living_space'):
                    # check if the livingspace is vacant
                    if room['male_living_space'][0].is_vacant():
                        # check if person is male or female
                        if person['fellow'].gender == 'male':
                            room['male_living_space'][0].add_occupant(
                                person['fellow'][0])

                        elif person['fellow'][0].gender == 'female':
                            room['female_living_space'].add_occupant(
                                person['fellow'][0])
                    else:
                        print('person cannot be reallocated to {}. Its not vacant'.format(
                            self.room_name))

                elif person.keys()[0] == 'staff' and room.keys()[0] in ('male_living_space', 'female_living_space'):
                    return 'Sorry staff cannot be reallocated to livingspace'

                elif person == False and room.keys()[0] in ('office', 'male_living_space', 'female_living_space'):
                    return 'The person is not on the system'

                elif room == False and person.keys()[0] in ('staff', 'fellow'):
                    return 'The room is not on the system'

            else:
                raise TypeError
        except TypeError:
            print('Inputs must be string')
