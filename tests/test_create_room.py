import unittest
from app.person import Person, Fellow, Staff
from app.amity import Amity, Room, Office, LivingSpace

class TestCreateRoom(unittest.TestCase):
    """docstring for TestRoom."""
    def setUp(self):
        self.amity  = Amity ()
        self.nania = Office('nania')
        self.oculus = Office('oculus')
        self.peri = LivingSpace('peri')
        self.shell = LivingSpace('shell')
        self.java = LivingSpace('java')
        self.react = LivingSpace('react')
        self.swift = LivingSpace('swift')


    # test if room has been added to the system
    def test_error_raised(self):
        self.assertRaises(TypeError, self.amity.create_room(344, 233))
        self.assertRaises(TypeError, self.amity.create_room())

    # check if error raised if room names are not all strings
    def test_office_created(self):
        self.amity.create_room('nania-o', 'peri-l-m', 'oculus-o')
        self.assertEqual(self.nania, self.amity.offices[0], 'office created')
        self.assertListEqual([self.nania, self.oculus], offices, 'both offices added to the system')

    # check if the offices added
    def test_living_space_created(self):
        self.assertIn(self.peri, self.amity.male_living_spaces, 'living space added')
        self.amity.create_room('shell-l-m', 'java-l-m')
        self.assertListEqual([self.peri, self.shell, self.java], self.amity.male_living_spaces)

    # check if error raised if an office exists on the system with the same name
    def test_existing_room_not_added(self):
        same_room_name = self.amity.create_room('react-l-f', 'swift-l-f', 'swift-l-f')
        self.assertTrue(same_room_name, 'room with the same name already exits.')
        self.assertListEqual([self.react, self.swift], self.amity.female_living_spaces)

    # check the no of offices and livingspaces are equal.
    def test_number_of_offices_and_living_spaces(self):
        self.assertTrue(2 is len(self.amity.offices))
        self.self.assertEqual(3, len(self.amity.male_living_spaces), 'Male living spaces are 3')
        self.self.assertEqual(2, len(self.amity.female_living_spaces), 'Female living spaces are 2')
