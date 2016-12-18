from app.person import Fellow, Staff
from app.room import Office
import unittest


class Testoffice(unittest.TestCase):
    """docstring for Testoffice."""
    def setUp(self):
        self.office = Office('Oculus')
        self.fellow = Fellow('sam', 'cheru', 'male')
        self.staff = Staff('angie', 'mugo', 'female')
        self.occupants =[{200: 'fellow'}, {230: 'fellow2'}, {235: 'staff2'}, {133: 'staff1'}]
    
