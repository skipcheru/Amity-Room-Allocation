import unittest
from app.person import Person, Fellow, Staff
from app.amity import Amity, Room, Office, LivingSpace

class TestOffice(unittest.TestCase):
    """docstring for TestOffice."""
    def setUp(self):
        self.office = Office('Lime')
        self.fellow = Fellow('ian', 'oti', 'male')
        self.staff = Staff('njira', 'persc', 'female')

    def test_office(self):
        self.assertIsInstance(self.office, Office, 'Object not an instance of Office')
        
