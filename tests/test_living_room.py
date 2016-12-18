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

        
