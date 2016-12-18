from app.amity import Amity
from app.room import Office, LivingSpace
from app.person import Fellow, Staff
import unittest

class TestPrintRoom(unittest.TestCase):
    """docstring for TestPrintRoom."""
    def setUp(self):
        self.amity = Amity()

    def test_error_raised(self):
        self.assertRaises(TypeError, self.amity.print_room())
        self.assertRaises(TypeError, self.amity.print_room(123))

    def test_empty_room(self):
        self.amity.create_room('lime-o')
        self.assertEqual('This room has no occupants', self.amity.print_room('lime'))

    def test_non_existent_room(self):
        self.assertEqual('This room does not exist', self.amity.print_room('spire'))

    def test_room_occupants_printed(self):
        self.amity.add_person('dindi', 'jane', 'staff', 'female')
        self.amity.add_person('mustafa', 'salim', 'fellow', 'male')
