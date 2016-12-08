from app.person import Fellow, Staff
from app.room import Office
import unittest


class Testoffice(unittest.TestCase):
    """docstring for Testoffice."""
    def setUp(self):
        self.office = Office('Oculus')
        self.fellow = Fellow('sam', 'cheru', 'male')
        self.staff = Staff('angie', 'mugo', 'female')
        self.occupants =[{200: 'fellow'}, {230: 'fellow2'}, {235: 'staff2'}, {133: 'staff1'}]

    def test_allocate_staff(self):
        self.office.add_occupant( {233: self.staff} )
        self.assertListEqual([{233: 'obj1'}], self.office.occupants, msg='list same')

    def test_allocate_fellow(self):
        self.office.add_occupant( {221: self.fellow} )
        self.assertIsNot([], self.office.occupants, msg='list should not be equal')
        self.assertListEqual([{221: self.fellow}, {233: self.staff}], self.office.occupants, msg='list same')

    def test_allocate_staff_if_no_vacany(self):
        self.office.occupants = self.occupants
        # add staff to a room which is not vacant
        add_staff = self.office.add_occupant({908: self.fellow})
        self.assertEqual(add_staff, 'Sorry! The office is Not Vacant')

    def test_reallocated_person_still_exits(self):
        self.office.occupants = self.occupants
         # remove fellow from list of occupants
        self.office.remove_occupant({200: 'fellow'})
        self.assertTrue(self.office.is_person_an_occupant({200: 'fellow'}), False)
