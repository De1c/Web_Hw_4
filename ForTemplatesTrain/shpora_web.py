# from jinja2 import Template

# name = "Yehor"
# age = 17

# tm = Template("My name is {{name}} and I am {{age}}")
# msg = tm.render(name=name, age=age)

# print(msg)


# persons = [
#     {'name': 'Andrej', 'age': 34},
#     {'name': 'Mark', 'age': 17},
#     {'name': 'Thomas', 'age': 44},
#     {'name': 'Lucy', 'age': 14},
#     {'name': 'Robert', 'age': 23},
#     {'name': 'Dragomir', 'age': 54}
# ]

# tm = Template("""{% for person in persons -%}
#         {{person.name}} {{person.age}}
# {% endfor %}""")

# print(tm.render(persons=persons))

# For HTML documents you can use ↓
from jinja2 import Environment, FileSystemLoader
import os

env = Environment(
    loader=FileSystemLoader(
        searchpath=f"{os.path.dirname(os.path.realpath(__file__))}\\templates"
    )
)

template = env.get_template("persons.html")


persons = [
    {"name": "Andrej", "age": 34},
    {"name": "Mark", "age": 17},
    {"name": "Thomas", "age": 44},
    {"name": "Lucy", "age": 14},
    {"name": "Robert", "age": 23},
    {"name": "Dragomir", "age": 54},
]

output = template.render(persons=persons,)

with open(
    f"{os.path.dirname(os.path.realpath(__file__))}\\new_persons.html",
    "w",
    encoding="utf-8",
) as fh:
    fh.write(output)
