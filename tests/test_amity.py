from app.amity import Amity
from app.room import Office, LivingSpace
from app.person import Fellow, Staff
import unittest


class TestAddPerson(unittest.TestCase):
    """TestAddPerson Class."""
    def setUp(self):
        self.amity = Amity()
        self.amity.create_room('oculus', 'office')
        self.amity.create_room('Java', 'l', 'male')
        self.amity.create_room('React', 'l', 'female')

        self.fellow = Fellow('sam', 'cheru', 'male')
        self.staff = Staff('carol', 'radul', 'female')

    # check if the person added to the system is a fellow
    def test_person_added_is_type_fellow(self):
        self.amity.add_person('sam', 'cheru', 'male', 'fellow', 'N')
        self.amity.add_person('debbie', 'asila', 'female', 'fellow', 'Y')
        fellow = list(self.amity.fellows[0].values())
        self.assertEqual(self.fellow, fellow[0])

    # check if the person added to the system is a staff
    def test_person_added_is_type_staff(self):
        self.amity.add_person('carol', 'radul', 'female', 'staff')
        staff = list(self.amity.staffs[0].values())
        self.assertEqual(self.staff, staff[0])
        self.assertEqual(len(self.amity.staffs), 1)

    # test if same person is not added twice and error is raised
    def test_person_added_is_not_added_twice(self):
        self.amity.add_person('carol', 'radul', 'female', 'staff')
        error = self.amity.add_person('carol', 'radul', 'female', 'staff')
        self.assertEqual(error, 'carol radul already exists')
        self.assertEqual(len(self.amity.staffs), 1)

    # check if the person is allocated a office
    def test_allocate_office_to_fellow_and_staff(self):
        self.amity.add_person('sam', 'cheru', 'male', 'fellow', 'N')
        self.amity.add_person('debbie', 'asila', 'female', 'fellow', 'Y')
        self.amity.add_person('carol', 'radul', 'female', 'staff')
        self.assertEqual(self.fellow, self.amity.rooms['office'][0].occupants[0])
        self.assertIn(self.staff, self.amity.rooms['office'][0].occupants)

    # check if fellows are allocated livingspaces
    def test_allocate_fellow_living_space(self):
        self.amity.add_person('sam', 'cheru', 'male', 'fellow', 'Y')
        self.amity.add_person('debbie', 'asila', 'female', 'fellow', 'Y')
        fellow = Fellow('debbie', 'asila', 'female')
        self.assertEqual(self.fellow, self.amity.rooms['male'][0].occupants[0])
        self.assertEqual(fellow, self.amity.rooms['female'][0].occupants[0])

    # test if fellow who does not need accommodation are not allocated living rooms
    def test_allocate_office_only(self):
        self.amity.add_person('sam', 'cheru', 'male', 'fellow', 'N')
        self.assertFalse(self.fellow in self.amity.rooms['male'][0].occupants)

    # check if fellow has been moved to unallocated if no living space
    def test_unallocated_living_space(self):
        self.amity.add_person('amina', 'abdi', 'female', 'fellow', 'Y')
        self.amity.add_person('chess', 'nyambura', 'female', 'fellow', 'Y')
        self.amity.add_person('njeri', 'thome', 'female', 'fellow', 'Y')
        self.amity.add_person('viola', 'jeruto', 'female', 'fellow', 'Y')
        self.amity.add_person('nchoe', 'soila', 'female', 'fellow', 'Y')

        fellow = Fellow('nchoe', 'soila', 'female')
        self.assertTrue(fellow in self.amity.fellows_unallocated_living_space)

    # check if fellow or staff has been moved to unallocated if no office
    def test_unallocated_offices(self):
        self.amity.add_person('amina', 'abdi', 'female', 'fellow', 'Y')
        self.amity.add_person('chess', 'nyambura', 'female', 'fellow')
        self.amity.add_person('njeri', 'thome', 'female', 'fellow', 'Y')
        self.amity.add_person('thumbi', 'njoroge', 'male', 'fellow')
        self.amity.add_person('mercy', 'adunga', 'female', 'staff')
        self.amity.add_person('nchoe', 'soila', 'female', 'fellow', 'Y')
        self.amity.add_person('viola', 'jeruto', 'female', 'fellow')
        self.amity.add_person('digo', 'halikan', 'male', 'staff')

        fellow = Fellow('viola', 'jeruto', 'female')
        staff = Staff('digo', 'halikan', 'male')

        self.assertTrue(len(self.amity.andelans_unallocated_offices), 2)
        self.assertTrue(fellow in self.amity.andelans_unallocated_offices)
        self.assertTrue(staff in self.amity.andelans_unallocated_offices)

