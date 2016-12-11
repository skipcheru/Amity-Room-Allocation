from app.amity import Amity
from app.room import Office, LivingSpace
from app.person import Fellow, Staff
import unittest

class TestAddPerson(unittest.TestCase):
    """docstring for TestAddPerson."""
    def setUp(self):
        self.amity = Amity()
        self.fellow1 = Fellow('sam', 'cheru', 'male')
        self.fellow2 = Fellow('ian', 'oti', 'male')
        self.fellow3 = Fellow('jones', 'mbabe', 'male')
        self.fellow4 = Fellow('amina', 'abdi', 'female')
        self.staff1 = Staff('carol', 'radul', 'female')

    #check if error raised if person details arenot strings or is null or incomplete
    def test_error_raised(self):
        self.assertRaises(TypeError, self.amity.add_person(), "error should be raised")
        self.assertRaises(TypeError, self.amity.add_person(1, 3, 'fellow', 'male'), "error should be raised")

    # check if the person added to the system is a fellow
    def test_person_added_is_type_fellow(self):
        self.amity.add_person('sam', 'cheru', 'fellow', 'male', 'N')
        self.assertIsInstance(self.amity.fellows[0]['F001'], Fellow)

    # check if the person added to the system is a staff
    def test_person_added_is_type_staff(self):
        self.amity.add_person('carol', 'radul', 'staff', 'female')
        self.assertIsInstance(self.amity.staffs[0]['S001'], Staff)

    # check if the person is allocated a office
    def test_added_fellow_and_staff_are_allocated_office(self):
        self.amity.create_room('oculus-o')
        staff = Staff('carol', 'radul', 'female')
        fellow = Fellow('sam', 'cheru', 'male')
        self.assertEqual(staff, self.amity.offices[1].occupants[1], 'staff assigned room')
        self.assertIn(fellow, self.amity.offices[1].occupants[0], 'fellow assigned office')

    # check if male fellows are allocated only male livingspaces
    def test_only_male_fellow_allocated_male_living_space(self):
        self.amity.create_room('java-l-m', 'swift-l-f')
        self.amity.add_person('jones', 'mbabe', 'fellow', 'male', 'Y')
        same_fellow = Fellow('jones', 'mbabe', 'male')
        self.assertIn(same_fellow, self.amity.male_living_spaces[0].occupants, 'fellow allocated only male room')
        self.assertFalse(same_fellow in self.amity.female_living_spaces[0].occupants, 'confirm fellow allocated only male room')

    # test if fellow who does not need accommodation are not allocated living rooms
    def test_fellow_who_doesnt_want_accommodation(self):
        self.amity.add_person('ian', 'oti', 'fellow', 'male', 'N')
        fellow_no_living = Fellow('ian', 'oti', 'male')
        self.assertFalse(fellow_no_living in self.amity.male_living_spaces[0].occupants, 'fellow not allocated livingspace')

    # check if the list of fellows has all the fellow added
    def test_no_of_fellows_added(self):
        added_fellows = [{'F001': self.fellow1}, {'F002': self.fellow2}]
        self.assertListEqual(added_fellows,  self.amity.fellows, 'list equal')

    # check if the list of staff has all the staff added
    def test_no_of_fellows_added(self):
        added_staffs = [{'S001': self.staff1}, {'S002': self.staff2}]
        self.assertListEqual(added_staffs,  self.amity.staffs, 'list equal')

    # check if person has been moved to unallocated if all rooms are full or no room
    def test_person_in_unallocated_list(self):
        self.amity.add_person('amina', 'abdi', 'fellow', 'female', 'Y')
        self.assertTrue(self.fellow4 in self.amity.andelans_unallocated_offices, 'fellow in waiting list')
