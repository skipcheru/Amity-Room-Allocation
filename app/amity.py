from app.room import Office, LivingSpace
from app.person import Fellow, Staff
import random
import string
import json


class Amity():
    """All app functions are implemented Here."""

    def __init__(self):
        self.people = {'fellows': {}, 'staff': {}}
        self.unallocated = {'office': [], 'living': []}
        self.rooms = {'office': [], 'female': [], 'male': []}
        self.set_of_ids = set()

    # create room and add to the list of rooms
    def create_room(self, room_name, room_type, living_type=None):

        if not room_name.isalpha() and not room_type.isalpha():
            return 'Room names in strings only'

        if room_type not in ('o', 'office', 'livingspace', 'l'):
            return 'Invalid room type'

        if living_type:
            if living_type not in ('m', 'male', 'f', 'female'):
                return 'Invalid gender room type'

        if self.check_room(room_name.lower()):
            return '{} already exists'.format(room_name)

        room_mapping = {'o': Office, 'office': Office, 'l': LivingSpace,
                        'living': LivingSpace}
        new_room = room_mapping[room_type](room_name.lower())

        # add the room type to the list
        if room_type in ('o', 'office'):
            self.rooms['office'].append(new_room)
            return 'Office created sucessfully'

        if living_type in ('m', 'male'):
            self.rooms['male'].append(new_room)
            return 'Male Living created sucessfully'

        if living_type in ('f', 'female'):
            self.rooms['female'].append(new_room)
            return 'Female Living created sucessfully'

    # Method to add person to the system and allocate room
    def add_person(self, first_name, last_name, gender, person_type,
                   accommodation='N'):

        person_details = [first_name, last_name, gender, person_type,
                          accommodation]

        if not all(details.isalpha() for details in person_details):
            return 'Null values or digits not accepted'

        if person_type.lower() not in ('fellow', 'f', 'staff', 's'):
            return 'Invalid person type. Either fellow, f, staff or s'

        if accommodation.lower() not in ('y', 'yes', 'n', 'no'):
            return 'Invalid option. Either Yes, y, No or n'

        if gender.lower() not in ('male', 'female'):
            return 'Invalid gender. Either male or female'

        fellow = Fellow(first_name.lower(), last_name.lower(), gender.lower())
        staff = Staff(first_name.lower(), last_name.lower(), gender.lower())
        # check if the person exists
        if self.check_names(fellow) or self.check_names(staff):
            return '{} {} already exists'.format(first_name, last_name)

        if person_type.lower() in ('fellow', 'f'):

            self.people['fellows'].update({self.generate_id(): fellow})

            # allocate  fellow livingspace if he/she needs
            if accommodation.lower() in ('y', 'yes'):
                self.allocate(fellow, 'Yes')

            elif accommodation.lower() in ('n', 'no'):
                self.allocate(fellow, 'No')

            return 'Fellow Added Successfully'

        if person_type.lower() in ('staff', 's'):

            self.people['staff'].update({self.generate_id(): staff})
            self.allocate(staff, 'No')

            return 'Staff Added Successfully'

    # print all fellows and staff
    def print_all_people(self):

        count = 0
        for key, value in self.people.items():
            print('\n'+ key +'\n' + '-'*16 + '\n   Id \t  Name')

            for person_id, person in value.items():
                print(count, ' ' + person_id + ' : '+ person.first_name.title(),
                      person.last_name.title())

                count += 1
        print('\n')

    # check if a person with same names exists
    def check_names(self, person_obj):

        person = [item for people in self.people.values() for item in people.values()]

        return person_obj in person

    # Room allocation method.
    def allocate(self, person, accommodation):
        # allocate random office to both fellow and staff
        if (len(self.rooms['office']) == 0 or all(not office.is_vacant() for office in self.rooms['office'])):

            self.unallocated['office'].append(person)
            print('Added to Unallocated Office.')

        if any(office for office in self.rooms['office'] if office.is_vacant()):
            for office in self.rooms['office']:
                random_office = random.choice(self.rooms['office'])
                if (random_office.is_vacant() and not
                        random_office.is_occupant(person)):
                    random_office.add_occupant(person)
                    print('Allocated Office.')
                    break

        # allocate random livingspace to fellow or if all living space are full
        if isinstance(person, Fellow) and accommodation == 'Yes':

            gender = 'male' if person.gender.lower() == 'male' else 'female'

            # add to Unallocated if there is no living space
            if (len(self.rooms[gender]) == 0 or
                all( not living.is_vacant() for living in self.rooms[gender])):
                self.unallocated['living'].append(person)
                print('Added to Unallocated livingspaces.')

            if (any(living for living in self.rooms[gender] if living.is_vacant())):

                for living in self.rooms[gender]:
                    random_living = random.choice(self.rooms[gender])
                    if (random_living.is_vacant() and not
                            random_living.is_occupant(person)):
                        random_living.add_occupant(person)
                        print('Allocated Living Space')
                        break

    # generate unique id for each Andelan
    def generate_id(self):

        chars = string.ascii_uppercase + string.digits

        andelan_id = ''.join(random.choice(chars) for i in range(4))

        # check if the id is unique
        while andelan_id not in self.set_of_ids:
            return andelan_id

    # Check if room exists in the system
    def check_room(self, room_name):
        # check if room with same name exits
        is_room = [(key, room) for key, value in self.rooms.items()
                    for room in value if room_name.lower() in room.name]
        if is_room:
            (room_type, room) = is_room[0]
            return room_type, room

    # check if person exists in the system
    def check_person(self, person_id):

        is_person = [(key, value[person_id]) for key, value in self.people.items()
                     if person_id in value]

        if is_person:
            key, person = is_person[0]
            return key, person


    # Realloctes a person from one room to another
    def reallocate_person(self, person_id, room_name):

        if self.check_person(person_id.upper()):
            person_type, person_obj = self.check_person(person_id.upper())

        if self.check_room(room_name.lower()):
            room_type, room_obj = self.check_room(room_name.lower())

        # check if person and room exists
        if (not self.check_person(person_id.upper()) and not
                self.check_room(room_name.lower())):
            return 'Both person and room are not on the system'

        if not self.check_person(person_id.upper()):
            return 'The person is not on the system'

        if not self.check_room(room_name.lower()):
            return 'The room is not on the system'

        if room_obj.is_occupant(person_obj):
            return 'Sorry Person is already an occupant of this room'

        if person_type == 'staff' and room_type in ('female', 'male'):
            return 'Sorry staff cannot be allocated livingspace'

        if room_type == 'male' and person_obj.gender == 'female':
            return 'Sorry female fellow cannot be reallocated to male livingspace'

        if room_type == 'female' and person_obj.gender == 'male':
            return 'Sorry male fellow cannot be reallocated to female livingspace'

        if not room_obj.is_vacant():
            return 'Person cannot be reallocated to {}. Not vacant '\
                    .format(room_name)

        if room_obj.is_vacant() and not room_obj.is_occupant(person_obj):
            room = 'male' if room_type == 'male' else 'female' if room_type == 'female' else 'office'

            # check the previous room and the current room if are same
            previous_room = self.check_room_occupants(person_obj, room)
            # remove the person from unallocated
            if person_obj in self.unallocated[room]:
                self.unallocated[room].remove(person_obj)

            # remove the person from previous room
            if previous_room:
                previous_room.occupants.remove(person_obj)
                room_obj.add_occupant(person_obj)

            else:
                room_obj.add_occupant(person_obj)

            return 'Person reallocated successfully'

    # get room occupant
    def check_room_occupants(self, person_obj, room_type):
        # check for person in all rooms and get room type

        is_room = [room for room in self.rooms[room_type] if person_obj
                     in room.occupants]

        return is_room[0] if is_room else False

    # print room and room members
    def print_room(self, room_name):
        # check if room exits
        if not self.check_room(room_name):
            print('\nThe room does not exist\n')
            return

        # check for occupants
        room_type, room_obj = self.check_room(room_name)
        if len(room_obj.occupants) == 0:
            print('\nRoom has no occupants\n')
            return

        # print all room occupants
        print('\n' + room_name.title() + '\n' + '-'*16)
        members = ''

        for occupant in room_obj.occupants:
            members += ('{} {}, '.format(
                occupant.first_name, occupant.last_name))

        print(members + '\n')

    # print all rooms with occupants
    def print_allocations(self, file_name=None):

        no_rooms = '\nCurrently there are no Rooms\n'
        empty_rooms = '\nAll rooms are empty\n '
        offices, male_living = '\nOFFICES', '\nMALE LIVING SPACES'
        female_living = '\nFEMALE LIVING SPACES'

        data = (offices + '\n' + self.print_room_members('office') + male_living
                + '\n' + self.print_room_members('male') + female_living + '\n'
                + self.print_room_members('female'))

        # check if rooms have been added to the system
        if all(not room for room in self.rooms.values()):

            if file_name:
                text_file = open(file_name + '.txt', 'w+')
                text_file.write(data)
                text_file.close()
                print('\nData saved in {}.txt\n'.format(file_name))
                return

            print(no_rooms)

        if file_name:
            text_file = open(file_name + '.txt', 'w+')
            text_file.write(data)
            text_file.close()
            print('\nData saved in {}.txt\n'.format(file_name))
            return

        # print all allocations
        print(data)

    # print all room occupants
    def print_room_members(self, room_type):

        room_detail = [room for room in self.rooms[room_type]]

        response = ''
        # Get all room occupants details
        for room in room_detail:
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
        andelans, fellows, count, deco = '', '', 0, '-'*30

        for person in self.unallocated['office']:
            andelans += ('{} {}, '.format(person.first_name, person.last_name))

        for person in self.unallocated['living']:
            fellows += ('{} {}, '.format(person.first_name, person.last_name))

        unallocated = ('\n' + title_one + '\n' + deco + '\n' + fellows + '\n' +
                       title_two + '\n' + deco + '\n' + andelans + '\n')
        # if file_name is passed write to the file and save
        if file_name:
            text_file = open(file_name + '.txt', 'w+')
            text_file.write(unallocated)
            text_file.close()

            print('\nData saved in {}.txt\n'.format(file_name))
            return

        # print all staff and fellows with no office
        print(unallocated)
