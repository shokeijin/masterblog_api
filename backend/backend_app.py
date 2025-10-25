from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

POSTS = [
    {"id": 1, "title": "First post", "content": "This is the first post."},
    {"id": 2, "title": "Second post", "content": "This is the second post about Flask."},
    {"id": 3, "title": "A post about Python", "content": "Python is a versatile language."}
]


@app.route('/api/posts', methods=['GET'])
def get_posts():
    return jsonify(POSTS)


@app.route('/api/posts/search', methods=['GET'])
def search_posts():
    """
    Dieser Endpunkt ermöglicht die Suche nach Beiträgen anhand von Titel und/oder Inhalt.
    Die Suchbegriffe werden als Query-Parameter übergeben (z.B. /api/posts/search?title=post&content=flask).
    """
    title_query = request.args.get('title')
    content_query = request.args.get('content')

    results = POSTS[:]  # Eine Kopie der Liste erstellen, um sie zu filtern

    if title_query:
        results = [post for post in results if title_query.lower() in post['title'].lower()]

    if content_query:
        results = [post for post in results if content_query.lower() in post['content'].lower()]

    return jsonify(results)


@app.route('/api/posts', methods=['POST'])
def add_post():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Request body must be a valid JSON"}), 400
    missing_fields = []
    if 'title' not in data or not data.get('title'):
        missing_fields.append('title')
    if 'content' not in data or not data.get('content'):
        missing_fields.append('content')
    if missing_fields:
        return jsonify({"error": f"Missing required fields: {', '.join(missing_fields)}"}), 400
    new_id = max(post['id'] for post in POSTS) + 1 if POSTS else 1
    new_post = {
        "id": new_id,
        "title": data['title'],
        "content": data['content']
    }
    POSTS.append(new_post)
    return jsonify(new_post), 201


@app.route('/api/posts/<int:id>', methods=['DELETE'])
def delete_post(id):
    post_to_delete = next((post for post in POSTS if post["id"] == id), None)
    if post_to_delete is None:
        return jsonify({"error": f"Post with id {id} not found"}), 404
    POSTS.remove(post_to_delete)
    return jsonify({"message": f"Post with id {id} has been deleted successfully."}), 200


@app.route('/api/posts/<int:id>', methods=['PUT'])
def update_post(id):
    post_to_update = next((post for post in POSTS if post["id"] == id), None)
    if post_to_update is None:
        return jsonify({"error": f"Post with id {id} not found"}), 404
    data = request.get_json()
    if not data:
        return jsonify({"error": "Request body must be a valid JSON"}), 400
    post_to_update['title'] = data.get('title', post_to_update['title'])
    post_to_update['content'] = data.get('content', post_to_update['content'])
    return jsonify(post_to_update), 200


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)