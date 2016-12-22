import sqlite3
from app.amity import Amity
import pickle

class AmityData(object):
    """Saving data and retrieving data Is implemented Here."""

    def __init__(self, db_name=None):
        self.database = 'data'

        if db_name:
            self.database = db_name

        self.conn = sqlite3.connect(self.database + '.db')
        self.cursor = self.conn.cursor()
        self.create_db()
        self.amity = Amity()

    def create_db(self):

        all_data = ('CREATE TABLE IF NOT EXISTS all_people(id INTEGER PRIMARY KEY,\
                    fellows TEXT, staffs TEXT, unallocated_living TEXT,\
                    unallocated_offices TEXT, offices TEXT, living_spaces TEXT);')

        self.cursor.execute(all_data)

    def save_state(self):

        fellows= pickle.dumps(self.amity.fellows)
        staffs = pickle.dumps(self.amity.staffs)
        unallocated_living = pickle.dumps(self.amity.fellows_unallocated_living_space)
        unallocated_offices = pickle.dumps(self.amity.andelans_unallocated_offices)
        offices = pickle.dumps(self.amity.offices)
        living_spaces = pickle.dumps(self.amity.living_spaces)


        query = 'INSERT OR REPLACE INTO all_people (id, fellows, staffs, unallocated_living,\
                    unallocated_offices, offices, living_spaces) VALUES (?, ?, ?, ?, ?, ?, ?)'

        self.cursor.execute(query, (1, fellows, staffs, unallocated_living,
                        unallocated_offices, offices, living_spaces))
        self.conn.commit()
        print('Data Saved Successfully in {}.db'.format(self.database))

    def load_state(self):
        # Fetch all data and convert to lists.
        query_section = 'SELECT * FROM all_people WHERE id=1'
        self.cursor.execute(query_section)
        data = self.cursor.fetchone()

        if not data:
            print("\nNo Data available.\n")
        else:
            self.amity.fellows = pickle.loads(data[1])
            self.amity.staffs = pickle.loads(data[2])
            self.amity.fellows_unallocated_living_space  = pickle.loads(data[3])
            self.amity.andelans_unallocated_offices  = pickle.loads(data[4])
            self.amity.offices = pickle.loads(data[5])
            self.amity.living_spaces = pickle.loads(data[6])

            print('Data Loaded Successfully')


    def load_people(self, file_name=None):
        # open file
        self.file_name = file_name
        local_file = 'andelans'

        if self.file_name:
            local_file = self.file_name

        text_file = open('app/'+ local_file + '.txt', 'r')
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

                    self.amity.add_person(first_name, last_name, gender,
                                person_type, allocation)

                elif len(line.split()) == 4:
                    first_name, last_name, gender, person_type = line.split()

                    self.amity.add_person(first_name, last_name, gender,
                        person_type, 'No')

                elif len(line.split()) < 4:
                    continue

        print('People Added Successfully')
