import sqlite3
from amity import Amity


class AmityData(object):
    """docstring for AmityData."""

    def __init__(self, db_name='data'):
        self.db_name = db_name

        if not isinstance(self.db_name, str):
            print('Only string allowed')

        self.conn = sqlite3.connect(self.db_name + '.db')
        self.cursor = self.conn.cursor()
        self.create_db()
        self.amity = Amity()

    def create_db(self):

        andelans = 'CREATE TABLE IF NOT EXISTS all_people(' \
                'id INTEGER PRIMARY KEY AUTOINCREMENT,' \
                'staffs TEXT,' \
                'fellows TEXT, ' \
                'unallocated_living TEXT, ' \
                'unallocated_offices TEXT);'

        offices = 'CREATE TABLE IF NOT EXISTS offices(' \
                  'id INTEGER PRIMARY KEY AUTOINCREMENT,' \
                  'occupants TEXT,' \
                  'room_name TEXT);'

        male_living_space = 'CREATE TABLE IF NOT EXISTS male_living(' \
                            'id INTEGER PRIMARY KEY AUTOINCREMENT,' \
                            'room_name TEXT,' \
                            'occupants TEXT);'

        female_living_space = 'CREATE TABLE IF NOT EXISTS female_living(' \
                              'id INTEGER PRIMARY KEY AUTOINCREMENT,'\
                              'room_name TEXT,' \
                              'occupants TEXT);'

        self.cursor.execute(andelans)
        self.cursor.execute(offices)
        self.cursor.execute(male_living_space)
        self.cursor.execute(female_living_space)

    # Save all rooms
    def save_all_rooms(self):

        self.save_room(self.amity.offices, 'offices')

        self.save_room(self.living_spaces['male'], 'male')

        self.save_room(self.living_spaces['female'], 'female')

    # save each room
    def save_room(self, rooms, room_type):
        self.rooms = rooms
        self.room_type = room_type

        table = ''

        if self.room_type == 'offices':
            table = 'offices'

        elif self.room_type == 'male':
            table = 'male_living'

        elif self.room_type == 'female':
            table = 'female_living'

        else:
            return False

        # Save all rooms with occupants
        room_details = [(room.name, str([(member.first_name, member.last_name,
                        member.gender) for member in room.occupants]))
                        for room in self.rooms]

        query = 'INSERT INTO '+ table + '(room_name, occupants) VALUES (?, ?)'

        self.cursor.executemany(query, room_details)
        self.conn.commit()


    def save_people(self, people):
        self.people = people
        fellows = [(fellow.first_name, fellow.last_name, fellow.gender) fellow in self.amity.fellows]

        staffs = [(staff.first_name, staff.last_name, staff.gender) staff in self.amity.staffs]

        fellows_unallocated_living_space = [(fellow.first_name, fellow.last_name, fellow.gender) fellow in self.amity.fellows]

        self.people = [(self.amity.staffs), (self.amity.fellows),
                (self.amity.fellows_unallocated_living_space),
                (self.amity.andelans_unallocated_offices)]

        query = 'INSERT INTO all_people (fellows, staffs, unallocated_living,\
                    unallocated_offices) VALUES (?, ?, ?, ?)'

        self.cursor.executemany(query, people)
        self.conn.commit()




amity = Amity()
amity.create_room(['Nania office', 'Oculus Office', 'Peri livingspace male'])

amity.add_person('Arya', 'Stark', 'female','staff')
amity.add_person('Ian', 'Oti', 'male', 'fellow', 'Y')
amity.add_person('njeri', 'mwangi', 'female','staff')
amity.add_person('kip', 'cheru', 'male', 'fellow', 'Y')


print(amity.living_spaces['male'][0].occupants)

da = AmityData('amdata')
da.save_room(amity.offices, 'offices')
da.save_room(amity.living_spaces['male'], 'male')

da.save_people([(amity.staffs), (amity.fellows),
        (amity.fellows_unallocated_living_space),
        (amity.andelans_unallocated_offices)])
