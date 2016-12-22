import sqlite3
from app.amity import Amity
import pickle


class AmityData(object):
    """docstring for AmityData."""

    def __init__(self, db_name=None):
        self.db_name = db_name
        database = 'data'

        if self.db_name:
            database = self.db_name

        self.conn = sqlite3.connect(self.db_name + '.db')
        self.cursor = self.conn.cursor()
        self.create_db()
        self.amity = Amity()

    def create_db(self):

        all_data = 'CREATE TABLE IF NOT EXISTS all_people(' \
                    'id INTEGER PRIMARY KEY AUTOINCREMENT,' \
                    'staffs TEXT,' \
                    'fellows TEXT, ' \
                    'unallocated_living TEXT, ' \
                    'unallocated_offices TEXT, ' \
                    'offices TEXT, ' \
                    'living_spaces TEXT);'

        self.cursor.execute(all_data)

    def save_data(self):

        fellows= pickle.dumps(self.amity.fellows)
        staffs = pickle.dumps(self.amity.staffs)
        unallocated_living = pickle.dumps(self.amity.fellows_unallocated_living_space)
        unallocated_offices = pickle.dumps(self.amity.andelans_unallocated_offices)
        offices = pickle.dumps(self.amity.offices)
        living_spaces = pickle.dumps(self.amity.living_spaces)


        query = 'INSERT INTO all_people (fellows, staffs, unallocated_living,\
                    unallocated_offices, offices, living_spaces) VALUES (?, ?, ?, ?, ?, ?)'

        self.cursor.execute(query, (fellows, staffs, unallocated_living,
                        unallocated_offices, offices, living_spaces))
        self.conn.commit()
        self.conn.close()


    def load_data(self):
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
            self.conn.close()
