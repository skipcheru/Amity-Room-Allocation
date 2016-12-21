#!/usr/bin/env python
"""
This example uses docopt with the built in cmd module to demonstrate an
interactive command application.
Usage:
    amity create_room <name>...
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
    intro = '\n\t++++++++++++++++++++++++++++++++++++++++++++++\n\n' \
            '\tWelcome to Amity Room Application!\n\n' \
            '\tThe Commands For Any Action Are Listed Below\n\n' \
            '\t---------------------------------------------\n'\
            '\ttodo task_name : Create A todo Task \n' \
            '\tdoing task_id  : Start Doing Task \n' \
            '\tdone task_id   : Mark Task Done \n' \
            '\tlist todo      : View Task You Supposed To Do\n' \
            '\tlist doing     : View Task You Are Doing \n' \
            '\tlist done      : View Task You Have Finished\n' \
            '\tlist all       : View All Your Tasks In All Sections\n' \
            '\tquit           : To Exit\n' \
            '\t---------------------------------------------\n\n' \
            '\t+++++++++++++++++++++++++++++++++++++++++++++++++\n'

    prompt = '(Amity App) '
    file = None
    amity = Amity()

    # start functions here
    def create_room(self, name):
        self.amity.create_room(name)

    # start commands here
    @docopt_cmd
    def do_create_room(self, args):
        """Create a todo task. For example todo email Kipngotie at 2pm
        Usage: todo <name>..."""
        self.create_room(args["<name>"])

    def do_quit(self, arg):
        """Quits out of Interactive Mode."""
        print('\nBye Bye! See you soon!\n')
        exit()

# interactive mode
opt = docopt(__doc__, sys.argv[1:])

if opt['--interactive']:
    MyInteractive().cmdloop()

print(opt)