class TestCreateRoom(unittest.TestCase):
    """Test Create Rooms."""
    def setUp(self):
        self.amity = Amity()

    def test_office_created(self):
        self.amity.create_room('Nania', 'office')
        self.assertEqual(len(self.amity.rooms['office']), 1)

    # check if the living spaces added
    def test_living_space_created(self):
        self.amity.create_room('shell', 'l', 'female')
        self.amity.create_room('java', 'l', 'male')
        self.assertEqual(len(self.amity.rooms['male']), 1)
        self.assertEqual(len(self.amity.rooms['female']), 1)
        self.assertIsInstance(self.amity.rooms['male'][0], LivingSpace)

    # check if an office on the system with the same name is created again
    def test_existing_room_not_added(self):
        self.amity.create_room('shell', 'l', 'female')
        name_error = self.amity.create_room('shell', 'l', 'female')
        self.assertEqual(len(self.amity.rooms['female']), 1)
        self.assertEqual(name_error, 'shell already exists')

    # check invalid names for offices and living spaces
    def test_invalid_names_of_offices_and_rooms(self):
        invalid_name = self.amity.create_room('java', 'h', 'male')
        self.assertEqual(invalid_name, 'Invalid room type')

class TestReallocatePerson(unittest.TestCase):
    """Tests for Reallocate Person."""
    def setUp(self):
        self.amity = Amity()
        self.amity.create_room('oculus', 'o')
        self.amity.create_room('nania', 'office')
        self.amity.create_room('peri', 'l', 'male')
        self.amity.create_room('react', 'l', 'female')

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
        self.amity.rooms['office'][0].add_occupant(self.staff)

        reallocate_staff = self.amity.reallocate_person('S001', 'Peri')
        error_msg = 'Sorry staff cannot be allocated livingspace'
        self.assertEqual(error_msg, reallocate_staff)
        self.assertFalse(self.staff in self.amity.rooms['male'][0].occupants)

    # check if fellow is reallocated to another livingspace
    def test_reallocte_fellow(self):
        self.amity.rooms['female'][0].add_occupant(self.fellow2)
        self.amity.reallocate_person('F002', 'react')
        self.assertTrue(self.fellow2 in self.amity.rooms['female'][0].occupants)

    # check if staff is reallocated to another office
    def test_reallocte_staff(self):
        self.amity.staffs.append({'S001': self.staff})
        self.amity.rooms['office'][0].add_occupant(self.staff)
        self.amity.reallocate_person('S001', 'nania')
        self.assertFalse(self.staff in self.amity.rooms['office'][0].occupants)
        self.assertTrue(self.staff in self.amity.rooms['office'][1].occupants)
        # check if person is reallocated to same room
        reallocate_again = self.amity.reallocate_person('S001', 'nania')
        self.assertEqual('Sorry Person is already an occupant of this room'
                         , reallocate_again)

    # check if the male fellow is not reallocated to female living_space and vice versa
    def test_reallocte_male_and_female_fellows(self):
        # add male and female fellow to system
        self.amity.fellows.append({'F001': self.fellow})
        self.amity.fellows.append({'F002': self.fellow2})
        print(self.amity.rooms['female'][0].name)
        print(self.amity.rooms['male'][0].name)

        # reallocate male to female living space and vice versa
        male_error = self.amity.reallocate_person('F002', 'peri')
        female_error = self.amity.reallocate_person('F001', 'react')

        response1 = 'Sorry female fellow cannot be reallocated to male livingspace'
        response2 = 'Sorry male fellow cannot be reallocated to female livingspace'

        self.assertEqual(male_error, response1)
        self.assertEqual(female_error, response2)

        self.assertFalse(self.fellow in self.amity.rooms['female'][0].occupants)
        self.assertFalse(self.fellow2 in self.amity.rooms['male'][0].occupants)
