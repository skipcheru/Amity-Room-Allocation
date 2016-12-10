import unittest
from app.person import Person, Fellow, Staff
from app.amity import Amity, Room, Office, LivingSpace

class TestCreateRoom(unittest.TestCase):
    """docstring for TestRoom."""
    def setUp(self):
        self.amity  = Amity ()

    # test if room has been added to the system
    def test_error_raised(self):
        self.assertRaises(TypeError, self.amity.create_room(344, 233))
        self.assertRaises(TypeError, self.amity.create_room())

    # check if  error raised if room names are not all strings
    def test_office_created(self):
        self.amity.create_room('nania-o', 'peri-l-m', 'oculus-o')
        self.assertEqual('oculus', self.amity.offices[1], 'office created')
        self.assertListEqual(['nania', 'oculus'], offices, 'both offices added to the system')

    # check if the offices added
    def test_living_space_created(self):
        self.assertIn('peri', self.amity.male_living_spaces, 'living space added')
        male_living_space = self.amity.create_room('shell-l-m', 'java-l-m')
        self.assertListEqual(['peri', 'shell', 'java'], self.amity.male_living_spaces)

    # check if error raised if an office exists on the system with the same name
    def test_existing_room_not_added(self):
        same_room_name = self.amity.create_room('react-l-f', 'swift-l-f', 'swift-l-f')
        self.assertTrue(same_room_name, 'room with the same name already exits.')
        self.assertListEqual(['react', 'swift'], self.amity.female_living_spaces)

    # check the no of offices and livingspaces are equal.
    def test_number_of_offices_and_living_spaces(self):
        self.assertTrue(2 is len(self.amity.offices))
        self.self.assertEqual(3, len(self.amity.male_living_spaces), 'Male living spaces are 3')
        self.self.assertEqual(2, len(self.amity.female_living_spaces), 'Female living spaces are 2')
