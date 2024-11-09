from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit_query', methods=['POST'])
def submit_query():
    data = request.get_json()
    query = data.get('query', '')
    print("Received query:", data)  # Print the natural language query to the console
    return jsonify({"message": query})

if __name__ == '__main__':
    app.run(debug=True)