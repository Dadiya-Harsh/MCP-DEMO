from typing import Annotated, TypedDict, Callable, get_type_hints


name = Annotated[str, "Name of the person"]

age = Annotated[int, "Age of the person"]   

class Person(TypedDict):
    name: name
    age: age

print(get_type_hints(Person))  # {'name': <class 'str'>, 'age': <class 'int'>} 
print(name.__metadata__)  # (str, 'Name of the person')