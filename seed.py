"""Seed file to populate pixly db with sample data."""

from app import app, S3
from models import Image, db
import datetime
import os

now = datetime.datetime.now()

with app.app_context():
    db.drop_all()
    db.create_all()

# List of sample images to upload
sample_images = [
    {
        "path": "./static/images/uni1.png",
        "date_time_created": now.strftime("%m/%d/%Y, %H:%M:%S"),
        "date_time_uploaded": now,
        "gps_latitude": "23.45",
        "gps_longitude": "35.67",
        "make": "CANON",
        "model": "CANON EOS DIGITAL REBEL XTi",
        "caption": "Image caption"
    },
    {
        "path": "./static/images/uni2.png",
        "date_time_created": now.strftime("%m/%d/%Y, %H:%M:%S"),
        "date_time_uploaded": now,
        "gps_latitude": "34.05",
        "gps_longitude": "-118.25",
        "make": "NIKON",
        "model": "D850",
        "caption": ""
    }
]

for image_data in sample_images:
    # Extract the filename from the path
    file_name = os.path.basename(image_data["path"])

    # Upload the image to S3
    with open(image_data["path"], "rb") as file:
        # Store the file in S3 and use the filename as is in S3
        S3.upload_file(file, file_name)

    # Create Image instance with updated path
    image_instance = Image(
        date_time_created=image_data["date_time_created"],
        date_time_uploaded=image_data["date_time_uploaded"],
        gps_latitude=image_data["gps_latitude"],
        gps_longitude=image_data["gps_longitude"],
        make=image_data["make"],
        model=image_data["model"],
        path=file_name,  # use the filename as path
        caption=image_data["caption"]
    )

    db.session.add(image_instance)

db.session.commit()
