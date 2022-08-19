##### Table of Contents  
[Project Writeup](#project-writeup)
[Distinctiveness and Complexity](#distinctiveness-and-complexity)


# Project Writeup
The title of this project is 'Geocache'. The aim is to support users who would like to take part in Geocaching. 

What is Geocaching? 
> Geocaching is an outdoor recreational activity, in which participants use a Global Positioning System device and other navigational techniques to hide and seek containers, called "geocaches" or "caches", at specific locations marked by GPS coordinates all over the world. 

Essentially, it is a form a treasure hunting! 

# Distinctiveness and Complexity

This project uses the following technologies: 
- 3 Django models 
- [Google Maps JavaScript API](https://developers.google.com/maps/documentation/javascript)
- [Google Maps Static API](https://developers.google.com/maps/documentation/maps-static/overview)
- JavaScript 
- CSS 
- HTML

## Django Models

There are 3 models used in this project: `Users`, `Geocache` and `DiscussionBoard`. 

### `Users`
The standard `User` model is used, to create new accounts. 

### `Geocache`
`Geocache` represents the geocache object itself. There are fields to store the latitude and longitude GPS coordinates, character fields to store the hints and titles as well as timestamps. The User fields are used to store the owner of the geocache and keep track of Users that have found the field. 

The other remaining fields are not currently in use. 

### `DiscussionBoard`
`DiscussionBoard` represents a single discussion forum post. There are fields to contain the comment itself (character and image field) as well as keeping track of the referenced `Geocache`, the `User` that created the post and the timestamp. 

## How Does This Application Help Geocachers? 

Using this application, users can log in and do the following: 
- Mark geocache locations via Google Maps 
- View all nearby geocaches near their location 
- Discuss with other users regarding a geocache

## Google Maps integration
What makes this project unique is that there is extensive interaction with the Google Maps API to render the maps and get inputs from the user. 
There are 3 webpages that interacts with the Google Maps API. Their features are detailed below. 
- `submit_geocache.html`: This page renders an interactable map using the Google Maps JavaScript API. To submit a geocache, a user needs to either manually supply the latitude and longitude coordinates or click on the map. This will autopopulate the input fields with the coordinates. 

<figure>
<img src="https://raw.githubusercontent.com/AhmadHatziq/cs50w/main/Project%205%20-%20Capstone/capstone/assets/submission_form.png" width="600" height = "350" alt="Submission Form Image">
<figcaption align = "left"><b>Fig. 1 - Form for submitting a geocache</b></figcaption>
</figure>

- `main_map.html`: This page renders an interactive map using the Google Maps JavaScript API. The main map will render all geocaches in close proximity to the user. 
    - Each geocache has a popup, which will display more information (such as the hints, time posted and link to the discussion page). 

    <figure>
    <img src="https://raw.githubusercontent.com/AhmadHatziq/cs50w/main/Project%205%20-%20Capstone/capstone/assets/pop_up_map.png" alt="Pop Up Geocache Display">
    <figcaption align = "left"><b>Fig. 2 - Pop-up content when the user clicks on a marker representing a geocache</b></figcaption>
    </figure>

    - The geocaches will be categorized into 3 categories:
        - `Created Geocaches` (A geocache owner cannot mark their own geocache as `discovered` or `undiscovered`)
        - `Undiscovered Geocaches`
        - `Discovered Geocaches`

    <figure>
    <img src="https://raw.githubusercontent.com/AhmadHatziq/cs50w/main/Project%205%20-%20Capstone/capstone/assets/main_map.png" alt="Geocache Map">
    <figcaption align = "left"><b>Fig. 3 - Map showing all geocaches in an area</b></figcaption>
    </figure>
   

- `geocache_discussion_post.html`: This page renders a static map using the Google Maps Static API. However, the views can be toggled using the side buttons. In the discussion page, the map image loaded is already zoomed in, allowing users to easily see the nearby landmarks. This would facillitate discussion about the geocache. 

    <figure>
    <img src="https://raw.githubusercontent.com/AhmadHatziq/cs50w/main/Project%205%20-%20Capstone/capstone/assets/static_toggle.png" alt="Static Maps With Toggle">
    <figcaption align = "left"><b>Fig. 4 - Static images with toggle buttons</b></figcaption>
    </figure>

# User Guide

## Adding A Geocache 

After logging in, a user will be able to add a geocache by clicking on `Input a Geocache` in the navigation bar. 

<figure>
<img src="https://raw.githubusercontent.com/AhmadHatziq/cs50w/main/Project%205%20-%20Capstone/capstone/assets/input_geocache_option.png" alt="Geocache Option Highlighted">
<figcaption align = "left"><b>Fig. 4 - Geocache input option on the navigation bar</b></figcaption>
</figure>

Once at the input page, the user can either manually input the GPS coordinates or click inside the map, which will auto populate the fields. 
Aside from the GPS longitude and latitude coordinates, the user will need to specify the geocache title and associated hint. 

<figure>
<img src="https://raw.githubusercontent.com/AhmadHatziq/cs50w/main/Project%205%20-%20Capstone/capstone/assets/submission_form.png" width="600" height = "350" alt="Submission Form Image">
<figcaption align = "left"><b>Fig. 1 - Form for submitting a geocache</b></figcaption>
</figure>

## Viewing Mearby Geocaches

After inputting the geocache, the user will be redirected to the `View Map` section of the application. 
Here, the user will be able to see any recently created geocaches (in blue), as well as discovered (in green) and undiscovered (in red) geocaches. The current user location will also be marked with the 'house' icon. 

<figure>
<img src="https://raw.githubusercontent.com/AhmadHatziq/cs50w/main/Project%205%20-%20Capstone/capstone/assets/new_input_geocache.png" width="600" height = 350 alt="Map">
<figcaption align = "left"><b>Fig. 5 - Map showing newly created and undiscovered geocaches</b></figcaption>
</figure>

## Marking/Unmarking A Geocache As Found/Unfound

While in the `View Map` portion of the application, the user will be able to click on any marker. An option for marking the geocache as found/undiscover is visible if the geocache is not created by the user. This is to prevent a geocache owner from marking his/her own cache. 

<figure>
<img src="https://raw.githubusercontent.com/AhmadHatziq/cs50w/main/Project%205%20-%20Capstone/capstone/assets/pop_up_map_all_markers.png"  alt="Pop Up Of All Categories">
<figcaption align = "left"><b>Fig. 6 - Pop up content for all 3 markers.</b></figcaption>
</figure>

## Discussing About A Geocache 

To get to the discussion page, the user can either click the link in the pop up above (Fig. 6) or nagivate to the `Discussion` section of the navigation bar. 

At the `Discussion` section, the user will be able to see a consolidated list of all the geocaches, seperated into the 3 previous categories.

<figure>
<img src="https://raw.githubusercontent.com/AhmadHatziq/cs50w/main/Project%205%20-%20Capstone/capstone/assets/discussion_board.png"  alt="Discussion Board View">
<figcaption align = "left"><b>Fig. 7 - Discussion board of all geocaches.</b></figcaption>
</figure>

The user will be able to click on any of the geocache titles to access the discussion for a single geocache. 

In the discussion page, users can discuss with each other regarding finding the geocache. The application accepts image uploads to facillitate the discussion. 

<figure>
<img src="https://raw.githubusercontent.com/AhmadHatziq/cs50w/main/Project%205%20-%20Capstone/capstone/assets/discussion_page_1.png"  alt="Discussion Page">
<figcaption align = "left"><b>Fig. 8 - Discussion page regarding a single geocache.</b></figcaption>
</figure>

At the bottom of the discussion page, a user can submit their comments and image (optional). 

<figure>
<img src="https://raw.githubusercontent.com/AhmadHatziq/cs50w/main/Project%205%20-%20Capstone/capstone/assets/discussion_page_2.png"  alt="Discussion Page">
<figcaption align = "left"><b>Fig. 9 - Comment submission for discussion page.</b></figcaption>
</figure>

# Folder Contents 

The contents of the directory represents a standard Django application. The notable core components are in the `geocache` folder. 

```
│   db.sqlite3 - Current implementation uses a sqlite3 file as the database. 
│   manage.py - Core file needed to run the application. 
│   README.md - This markdown file. 
│
├───assets/ - Images used for the markdown. 
│
├───capstone/ - Main folder created by Django. 
│
├───geocache/ - Main folder for the Geocache application.
│   │   admin.py - Creates the views for the admin UI for the data models used.
│   │   apps.py
│   │   models.py - Contains the 3 Django models used.
│   │   tests.py
│   │   urls.py - Contains the URL routes for the application as well as static URLs to serve images (for the comments).
│   │   utils.py - Contains the function used to load the Google Maps API key from the local directory.
│   │   views.py - Contains the main logic for the whole application.
│   │   __init__.py
│   │
│   ├───api_key
│   │       GOOGLE_MAPS_API.txt - Contains the API key needed to interact with Google Maps
│   │
│   ├───migrations
|   | 
│   ├───static
│   │   └───geocache
│   │       │   styles.css
│   │       │
│   │       └───images/ - Contains the icons used to serve as markers on the map. 
│   │
│   ├───templates
│   │   └───geocache
│   │           layout.html - Represents the layout used for the other HTML pages. 
│   │           register.html - Allows the user to register for an account. 
│   │           login.html - Enables the user to login and use the application. 
│   │           error.html - Displays a generic error page. 
│   │           index.html - Landing page when the user logs in. Gives an introduction of geocaching to the user and asks for location access. 
│   │           submit_geocache.html - Renders a Google map instance to the user using JavaScript. Allows the user to input a geocache.
|   |                                  JavaScript is also used to automatically retrieve the coordinates based on mouseClick events. 
│   │           main_map.html - Renders a Google map instance to the user using JavaScript. Inside the map, the markers are added as well as 
|   |                           their relevant contents. When the user marks a geocache as found/unfound, an asynchronous request is sent to
|   |                           the back-end while the front-end content is also updated.      
│   │           discussion_board.html - Displays all the geocaches as well as their discussion page links. 
│   │           geocache_discussion_post.html - Displays the contents of a single geocache. Renders a static Google map instance with 
|   |                                           toggleable buttons. 
│   │           test_geoposition.html - Used for testing purposes. 
│   │
│   └───__pycache__
│
└───image_storage/ - Used to store the images uploaded by users as comments. 
```
# Python Package Dependencies & Setup

The list of dependencies can be found in [`requirements.txt`](https://github.com/AhmadHatziq/cs50w/blob/main/Project%205%20-%20Capstone/capstone/requirements.txt). 

The application was developed using a Windows11 64-bit machine running Anaconda and Python version 3.9.12.  

# How To Run The Application 

Before running the application, ensure that all dependencies are installed and a valid Google Maps API key is obtained. The Google Maps API key can be obtained [here](https://developers.google.com/maps/documentation/javascript/get-api-key).

Please save your API key in a text file inside the [`/api_key`](https://github.com/AhmadHatziq/cs50w/tree/main/Project%205%20-%20Capstone/capstone/geocache/api_key) directory. 

As per usual Django projects, avigate to the folder with the file `manage.py` and run the following command. 

`python manage.py runserver`

The loaded Google Maps API key should be printed in the console, as well as the local address of the index page. 

# Demo Video Link 

<a href="http://www.youtube.com/watch?v=dQw4w9WgXcQ">
<img src="https://raw.githubusercontent.com/AhmadHatziq/cs50w/main/Project%205%20-%20Capstone/capstone/assets/video_thumbnail.png" alt="YouTube Demo Video" width="600" height = "350">
</a>
