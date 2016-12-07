import unittest
from app.person import Person, Fellow, Staff
from app.amity import Amity, Room, Office, LivingSpace

class TestAmity(unittest.TestCase):
    """docstring for TestRoom."""
    def setUp(self):
        self.amity  = Amity ()
        self.room = Room('vanhala')

    def test_create_office(self):
        # test number of rooms in amity and rooms created
        self.amity.create_room('hogwarts-o', 'vanhala-o' 'ruby-l')
        self.assertEqual('hogwarts', self.amity.offices.[0].name, 'Room names dont match')

        office_names = [room.name for room in self.amity.offices]
        self.assertListEqual(['hogwarts', 'vanhala', 'ruby'], office_names , 'offices dont match')
        self.assertNotEqual('php', office_names[0], 'No office called php')

    def test_create_living(self):
        # test number of rooms in amity and rooms created
        self.amity.create_room('java-l', 'ruby-l', 'python-l')
        self.assertEqual(3, self.amity.living_spaces, 'does not match')
        living_spaces_names = [room.name for room in self.amity.living_spaces]
        self.assertListEqual(['ruby', 'python', 'java'], living_spaces_names , 'rooms dont match')
        self.assertNotEqual('hogwarts', living_spaces_names[1], 'No living room called hogwarts')


    def test_add_person(self):
        fellow = self.amity.add_person('arya', 'stark', 'FELLOW', 'female')
        staff = self.amity.add_person('king', 'lanister', 'STAFF', 'male')
        self.assertIsInstance(fellow, Fellow, 'message')
        self.assertIsInstance(staff, Staff, 'message')
        self.assertEqual(1, len(self.amity.fellows), 'One fellow added only')
        self.assertEqual(1, len(self.amity.staffs), 'One staff added only')
