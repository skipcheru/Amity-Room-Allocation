from app.room import Room, Office, LivingSpace
from app.person import Fellow, Staff
from abc import abstractmethod
import random
import string

class Amity(object):
    """docstring for Amity."""
    def __init__(self):
        self.staffs = []
        self.fellows = []
        self.fellows_unallocated_living_space = []
        self.andelans_unallocated_offices = []
        self.offices = []
        self.male_living_spaces = []
        self.female_living_spaces = []
        self.set_of_ids = set()

    # create room and add to the list of rooms
    def create_room(self, *room_names):
        '''Test for this method'''
        # check if  error raised if room names are not all strings or empty
        # check if the offices added
        # check if livingspaces added
        # check if the number of male livingspaces and female_living_spaces
        # check the no of offices and livingspaces are equal.
        # check if the list of offices contains only objects of type Office
        # check if the list of living spaces contains objects of type LivingSpace
        # check if error raised if an office exists on the system with the same name


        '''algorithm'''
        #check if room names are all strings
        # for each name the format should be name-o or name-l-m
            # for each name split -
                # if the letter after - is o
                    # create office
                    # add office to list of offices
                # if the letter after - is l
                    # create livingspace
                    # add livingspace to list of livingspaces


    # add person to system
    def add_person(self, first_name, last_name, person_type, gender, accommodation='N'):
        ''''Test for this method'''
        # check if error raised if person details are all not strings
        # check if error raised if person details is null or incomplete
        # check if the person added to the system is a fellow if person type is fellow
        # check if the person added to the system is a staff if person type is staff
        # check if the fellow who wants accommodation is allocated a room
        # check if both the fellow and staff are allocated offices
        # check if male fellows who wants accommodation are allocated only male livingspaces
        # check if female fellows who wants accommodation are allocated only female livingspaces
        # check if the list of fellows has the person added
        # check if the list of staff has the person added
        # check if person has been moved to unallocated if all rooms are full
            # check if offices are full people are moved to unallocated_offices
            # check if livingspaces are full fellow are moved to unallocated_living_space

        '''algorithm'''
        # check if person details are all strings
            # if not
                #raise error
            # if person details is none
                # raise error
            # if type of person is fellow
                # create fellow, add unique id and add fellow to dictionary
                # allocate fellow an office [done by room]
                # if fellow wants accommodation
                    # if fellow is male
                        # allocate the fellow a male livingspace [done by room]
                    # if fellow is female
                        # allocate the fellow a female livingspace
                # else
                    # pass
            # if type of person is staff
                # create fellow, add unique id and add fellow to dictionary
                # allocate fellow an office [done by room]


    def generate_id(self):
        pass

    # reallocates person to another room
    def reallocate_person(self, person_id, room_name):
        ''''Tests for this method'''
        # check if error raised if both params are not strings.
        # check if error raised if both params or one param is empty.
        # check if error raised if the person doesn't exist in the system.
        # check if error raised if the room doesn't exist in the system.
        # check if the person is successfully reallocated to the room specified
        # check if error is raised if person is staff and the room to be allocated is living
        # check if the person above is not reallocated to any room
        # check if error raised if all rooms in amity are full
        # check if the person is reallocated to livingspace
        # >> if the room type is living space and the person has been allocated livingspace
        # check if staff is moved to another office
        # check if fellow is moved to another office
        # check if the room to be reallocated is the same room which the person occupies


        '''algorithm'''
        # check if person id and room name are all strings or null
            # if not
                # raise error
            # if person does not exist in system
                # raise error
            # if room does not exist in system
                # raise error
            # if both exist
                # check person type
                # check room type
                # if room is vacant
                    # if person = fellow and room = livingspace
                        # move fellow to vacant space
                        # remove fellow from previous room
                    # if person = (fellow or fellow) and room = office
                        # move person to vacant office
                        # remove person from previous office
                    # if person = staff and room = livingspace
                        # return error
                # else raise error


    def print_room(self, room_name):
        '''Tests'''
        # check if error raised if room name is null or not strings
        # check if the number of people listed are same as the people in room_name
        # check if prompt is issued if the room is empty
        # check if error is raised if the room does not exist

        '''algorithm'''
        # check if room name is string
            # if not raise error.
        # check if room exists
            # if not
                # raise error
            # else
                # if room has occupants
                    # print all
                # else
                    # prompt room has no occupants

    def load_people(self):
        '''Tests'''
        # check if error is raised if the text if file is emty
        # check if prompt raised and they are not allocated rooms
            # if some lines in the text file does not conform to the format
        # check if all people in the file has been added to the system.
        # check if all both fellows and staff in the file has been allocated offices
        # check if fellows who need living space have been allocated

        '''algorithm'''
        # check if the text if file is emty
            # if true
                # prompt user
            # else
                # for each line check if text format is ok
                    # if ok
                        # add person to system and allocate room
                        # output the list of people added to the system.
                    # if not add to list of errors
                        # output the people not added to the system


    def print_allocations(self):
        '''Tests'''
        # check if prompt is raised no room has been added to the system
        # check if prompt is raised if no room have not been allocated to anyone
        # check if all offices are printed with their respective occupants
        # check if all living spaces for male and female are printed


        '''algorithm'''
        # check if rooms have been added to the system
            # if true
                # print all offices + occupants
                # print all living spaces for male + occupants
                # print all living spaces for female + occupants
                # print all rooms which have no occupants

            # else
                # raise prompt


    def print_unallocated(self):
        '''Tests'''
        # check if the number of people listed equal the lenght of unallocated list
        # check if prompt is issued if there is no people on allocated list

        '''algorithm'''
