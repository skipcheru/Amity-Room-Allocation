import sqlite3
from app.amity import Amity
import pickle


class AmityData(object):
    """Saving data and retrieving data Is implemented Here."""
    amity = Amity()

    def __init__(self, db_name=None):
        self.database = 'data'

        if db_name:
            self.database = db_name

        self.conn = sqlite3.connect(self.database + '.db')
        self.cursor = self.conn.cursor()
        self.create_db()

    def create_db(self):

        all_data = ('CREATE TABLE IF NOT EXISTS all_people(id INTEGER PRIMARY KEY,\
                    people TEXT, unallocated TEXT, rooms TEXT);')

        self.cursor.execute(all_data)

    def save_state(self):

        people = pickle.dumps(self.amity.people)
        unallocated = pickle.dumps(self.amity.unallocated)
        rooms = pickle.dumps(self.amity.rooms)

        query = 'INSERT OR REPLACE INTO all_people (id, people, unallocated,\
                    rooms) VALUES (?, ?, ?, ?)'

        self.cursor.execute(query, (1, people, unallocated, rooms))
        self.conn.commit()

        print('Data Saved Successfully in {}.db'.format(self.database))

    # load data to amity
    def load_state(self):
        # Fetch all data and convert to lists.
        query_section = 'SELECT * FROM all_people WHERE id=1'
        self.cursor.execute(query_section)
        data = self.cursor.fetchone()

        if not data:
            print("\nNo Data available.\n")

        self.amity.people = pickle.loads(data[1])
        self.amity.unallocated = pickle.loads(data[2])
        self.amity.rooms  = pickle.loads(data[3])

        print('Data Loaded Successfully')

    def load_people(self, file_name=None):
        # open file
        self.file_name = file_name
        local_file = 'andelans'

        if self.file_name:
            local_file = self.file_name

        # check if file exists
        try:
            with open('app/'+ local_file + '.txt', 'r') as f:
                file_content = f.readlines()

                # check if file is empty
                if file_content:
                    for line in file_content:
                        if not line:
                            continue

                        if len(line.split()) == 5:
                            first_name, last_name, gender, person_type, allocation = line.split()

                            print(self.amity.add_person(first_name, last_name, gender,
                                        person_type, allocation))

                        elif len(line.split()) == 4:
                            first_name, last_name, gender, person_type = line.split()

                            print(self.amity.add_person(first_name, last_name, gender,
                                person_type, 'No'))

                        elif len(line.split()) < 4:
                            continue

                    print('People Loaded Successfully')

                else:
                    print('File is empty')

        except Exception as e:
             print('Sorry file not found')
