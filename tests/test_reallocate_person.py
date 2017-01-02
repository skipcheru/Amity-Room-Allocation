from app.amity import Amity
from app.room import Office, LivingSpace
from app.person import Fellow, Staff
import unittest


class TestReallocatePerson(unittest.TestCase):
    """Tests for Reallocate Person."""
    def setUp(self):
        self.amity = Amity()
        self.amity.create_room(['oculus o', 'nania o', 'peri l male', 'react l female'])

        self.staff = Staff('carol', 'radul', 'female')
        self.fellow = Fellow('Sam', 'Kip', 'male')
        self.fellow2 = Fellow('Ivy', 'osodo', 'female')

    # check if error raised if the person doesn't exist in the system.
    def test_reallocate_unknown_person(self):
        unknown_person = self.amity.reallocate_person('F101', 'oculus')
        self.assertEqual(unknown_person, 'The person is not on the system')

    # check if error raised if the room doesn't exist in the system.
    def test_reallocate_unknown_room(self):

        self.amity.fellows.append({'F001': self.fellow})
        unknown_room = self.amity.reallocate_person('F001', 'room')
        self.assertEqual('The room is not on the system', unknown_room)

    # check if error is raised if person is staff and
    # the room to be allocated is living
    def test_reallocate_staff_to_livingspace(self):
        self.amity.staffs.append({'S001': self.staff})
        self.amity.offices[0].occupants.append(self.staff)

        reallocate_staff = self.amity.reallocate_person('S001', 'Peri')
        error_msg = 'Sorry staff cannot be allocated livingspace'
        self.assertEqual(error_msg, reallocate_staff)

    # check if staff above is not reallocated to the living space
    def test_staff_not_reallocated_to_living_space(self):

        self.assertFalse(self.staff in self.amity.living_spaces['male'][0].occupants)

    # check if fellow is reallocated to another livingspace
    def test_reallocte_fellow(self):
        self.amity.living_spaces['female'][0].occupants.append(self.fellow2)
        self.amity.reallocate_person('F002', 'react')
        self.assertTrue(self.fellow2 in self.amity.living_spaces['female'][0].occupants)

    # check if staff is reallocated to another office
    def test_reallocte_staff(self):
        self.amity.reallocate_person('S001', 'oculus')
        self.amity.reallocate_person('S001', 'nania')
        self.assertFalse(self.staff in self.amity.offices[0].occupants)
        self.assertTrue(self.staff in self.amity.offices[1].occupants)
        # check if person is reallocated to same room
        reallocate_again = self.amity.reallocate_person('S001', 'nania')
        self.assertEqual('Sorry Person is already an occupant of this room'
                         , reallocate_again)

    # check if the male fellow is not reallocated to female living_space and vice versa
    def test_reallocte_male_and_female_fellows(self):
        # add male fellow to system
        self.amity.fellows.append({'F001': self.fellow})
        self.amity.fellows.append({'F002': self.fellow2})
        # reallocate male to female living space and vice versa
        male_error = self.amity.reallocate_person('F002', 'peri')
        female_error = self.amity.reallocate_person('F001', 'react')

        self.assertFalse(self.fellow in self.amity.living_spaces['female'][0].occupants)
        self.assertFalse(self.fellow2 in self.amity.living_spaces['male'][0].occupants)
