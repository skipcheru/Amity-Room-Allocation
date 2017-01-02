from app.room import Room, Office, LivingSpace
from app.person import Fellow, Staff
from app.singleton import Singleton
from abc import abstractmethod
import random
import string
import json


class Amity(metaclass=Singleton):
    """All app functions are implemented Here."""

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
        error_list = []
        room_type_error = {'room_type': [], 'living_type': []}

        for room in rooms:
            if len(room.split()) <= 1:
                error_list.append(room)

            elif len(room.split()) == 2:

                if all(details.isalpha() for details in room.split()):
                    room_name, room_type = room.split()

                    # check if room with same name exists
                    if not self.check_room(room_name):

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
                        print('Romm with {} exists'.format(room_name))

                else:
                    error_list.append(room)

            elif len(room.split()) == 3:
                room_name, room_type, living_type = room.split()
                # check if room with same name exists
                if not self.check_room(room_name):

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
                else:
                    print('Romm with {} exists'.format(room_name))

        # check errors
        if not error_list:
            print('Rooms created successfully')
        else:
            print('{} These names are invalid '.format(error_list))

    # Method to add person to the system and allocate room
    def add_person(self, first_name, last_name, gender, person_type,
                   accommodation='N'):

        person_details = [first_name, last_name, gender, person_type,
                          accommodation]

        if all(details.isalpha() for details in person_details):

            fellow = Fellow(first_name, last_name, gender)
            staff = Staff(first_name, last_name, gender)
            # check if the person exists
            if self.check_names(fellow) or self.check_names(staff):
                print('{} {} already exists'.format(first_name, last_name))

            else:
                if person_type.lower() == 'fellow':

                    self.fellows.append({self.generate_id(): fellow})
                    print('Fellow Added Successfully')

                    # allocate  fellow livingspace if he/she needs
                    if accommodation.lower() in ('y', 'yes'):
                        self.allocate(fellow, 'Yes')

                    elif accommodation.lower() in ('n', 'no'):
                        self.allocate(fellow, 'No')

                    else:
                        return 'Invalid option. Either Yes or No'

                elif person_type.lower() == 'staff':

                    self.staffs.append({self.generate_id(): staff})
                    self.allocate(staff, 'No')

                    return 'Staff Added Successfully'

                else:
                    return 'Sorry person must be either Staff or Fellow'
        else:
            return 'Null values or digits not accepted'

    # print all fellows and staff
    def print_all_people(self):

        print('\nSTAFF\n' + '-'*16 + '\n   Id \t  Name')
        count = 0
        for staff in self.staffs:
            for person_id, person in staff.items():
                print(count, ' ' + person_id + ' : '+person.first_name.title(),
                      person.last_name.title())
                count += 1

        print('\nFELLOWS\n' + '-'*16 + '\n   Id \t  Name')

        for fellow in self.fellows:
            for person_id, person in fellow.items():
                print(count, ' ' + person_id + ' : '+person.first_name.title(),
                      person.last_name.title())
                count += 1

        print('\n')

    # check if a person with same names exists
    def check_names(self, person_obj):

        fellows = [item for fellow in self.fellows for item in fellow.values()]

        staffs = [item for staff in self.staffs for item in staff.values()]

        if person_obj in fellows or person_obj in staffs:
            return True

        return False

    # Room allocation method.
    def allocate(self, person_type, accommodation):
        # allocate random office to both fellow and staff
        if len(self.offices) == 0:
            self.andelans_unallocated_offices.append(person_type)
            print('Added to Unallocated Office.')

        elif any(office for office in self.offices if office.is_vacant()):
            for office in self.offices:
                random_office = random.choice(self.offices)
                if (random_office.is_vacant() and not
                        random_office.is_occupant(person_type)):
                    random_office.add_occupant(person_type)
                    break
        else:
            self.andelans_unallocated_offices.append(person_type)
            print('Added to Unallocated Office.')

        # allocate random livingspace to fellow
        if isinstance(person_type, Fellow) and accommodation == 'Yes':

            if (len(self.living_spaces['male']) == 0 and
                    person_type.gender.lower() == 'male'):
                self.fellows_unallocated_living_space.append(person_type)
                print('Added to Unallocated livingspaces.')

            elif (len(self.living_spaces['female']) == 0 and
                    person_type.gender.lower() == 'female'):
                self.fellows_unallocated_living_space.append(person_type)
                print('Added to Unallocated livingspaces.')

            elif (any(living for living in self.living_spaces['male']
                  if living.is_vacant()) and
                    any(living for living in self.living_spaces['female']
                        if living.is_vacant())):

                if person_type.gender.lower() == 'male':
                    for living in self.living_spaces['male']:
                        random_living_male = random.choice(
                            self.living_spaces['male'])
                        if (random_living_male.is_vacant() and not
                                random_living_male.is_occupant(person_type)):
                            random_living_male.add_occupant(person_type)
                            return 'Allocated Living Space'
                            break

                elif person_type.gender.lower() == 'female':
                    for living in self.living_spaces['female']:
                        random_living_female = random.choice(
                            self.living_spaces['female'])

                        if (random_living_female.is_vacant() and not
                                random_living_female.is_occupant(person_type)):
                            random_living_female.add_occupant(person_type)
                            return 'Allocated Living Space'
                            break

            else:
                self.fellows_unallocated_living_space.append(person_type)
                print('Added to Unallocated livingspaces.')

    # generate unique id for each Andelan
    def generate_id(self):

        chars = string.ascii_uppercase + string.digits

        andelan_id = ''.join(random.choice(chars) for i in range(4))

        # check if the id is unique
        while andelan_id not in self.set_of_ids:
            return andelan_id

    # Check if room exists in the system
    def check_room(self, room_name):
        # check if room exits in offices
        is_office = [
            office for office in self.offices
            if room_name.lower() in office.name]

        is_male_living_space = [
            living for living in self.living_spaces['male']
            if room_name.lower() in living.name]

        is_female_living_space = [
            living for living in self.living_spaces['female']
            if room_name.lower() in living.name]

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

        is_staff = [
            staff[person_id] for staff in self.staffs if person_id in staff]

        is_fellow = [
            fellow[person_id] for fellow in self.fellows if person_id in fellow]

        if is_staff:
            return 'staff', is_staff[0]

        elif is_fellow:
            return 'fellow', is_fellow[0]

        else:
            return False

    # Realloctes a person from one room to another
    def reallocate_person(self, person_id, room_name):

        # check if both params are correct
        if isinstance(person_id, str) and isinstance(room_name, str):

            if self.check_person(person_id.upper()):
                person_type, person_obj = self.check_person(person_id.upper())

            if self.check_room(room_name):
                room_type, room_obj = self.check_room(room_name)

            # check if person and room exists
            if (not self.check_person(person_id.upper()) and not
                    self.check_room(room_name)):
                return 'Both person and room are not on the system'

            elif not self.check_person(person_id.upper()):
                return 'The person is not on the system'

            elif not self.check_room(room_name):
                return 'The room is not on the system'

            elif (person_type == 'fellow' and room_type == 'male_living_space'
                    and person_obj.gender == 'female'):
                return 'Sorry female fellow cannot be reallocated\
                        to male livingspace'

            elif (person_type == 'fellow' and room_type == 'female_living_space'
                    and person_obj.gender == 'male'):
                    return 'Sorry male fellow cannot be reallocated to\
                            female livingspace'

            elif (person_type == 'staff' and room_type in
                    ('female_living_space', 'male_living_space')):

                    return 'Sorry staff cannot be allocated livingspace'
            else:

                if not room_obj.is_vacant():
                    return 'Person cannot be reallocated to {}. Not vacant '\
                            .format(room_name)

                elif person_obj in room_obj.occupants:
                    return 'Sorry Person is already an occupant of this room'

                if room_obj.is_vacant() and person_obj not in room_obj.occupants:
                    # check the previous room and the current room if are same
                    if room_type == 'office':
                        previous_room = self.check_room_occupants(person_obj,
                                                                  'office')
                        # remove the person from unallocated
                        if person_obj in self.andelans_unallocated_offices:
                            self.andelans_unallocated_offices.remove(person_obj)
                        # remove the person from previous room
                        if previous_room:
                            previous_room.occupants.remove(person_obj)
                            room_obj.add_occupant(person_obj)

                        else:
                            room_obj.add_occupant(person_obj)

                        return 'Person reallocated successfully'

                    elif room_type == 'male_living_space':
                        previous_room = self.check_room_occupants(person_obj,
                                                                  'male')
                        # remove the person from previous room
                        if previous_room:
                            previous_room.occupants.remove(person_obj)
                            room_obj.add_occupant(person_obj)

                        if person_obj in self.living_spaces['male']:
                            self.living_spaces['male'].remove(person_obj)
                        else:
                            room_obj.add_occupant(person_obj)

                        return 'Person reallocated successfully'

                    elif room_type == 'female_living_space':
                        previous_room = self.check_room_occupants(person_obj,
                                                                  'female')
                        # remove the person from previous room
                        if previous_room:
                            previous_room.occupants.remove(person_obj)
                            room_obj.add_occupant(person_obj)

                        if person_obj in self.living_spaces['female']:
                            self.living_spaces['female'].remove(person_obj)

                        else:
                            room_obj.add_occupant(person_obj)

                        return 'Person reallocated successfully'

        else:
            return 'Inputs must be string'

    # get room occupant
    def check_room_occupants(self, person_obj, room_type):
        # check for person in all rooms and get room type

        is_office = [office for office in self.offices if person_obj
                     in office.occupants]

        is_male = [living for living in self.living_spaces['male']
                   if person_obj in living.occupants]

        is_female = [living for living in self.living_spaces['female']
                     if person_obj in living.occupants]

        if room_type == "office":
            if is_office:
                return is_office[0]
            else:
                return False

        elif room_type == "male":
            if is_male:
                return is_male[0]
            else:
                return False

        elif room_type == "female":
            if is_female:
                return mis_female[0]
            else:
                return False

    # print room and room members
    def print_room(self, room_name):

        if isinstance(room_name, str):

            if self.check_room(room_name) is False:
                print('\nThe room does not exist\n')

            else:
                room_type, room_obj = self.check_room(room_name)

                if len(room_obj.occupants) == 0:
                    print('\nRoom has no occupants\n')

                else:
                    print('\n' + room_name.title() + '\n' + '-'*16)
                    members = ''

                    for occupant in room_obj.occupants:
                        members += ('{} {}, '.format(
                            occupant.first_name, occupant.last_name))

                    print(members + '\n')
        else:
            raise TypeError
            print('only strings allowed')

    # print all rooms with occupants
    def print_allocations(self, file_name=None):

        no_rooms = '\nCurrently there are no Rooms\n'
        empty_rooms = '\nAll rooms are empty\n '
        offices = '\nOFFICES'
        male_living = '\nMALE LIVING SPACES'
        female_living = '\nFEMALE LIVING SPACES'

        data = (offices + '\n' + self.print_room_members('office') + male_living
                + '\n' + self.print_room_members('male') + female_living + '\n'
                + self.print_room_members('female'))

        # check if rooms have been added to the system
        if (len(self.offices) == 0 and len(self.living_spaces['female']) == 0
                and len(self.living_spaces['male']) == 0):

            if file_name:
                text_file = open(file_name + '.txt', 'w+')
                text_file.write(data)
                text_file.close()
                print('\nData saved in {}.txt\n'.format(file_name))

            else:
                print(no_rooms)

        else:

            if file_name:
                text_file = open(file_name + '.txt', 'w+')
                text_file.write(data)
                text_file.close()
                print('\nData saved in {}.txt\n'.format(file_name))

            else:
                # print all allocations
                print(data)

    # print all room occupants
    def print_room_members(self, room_type):
        self.room_type = room_type
        room_type_list = []
        # Get room type
        if self.room_type == 'office':
            room_type_list = self.offices

        elif self.room_type == 'male':
            room_type_list = self.living_spaces['male']

        elif self.room_type == 'female':
            room_type_list = self.living_spaces['female']

        else:
            return False

        rooms_with_occupants = [room for room in room_type_list]

        response = ''
        # Get all room occupants details
        for room in rooms_with_occupants:
            response += '\n' + room.name.title() + '\n' + '-'*15 + '\n'

            for occupant in room.occupants:
                response += ('{} {}, '.format(occupant.first_name,
                             occupant.last_name))

            response += '\n'

        return response + '\n'

    # prints all fellows and staffs who are not allocated offices or
    # livingspaces
    def print_unallocated(self, file_name=None):

        title_one = 'All Fellows Unallocated LivingSpace\n'
        title_two = '\nAll Andelans Unallocated Office\n'
        andelans = ''
        deco = '-'*30
        fellows = ''

        for fellow in self.fellows_unallocated_living_space:
            fellows += ('{} {}, '.format(fellow.first_name, fellow.last_name))

        for andelan in self.andelans_unallocated_offices:
            andelans += ('{} {}, '.format(andelan.first_name, andelan.last_name))

        unallocated = ('\n' + title_one + '\n' + deco + '\n' + fellows + '\n' +
                       title_two + '\n' + deco + '\n' + andelans + '\n')
        # if file_name is passed write to the file and save
        if file_name:
            text_file = open(file_name + '.txt', 'w+')
            text_file.write(unallocated)
            text_file.close()

            print('\nData saved in {}.txt\n'.format(file_name))

        else:
            # print all staff and fellows with no office
            print(unallocated)
