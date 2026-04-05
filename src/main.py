import os
import json
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Default user data file path (can be overridden by environment variable)
USER_DATA_FILE = os.getenv("USER_DATA_FILE", "user_data.json")


def load_user_data():
    """Loads user data from the JSON file."""
    try:
        with open(USER_DATA_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}  # Return an empty dictionary if the file doesn't exist
    except json.JSONDecodeError:
        print(f"Error decoding JSON from {USER_DATA_FILE}. Returning empty data.")
        return {} # Return an empty dictionary if JSON is invalid


def save_user_data(user_data):
    """Saves user data to the JSON file."""
    try:
        with open(USER_DATA_FILE, "w") as f:
            json.dump(user_data, f, indent=4)
    except Exception as e:
        print(f"Error saving user data to {USER_DATA_FILE}: {e}")


@app.route("/")
def index():
    """Renders the main user dashboard page."""
    user_data = load_user_data()
    return render_template("index.html", user_data=user_data)


@app.route("/user/<username>", methods=["GET"])
def get_user(username):
    """Retrieves user data for a specific user."""
    user_data = load_user_data()
    user = user_data.get(username)
    if user:
        return jsonify(user)
    return jsonify({"error": "User not found"}), 404


@app.route("/user/<username>", methods=["POST"])
def create_or_update_user(username):
    """Creates a new user or updates an existing user's data."""
    user_data = load_user_data()
    new_data = request.get_json()

    if new_data is None:
        return jsonify({"error": "Invalid JSON data"}), 400

    user_data[username] = new_data
    save_user_data(user_data)
    return jsonify({"message": f"User {username} created/updated successfully"}), 201 # 201 Created


@app.route("/user/<username>", methods=["DELETE"])
def delete_user(username):
    """Deletes a user from the user data."""
    user_data = load_user_data()
    if username in user_data:
        del user_data[username]
        save_user_data(user_data)
        return jsonify({"message": f"User {username} deleted successfully"})
    return jsonify({"error": "User not found"}), 404


if __name__ == "__main__":
    # Determine the port to listen on.  Defaults to 5000.
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)