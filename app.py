import base64

import bcrypt
from flask import Flask, request, abort, jsonify, render_template
import re

import pyrebase
import firebase_admin
from firebase_admin import credentials, auth
from firebase_admin import firestore

from Entities.User import User

app = Flask(__name__)

firebaseConfig = {

}

cred = credentials.Certificate("static/pyproject-63c10-firebase-adminsdk-98zc9-532150f44b.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

firebase = pyrebase.initialize_app(firebaseConfig)
storage = firebase.storage()


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
    products = db.collection(u'products').stream()
    product_list = [{doc.id: doc.to_dict()} for doc in products]
    return jsonify(product_list), 200


# Endpoint to insert a new product
@app.route('/insert-product', methods=['POST'])
def insert_product():
    data = request.get_json()  # Assuming you send product data as a JSON payload
    if not data:
        return jsonify({'error': 'Missing product data'}), 400

    # Validate and extract product fields
    name = data.get('name')
    specifications = data.get('specifications')
    description = data.get('description')
    ai_description = data.get('ai_description')
    reviews = data.get('reviews', [])
    pictures = data.get('pictures', [])

    if not name or not specifications or not description:
        return jsonify({'error': 'Incomplete product data'}), 400

    product_data = {
        u'name': name,
        u'specifications': specifications,
        u'description': description,
        u'ai_description': ai_description,
        u'reviews': reviews,
        u'pictures': pictures
    }

    # Add product to Firestore
    db.collection(u'products').add(product_data)

    return jsonify({'message': 'Product inserted successfully'}), 200


@app.route('/search-products', methods=['GET'])
def search_products():
    search_term = request.args.get('query', '')
    products_query = db.collection(u'products').where(u'name', u'==', search_term).get()
    products = [{product.id: product.to_dict()} for product in products_query]
    return jsonify(products), 200

@app.route('/get-picture-url', methods=['GET'])
def get_picture_url():
    # Considering the image is stored under the 'static' folder and named 'uploaded_image.png'
    image_url = request.url_root + 'static/uploaded_image.png'
    return jsonify({'image_url': image_url}), 200


@app.route('/upload-picture', methods=['POST'])
def upload_picture():
    data = request.get_json()
    if not data or 'picture' not in data:
        return jsonify({'error': 'No picture data provided'}), 400

    picture_data = data['picture']
    try:
        # Assume picture_data is a base64 encoded string
        # This decodes the string but does not write to a file
        image_data = base64.b64decode(picture_data)
    except base64.binascii.Error as e:
        return jsonify({'error': 'Invalid base64 data'}), 400

    # Create a unique file path or name for your image
    filename = "uploaded_image.png"  # Modify this to generate a unique name if needed

    # Save the image to Firebase Storage
    storage.child("images/" + filename).put(image_data)

    # Get the image URL
    image_url = storage.child("images/" + filename).get_url(None)

    return jsonify({'message': 'Picture uploaded successfully', 'image_url': image_url}), 200



def get_all_products():
    return 'Get all products'



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
