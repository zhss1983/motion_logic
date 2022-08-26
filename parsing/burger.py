import json

with open('Burger-king.json') as burger_king:
    data = json.load(burger_king)

for bk_point in data:
    print(bk_point)