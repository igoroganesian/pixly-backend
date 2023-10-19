"""Seed file to populate pixly db with sample data."""

from app import app
from models import Image, db
import datetime

now = datetime.datetime.now()

with app.app_context():
    db.drop_all()
    db.create_all()

image1 = Image(
    date_time_created=now.strftime("%m/%d/%Y, %H:%M:%S"),
    date_time_uploaded=now,
    gps_latitude="23.45",
    gps_longitude="35.67",
    make="CANON",
    model="CANON EOS DIGITAL REBEL XTi",
    path="img.jpeg",
    caption="Image caption")

image2 = Image(
    date_time_created=now.strftime("%m/%d/%Y, %H:%M:%S"),
    date_time_uploaded=now,
    gps_latitude="34.05",
    gps_longitude="-118.25",
    make="NIKON",
    model="D850",
    path="img2.jpeg",
    caption="")

db.session.add_all([image1, image2])
db.session.commit()
