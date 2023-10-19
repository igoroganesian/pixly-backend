import os

from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
# from flask_debugtoolbar import DebugToolbarExtension
from flask_cors import CORS
from models import  connect_db, Image
from s3 import S3

from dotenv import load_dotenv
load_dotenv()

AWS_BUCKET_URL = "https://io-pixly.s3.us-west-1.amazonaws.com"

app = Flask(__name__)
# CORS(app, resources={r"*": {"origins": "http://localhost:3000"}},
#      supports_credentials=True)
CORS(app)

app.config['SECRET_KEY'] = "secret"

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    "DATABASE_URL", 'postgresql:///pixly')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True # displays SQL in terminal
# app.config['CORS_HEADERS'] = 'Content-Type'

connect_db(app)

# debug = DebugToolbarExtension(app)

# @app.route('/test-cors', methods=['GET'])
# def test_cors():
#     return "CORS headers should be set!"

@app.get("/images")
def get_images():

    search_term = request.args.get('search_term')
    images = Image.query_images(search_term)

    images_with_urls = []
    for image in images:
        url = S3.get_presigned_url(image.path)
        serialize = image.serialize()

        images_with_urls.append({"image_data":serialize, "url":url})

    return jsonify(images=images_with_urls)

def add_image_to_db(file, file_name, caption):
    return Image.add_image_data(file=file, path=file_name, caption=caption)


def upload_image_to_s3(file, file_name):
    S3.upload_file(file_name=file, save_as_name=file_name)

@app.post("/images/upload")
def upload_image():
    """
    Adds new photo to db and aws
    returns images with url {images: [{img_data, url}]}
    """
    file = request.files.get('file')

    if not file or file.filename == '':
        return jsonify(error="Invalid file or filename")

    file_name = secure_filename(file.filename)
    caption = request.form.get('caption', '')

    try:
        image = add_image_to_db(file, file_name, caption)
        upload_image_to_s3(file, file_name)
    except Exception as e:
        app.logger.error(f"Image upload failed: {e}")
        return jsonify(error=e)

    url = S3.get_presigned_url(image.path)
    serialize = image.serialize()

    return jsonify(images=[{"image_data": serialize, "url": url}])

@app.get("/images/<int:id>")
def get_image_by_id(id):
    """
    Retrieve an AWS-stored image by its ID.

    Parameters:
    - id (int): The ID of the desired image.

    Returns:
    - dict: A dictionary containing the image data and its S3 URL.
            {images: [{"image_data": <serialized_image_data>, "url": <s3_url>}]}
    """
    try:
        image = Image.get_image_data(id=id)
    except Exception as e:
        app.logger.error(f"Error fetching image with id {id}: {e}")
        return jsonify(error=e)

    image_url = S3.get_preassigned_url(image.path)
    image_data = image.serialize()

    return jsonify(images=[{"image_data": image_data, "url": image_url}])