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
                    fellows TEXT, staffs TEXT, unallocated_living TEXT,\
                    unallocated_offices TEXT, offices TEXT, male_living TEXT,\
                    female_living TEXT);')

        self.cursor.execute(all_data)

    def save_state(self):

        fellows= pickle.dumps(self.amity.fellows)
        staffs = pickle.dumps(self.amity.staffs)
        unallocated_living = pickle.dumps(self.amity.fellows_unallocated_living_space)
        unallocated_offices = pickle.dumps(self.amity.andelans_unallocated_offices)
        offices = pickle.dumps(self.amity.rooms['office'])
        male_living = pickle.dumps(self.amity.rooms['male'])
        female_living = pickle.dumps(self.amity.rooms['female'])

        query = 'INSERT OR REPLACE INTO all_people (id, fellows, staffs, unallocated_living,\
                    unallocated_offices, offices, male_living, female_living) VALUES (?, ?, ?, ?, ?, ?, ?, ?)'

        self.cursor.execute(query, (1, fellows, staffs, unallocated_living,
                        unallocated_offices, offices, male_living, female_living))
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

        else:
            self.amity.fellows = pickle.loads(data[1])
            self.amity.staffs = pickle.loads(data[2])
            self.amity.fellows_unallocated_living_space  = pickle.loads(data[3])
            self.amity.andelans_unallocated_offices  = pickle.loads(data[4])
            self.amity.rooms['office'] = pickle.loads(data[5])
            self.amity.rooms['male']= pickle.loads(data[6])
            self.amity.rooms['female'] = pickle.loads(data[7])

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
