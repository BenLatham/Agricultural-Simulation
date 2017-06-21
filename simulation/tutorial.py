# My notes from a quick python tutorial at
# https://www.youtube.com/watch?v=N4mEzFDjqtA
# as a personal reminder in case I forget something

import random
import sys
import os
print("Hello world")

# comment

'''this is
a multi-line comment -but is not an official way of doing it'''

name = "Ben"
print(name)

name = 15
print(name)

# Data types: numbers strings lists tuples dictionaries
# Operators: + - * / % **(exponent) //(floor devision)
print("5 + 2 =", 5+2)
print("5 - 2 =", 5-2)
print("5 * 2 =", 5*2)
print("5 / 2 =", 5/2)
print("5 % 2 =", 5 % 2)
print("5 ** 2 =", 5**2)
print("5 // 2 =", 5//2)

# use \ to escape quotes, to create newline \n
quote = "\"This is something someone said\"\n"
print(quote)

# use tripple single quotes for multiline quotes
multilinequote = '''This is what someone said:
\"I like my quotes on multiple lines\"'''
print(multilinequote)

# use %s like in printf in PHP and c
print("%s-%s-%s" % ("a nice string", quote, multilinequote))

# print usually ends each print statement with a default \n change this use end
print("I don't like ", end="")
print("newlines.")

# repeat print statements
print("repeat "*5)

# Lists
# not all items have to have the same type
shopping_list = ['Oil', 'Peanut Butter', 'fruit', 'veg']
print("First item to buy:", shopping_list[0])
shopping_list[0] = "cooking oil"
print("First item is now:", shopping_list[0])

# refer to multiple items
print("Items 1 and 2:", shopping_list[1:3])

presentlist = ["watch", "top", "DVD"]

tobuy = [shopping_list, presentlist]
print(tobuy)
print(tobuy[0][0])

# ammending a list
shopping_list.append("onions")
print(shopping_list)
print(tobuy)  # note that appending one of the lists included in to buy also affects tobuy
shopping_list.insert(2, "Jam")
print(shopping_list)
shopping_list.remove("Peanut Butter")
print(shopping_list)
shopping_list.reverse()
print(shopping_list)
shopping_list.sort()
print(shopping_list)
del shopping_list[0]
print(shopping_list)

# adding lists
new_shopping_list = shopping_list + presentlist
print(new_shopping_list)
print(len(new_shopping_list))
print(max(new_shopping_list))
print(min(new_shopping_list))

# tuples (non-editable lists)
pi_tuple = (3, 1, 4, 1, 5, 9, 2, 6, 5, 4)
pi_list = list(pi_tuple)
del pi_list[9]
pi_list += [3, 5]  # += and so on are allowed in python
new_tuple = tuple(pi_list)
print(pi_tuple)
print(pi_list)
print(new_tuple)

print(len(new_tuple))  # max and min also work

# maps -list with a unique key for each value; cannot be joined with +
books = {"The normal christian worker": "Watchman Nee",
         "Horse and his boy": "C.S. Lewis",
         "The selfish gene": "Richard Dawkins"}

# to access a value
print(books["Horse and his boy"])
# or
print(books.get("Horse and his boy"))

print(books.keys())  # access keys
print(books.values())  # access values

# conditionals if, else, elif
# comparators == != > < >= <=
# logical operators and, or, not
shelf_space = 100
books_read = ["The normal christian worker", "Horse and his boy", "The selfish gene"]
if len(books) > shelf_space:
    print("Buy more shelves")
elif len(books) <= len(books_read):
    print("Buy more books")
else:
    print("read more books")


# for loop
for i in range(0, 10):
    print(i)

# random numbers
rannum = random.normalvariate(0, 3)
print(rannum)

# while loop
while rannum < 10:
    print(rannum)
    rannum = random.normalvariate(0, 3)
print(rannum)


# functions
def add_number(fnum, lnum):
    sumnum = fnum+lnum
    return sumnum

print(add_number(1, 91))



# strings
long_string = "on the first day of christmas my true love gave to me one calling bird"
print(long_string.capitalize())
print(long_string.find("christmas"))
print(long_string.isalpha())
print(long_string.isalnum())
print(len(long_string))
print(long_string.replace("christmas", "Christmas"))

# filesystem
practice_file = open("practice.txt", "wb")
print(practice_file.mode)
print(practice_file.name)
practice_file.write(bytes("write me to the file\n", "UTF-8"))
practice_file.close()
practice_file = open("practice.txt", "r+")
text = practice_file.read()
print(text)
practice_file.close()
os.remove("practice.txt")


# objects
class Animal(object):
    __name = ""
    __height = 0
    __weight = 0
    __sound = 0

    def __init__(self, name, height, weight, sound):
        self.__name = name
        self.__height = height
        self.__weight = weight
        self.__sound = sound

    def set_name(self, name):
        self.__name = name

    def get_name(self):
        return self.__name

    def set_height(self, height):
        self.__height = height

    def get_height(self):
        return self.__height

    def set_weight(self, weight):
        self.__weight = weight

    def get_weight(self):
        return self.__weight

    def set_sound(self, sound):
        self.__sound = sound

    def get_sound(self):
        return self.__sound

    def get_type(self):
        print("Animal")

    def to_string(self):
        return "The {} is {}m tall and {} kg, it goes {}".format(self.__name,
                                                                 self.__height,
                                                                 self.__weight,
                                                                 self.__sound)
Bonkers = Animal("cat", 0.03, 3, "prrrrr")
print(Bonkers.to_string())


# inheritance
class Dog(Animal):
    __owner = ""

    def __init__(self, name, height, weight, sound, owner):
        self.__owner = owner
        super(Dog, self).__init__(name, height, weight, sound)

    def set_owner(self, owner):
        self.__owner = owner

    def get_owner(self):
        return self.__owner

    def get_type(self):
        print("Dog")

    def tostring(self):
        return "The {} is {}m tall and {} kg, it goes {}, its owner is {}".format(self.get_name(),
                                                                                  self.get_height(),
                                                                                  self.get_weight(),
                                                                                  self.get_sound(),
                                                                                  self.__owner)

    # method overloading
    def multiple_sounds(self, how_many=None):
        if how_many is None:
            print(self.get_sound())
        else:
            print(self.get_sound() * how_many)

Maddi = Dog("dog", 0.5, 20, "woooWoooWoo", "Tim")

print(Maddi.get_height())

print(Maddi.tostring())

Maddi.multiple_sounds(3)

class AnimalTesting:
    def get_type(self, animal):
        animal.get_type()

test_animals = AnimalTesting()

print("Bonkers is a:")
test_animals.get_type(Bonkers)
print("Maddi is a:")
test_animals.get_type(Maddi)

# well thats the basics!

# exception handling

def failingfunction():
    while True:
        raise Exception("BFG")
        print("in While")
        break;
    print("out of While")

try:
    failingfunction()
# except :
#     print("BFG is too small")
except:
    print("Caught it at last")
print ("Pfew! glad I caught that")