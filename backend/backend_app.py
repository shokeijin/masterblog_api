from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

POSTS = [
    {"id": 1, "title": "First post", "content": "This is the first post."},
    {"id": 2, "title": "Second post", "content": "This is the second post."},
]


@app.route('/api/posts', methods=['GET'])
def get_posts():
    return jsonify(POSTS)


@app.route('/api/posts', methods=['POST'])
def add_post():
    """
    Dieser Endpunkt fügt einen neuen Blog-Beitrag hinzu.
    Er erwartet ein JSON-Objekt mit "title" und "content".
    """
    data = request.get_json()

    # Überprüfen, ob Daten im Anforderungs-Body gesendet wurden
    if not data:
        return jsonify({"error": "Request body must be a valid JSON"}), 400

    # Überprüfen auf fehlende oder leere Felder
    missing_fields = []
    if 'title' not in data or not data.get('title'):
        missing_fields.append('title')
    if 'content' not in data or not data.get('content'):
        missing_fields.append('content')

    if missing_fields:
        return jsonify({"error": f"Missing required fields: {', '.join(missing_fields)}"}), 400

    # Generieren einer neuen eindeutigen ID
    new_id = max(post['id'] for post in POSTS) + 1 if POSTS else 1

    # Erstellen des neuen Beitrags-Wörterbuchs
    new_post = {
        "id": new_id,
        "title": data['title'],
        "content": data['content']
    }

    # Hinzufügen des neuen Beitrags zur Liste
    POSTS.append(new_post)

    # Zurückgeben des neuen Beitrags mit dem Statuscode 201 Created.
    return jsonify(new_post), 201


@app.route('/api/posts/<int:id>', methods=['DELETE'])
def delete_post(id):
    """
    Dieser Endpunkt löscht einen Beitrag anhand seiner ID.
    """
    # Finden des Beitrags mit der angegebenen ID
    post_to_delete = next((post for post in POSTS if post["id"] == id), None)

    # Wenn kein Beitrag gefunden wird, einen 404-Fehler zurückgeben
    if post_to_delete is None:
        return jsonify({"error": f"Post with id {id} not found"}), 404

    # Den gefundenen Beitrag aus der Liste entfernen
    POSTS.remove(post_to_delete)

    # Erfolgsmeldung zurückgeben
    return jsonify({"message": f"Post with id {id} has been deleted successfully."}), 200


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)