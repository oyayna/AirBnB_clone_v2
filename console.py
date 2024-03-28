#!/usr/bin/python3
# console.py

import cmd
import sys
from models import storage
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review


class HBNBCommand(cmd.Cmd):
    prompt = "(hbnb)" if sys.__stdin__.isatty() else ""
    classes = {
        "BaseModel": BaseModel,
        "User": User,
        "State": State,
        "City": City,
        "Amenity": Amenity,
        "Place": Place,
        "Review": Review,
    }  # Add other classes as needed

    def preloop(self):
        """Prints if isatty is false"""
        if not sys.__stdin__.isatty():
            print("(hbnb)")

    def emptyline(self):
        """Overrides the emptyline method of CMD"""
        pass

    def do_quit(self, arg):
        """Quit command to exit the program"""
        return True

    def do_EOF(self, arg):
        """EOF command to exit the program"""
        print()  # Print a newline for better appearance
        return True

    def do_help(self, arg):
        """Help command to display help information"""
        cmd.Cmd.do_help(self, arg)

    # def do_create(self, arg):
    #     """Create a new instance of BaseModel, save it, and print the id"""
    #     if not arg:
    #         print("** class name missing **")
    #         return
    #     elif arg not in self.classes:
    #         print("** class doesn't exist **")
    #         return
    #     instance = self.classes[arg]()
    #     instance.save()
    #     print(instance.id)

    def do_create(self, arg):
        """Create a new instance with given parameters, save it, and print the id"""
        if not arg:
            print("** class name missing **")
            return

        args_list = arg.split()
        class_name = args_list[0]
        if class_name not in self.classes:
            print("** class doesn't exist **")
            return
        params = {}
        for param in args_list[1:]:
            key_value = param.split("=")
            if len(key_value) != 2:
                print(f"Invalid parameter: {param}. Skipping...")
                continue
            key, value = key_value
            params[key] = value.replace("_", " ").replace('"', "")
        try:
            instance = self.classes[class_name](**params)
            instance.save()
            print(instance.id)
        except Exception as e:
            print(f"Error creating instance: {e}")

    def do_show(self, arg):
        """Print the string representation of an instance"""
        args = arg.split()
        if not args:
            print("** class name missing **")
            return
        elif args[0] not in self.classes:
            print("** class doesn't exist **")
            return
        if len(args) < 2:
            print("** instance id missing **")
            return
        key = f"{args[0]}.{args[1]}"
        objects = storage.all()
        if key not in objects:
            print("** no instance found **")
        else:
            print(objects[key])

    def do_all(self, arg):
        """Print all string representations of instances"""
        objects = storage.all()
        if arg and arg not in self.classes:
            print("** class doesn't exist **")
            return
        else:
            result = [
                str(value)
                for value in objects.values()
                if not arg or value.__class__.__name__ == arg
            ]
        print(result)

    def do_update(self, arg):
        """Update an instance based on the class name and id"""
        args = arg.split()
        if not args:
            print("** class name missing **")
            return
        elif args[0] not in self.classes:
            print("** class doesn't exist **")
            return
        if len(args) < 2:
            print("** instance id missing **")
            return
        key = f"{args[0]}.{args[1]}"
        objects = storage.all()
        if key not in objects:
            print("** no instance found **")
            return
        if len(args) < 3:
            print("** attribute name missing **")
            return
        if len(args) < 4:
            print("** value missing **")
            return
        attribute = args[2]
        value = args[3]
        try:
            value = eval(value)
        except (NameError, SyntaxError):
            pass
        setattr(objects[key], attribute, value)
        objects[key].save()

    def do_destroy(self, arg):
        """Delete an instance based on the class name and id"""
        args = arg.split()
        if not args:
            print("** class name missing **")
            return
        elif args[0] not in self.classes:
            print("** class doesn't exist **")
            return
        if len(args) < 2:
            print("** instance id missing **")
            return
        key = f"{args[0]}.{args[1]}"
        objects = storage.all()
        if key not in objects:
            print("** no instance found **")
        else:
            del objects[key]
            storage.save()

    def default(self, line):
        """
        Called on an input line when the command prefix is not recognized.
        If this method is not overridden, it prints an error message and returns.
        """
        try:
            class_name, cmd = line.split(".", 1)

            if cmd == "all()" and class_name in self.classes:
                objects = storage.all()
                # Retrieve all instances for the specified class
                result = [
                    str(value)
                    for value in objects.values()
                    if value.__class__.__name__ == class_name
                ]
                print(result)
                return
            elif cmd == "count()" and class_name in self.classes:
                # Retrieve the count of instances for the specified class
                count = sum(
                    1
                    for value in storage.all().values()
                    if value.__class__.__name__ == class_name
                )
                print(count)
                return
            elif cmd[0:4] == "show" and class_name in self.classes:
                objects = storage.all()
                instance = None
                for value in objects.values():
                    if value.id == cmd[6:-2] and value.__class__:
                        instance = value
                        break
                if instance:
                    print(str(instance))
                else:
                    print("** no instance found **")
                return
            elif cmd[0:7] == "destroy" and class_name in self.classes:
                objects = storage.all()
                key = f"{class_name}.{cmd[9:-2]}"
                if key in objects:
                    del objects[key]
                    storage.save()
                else:
                    print("** no instance found **")
                return
            elif cmd[0:6] == "update" and class_name in self.classes:
                words = cmd.split()

                if class_name not in self.classes:
                    print("** class doesn't exist **")
                    return

                cmd3 = words[0].strip('update("),')

                if (words[0] == "update()" or 'update("")') and not cmd3:
                    print("** instance id missing **")
                    return

                objects = storage.all()
                key = f"{class_name}.{cmd3}"

                if not key in objects:
                    print("** no instance found **")
                    return

                if len(words) < 2:
                    print("** attribute name missing **")
                    return

                if len(words) < 3:
                    print("** value missing **")
                    return

                cmd1 = words[1].strip('",')
                cmd2 = words[2].strip('(")')
                if cmd2.isdigit():
                    val = cmd2
                    try:
                        val = eval(val)
                    except (NameError, SyntaxError):
                        pass
                    setattr(objects[key], cmd1, val)
                    objects[key].save()
                else:
                    setattr(objects[key], cmd1, cmd2)
                    objects[key].save()
                return

            else:
                print("** class doesn't exist **")
                return

        except Exception as e:
            pass
        print("*** Unknown syntax:", line)


if __name__ == "__main__":
    HBNBCommand().cmdloop()
