from room import Room, Office, LivingSpace
from person import Fellow, Staff
from abc import abstractmethod
import random
import string
# from tabulate import tabulate


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

    # Check if room exists in the system

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
            return 'office', is_office[0]

        elif is_male_living_space:
            return 'male_living_space', is_male_living_space[0]

        elif is_female_living_space:
            return 'female_living_space', is_female_living_space[0]
        else:
            return False

    # check if person exists in the system

    def check_person(self, person_id):
        self.person_id = person_id

        is_staff = [
            staff[self.person_id] for staff in self.staffs if self.person_id in staff]

        is_fellow = [
            fellow[self.person_id] for fellow in amity.fellows if self.person_id in fellow]

        if is_staff:
            return 'staff', is_staff[0]

        elif is_fellow:
            return 'fellow', is_fellow[0]

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

                person_type, person_obj = self.check_person(self.person_id)
                room_type, room_obj = self.check_room(self.room_name)
                print(person_obj)

                if person_type in ('fellow', 'staff') and room_type == 'office':
                    # check if the office is vacant
                    if room_obj.is_vacant():
                        room_obj.add_occupant(person_obj)
                        print('person reallocated successfully')

                    else:
                        print('person cannot be reallocated to {}. Its not vacant'.format(
                            self.room_name))

                elif person_type == 'fellow' and room_type in ('male_living_space', 'female_living_space'):
                    # check if the livingspace is vacant
                    if room_obj.is_vacant():
                        # check if person is male or female
                        if person_obj.gender == 'male' and room_type == 'male_living_space':
                            room_obj.add_occupant(person_obj)
                            print('male fellow reallocated successfully')

                        elif person_obj.gender == 'female' and room_type == 'female_living_space':
                            room_obj.add_occupant(person_obj)
                            print('female reallocated successfully')

                        elif person_obj.gender == 'male' and room_type == 'female_living_space':
                            print(
                                'male fellow cannot be reallocated to female livingspace')

                        elif person_obj.gender == 'female' and room_type == 'male_living_space':
                            print(
                                'female fellow cannot be reallocated to male livingspace')

                    else:
                        print('person cannot be reallocated to {}. Its not vacant'.format(
                            self.room_name))

                elif person_type == 'staff' and room_type in ('male_living_space', 'female_living_space'):
                    return 'Sorry staff cannot be reallocated to livingspace'

                elif person == False and room_type in ('office', 'male_living_space', 'female_living_space'):
                    return 'The person is not on the system'

                elif room == False and person_type in ('staff', 'fellow'):
                    return 'The room is not on the system'

            else:
                raise TypeError
        except TypeError:
            print('Inputs must be string')

    '''print room members'''

    def print_room(self, room_name):
        self.room_name = room_name

        if isinstance(self.room_name, str):

            if self.check_room(self.room_name) is False:
                print('The room does not exist')

            else:
                room_type, room_obj = self.check_room(self.room_name)

                if len(room_obj.occupants) == 0:
                    print('Room has no occupants')

                else:
                    print(self.room_name.upper())

                    for occupant in room_obj.occupants:
                        print('{} {}'.format(
                            occupant.first_name, occupant.last_name))
        else:
            raise TypeError
            print('only strings allowed')

    # PRINT ALL ROOMS WITH THE OCCUPANTS
    def print_allocations(self):
        # check if rooms have been added to the system
        if (len(self.offices) == 0 and len(self.living_spaces['female']) == 0
                and len(self.living_spaces['male']) == 0):

            print('currently there are no Rooms')

        elif (all(len(office.occupants) == 0 for office in self.offices) and
              all(len(living.occupants) == 0 for living in self.living_spaces['male']) and
              all(len(living.occupants) == 0 for living in self.living_spaces['female'])):

            print('All rooms are empty')

        else:

            # print all offices
            print('OFFICES')
            self.print_room_members('office')

            # print all male living spaces
            print('MALE LIVING SPACES')
            self.print_room_members('male')

            # print all female living spaces
            print('FEMALE LIVING SPACES')
            self.print_room_members('female')

    # print all room occupants
    def print_room_members(self, room_type):
        self.room_type = room_type
        room_type_list = []

        if self.room_type == 'office':
            room_type_list = self.offices

        elif self.room_type == 'male':
            room_type_list = self.living_spaces['male']

        elif self.room_type == 'male':
            room_type_list = self.living_spaces['female']

        else:
            return False

        rooms_with_occupants = [
            room for room in room_type_list if len(room.occupants) > 0]

        for room in rooms_with_occupants:
            print(room.name.upper())

            for occupant in room.occupants:
                print('{} {}'.format(occupant.first_name, occupant.last_name))


amity = Amity()
# amity.create_room(['Nania office', 'Oculus office',
#                    'Peri livingspace male', 'React livingspace female'])

# amity.add_person('Ian', 'Oti', 'male', 'fellow', 'Y')
# amity.add_person('Arya', 'Stark', 'female', 'fellow', 'Y')
# amity.add_person('saya', 'jack', 'male', 'staff')
# print(amity.offices)
# print(amity.offices[0].occupants)
amity.print_allocations()
