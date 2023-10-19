import os

from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
from flask_debugtoolbar import DebugToolbarExtension
from flask_cors import CORS
from models import db, connect_db, PILImage, Image, S3

from dotenv import load_dotenv
load_dotenv()
AWS_BUCKET_URL = "https://io-pixly.s3.us-west-1.amazonaws.com"

app = Flask(__name__)
cors = CORS(app)

app.config['SECRET_KEY'] = "secret"

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    "DATABASE_URL", 'postgresql:///pixly')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True # displays SQL in terminal
app.config['CORS_HEADERS'] = 'Content-Type'

connect_db(app)

debug = DebugToolbarExtension(app)

@app.get("/images")
def get_images():

    search_term = request.args.get('search_term')
    images = Image.query_images(search_term)

    images_with_urls = [
        {
            "image_data": image.serialize(),
            "url": S3.get_presigned_url(image.path)
        }
        for image in images
    ]

    return jsonify(images=images_with_urls)