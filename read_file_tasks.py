import json


def search_id(id):
    with open('tasks.json', 'r') as file:
        data = json.load(file)
    for post in data:
        if post['id'] == id:
            search = post
        else:
            search = []  
    if search != []:
        return search
    else:
        return f"Task {id} not found"
        
def search_cat(category):
    with open('tasks.json', 'r') as file:
        data = json.load(file)
    for post in data:
        if post['category'] == category:
            search = post
        else:
            search = []  
    if search != []:
        return search
    else:
        return f"{category} not found"

search = search_id(1)
print(search)
        
search = search_cat('Lorum')
print(search)

    


