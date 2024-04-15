
import bcrypt
from flask import Flask, request, abort, jsonify, render_template
import re

import firebase_admin
from firebase_admin import credentials, auth
from firebase_admin import firestore

from Entities.User import User

app = Flask(__name__)

cred = credentials.Certificate("static/pyproject-63c10-firebase-adminsdk-98zc9-532150f44b.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

GMAIL_REGEX = re.compile(r'^[a-z0-9]+[\._]?[a-z0-9]+[@]\bgmail\b[.]\bcom\b$', re.IGNORECASE)


# User REST API

@app.route('/login', methods=['POST'])
def login_firebase():
    username_or_email = request.form.get('username_or_email')
    password = request.form.get('password')

    if username_or_email is None or password is None:
        return jsonify({'error': 'Username/email or password missing'}), 400

    # Check if the input is an email or a username
    is_email = '@' in username_or_email

    if is_email:
        # Check if email exists in Firestore
        user_query = db.collection(u'users').where(u'email', u'==', username_or_email).limit(1).get()
    else:
        # Check if username exists in Firestore
        user_query = db.collection(u'users').where(u'username', u'==', username_or_email).limit(1).get()

    if not user_query:
        return jsonify({'error': 'Invalid credentials'}), 401

    user_doc = user_query[0]

    # Check if the password matches
    if not bcrypt.checkpw(password.encode('utf-8'), user_doc.to_dict()['password_hash'].encode('utf-8')):
        return jsonify({'error': 'Invalid credentials'}), 401

    return jsonify({'message': 'Login successful'}), 200

@app.route('/register', methods=['POST'])
def insert_user_firebase():
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')
    admin = request.form.get('admin', False)

    # Check if the email provided is a valid Gmail address
    if not GMAIL_REGEX.match(email):
        return jsonify({'error': 'Invalid email format, must be a Gmail address'}), 400

    # Check if username or email already exists
    user_query = db.collection(u'users').where(u'username', u'==', username).limit(1).get()
    email_query = db.collection(u'users').where(u'email', u'==', email).limit(1).get()

    if user_query or email_query:
        return jsonify({'error': 'Username or email already exists'}), 409

    # Hash the password
    password_hash = User.hash_password(password)

    # Create user document
    user_data = {
        u'username': username,
        u'email': email,
        u'password_hash': password_hash,
        u'admin': admin
    }

    # Add user to Firestore
    db.collection(u'users').add(user_data)

    return jsonify({'message': 'User inserted successfully'}), 200


# Product REST API

@app.route('/all-products', methods=['GET'])
def get_products():
    return 'Get products'


@app.route('/insert-product', methods=['POST'])
def insert_product():
    return 'Insert product'


# @app.route('/upload-image', methods=['POST'])
# def upload_image():
#     image = request.files['image']
#     image_id = save_image(image)
#     return str(image_id)
#
#
# @app.route('/display-images')
# def display_images():
#     images = get_all_images()
#     return render_template('display_images.html', images=images)


# Methods

# def save_image(image):
#     fs = gridfs.GridFS(entities_db)
#     image_id = fs.put(image)
#     return image_id
#
#
# def get_all_images():
#     fs = gridfs.GridFS(entities_db)
#     images = []
#     for image in fs.find():
#         images.append(base64.b64encode(image.read()).decode('utf-8'))
#     return images


def get_all_products():
    return 'Get all products'


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
