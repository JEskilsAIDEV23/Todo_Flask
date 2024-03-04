import sqlite3
from flask import Flask, render_template, request, url_for, flash, redirect, jsonify
from werkzeug.exceptions import abort
import requests
import json
from db_OOP import *

app = Flask(__name__)
app.config['SECRET_KEY'] = '@1dEvtwo3s'

#____Configuration____
class Config:
    TASK_FILE = 'tasks.json'  

#____Load configuration____
app.config.from_object(Config)
task_file = app.config['TASK_FILE']
#db = get_db_conn()

@app.route('/')
def index():
    return render_template('index.html')

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
            return render_template('task_id.html',task=data_extr)
    except FileNotFoundError:
        return jsonify({"error": "File not found"}), 404
    except json.JSONDecodeError:
        return jsonify({"error": "JSON decoding error"}), 500

@app.route("/tasks", methods=["GET"])
def return_tasks():
    try:
        with open(task_file, 'r') as file:
            data = json.load(file)
            status = request.args.get('status')
            if status:
                filtered_data = [task for task in data if task.get('status') == status]
                sorted_data = sorted(filtered_data, key=lambda x: x.get('status'))
                return render_template('tasks.html',tasks=sorted_data)
            else:
                return render_template('tasks.html',tasks=data)
    except FileNotFoundError:
        return jsonify({"error": "File not found"}), 404
    except json.JSONDecodeError:
        return jsonify({"error": "JSON decoding error"}), 500

# @app.route("/tasks/<int:post_id>", methods=["PUT"])
# def search_and_update_post(post_id):

#     data = request.json
#     status = "pending"
#     dc = ''
#     if 'description' in data:
#         description = data['description']
#         if description.strip() == '':
#             description = "Not given"
#         dc += 'd'
#     if "category" in data:
#         category = data['category']
#         if category.strip() == '':
#             category = "Not defined"
#         dc += 'c'
#     # Read JSON file
#     try:
#         with open(task_file, 'r') as f:
#             data = json.load(f)
#         # Search and update post with specified ID
#         update = False
#         n = 0
#         for post in data:
#             if dc != 'dc':
#                 return f"Error Missing Data: dc != dc, dc == {dc}, d=description, c=category"
#             if post['id'] == post_id:
#                 data[n]['status'] = status
#                 data[n]['category'] = category
#                 data[n]['description'] = description
#                 update = True
#                 break
#             n+=1
#         # Write back to the JSON file if post is deleted
#         if update:
#             with open(task_file, 'w') as f:
#                 json.dump(data, f, indent=4)
#             return render_template('index.html')
#             # return f"Post with ID {post_id} updated successfully."
#         else:
#             return f"Post with ID {post_id} not found."
#     except FileNotFoundError:
#         return jsonify({"error": "File not found"}), 404
#     except json.JSONDecodeError:
#         return jsonify({"error": "JSON decoding error"}), 500


@app.route("/tasks/<int:post_id>", methods=["POST"])
def search_and_update_post(post_id):
    if request.method == "POST":
        status = request.form.get("status", "")
        description = request.form.get("description", "")
        category = request.form.get("category", "")

        if description.strip() == "":
            description = "Not given"
        
        if status.strip() == "":
            status = "pending"

        if category.strip() == "":
            category = "Not defined"

        dc = 'dc' if description and category else ''

        try:
            with open(task_file, 'r') as f:
                data = json.load(f)

            update = False
            for n, post in enumerate(data):
                if post['id'] == post_id:
                    data[n]['status'] = status
                    data[n]['category'] = category
                    data[n]['description'] = description
                    update = True
                    break

            if update:
                with open(task_file, 'w') as f:
                    json.dump(data, f, indent=4)
                return render_template('update.html')
            else:
                return f"Post with ID {post_id} not found."
        except FileNotFoundError:
            return jsonify({"error": "File not found"}), 404
        except json.JSONDecodeError:
            return jsonify({"error": "JSON decoding error"}), 500
    else:
        # Handle other HTTP methods like GET, PUT, etc.
        return "Method not allowed"  

@app.route("/tasks/delete", methods=["GET"])
def search_and_delete():
    # Read JSON file
    deleted = False
    try:
        with open(task_file, 'r') as f:
            data = json.load(f)
        n = 0
        for post in data:
            if post['status'] == 'delete':
                del data[n]
                deleted = True
                break
            n+=1
        # Write back to the JSON file if posts are deleted
        if deleted:
            with open(task_file, 'w') as f:
                json.dump(data, f, indent=4)
            return render_template('delete.html')
        else:
            return render_template('none.html')
    except FileNotFoundError:
        return jsonify({"error": "File not found"}), 404
    except json.JSONDecodeError:
        return jsonify({"error": "JSON decoding error"}), 500 
    

@app.route("/tasks/new", methods=["GET"])
def new_task():
    return render_template('add_task.html')

@app.route("/tasks/add", methods=["POST"])
def add_task():

    if request.method == "POST":
        status = "pending"
        id = request.form.get("id", "")
        description = request.form.get("description", "")
        category = request.form.get("category", "")
        idc = ''

        if id.strip() == "":
            id = "Not defined"
        else:
            try:
                id = int(id)
                idc +='i'
            except:
                error = f"id: must be an integer or 'integer' not char-string, empty or space"
                return render_template('error.html', error=error)
        if description.strip() == "":
            description = "Not defined"
        else:
            idc += 'd'

        if category.strip() == "":
            category = "Not defined"
        else:
            idc += 'c'

    try:
        with open(task_file,'r+') as file:
            # python object to be appended
            if idc == 'idc':
                add_task = {"id":id, "description":description, "category":category, "status":status}
            else:
                error =  f"Error Missing data: {idc} != idc, i=id, d=description, c=category"
                return render_template('error.html', error=error)
            # First we load existing data into a dict.
            file_data = json.load(file)
 
            # Join new_data with file_data
            file_data.append(add_task)
            # Sets file's current position at offset.
            file.seek(0)
            # convert back to json.
            json.dump(file_data, file, indent = 4)
        # return f"Task with id: {id} added" 
        return render_template('added.html', id=id, status=status, category=category, description=description)
    
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
                my_new_extr.append(data_extr["category"].strip())

            my_new_extr = set(my_new_extr)
            my_new_extr = list(my_new_extr)  
        # return jsonify(my_new_extr) 
        return render_template('categories.html', category=my_new_extr)
    except FileNotFoundError:
        return jsonify({"error": "File not found"}), 404
    except json.JSONDecodeError:
        return jsonify({"error": "JSON decoding error"}), 500

if __name__ == '__main__':
    app.run(debug=True)