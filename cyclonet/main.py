import os
import psycopg2
import psycopg2.extras
import jinja2
import io
import torch
import torch.nn as nn
import torchvision.transforms as transforms
import numpy as np
import cv2
from PIL import Image
from psycopg2 import Error
from flask import Flask, flash, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename

'''
CORE CNN MODEL
'''


# Model initialise and loading
# DO NOT EDIT THIS :D
class Model(nn.Module):
    def __init__(self):
        super().__init__()
        self.model = nn.Sequential(
            nn.Conv2d(3, 256, kernel_size=3, stride=1, padding=1),
            nn.BatchNorm2d(256),
            nn.ReLU(),
            nn.Conv2d(256, 256, kernel_size=3, stride=1, padding=1),
            nn.BatchNorm2d(256),
            nn.ReLU(),
            nn.MaxPool2d(2),

            nn.Conv2d(256, 128, kernel_size=3, stride=1, padding=1),
            nn.BatchNorm2d(128),
            nn.ReLU(),
            nn.Conv2d(128, 128, kernel_size=3, stride=1, padding=1),
            nn.BatchNorm2d(128),
            nn.ReLU(),
            nn.MaxPool2d(2),

            nn.Conv2d(128, 64, kernel_size=3, stride=1, padding=1),
            nn.BatchNorm2d(64),
            nn.ReLU(),
            nn.Conv2d(64, 64, kernel_size=3, stride=1, padding=1),
            nn.BatchNorm2d(64),
            nn.ReLU(),
            nn.MaxPool2d(2),

            nn.Conv2d(64, 32, kernel_size=3, stride=1, padding=1),
            nn.BatchNorm2d(32),
            nn.ReLU(),
            nn.Conv2d(32, 32, kernel_size=3, stride=1, padding=1),
            nn.BatchNorm2d(32),
            nn.ReLU(),
            nn.MaxPool2d(2),

            nn.Conv2d(32, 16, kernel_size=3, stride=1, padding=1),
            nn.BatchNorm2d(16),
            nn.ReLU(),
            nn.Conv2d(16, 16, kernel_size=3, stride=1, padding=1),
            nn.BatchNorm2d(16),
            nn.ReLU(),
            nn.MaxPool2d(2),

            nn.Flatten(),
            nn.Linear(784, 1),
        )

    def forward(self, x):
        return self.model(x)


model = Model()
model.load_state_dict(torch.load('saved_modelcyclone', map_location=torch.device('cpu')))
model.eval()
# model ends here


app = Flask(__name__)

'''Connect to PostgreSQL Database'''

DB_HOST = "localhost"
DB_NAME = "cyclone_intensity"
DB_USER = "postgres"
DB_PASSWORD = "admin"

try:
    # establish connection with db
    connection = psycopg2.connect(user=DB_USER,
                                  password=DB_PASSWORD,
                                  host=DB_HOST,
                                  database=DB_NAME)

    connection.autocommit = True

    # create cursor to perform database operations
    cursor = connection.cursor()
    # print PostgreSQL details
    print("PostgreSQL server information:")
    print(connection.get_dsn_parameters(), "\n")

    # permanently commit changes to table
    # connection.commit()

except(Exception, Error) as error:
    print("Error while connecting to PostgreSQL", error)


@app.route("/")
def index():
    return render_template("index.html", rain=1, x=0)


'''Image upload and display'''

UPLOAD_FOLDER = 'static/uploads/'

app.secret_key = "trailblazers"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])


def allowed_img(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# upload form data to database
@app.route("/", methods=['POST'])
def predict():
    # get values from html form
    img_date = request.form.get("image_date")
    img_time = request.form.get("image_time")
    latitude = request.form.get("latitude")
    longitude = request.form.get("longitude")
    print(img_date)
    print(img_time)
    print(latitude)
    print(longitude)
    # get image from html form
    imagefile = request.files['imagefile']

    if imagefile and allowed_img(imagefile.filename):
        filename = secure_filename(imagefile.filename)
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        imagefile.save(image_path)

        image = cv2.imread(image_path)
        image = np.array(image)
        totensor = transforms.ToTensor()
        image = totensor(image)
        resize = transforms.Resize(size=(250, 250))
        image = resize(image)
        image = image.unsqueeze(0)
        predicted_intensity = torch.round(model(image)).item()
        print(predicted_intensity)
        r=100
        if predicted_intensity >= 0 and predicted_intensity <= 30:
            r = 50
        if predicted_intensity >= 30 and predicted_intensity <= 50:
            r = 70
        if predicted_intensity >= 50 and predicted_intensity <= 70:
            r = 80
        if predicted_intensity >= 70 and predicted_intensity <= 100:
            r = 90

        print(r)

        # execute SQL Queries
        cursor.execute("""
                            INSERT INTO insat_data(upload_datetime, coordinates, intensity, images, img_date, img_time)
                            VALUES(current_timestamp,point(%s,%s), %s, %s, %s, %s);""",
                       (latitude, longitude, str(predicted_intensity), filename, img_date, img_time))
        # # fetch result

        # record = cursor.fetchmany()
        # print(record, "\n")
        # close connection and commit to database
        connection.commit()

        print('upload_image filename: ', filename)
        print('image date: ', img_date)
        print('image time: ', img_time)
        print('cyclone latitude: ', latitude)
        print('cyclone longitude: ', longitude)

        # flash('Image successfully uploaded and displayed below')
        return render_template('index.html', prediction=predicted_intensity, filename=filename, rain=r, x=1)
    else:
        flash('Allowed image types are jpg, jpeg, png')
        return redirect(request.url)


# display image after upload
@app.route('/<filename>')
def display_image(filename):
    # print('display_image flename: ' + filename)
    # return redirect(url_for('static', filename='uploads/' + filename), code=301)
    return render_template('image.html', filename=filename)


# archive page
@app.route('/archive')
def archive():
    # execute SQL Queries
    cursor.execute("""
                SELECT * FROM insat_data
                ORDER BY upload_datetime DESC
                LIMIT 20;
                """)
    # # fetch result
    records = cursor.fetchall()
    print("Number of rows: ", len(records))

    arranged_records = []
    for row in records:
        # extract lat, long from coordinates(x,y)
        separator = row[1].find(",")
        lat = row[1][1:separator]
        long = row[1][separator + 1:-1]

        predicted_intensity = row[2]
        image_filename = row[3]
        capture_date = row[4].strftime("%d/%m/%Y")
        capture_time = row[5].strftime("%H:%M:%S")
        # print(lat, long, capture_date, capture_time, image_filename, predicted_intensity)

        record = dict(lat=lat, long=long, predicted_intensity=predicted_intensity,
                      image_filename=image_filename, capture_date=capture_date, capture_time=capture_time)
        arranged_records.append(record)
        # table_items = {lat, long, predicted_intensity, image_filename, capture_date, capture_time}

    # record = cursor.fetchmany()
    # print(record, "\n")
    # close connection and commit to database
    connection.commit()

    return render_template('archive.html', items=arranged_records)


if __name__ == "__main__":
    app.run(debug=True)

if (connection):
    cursor.close()
    connection.close()
    print("PostgreSQL connection closed")