from app.room import Room, Office, LivingSpace
from app.person import Fellow, Staff
from abc import abstractmethod
import random
import string
import json

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

        # check errors
        if not error_list:
            print('Rooms created successfully')
        else:
            print('{} These names are invalid '.format(error_list))

    # Method to add person to the system and allocate room
    def add_person(self, first_name, last_name, gender, person_type, accommodation='No'):

        self.first_name = first_name
        self.last_name = last_name
        self.person_type = person_type
        self.gender = gender
        self.accommodation = accommodation

        person_details = [self.first_name, self.last_name,
                          self.gender, self.person_type, self.accommodation]

        if all(isinstance(details, str) for details in person_details):
            # check for null values or digits
            if all(details.isalpha() for details in person_details):

                # check if the person exists
                fellow = Fellow(self.first_name, self.last_name, self.gender)
                staff = Staff(self.first_name, self.last_name, self.gender)

                if self.check_names(fellow) or self.check_names(staff):
                    print('{} {} already exists'.format(self.first_name, self.last_name ))

                else:

                    if self.person_type.lower() == 'fellow':
                        fellow = Fellow(self.first_name, self.last_name, self.gender)

                        self.fellows.append({self.generate_id(): fellow})
                        print('Fellow Added Successfully')

                        # allocate  fellow livingspace if he/she needs
                        if self.accommodation.lower() in ('y', 'yes'):
                            self.allocate(fellow, 'Yes')

                        elif self.accommodation.lower() in ('n', 'no'):
                            self.allocate(fellow, 'No')

                        else:
                            print('Invalid option. Either Yes or No')

                    elif self.person_type.lower() == 'staff':
                        staff = Staff(self.first_name, self.last_name, self.gender)

                        self.staffs.append({self.generate_id(): staff})
                        self.allocate(staff, 'No')
                        print('Staff Added Successfully')

                    else:
                        print('Sorry person must be either Staff or Fellow')

            else:
                print('Null values or digits not accepted')
        else:
            print("All values must be characters.")

    # check if a person with same names exists
    def check_names(self, person_obj):
        self.person_obj = person_obj

        fellows = [item for fellow in self.fellows for item in fellow.values()]

        staffs = [item for staff in self.staffs for item in staff.values()]

        if self.person_obj in fellows or self.person_obj in staffs:
            return True

        return False

    # Room allocation method.
    def allocate(self, person_type, accommodation):
        self.person_type = person_type
        self.accommodation = accommodation

        # allocate random office to both fellow and staff
        if len(self.offices) == 0:
            self.andelans_unallocated_offices.append(self.person_type)
            #print('No office to allocate you currently.')

        elif any(office for office in self.offices if office.is_vacant()):
            for office in self.offices:
                random_office = random.choice(self.offices)
                if random_office.is_vacant() and not random_office.is_person_an_occupant(self.person_type):
                    random_office.add_occupant(self.person_type)
                    break

        else:
            self.andelans_unallocated_offices.append(self.person_type)
            print('All offices are full.')

        # allocate random livingspace to fellow
        if isinstance(self.person_type, Fellow) and self.accommodation == 'Yes':

            if len(self.living_spaces['male']) == 0 and self.person_type.gender.lower() == 'male':
                self.fellows_unallocated_living_space.append(self.person_type)
                #print('No livingspace to allocate you currently.')

            elif len(self.living_spaces['female']) == 0 and self.person_type.gender.lower() == 'female':
                self.fellows_unallocated_living_space.append(self.person_type)
                #print('No livingspace to allocate you currently.')

            elif any(living for living in self.living_spaces['male'] if living.is_vacant()):

                if self.person_type.gender.lower() == 'male':
                    for living in self.living_spaces['male']:
                        random_living_male = random.choice(
                            self.living_spaces['male'])
                        if random_living_male.is_vacant() and not random_living_male.is_fellow_an_occupant(self.person_type):
                            random_living_male.add_occupant(self.person_type)
                            break

            elif any(living for living in self.living_spaces['female'] if living.is_vacant()):

                if self.person_type.gender.lower() == 'female':
                    for living in self.living_spaces['female']:
                        random_living_female = random.choice(
                            self.living_spaces['female'])
                        if random_living_female.is_vacant() and not random_living_female.is_fellow_an_occupant(self.person_type):
                            random_living_female.add_occupant(self.person_type)
                            break

            else:
                self.fellows_unallocated_living_space.append(self.person_type)
                print('All livingspaces are full.')

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
            office for office in self.offices if self.room_name.lower() in office.name]

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
            fellow[self.person_id] for fellow in self.fellows if self.person_id in fellow]

        if is_staff:
            return 'staff', is_staff[0]

        elif is_fellow:
            return 'fellow', is_fellow[0]

        else:
            return False

    # Realloctes a person from one room to another
    def reallocate_person(self, person_id, room_name):
        self.person_id = person_id
        self.room_name = room_name

        # check if both params are correct
        if isinstance(self.person_id, str) and isinstance(self.room_name, str):

            if self.check_person(self.person_id.upper()) != False:
                person_type, person_obj = self.check_person(self.person_id.upper())

            if self.check_room(self.room_name) != False:
                room_type, room_obj = self.check_room(self.room_name)

            # check if person and room exists
            if not self.check_person(self.person_id.upper()) and not self.check_room(self.room_name):
                print('\nBoth person and room are not on the system\n')

            elif not self.check_person(self.person_id.upper()):
                print('\nThe person is not on the system\n')

            elif not self.check_room(self.room_name):
                print('\nThe room is not on the system\n')

            elif (person_type == 'fellow' and room_type == 'male_living_space'
                    and person_obj.gender == 'female'):
                print(
                    '\nSorry female fellow cannot be reallocated to male livingspace\n')

            elif (person_type == 'fellow' and room_type == 'female_living_space'
                  and person_obj.gender == 'male'):
                    print(
                        '\nSorry male fellow cannot be reallocated to female livingspace\n')

            elif (person_type == 'staff' and room_type in
                        ('female_living_space', 'male_living_space')):

                    print('\nSorry staff cannot be allocated livingspace\n')
            else:

                if not room_obj.is_vacant():
                    print('\nPerson cannot be reallocated to {}.\
                        Its not vacant\n'.format(self.room_name))

                elif person_obj in room_obj.occupants:
                    print('\nSorry cannot reallocate. Person is an occupant of this room\n')

                if room_obj.is_vacant() and not person_obj in room_obj.occupants:
                    # get person previous room

                    # check the previous room and the current room if are type same
                    if room_type == 'office':
                        previous_room = self.check_room_occupants(person_obj, 'office')
                        room_obj.add_occupant(person_obj)
                        # remove the person from previous room
                        previous_room.occupants.pop(person_obj)
                        print('\nPerson reallocated successfully\n')

                    elif room_type == 'male_living_space':
                        previous_room = self.check_room_occupants(person_obj, 'male')
                        room_obj.add_occupant(person_obj)

                        # remove the person from previous room
                        previous_room.occupants.pop(person_obj)
                        print('\nPerson reallocated successfully\n')

                    elif room_type == 'female_living_space':
                        previous_room = self.check_room_occupants(person_obj, 'female')
                        room_obj.add_occupant(person_obj)

                        # remove the person from previous room
                        previous_room.occupants.pop(person_obj)
                        print('\nPerson reallocated successfully\n')

        else:
            print('Inputs must be string')

    # get room occupant
    def check_room_occupants(self, person_obj, room_type):
        self.person_obj = person_obj
        self.room_type = room_type
        # check for person in all rooms and get room type

        is_office = [office for office in self.offices if self.person_obj in office.occupants]

        is_male = [living for living in self.living_spaces['male'] if self.person_obj in living.occupants]

        is_female = [living for living in self.living_spaces['female'] if self.person_obj in living.occupants]

        if self.room_type == "office":
            return office[0]

        elif self.room_type == "male":
            return male_living[0]

        elif self.room_type == "female":
            return female_living[0]

    # print room and room members
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

            print('\nCurrently there are no Rooms\n')

        elif (all(len(office.occupants) == 0 for office in self.offices) and
              all(len(living.occupants) == 0 for living in self.living_spaces['male']) and
              all(len(living.occupants) == 0 for living in self.living_spaces['female'])):

            print('\nAll rooms are empty\n ')

        else:

            # print all offices
            print('\nOFFICES\n')
            self.print_room_members('office')

            # print all male living spaces
            print('\nMALE LIVING SPACES\n')
            self.print_room_members('male')

            # print all female living spaces
            print('\nFEMALE LIVING SPACES\n')
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
            print(room.name.title())
            print('-'*15)
            names = ""
            for occupant in room.occupants:
                names += ('{} {}'.format(occupant.first_name, occupant.last_name))

            print(names)

    # prints all fellows and staffs who are not allocated offices or
    # livingspaces
    def print_unallocated(self):
        # check if there are people in unallocated list
        if (len(self.fellows_unallocated_living_space) == 0 and
                len(self.andelans_unallocated_offices) == 0):

            print('\nCurrently no andelan has not been allocated an office or living space\n')

        elif (len(self.fellows_unallocated_living_space) > 0
                and len(self.fellows_unallocated_living_space) > 0):

            # print all fellows with no living space
            print('\nAll Fellows Unallocated LivingSpace\n')

            for fellow in self.fellows_unallocated_living_space:
                print('{} {}'.format(fellow.first_name, fellow.last_name))

            # print all staff and fellows with no office
            print('All Andelans Unallocated Office')

            for andelan in self.andelans_unallocated_offices:
                print('{} {}'.format(andelan.first_name, andelan.last_name))

    def load_people(self):
        # open file
        text_file = open('app/andelans.txt', 'r')
        first_line = text_file.read(1)

        # check if file is empty
        if not first_line:
            print('File is empty')

        else:
            for line in text_file:
                if not line:
                    continue

                if len(line.split()) == 5:
                    first_name, last_name, gender, person_type, allocation = line.split()

                    self.add_person(first_name, last_name, gender,
                                    person_type, allocation)

                elif len(line.split()) == 4:
                    first_name, last_name, gender, person_type = line.split()

                    self.add_person(first_name, last_name, gender,
                                    person_type, 'No')

                elif len(line.split()) < 4:
                    continue

            print('People Added Successfully')
