#!/usr/bin/env python
"""
This example uses docopt with the built in cmd module to demonstrate an
interactive command application.
Usage:
    amity create_room <name>...
    amity add_person <first_name> <last_name> <gender> <person_type> [<accommodation>]
    amity print_room <room_name>
    amity reallocate_person <person_id> <room_name>
    amity print_all
    amity print_unallocated [<file_name>]
    amity print_allocations [<file_name>]
    amity load_people [<file_name>]
    amity save_state [<db_name>]
    amity load_state [<db_name>]
    amity (-i | --interactive)
    amity (-h | --help | --version)
Options:
    -i, --interactive  Interactive Mode
    -h, --help  Show this screen and exit.
"""

import sys
import cmd
from docopt import docopt, DocoptExit
from app.amity import Amity
from app.database import AmityData


def docopt_cmd(func):
    """
    This decorator is used to simplify the try/except block and pass the result
    of the docopt parsing to the called action.
    """

    def fn(self, arg):
        try:
            opt = docopt(fn.__doc__, arg)

        except DocoptExit as e:
            # The DocoptExit is thrown when the args do not match.
            # We print a message to the user and the usage block.

            print('Invalid Command! Try Another one.')
            print(e)
            return

        except SystemExit:
            # The SystemExit exception prints the usage for --help
            # We do not need to do the print here.

            return

        return func(self, opt)

    fn.__name__ = func.__name__
    fn.__doc__ = func.__doc__
    fn.__dict__.update(func.__dict__)
    return fn


class MyInteractive(cmd.Cmd):
    intro = '\tWelcome to Amity Room Application!\n\n' \
            '\tThe Commands Are Listed Below\n\n' \
            '\t---------------------------------------------\n'\
            '\tCreate Rooms        : create_room names \n' \
            '\tAdd Person          : add_person <f_name> <l_name> <gender> <type> [<accommodation>] \n' \
            '\tView Room Occupants : print_allocations  [<accommodation>]     \n' \
            '\tView All People     : print_all     \n' \
            '\tPrint Room Details  : print_room <room_name>   \n' \
            '\tView unallocated    : print_unallocated  [<file_name>] \n' \
            '\tReallocate Person   : reallocate_person <person_id> <room_name>   \n' \
            '\tLoad People List    : load_people [<file_name>]   \n' \
            '\tSave App state      : save_state [<db_name>]  \n' \
            '\tLoad App state      : load_state [<db_name>]  \n' \
            '\tquit                : To Exit\n' \
            '\t---------------------------------------------\n\n'


    prompt = '(Amity App) '
    file = None
    amity = Amity()
    amity_data = AmityData()

    # start commands here
    @docopt_cmd
    def do_create_room(self, args):
        """Create Rooms. Usage: create_room <name>..."""

        names = args['<name>']
        rooms = ' '.join(names)
        self.amity.create_room(rooms.split(','))

    @docopt_cmd
    def do_add_person(self, args):
        """Usage: add_person <first_name> <last_name> <gender> <person_type>
         [<accommodation>]"""

        first_name = args['<first_name>']
        last_name = args['<last_name>']
        gender = args['<gender>']
        person_type = args['<person_type>']
        accomm = args['<accommodation>']

        if accomm:
            self.amity.add_person(first_name, last_name, gender, person_type, accomm)
        else:
            self.amity.add_person(first_name, last_name, gender, person_type)


    @docopt_cmd
    def do_print_room(self, args):
        """Usage: print_room <room_name>"""

        room_name = args['<room_name>']
        self.amity.print_room(room_name)

    @docopt_cmd
    def do_print_unallocated(self, args):
        """Usage: print_unallocated [<file_name>]"""
        file_name = args['<file_name>']

        self.amity.print_unallocated(file_name)

    @docopt_cmd
    def do_print_allocations(self, args):
        """Usage: print_allocations [<file_name>]"""
        file_name = args['<file_name>']

        self.amity.print_allocations(file_name)

    @docopt_cmd
    def do_reallocate_person(self, args):
        """Usage: reallocate_person <person_id> <room_name>"""

        person_id = args['<person_id>']
        room_name  = args['<room_name>']

        print(self.amity.reallocate_person(person_id, room_name))

    @docopt_cmd
    def do_print_all(self, args):
        """Usage: print_all """

        self.amity.print_all_people()

    @docopt_cmd
    def do_load_people(self, args):
        """Usage: load_people [<file_name>] """
        file_name = args['<file_name>']

        self.amity_data.load_people(file_name)

    @docopt_cmd
    def do_save_state(self, args):
        """Usage: save_state [<db_name>]"""
        db_name = args['<db_name>']

        AmityData(db_name).save_state()

    @docopt_cmd
    def do_load_state(self, args):
        """Usage: load_state [<db_name>]"""
        db_name = args['<db_name>']

        AmityData(db_name).load_state()

    def do_quit(self, arg):
        """Quits out of Interactive Mode."""
        print('\nBye Bye!\n')
        exit()

# interactive mode
opt = docopt(__doc__, sys.argv[1:])

if opt['--interactive']:
    MyInteractive().cmdloop()

print(opt)
