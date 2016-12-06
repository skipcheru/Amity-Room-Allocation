from app.person import Fellow, Staff
from app.room import LivingSpace
import unittest


class TestLivingSpace(unittest.TestCase):
    """docstring for TestLivingSpace."""
    def setUp(self):
        self.living = LivingSpace('shell')
        self.fellow = Fellow('ian', 'oti', 'male')
        self.staff = Staff('njira', 'persc', 'female')

    def test_living_space(self):
        self.assertNotIsInstance(None, LivingSpace, 'Object not an instance of LivingSpace')

    def test_living_space_raise_error(self):
        error = self.living.add_occupant(self.staff)
        self.assertRaises(TypeError, error, 'error should be raised')
