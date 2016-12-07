import unittest
from app.person import Person, Fellow, Staff
from app.amity import Amity, Room, Office, LivingSpace

class TestAmity(unittest.TestCase):
    """docstring for TestRoom."""
    def setUp(self):
        self.amity  = Amity ()
        self.room = Room('vanhala')

    def test_room(self):
        self.assertIsInstance(self.room, Room, 'room is not an object')

    def test_amity(self):
        self.assertIsInstance(self.amity, Amity)

    def test_create_room(self):
        room = self.amity.create_room('hogwarts', 'vanhala')
        self.assertEqual('hogwarts', self.amity.rooms[0].name, 'Room names dont match')

    def test_no_of_rooms(self):
        self.amity.create_room('php', 'ruby', 'python', 'java')
        no_of_rooms = self.amity.no_of_rooms()
        self.assertEqual(4, no_of_rooms, 'Error does not match')

    def test_add_fellow(self):
        fellow = self.amity.add_person('arya', 'stark', 'FELLOW', 'female')
        staff = self.amity.add_person('king', 'lanister', 'STAFF', 'male')
        self.assertIsInstance(fellow, Fellow, 'message')
        self.assertIsInstance(staff, Staff, 'message')

    def test_list_rooms(self):
        rooms = self.amity.create_room('hogwarts', 'vanhala', 'lime')
        room_names = [room.name for room in self.amity.rooms]
        self.assertEqual(['hogwarts', 'vanhala', 'lime'], room_names , 'rooms dont match')
