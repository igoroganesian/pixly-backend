from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import PIL.Image as PILImage
from PIL.ExifTags import TAGS

db = SQLAlchemy()

EXIF_TAGS = ["DateTimeOriginal",
             "GPSLatitude",
             "GPSLongitude",
             "Make",
             "Model"]


def connect_db(app):
    """Connect to database."""

    app.app_context().push()
    db.app = app
    db.init_app(app)
