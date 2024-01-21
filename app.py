from flask import Flask, render_template, request
from difflib import get_close_matches

app = Flask(__name__)
dataset_path = 'proverbs-kashmiri.txt'

def read_proverbs_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return [line.strip() for line in file.readlines()]

def extract_proverb_data(data, proverb):
    possibilities = [item.split(':')[0].lower() for item in data]  # Define possibilities here
    matches = get_close_matches(proverb.lower(), possibilities, n=1)

    if matches:
        matched_proverb = matches[0]
        index = possibilities.index(matched_proverb)  # Use possibilities for index

        if index is not None:
            proverb_entry = data[index].split(':')

            real_proverb = proverb_entry[0].strip()
            translation = proverb_entry[1].strip() if len(proverb_entry) > 1 else "Not available"
            meaning = proverb_entry[2].strip() if len(proverb_entry) > 2 else "Not available"

            return {"proverb": real_proverb, "user_proverb": proverb, "translation": translation, "meaning": meaning, "suggestion": None}
        else:
            return {"proverb": proverb, "user_proverb": proverb, "translation": "Not found", "meaning": "Not found", "suggestion": None}
    else:
        return {"proverb": proverb, "user_proverb": proverb, "translation": "Not found", "meaning": "Not found", "suggestion": None}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    proverb_to_search = request.form['proverb']

    # Extract details for the proverb
    proverbs_from_file = read_proverbs_file(dataset_path)
    result = extract_proverb_data(proverbs_from_file, proverb_to_search)

    return render_template('result.html', result=result)

if __name__ == '__main__':
    app.run(debug=True)
