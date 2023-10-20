# Pix.ly Backend

Pix.ly is a RESTful API that manages images and metadata using AWS bucket storage. 
It pairs with the [Pix.ly frontend](https://github.com/igoroganesian/pixly-frontend) for a comprehensive image gallery and upcoming editing features.

## Table of Contents
- [About The Project](#about-the-project)
- [Built With](#built-with)
- [Getting Started](#getting-started)
- [Prerequisites](#prerequisites)
- [Installation](#installation)

[Back to top](#pixly-backend)

## Stack
- Flask
- AWS
- Postgres

[Back to top](#pixly-backend)

### Prerequisites
- Python3
- PostgreSQL
- AWS account

### Installation

1. Set up an AWS Bucket at [https://aws.amazon.com/s3/](https://aws.amazon.com/s3/)
2. Clone the repo:
   ```bash
   git clone https://github.com/igoroganesian/pixly-backend.git
   ```
3. Set up virtual env & install requirements
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip3 install -r requirements.txt
   ```
4. Replace the AWS bucket in app.py with your own:
   ```bash
   AWS_BUCKET_URL = "....s3.us-west-1.amazonaws.com"
   ```
5. Create a PSQL database:
   ```bash
   psql createdb pixly
   ```
6. Change the database link in app.py:
   ```bash
   app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    "DATABASE_URL", 'postgresql:///YOUR_DB')
   ```
7. Run seed.py:
   ```bash
   python3 seed.py
   ```
8. Run app:
   ```bash
   flask run
   (will likely require `flask run -p 5001` on macOS)
   ```
