
from app.room import Office, LivingSpace
from app.person import Fellow, Staff
import unittest

class TestRoom(unittest.TestCase):
    """docstring for TestRoom."""
    def setUp(self):
        self.office = Office('mac')
        self.living = LivingSpace('ubuntu')

    def test_add_occupant(self):
        self.office.add_occupant('bob')
        self.living.add_occupant('brio')
        self.assertEqual(len(self.office.occupants), 1)
        self.assertEqual(len(self.living.occupants), 1)

    def test_remove_occupant(self):
        self.office.add_occupant('bob')
        self.assertEqual(len(self.office.occupants), 1)
        self.office.remove_occupant('bob')
        self.assertEqual(len(self.office.occupants), 0)

    def test_office_capacity(self):
        self.office.add_occupant('lewy')
        self.office.add_occupant('rose')
        self.office.add_occupant('jane')
        self.office.add_occupant('ann')
        self.office.add_occupant('subi')
        self.office.add_occupant('steve')
        self.office.add_occupant('kim')

        self.assertEqual(len(self.office.occupants), 6)

    def test_living_capacity(self):
        self.living.add_occupant('bob')
        self.living.add_occupant('don')
        self.living.add_occupant('jane')
        self.living.add_occupant('ann')
        self.living.add_occupant('jude')

        self.assertEqual(len(self.living.occupants), 4)
