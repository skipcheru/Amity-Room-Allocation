from app.amity import Amity
from app.room import Office, LivingSpace
from app.person import Fellow, Staff
import unittest

class TestReallocatePerson(unittest.TestCase):
    """docstring for TestReallocatePerson."""
    def setUp(self):
        self.amity = Amity()

    # check if error raised if both params are not strings.
    def test_error_raised(self):
        self.assertRaises(TypeError, self.amity.reallocate_person())
        self.assertRaises(TypeError, self.amity.reallocate_person(123, 'nania'))

    # check if error raised if the person doesn't exist in the system.
    def test_reallocate_unknown_person(self):
        unknown_person_error = self.amity.reallocate_person('F101', 'Oculus')
        self.assertEqual('person has not been added to the system', unknown_person_error)

    # check if error raised if the room doesn't exist in the system.
    def test_reallocate_unknown_room(self):
        unknown_room_error = self.amity.reallocate_person('F001', 'room')
        self.assertEqual('the room is not in the system', unknown_room_error)

    # check if error is raised if person is staff and the room to be allocated is living
    def test_reallocate_staff_to_livingspace(self):
        self.amity.create_room('nania-o', 'peri-l-m', 'oculus-o', 'swift-l-f')
        self.amity.add_person('carol', 'radul', 'staff', 'female')
        reallocate_staff = self.amity.reallocate_person('S001', 'peri')
        self.assertEqual('staff cannot be reallocated to living room', reallocate_staff)

    # check if the person above is not reallocated to the specified room
    def test_staff_not_reallocated_to_living_space(self):
        staff = Staff('carol', 'radul', 'female')
        self.assertFalse(staff in self.amity.female_living_spaces[0].occupants)

    # check if fellow is reallocated to another livingspace
    def test_reallocte_fellow(self):
        # add ivy to system and create new female livingspace
        self.amity.add_person('ivy', 'osodo', 'fellow', 'female')
        self.amity.create_room('react-l-f')
        fellow = Fellow('ivy', 'osodo', 'female', 'Y')
        self.amity.reallocate_person('F001', 'react') # assume carol was allocated office Nania initially
        self.assertIn(fellow, self.amity.female_living_spaces[1].occupants, 'Felllow reallocated from Swift to React livingspace')

    # check if staff is moved to another office
    def test_reallocte_staff(self):
        carol = Staff('carol', 'radul', 'female')
        self.amity.reallocate_person('S001', 'oculus') # assume carol was allocated office Nania initially
        self.assertIn(carol, self.amity.offices[1].occupants, 'carol reallocated to office Oculus')
        self.assertFalse(carol in self.amity.offices[0].occupants, 'carol is not in office Nania')

    # check if error raised if all rooms in amity are full
    def test_reallocte_if_all_rooms_are_full(self):
        self.amity.create_room('krypton-o')
        # assert all offices are not vacant
        self.amity.offices[0].is_vacant = False
        self.amity.offices[1].is_vacant = False
        self.amity.offices[2].is_vacant = False

        reallocate_carol = self.amity.reallocate_person('S001', 'krypton')
        self.assertTrue(len(self.amity.offices[2].occupants) is 4, 'message')
        self.assertEqual('All offices not vacant curently.', reallocate_carol)

    # check if the room to be reallocated is the same room which the person occupies
    def test_reallocate_room_occupant_to_same_room(self):
        reallocate_again_carol = self.amity.reallocate_person('S001', 'krypton')
        self.assertTrue(len(self.amity.offices[2].occupants) is 4, 'message')
        self.assertEqual('Person is already an occupant of this room.', reallocate_again_carol)
