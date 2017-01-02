from app.amity import Amity
from app.room import Office, LivingSpace
from app.person import Fellow, Staff
import unittest


class TestAddPerson(unittest.TestCase):
    """TestAddPerson Class."""
    def setUp(self):
        self.amity = Amity()
        self.amity.create_room(['oculus office', 'Java l male', 'React l female'])
        self.fellow1 = Fellow('sam', 'cheru', 'male')
        self.fellow2 = Fellow('debbie', 'asila', 'female')
        self.fellow3 = Fellow('jones', 'mbabe', 'male')
        self.fellow4 = Fellow('debbie', 'asila', 'female')
        self.staff1 = Staff('carol', 'radul', 'female')
        self.staff2 = Staff('Janet', 'kamau', 'female')

    # check if the person added to the system is a fellow
    def test_person_added_is_type_fellow(self):
        self.amity.add_person('sam', 'cheru', 'male', 'fellow', 'N')
        self.amity.add_person('debbie', 'asila', 'female', 'fellow', 'Y')
        fellow = list(self.amity.fellows[0].values())
        self.assertEqual(self.fellow1, fellow[0])

    # check if the person added to the system is a staff
    def test_person_added_is_type_staff(self):
        self.amity.add_person('carol', 'radul', 'female', 'staff')
        staff = list(self.amity.staffs[0].values())
        self.assertEqual(self.staff1, staff[0])

    # test if same person is added twice
    def test_person_added_is_not_added_twice(self):
        self.amity.add_person('carol', 'radul', 'female', 'staff')
        self.assertEqual(len(self.amity.staffs), 1)

    # check if the person is allocated a office
    def test_allocate_office_to_fellow_and_staff(self):
        self.amity.add_person('sam', 'cheru', 'male', 'fellow', 'N')
        self.amity.add_person('debbie', 'asila', 'female', 'fellow', 'Y')
        self.amity.add_person('carol', 'radul', 'female', 'staff')
        self.assertEqual(self.fellow1, self.amity.offices[0].occupants[0])
        self.assertEqual(self.staff1, self.amity.offices[0].occupants[2])

    # check if fellows are allocated livingspaces
    def test_allocate_fellow_living_space(self):
        self.amity.add_person('sam', 'cheru', 'male', 'fellow', 'Y')
        self.amity.add_person('debbie', 'asila', 'female', 'fellow', 'Y')
        self.assertEqual(self.fellow1, self.amity.living_spaces['male'][0].occupants[0])
        self.assertEqual(self.fellow4, self.amity.living_spaces['female'][0].occupants[0])

    # test if fellow who does not need accommodation are not allocated living rooms
    def test_allocate_office_only(self):
        self.amity.add_person('ian', 'oti', 'fellow', 'male', 'N')
        fellow_no_living = Fellow('ian', 'oti', 'male')
        self.assertFalse(fellow_no_living in self.amity.living_spaces['male'][0].occupants)

    # check if the list of fellows has all the fellow added
    def test_no_of_fellows_and_staffs_added(self):
        self.assertEqual(len(self.amity.fellows), 2)
        self.assertEqual(len(self.amity.staffs), 1)

    # check if fellow has been moved to unallocated if no living space
    def test_unallocated_living_space(self):
        self.amity.add_person('amina', 'abdi', 'female', 'fellow', 'Y')
        self.amity.add_person('chess', 'dickson', 'male', 'fellow', 'Y')
        self.amity.add_person('njeri', 'thome', 'female', 'fellow', 'Y')
        self.amity.add_person('viola', 'jeruto', 'female', 'fellow', 'Y')
        self.amity.add_person('nchoe', 'soila', 'female', 'fellow', 'Y')

        fellow = Fellow('nchoe', 'soila', 'female')
        self.assertTrue(fellow in self.amity.fellows_unallocated_living_space)

    # check if fellow or staff has been moved to unallocated if no office
    def test_unallocated_offices(self):
        self.amity.add_person('digo', 'halikan', 'male', 'staff')
        fellow = Fellow('viola', 'jeruto', 'female')
        staff = Staff('digo', 'halikan', 'male')

        self.assertTrue(len(self.amity.andelans_unallocated_offices), 2)
        self.assertTrue(fellow in self.amity.andelans_unallocated_offices)
        self.assertTrue(staff in self.amity.andelans_unallocated_offices)
