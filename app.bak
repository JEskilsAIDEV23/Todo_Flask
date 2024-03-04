#____________________________________
#               ROUTES
#____________________________________
#
# GET: /tasks
# GET: /tasks/<id>
# GET: /tasks?status=complete
# GET: /tasks?status=pending
# GET: /tasks/categories
# GET: /tasks/categories/<category>
#
# POST: /tasks
"""
{
    "id":id, 
    "category":"sumThing", 
    "description":"sumThinkz"
}
"""
# PUT: /tasks/<id>/completed
# PUT: /tasks/<id>
"""
{
    "category":"sumThing", 
    "description":"sumThinkz"
}
"""
# DELETE: /tasks/delete/<id>
#____________________________________

import json
from flask import Flask, jsonify, request
# Creating a Flask Application
app = Flask(__name__)

#____Configuration____
class Config:
    TASK_FILE = 'tasks.json'  # Example configuration setting

#____Load configuration____
app.config.from_object(Config)
task_file = app.config['TASK_FILE']

#____Routes____
@app.route("/tasks", methods=["GET"])
def return_data():
    try:
        with open(task_file, 'r') as file:
            data = json.load(file)
            status = request.args.get('status')
            if status:
                filtered_data = [task for task in data if task.get('status') == status]
                sorted_data = sorted(filtered_data, key=lambda x: x.get('status'))
                return jsonify(sorted_data)
            else:
                return jsonify(data)
    except FileNotFoundError:
        return jsonify({"error": "File not found"}), 404
    except json.JSONDecodeError:
        return jsonify({"error": "JSON decoding error"}), 500

@app.route("/tasks/<int:id>", methods=["GET"])
def return_task(id):
    my_new_extr = []
    try:
        with open(task_file, 'r') as file:
            data = json.load(file)

            for post in data:
                if post['id'] == id:
                    data_extr = {
                        "id": post['id'],
                        "category": post["category"],
                        "description": post["description"],
                        "status": post["status"]
                    }
                    my_new_extr.append(data_extr)

        if not my_new_extr:
            return jsonify({"error": f"Task with id {id} not found"}), 404
        else:
            return jsonify(my_new_extr), 200
    except FileNotFoundError:
        return jsonify({"error": "File not found"}), 404
    except json.JSONDecodeError:
        return jsonify({"error": "JSON decoding error"}), 500
        
@app.route("/tasks/categories", methods=["GET"])
def return_cat():
    my_new_extr = []
    data_extr = {}
    try:
        with open(task_file, 'r') as file:
            data = json.load(file)
            for i in data:
                data_extr.update(i)
                my_new_extr.append(data_extr["category"])      
        return jsonify(my_new_extr) 
    except FileNotFoundError:
        return jsonify({"error": "File not found"}), 404
    except json.JSONDecodeError:
        return jsonify({"error": "JSON decoding error"}), 500

@app.route('/tasks/categories/<category>', methods=["GET"])
def search_cats(category):
    my_new_extr = []
    data_extr = {}
    try:
        with open(task_file, 'r') as file:
            data = json.load(file)
            n = 0
            for post in data:
                if post['category'] == category:
                    data_extr[n] = {"id": post['id'], "category": post["category"], "description": post["description"], "status": post["status"]}
                    my_new_extr.append(data_extr[n])
                    n += 1
                    return jsonify(my_new_extr)
                if post['category'].startswith(category):
                    data_extr[n] = {"id": post['id'], "category": post["category"], "description": post["description"], "status": post["status"]}
                    my_new_extr.append(data_extr[n])
                    n += 1
                if post['category'].endswith(category):
                    data_extr[n] = {"id": post['id'], "category": post["category"], "description": post["description"], "status": post["status"]}
                    my_new_extr.append(data_extr[n])
                    n += 1
        if not my_new_extr:
            return jsonify({"error": f"No such category as {category} exists"}), 404 
        else:
            return jsonify(my_new_extr), 200
    except FileNotFoundError:
        return jsonify({"error": "File not found"}), 404
    except json.JSONDecodeError:
        return jsonify({"error": "JSON decoding error"}), 500

