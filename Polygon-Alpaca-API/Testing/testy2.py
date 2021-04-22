import sys
import traceback
import ipdb


class CarTypes:
    class Toyota:
        def __repr__(self):
            return "Toyota()"
        def __str__(self):
            return "Instance of Toyota() class"
    class Nissan:
        def __repr__(self):
            return "Nissan()"
        def __str__(self):
            return "Instance of Nissan() class"


class Car:
    def __init__(self):
        self._all_classes = {}

    def construct(self, builder_name):
        setattr(self, builder_name, CarTypes())
        try:
            target_class = getattr(CarTypes, builder_name)
            instance = target_class()
            self._all_classes[builder_name] = instance
        except AttributeError:
            print("Builder {} not defined.".format(builder_name))
            traceback.print_stack()

    def __getitem__(self, type_name):
        return self._all_classes[type_name]

    def car_type(self, type_name):
        return self._all_classes[type_name]


IDS = ["Toyota", "Nissan", "Unknown"]

director = Car()
for id in IDS:
    director.construct(id)

print(director["Toyota"])
print(director["Nissan"])
print(director.car_type("Toyota"))
print(director.car_type("Nissan"))