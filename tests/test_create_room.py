import unittest
from app.amity import Amity, Room, Office, LivingSpace


class TestCreateRoom(unittest.TestCase):
    """Test Create Rooms."""
    def setUp(self):
        self.amity = Amity()

    def test_office_created(self):
        self.amity.create_room(['Nania office', 'peri l male', 'oculus o'])
        self.assertEqual(len(self.amity.offices), 2)

    # check if the living spaces added
    def test_living_space_created(self):
        self.amity.create_room(['shell l female', 'java l male'])
        self.assertEqual(len(self.amity.living_spaces['male']), 1)
        self.assertEqual(len(self.amity.living_spaces['female']), 1)
        self.assertIsInstance(self.amity.living_spaces['male'][0], LivingSpace)

    # check if an office exists on the system with the same name
    def test_existing_room_not_added(self):
        self.amity.create_room(['shell l female', 'Nania o', 'Nania office'])
        self.amity.create_room(['shell l female'])
        self.assertEqual(len(self.amity.living_spaces['female']), 1)
        self.assertEqual(len(self.amity.offices), 1)

    # check invalid names for offices and living spaces
    def test_invalid_names_of_offices_and_living_spaces(self):
        self.amity.create_room(['react female', 'hogwarts p', 'java h male'])
        java = LivingSpace('java')
        react = LivingSpace('React')
        self.assertEqual(len(self.amity.offices), 1)
        self.assertNotIn(java, self.amity.living_spaces['male'])
        self.assertNotIn(react, self.amity.living_spaces['female'])
