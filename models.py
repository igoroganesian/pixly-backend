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

class Image (db.Model):
    """Creates an image instance"""

    __tablename__ = "images"

    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    date_time_uploaded = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )
    date_time_created = db.Column(
        db.String,
    )

    gps_latitude = db.Column(
        db.String,
    )

    gps_longitude = db.Column(
        db.String,
    )

    path = db.Column(
        db.String,
        nullable=False
    )

    caption = db.Column(
        db.String,
        nullable=False
    )

    make = db.Column(
        db.String,
    )

    model = db.Column(
        db.String,
    )

    def serialize(self):
        """Returns a dictionary representation of the Image object."""
        return {
            "id": self.id,
            "date_time_uploaded": self.date_time_uploaded,
            "date_time_created": self.date_time_created,
            "gps_latitude": self.gps_latitude,
            "gps_longitude": self.gps_longitude,
            "make": self.make,
            "model": self.model,
            "path": self.path,
            "caption": self.caption,
        }

    @classmethod
    def add_image_data(cls, path, file, caption):
        """Saves the uploaded image properties to the database.

        Args:
            path (str): AWS key path for the image.
            file: File storage object (expected to be a .jpeg).
            caption (str): Caption for the image.

        Returns:
            Image: The created Image object.
        """

        exif_data = cls.get_img_exif_data(file=file)
        image = Image(
            date_time_created=exif_data.get("DateTimeOriginal"),
            gps_latitude=exif_data.get("GPSLatitude"),
            gps_longitude=exif_data.get("GPSLongitude"),
            path=path,
            caption=caption,
            make=exif_data.get("Make"),
            model=exif_data.get("Model")
        )
        db.session.add(image)
        db.session.commit()
        return image

    @classmethod
    def get_image_data(cls, id):
        """Retrieves the image properties from the database by its ID.

        Args:
            id (int): Image ID.

        Returns:
            Image: The fetched Image object or 404 error if not found.
        """
        return cls.query.get_or_404(id)

    @classmethod
    def query_images(cls, search_term=None):
        """Retrieves images from the database, optionally filtering by caption.

        Args:
            search_term (str, optional): Term to filter captions. Defaults to None.

        Returns:
            List[Image]: List of Image objects.
        """
        if search_term:
            # Using parameterized query to prevent SQL injections.
            images = (cls.query
                      .filter(cls.caption.ilike(f"%{search_term}%"))
                      .order_by(cls.date_time_uploaded)
                      .all())
            return images
        return cls.query.all()

    @classmethod
    def get_img_exif_data(cls, file):
        """Extracts the EXIF data from an image file.

        Args:
            file: File storage object (expected to be a .jpeg).

        Returns:
            dict: Dictionary with EXIF data of interest.
        """
        img = PILImage.open(file)
        exif_data = img._getexif()

        if exif_data is None:
            return {}

        return {TAGS[key]: value for key, value in exif_data.items()
                if TAGS[key] in EXIF_TAGS}