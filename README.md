# CycloNet

## Cyclone Intensity Estimation using Deep Learning

A Web-App User Interface where the user can upload INSAT-3D IR Satellite Image of Cyclone which is then passed to our Deep Convolutional Neural Network built in PyTorch which is trained on Cyclone imagery of various intensities on our custom dataset curated from Raw INSAT-3D satellite captured images on MOSDAC server. 

The CNN eliminates the need for usage of traditional methods for accurate center determination to estimate the Cyclone intensity using Satellite imagery. 

The Model will return the estimated Intensity of satellite cyclone image in KNOTS instantly, the user would also have the option to upload metadata values like Datetime, latitudinal position, etc. for the Cyclonic event which will be stored in the Database pushing it in a archive of all past cyclonic events that have been inputted in the interface. User can view the past cyclonic events in the database with event-related metadata in the archive and visualize the imagery. Flask will be used to integrate the web-application together in Python.

## Dataset

[Curated Dataset link](https://www.kaggle.com/datasets/sshubam/insat3d-infrared-raw-cyclone-images-20132021)

## Tech Stack Used

Front-end: HTML , CSS, Bootstrap and JavaScript

Back-end: PostgreSQL, Flask, psycopg2 and Python

Machine-learning-pipeline: PyTorch

## Team Description



```
Team Leader Name: Sshubam Verma
Team Leader GitHub: Sshubam
Linkedin: https://www.linkedin.com/in/sshubam-verma-7b70bb19b/
DiscordTag: Sshubam#5388

Team Member Name: Vansh Comar
Team Member GitHub: vacom13
Twitter: vacom13
Linkedin: https://www.linkedin.com/in/vanshcomar/
DiscordTag: honeybubble#7906

Team Member Name: Amith Harish
Team Member GitHub: Amith0205
Linkedin: https://www.linkedin.com/in/amith-harish-59aa8221b/
DiscordTag: Amith#3879

Team Member Name: Ishank Jena
Team Member GitHub: ishankjena
Linkedin: https://www.linkedin.com/in/ishank-jena-3362b2212/
DiscordTag: jenzen#1132
```


## Screenshots and reference Images

``Home section:`` landing section of the website

![Hero](https://user-images.githubusercontent.com/101162842/163724950-78dbfb1e-c414-4d2d-8a12-b7d4b2d4bdc6.jpg)


``Form section:`` used to pass the image to the model which computes intensity and forwards input data to the archive via database

![Form](https://user-images.githubusercontent.com/101162842/163724953-f8479e57-267e-4560-8a1c-9761afe49f35.jpg)


``Live Weather Map:`` made using Windy API, showing live wind patterns and redirects the map to the coordinates recieved as input, incase of a cyclone, highlights the area with strong wind pattern

![Windy map](https://user-images.githubusercontent.com/101162842/163724954-7d91ff9a-be77-436a-967c-a067c485af4f.jpg)


``Archive Table:`` displaying all previously uploaded data stored in database

![Archive Table](https://user-images.githubusercontent.com/101162842/163724961-db84f65f-4d13-49dc-8d97-d30726918a14.jpg)


``Submitted Image:`` Would be displayed as

![Image image](https://user-images.githubusercontent.com/101162842/163724965-9bdb6f09-1d3f-4d4b-be08-dfd7bfdcde03.jpg)


## Links and References: 


- [GitHub](https://github.com/cycloneintensity/CrossKnotHacks-Cyclonet)

- [Youtube](https://www.youtube.com/watch?v=MDmG44oK8Bs)

- [Devfolio](https://devfolio.co/projects/cyclonet-fd57)