@app.route("/tasks", methods=["POST"])
def add_task():
    # function to add to JSON
    data = request.json
    idc = ''
    if 'id' in data:
        if data['id'].strip() != '':
            try:
                id = int(data['id'])
                idc += 'i'
            except:
                return f"id: must be an integer or 'integer' not char-string, empty or space"
        else:
            return f"id: must be an integer or 'integer' not char-string, empty or space"
        if data['description'].strip() != '':
            description = data['description']
            idc += 'd'
        else:
            description = "None Given"
            idc += 'd' 
    if "category" in data:
        if data['category'].strip() !='':
            category = data['category']
            idc += 'c'
        else:
            category = "Not defined"
            idc += 'c'
    status = "pending"

    try:
        with open(task_file,'r+') as file:
            # python object to be appended
            if idc == 'idc':
                add_task = {"id":id, "description":description, "category":category, "status":status}
            else:
                return f"Error Missing data: {idc} != idc, i=id, d=description, c=category"
            # First we load existing data into a dict.
            file_data = json.load(file)
            # Join new_data with file_data
            file_data.append(add_task)
            # Sets file's current position at offset.
            file.seek(0)
            # convert back to json.
            json.dump(file_data, file, indent = 4)
        return f"Task with id: {id} added" 
    except FileNotFoundError:
        return jsonify({"error": "File not found"}), 404
    except json.JSONDecodeError:
        return jsonify({"error": "JSON decoding error"}), 500

@app.route("/tasks/<int:post_id>", methods=["DELETE"])
def search_and_delete_post(post_id):
    # Read JSON file
    try:
        with open(task_file, 'r') as f:
            data = json.load(f)
        # Search and delete post with specified ID
        deleted = False
        n = 0
        for post in data:
            if post['id'] == post_id:
                del data[n]
                deleted = True
                break
            n+=1
        # Write back to the JSON file if post is deleted
        if deleted:
            with open(task_file, 'w') as f:
                json.dump(data, f, indent=4)
            return f"Post with ID {post_id} deleted successfully."
        else:
            return f"Post with ID {post_id} not found."
    except FileNotFoundError:
        return jsonify({"error": "File not found"}), 404
    except json.JSONDecodeError:
        return jsonify({"error": "JSON decoding error"}), 500

@app.route("/tasks/<int:post_id>", methods=["PUT"])
def search_and_update_post(post_id):

    data = request.json
    status = "pending"
    dc = ''
    if 'description' in data:
        description = data['description']
        if description.strip() == '':
            description = "Not given"
        dc += 'd'
    if "category" in data:
        category = data['category']
        if category.strip() == '':
            category = "Not defined"
        dc += 'c'
    # Read JSON file
    try:
        with open(task_file, 'r') as f:
            data = json.load(f)
        # Search and update post with specified ID
        update = False
        n = 0
        for post in data:
            if dc != 'dc':
                return f"Error Missing Data: dc != dc, dc == {dc}, d=description, c=category"
            if post['id'] == post_id:
                data[n]['status'] = status
                data[n]['category'] = category
                data[n]['description'] = description
                update = True
                break
            n+=1
        # Write back to the JSON file if post is deleted
        if update:
            with open(task_file, 'w') as f:
                json.dump(data, f, indent=4)
            return f"Post with ID {post_id} updated successfully."
        else:
            return f"Post with ID {post_id} not found."
    except FileNotFoundError:
        return jsonify({"error": "File not found"}), 404
    except json.JSONDecodeError:
        return jsonify({"error": "JSON decoding error"}), 500

@app.route("/tasks/<int:post_id>/complete", methods=["PUT"])
def set_task_complete(post_id):
    # Read JSON file
    try:
        with open(task_file, 'r') as f:
            data = json.load(f)
        # Search and update post with specified ID
        complete = False
        n = 0
        for post in data:
            if post['id'] == post_id:
                data[n]['status'] = "complete" 
                complete = True
                break
            n+=1
        # Write back to the JSON file if post is deleted
        if complete:
            with open(task_file, 'w') as f:
                json.dump(data, f, indent=4)
            return f"Post with ID {post_id} set as complete successfully."
        else:
            return f"Post with ID {post_id} not found."
    except FileNotFoundError:
        return jsonify({"error": "File not found"}), 404
    except json.JSONDecodeError:
        return jsonify({"error": "JSON decoding error"}), 500

if __name__ == '__main__':
    app.run(debug=True)