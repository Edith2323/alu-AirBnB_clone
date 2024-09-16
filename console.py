#!/usr/bin/python3
"""console"""

import cmd
from os import system
import sys
from models.base_model import BaseModel
from models.user import User
from models.engine.file_storage import FileStorage
from models.user import User
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
import re

# models class stored in dict for easier access.
classes = {
    "BaseModel": BaseModel,
    "User": User,
    "City": City,
    "Place": Place,
    "Review": Review,
    "State": State,
    "Amenity": Amenity
}


class HBNBCommand(cmd.Cmd):
    """Command processor for ALU-AirBnB project"""

    prompt = '(hbnb) '
    ruler = '-'

    def default(self, line):
        """Default method for handling dot notation commands."""

        if "." in line:
            command = line.split(".")
            if command[1] == "all()":
                self.do_all(command[0])

            elif command[1] == "count()":
                self.do_count(command[0])

            elif command[1].startswith("show("):
                self.do_show(command[0] + " " + command[1][6:-2])

            elif command[1].startswith("destroy("):
                self.do_destroy(command[0] + " " + command[1][9:-2])

            elif command[1].startswith("update("):
                command_pattern = re.compile(r"update\((.+)\)")
                command_result = command_pattern.search(line).group()

                id_pattern = re.compile(
                    r"[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}"
                    r"-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}"
                )
                id = id_pattern.search(command_result).group() if id else None

                dict_repr_pattern = re.compile(r"{.+}")
                dict_repr = dict_repr_pattern.search(line)
                if dict_repr:
                    dict_repr = eval(dict_repr.group())
                    for key, value in dict_repr.items():
                        param_to_pass = f"{command[0]} {id} {key} {value}"
                        self.do_update(param_to_pass)
                else:
                    params = command_result[7:-1].split(",")
                    if any([len(param.split()) == 1 for param in params]):
                        print("Insert spaces after commas to divide parameters.")
                        return
                    attr = params[1][2:-1]
                    value = eval(params[2][1:]) if params[2].strip().isdigit() else params[2][1:]
                    param_to_pass = f"{command[0]} {id} {attr} {value}"
                    self.do_update(param_to_pass)
            else:
                print("*** Unknown syntax: {}".format(line))
        else:
            print("*** Unknown syntax: {}".format(line))

    def do_EOF(self, line):
        return True

    def do_quit(self, arg):
        return True
    do_q = do_quit

    def help_quit(self):
        print("Quit command to exit the program")

    def help_EOF(self):
        print("EOF command to exit the program")

    def help_help(self):
        print("Help command to print help information about a command")

    def emptyline(self):
        pass

    def do_clear(self, arg):
        system('cls')

    def do_create(self, cls):
        if not cls:
            print("** class name missing **")
        elif cls not in classes.keys():
            print("** class doesn't exist **")
        else:
            new_model = classes[cls]()
            new_model.save()
            print(new_model.id)

    def help_create(self):
        print("Create command to create a new instance of a class")
        print("Usage: create <class name>")

    def do_show(self, cls_and_id):
        if not cls_and_id:
            print("** class name missing **")
            return
        elif len(cls_and_id.split()) == 1:
            print("** instance id missing **")
            return
        elif cls_and_id.split()[0] not in classes.keys():
            print("** class doesn't exist **")
            return

        user_key = f"{cls_and_id.split()[0]}.{cls_and_id.split()[1]}"
        storage = FileStorage()
        storage.reload()
        all_objects = storage.all()

        if user_key in all_objects.keys():
            print(all_objects[user_key])
        else:
            print("** no instance found **")

    def help_show(self):
        print("Show command to print the string representation of an instance")
        print("Usage: show <class name> <id>")

    def do_destroy(self, cls_and_id):
        if not cls_and_id:
            print("** class name missing **")
            return
        elif len(cls_and_id.split()) == 1:
            print("** instance id missing **")
            return
        elif cls_and_id.split()[0] not in classes.keys():
            print("** class doesn't exist **")
            return

        user_key = f"{cls_and_id.split()[0]}.{cls_and_id.split()[1]}"
        storage = FileStorage()
        storage.reload()
        all_objects = storage.all()

        if user_key in all_objects.keys():
            del all_objects[user_key]
            storage.save()
            print("Destroyed successfully!")
        else:
            print("** no instance found **")

    def help_destroy(self):
        print("Destroy command to delete an object from storage")
        print("Usage: destroy <class name> <id>")

    def do_all(self, cls):
        storage = FileStorage()
        storage.reload()
        all_objects = storage.all()
        if not cls:
            print([str(obj) for obj in all_objects.values()])
        elif cls not in classes.keys():
            print("** class doesn't exist **")
        else:
            print([str(obj) for key, obj in all_objects.items()
                   if key.split('.')[0] == cls])

    def help_all(self):
        print("All command to print all string representation of all instances")
        print("Usage: all or all <class name>")

    def do_update(self, args):
        args_split = args.split()
        if len(args_split) < 4:
            if len(args_split) == 1:
                print("** instance id missing **")
            elif len(args_split) == 2:
                print("** attribute name missing **")
            elif len(args_split) == 3:
                print("** value missing **")
        else:
            cls_name, obj_id, attr_name, attr_value = args_split[:4]
            storage = FileStorage()
            storage.reload()
            all_objects = storage.all()
            user_key = f"{cls_name}.{obj_id}"

            if cls_name not in classes.keys():
                print("** class doesn't exist **")
                return
            if user_key not in all_objects.keys():
                print("** no instance found **")
                return

            obj = all_objects[user_key]
            setattr(obj, attr_name, attr_value)
            obj.save()

    def help_update(self):
        print("Update command to update an attribute of an object")
        print("Usage: update <class name> <id> <attr name> <attr value>")

    def do_count(self, cls):
        storage = FileStorage()
        storage.reload()
        all_objects = storage.all()
        if cls in classes.keys():
            print(len([obj for key, obj in all_objects.items()
                       if key.split('.')[0] == cls]))
        else:
            print("** class doesn't exist **")


if __name__ == '__main__':
    HBNBCommand().cmdloop()
