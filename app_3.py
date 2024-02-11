from flask import Flask, render_template, jsonify, request, abort
import os
app = Flask(__name__)


def file_or_folder_exists(path):
    return os.path.exists(path)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/app')
def app_page():
    root_directory = os.getcwd()
    if not file_or_folder_exists(root_directory):
        abort(404)
    else:
        folder_tree = generate_folder_tree(root_directory)
        return render_template('app.html', folder_tree=folder_tree, root_directory=root_directory)


@app.route('/save.txt', methods=['POST'])
def save_txt():
    text = request.form.get('prompt')
    print(text)
    return jsonify({'message': 'Text received!'})


@app.route('/fs')
def folder_structure():
    root_directory = os.getcwd()
    if not file_or_folder_exists(root_directory):
        abort(404)
    folder_tree = generate_folder_tree(root_directory)
    return render_template('folder_structure.html', folder_tree=folder_tree, root_directory=root_directory)


def generate_folder_tree(root_path):
    folder_tree = []
    # Rozszerzenia do pominięcia
    excluded_extensions = ['pcg,', '.git', '.log']
    excluded_folders = ['private']
    for root, dirs, files in os.walk(root_path):
        rel_path = os.path.relpath(root, root_path)
        if any(excluded_folder in rel_path for excluded_folder in excluded_folders):
            filtered_files = [file for file in files if not any(
                file.endswith(ext)for ext in excluded_extensions)]
            folder_tree.append((rel_path, dirs, filtered_files))
    return folder_tree


@app.route('/fetch_file_content')
def fetch_file_content():
    filename = request.args.get('filename')
    file_path = os.path.join(os.getcwd(), filename)
    if not file_or_folder_exists(file_path):
        abort(404)
    try:
        with open(file_path, 'r') as file:
            content = file.read()
        return content
    except Exception as e:
        return str(e)


if __name__ == '__main__':
    app.run(debug=True)
