from app.person import Fellow, Staff
from app.room import LivingSpace
import unittest


class TestLivingSpace(unittest.TestCase):
    """docstring for TestLivingSpace."""
    def setUp(self):
        self.living = LivingSpace('shell')
        self.fellow = Fellow('ian', 'oti', 'male')
        self.staff = Staff('njira', 'persc', 'female')
        self.occupants =[{233: 'obj1'}, {234: 'obj2'}, {235: 'obj3'}, {236: 'obj4'}]

    # def test_living_space_name_error(self):
    #     self.assertRaises(TypeError, LivingSpace(), msg='room name must be string')

    def test_allocate_staff(self):
        error = self.living.add_occupant( {233: self.staff} )
        self.assertRaises(TypeError, error, msg='staff not fellow')

    def test_allocate_fellow(self):
        self.living.add_occupant( {221: self.fellow} )
        self.assertIsNot([], self.living.occupants, msg='list should not be equal')

    def test_allocate_fellow_if_no_vacany(self):
        self.living.occupants = self.occupants
        # add felllow to a room which is not vacant
        add_fellow = self.living.add_occupant( {221: self.fellow} )
        self.assertEqual(add_fellow, 'Sorry! The office is Not Vacant')

    def test_reallocated_fellow_still_exits(self):
        self.living.occupants = self.occupants
        # remove fellow from list of occupants
        self.living.remove_occupant({233: 'obj1'})
        self.assertTrue(self.living.is_fellow_an_occupant({233: 'obj1'}), False)
