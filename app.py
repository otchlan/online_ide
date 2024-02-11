from flask import Flask, render_template, request, jsonify
from markupsafe import escape
from flask_cors import CORS
import json
import os
import logging

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    filename='app.log',  # Log to file named 'app.log'
                    filemode='a')

app = Flask(__name__)
CORS(app)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/app')
def app_page():
    root_directory = os.getcwd()
    folder_tree = generate_folder_tree(root_directory)
    return render_template('app.html', folder_tree=folder_tree, root_directory=root_directory)


@app.route('/save_text', methods=['POST'])
def save_text():
    text = request.form.get('prompt')
    print(text)
    return jsonify({"message": "Text received!"})

@app.route('/fs')
def folder_structure():
    logging.info("Rendering folder_structure.html")
    root_directory = os.getcwd()  # Get the current working directory
    folder_tree = generate_folder_tree(root_directory)
    return render_template('folder_structure.html', folder_tree=folder_tree, root_directory=root_directory)

def generate_folder_tree(root_path):
    logging.info("Generating folder tree")
    folder_tree = []
    included_directories = ['templates', 'static',
                            'readme_issues', 'static/js', 'static/css']

    for root, dirs, files in os.walk(root_path, topdown=True):
        rel_path = os.path.relpath(root, root_path)

        if rel_path == '.':
            folder_tree.append((rel_path, [], files))
            dirs[:] = [d for d in dirs if d in included_directories]
        elif rel_path in included_directories:
            folder_tree.append((rel_path, dirs, files))

        if rel_path not in ['.', *included_directories]:
            del dirs[:]

    return folder_tree

@app.route('/fetch_file_content')
def fetch_file_content():
    filename = request.args.get('filename')
    logging.info(f"Fetching file content for: {filename}")

# TODO --> te foldery powinny być automatycznie wyszukiwane w procjecie i ładowane
    potential_paths = [
        os.path.join(os.getcwd(), filename),
        os.path.join(os.getcwd(), 'templates', filename),
        os.path.join(os.getcwd(), 'static', filename),
        os.path.join(os.getcwd(), 'static', 'js', filename),
        os.path.join(os.getcwd(), 'static', 'css', filename)
    ]

    file_path = next(
        (path for path in potential_paths if os.path.exists(path)), None)

    if file_path:
        print(f"Trying to fetch content from: {file_path}")
        try:
            with open(file_path, 'r') as file:
                content = file.read()
            return content
        except Exception as e:
            print(f"Error encountered: {str(e)}")
            return f"Error: {str(e)}"
    else:
        return f"Error: File '{filename}' not found in expected directories."


@app.route('/ide')
def ide_page():
    root_directory = os.getcwd()
    folder_tree = generate_folder_tree(root_directory)
    return render_template('ide.html', folder_tree=folder_tree, root_directory=root_directory)

@app.template_filter('html_escape')
def html_escape_filter(s):
    return escape(s)


@app.route('/main')
def main():
    logging.info(f"Rendering main.html")
    return render_template('main.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message')
    logging.info(f"Received user message: {user_message}")

    try:
        # Load data_mock.json
        with open("data_mock.json", "r") as file:
            data = json.load(file)
    except Exception as e:
        logging.error(f"Error loading data_mock.json: {e}")
        return jsonify({"error": "Internal server error"}), 500

    # Find the matching data
    for entry in data:
        if entry["user_msg"] == user_message:
            logging.info(f"Found matching entry for user message: {entry}")
            return jsonify({
                "user_msg": entry["user_msg"],
                "ai_msg": entry["ai_msg"],
                "image": entry["image"]
            })

    logging.warning(
        f"No matching entry found for user message: {user_message}")

    # If no match found
    return jsonify({
        "user_msg": user_message,
        "ai_msg": "Sorry, I don't understand that.",
        "image": "default_image.jpg"
    })

@app.route('/save_code', methods=['POST'])
def save_code():
    logging.info("Save code endpoint called")
    data = request.get_json()
    code_content = data.get('code')
    filename = data.get('filename')  # Get filename from the request
    file_path = os.path.join(os.getcwd(), filename)  # Dynamic file path

    logging.info(f"Attempting to save code to: {file_path}")

    try:
        with open(file_path, 'w') as file:
            file.write(code_content)
        logging.info("Code saved successfully")
        return jsonify({"message": "Code saved successfully"})
    except Exception as e:
        logging.error(f"Error saving code: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/create_new_file', methods=['POST'])
def create_new_file():
    data = request.get_json()
    filename = data.get('filename')
    try:
        if not os.path.exists(filename):
            with open(filename, 'w') as file:
                file.write('')  # Creating an empty file
            return jsonify({"message": "File created successfully."})
        else:
            return jsonify({"error": "File already exists."}), 409
    except Exception as e:
        logging.error(f"Error creating file: {e}")
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    host = "0.0.0.0"  # Use "0.0.0.0" to make your app accessible from external IPs
    port = 5005       # Default Flask port; you can change it if needed
    logging.info(f"Starting Flask app on http://{host}:{port}")
    app.run(host=host, port=port, debug=True)
