import unittest
from app.person import Person, Fellow, Staff
from app.amity import Amity, Room, Office, LivingSpace

class TestPerson(unittest.TestCase):
    def setUp(self):
        self.person = Person('sam', 'cheru', 'male')
        self.fellow = Fellow('ian', 'oti', 'male')
        self.staff = Staff('poach', 'ing', 'male')

    def test_person(self):
        self.assertIsInstance(self.staff, Person, '')

    def test_person_details(self):
        self.assertEqual(str(self.person), self.person.first_name + ' ' + self.person.last_name, 'Names doesnt match')

    def test_fellow(self):
        self.assertNotEqual(self.person.gender, 'female')
