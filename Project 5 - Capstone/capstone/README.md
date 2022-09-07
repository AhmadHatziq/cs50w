##### Table of Contents  
- [Project Writeup](#project-writeup)
- [Distinctiveness and Complexity](#distinctiveness-and-complexity)
    - [Code Contributions For Significant Files](#code-contributions-for-significant-files-what-i-did)
    - [Design Considerations](#design-considerations)
    - [Justifications for Distinctiveness and Complexity Requirements](#justifications-for-distinctiveness-and-complexity-requirements)
    - [Django Models](#django-models)
        - [`Users`](#users)
        - [`Geocache`](#geocache)
        - [`DiscussionBoard`](#discussionboard)
    - [How Does This Application Help Geocachers? ](#how-does-this-application-help-geocachers)
    - [Google Maps integration (with screenshots)](#google-maps-integration)
- [User Guide](#user-guide)
    - [Adding A Geocache](#adding-a-geocache)
    - [Viewing Nearby Geocaches](#viewing-nearby-geocaches)
    - [Marking A Geocache As Found/Unfound](#markingunmarking-a-geocache-as-foundunfound)
    - [Discussing About A Geocache](#discussing-about-a-geocache)
- [Folder Contents](#folder-contents)
- [Python Package Dependencies & Setup](#python-package-dependencies--setup)
- [How To Run The Application](#how-to-run-the-application)
- [Demo Video Link](#demo-video-link)

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li>
      <a href="#usage">Usage</a>
      <ul>
        <li><a href="#authentication">Authentication</a></li>
        <li><a href="#intake-calculator">Intake Calculator</a></li>
        <li><a href="#user-profile">User Profile</a></li>
      </ul>
    </li>
    <li><a href="#file-structure">File Structure</a></li>
    <li>
      <a href="#distinctiveness-and-complexity">Distinctiveness and Complexity</a>
      <ul>
        <li><a href="#distinctiveness">Distinctiveness</a></li>
        <li><a href="#complexity">Complexity</a></li>
      </ul>
    </li>
  </ol>
</details>

# Project Writeup
The title of this project is 'Geocache'. The aim is to support users who would like to take part in Geocaching. 

What is Geocaching? 
> Geocaching is an outdoor recreational activity, in which participants use a Global Positioning System device and other navigational techniques to hide and seek containers, called "geocaches" or "caches", at specific locations marked by GPS coordinates all over the world. 

Essentially, it is a form a treasure hunting! 

This application will help users view geocaches hosted in their surrounding areas and discuss about each geocache post. 


# Distinctiveness and Complexity

This project uses the following technologies: 
- 3 Django models 
- [Google Maps JavaScript API](https://developers.google.com/maps/documentation/javascript)
- [Google Maps Static API](https://developers.google.com/maps/documentation/maps-static/overview)
- JavaScript 
- CSS 
- HTML

## Justifications for Distinctiveness and Complexity Requirements 

This project is sufficiently different from the old CS50W Pizza project and Project 2 (Commerce) as there are no items being sold/bought/auctioned etc. The only entity in this project are the `Geocaches`. 

The project is different from Project 4 (Network) as although there are posts being displayed in this project, the posts here utilize both text and image contents, rather than just text contents. Furthermore, the only asynchronous function is when a `Geocache` is marked as `found` or `unfound`, which I have implemented using the `PUT` method. 

This project is sufficiently different from the other projects as it extensively interacts with the Google Maps API using JavaScript. 

## Design Considerations

One of the main motivations of this project was to enhance my skills in using public APIs, in this case the Google Maps API. A location-based treasure hunting activity (geocaching) appears to fulfil the use-case of using the Google Maps API. 

To keep the data models manageable, only 3 data models were used. One for the user accounts, another for the geocache data and lastly for the discussion posts. 

The challenge of this project comes in knowing how to render data via Google Maps and obtaining user inputs (coordinates) for it. Vanilla JavsScript is extensively used to support the interaction with Google Maps.

This project is mobile responsive with the help of Bootstrap. 

## Code Contributions For Significant Files (What I Did)  

The significant code contributions are listed below: 

| Filename      | Code Contributions |
| ----------- | ----------- |
| `admin.py`      | 3 data models are registered with the admin site. To display the fields which have multiple foreign keys, such as `models.ManyToManyField(User)`,  a string method is generated. The method will iterate over each `User` field and concatenate them into a single field.     |
| `utils.py`   | Contains a single function, `load_google_maps_API_key()`. This function will look into the folder called `/api_key` for any text files and load it as the Google Maps API key.        |
| `urls.py` | Contains 11 URL routes. One URL route is used to serve images. Another URL route is used to test the geoposition and another is used to serve error messages. The remaining 8 URL routes are used to serve the core application: index, login, logout, register, view_map, submit_geocache, view discussion_board and view geocache_discussion_post. |
| `views.py` | There are 11 functions within this file. Their elaborations are as follows: <ul><li>`index(request)`: Serves the index page, `index.html`. </li><li>`login_view(request)`: Serves the login page if accessed via `GET`. Processes the login information if data is sent via `POST`.</li> <li> `logout_view(request)`: Logs the user out. </li> <li> `register(request)`: Handles the user account registration procedures. Either serves the registration form (via `GET`) or processes the registration details (via `POST`). </li> <li> `process_geocache(request)`: Is a helper function for `view_map()` and `submit_geocache()`. This function will extract all the records in `Geocache` and categorize each based on the current `User` logged in. It returns a list of `Geocache` objects.  </li> <li> `view_map(request)`: If accessed via `GET`, this method will call `process_geocache()` to obtain a list of `Geocache` objects. The list will be converted to a `JSON` object and passed to the template page, `main_map.html`. If data is sent via 'PUT', the `User` will either be added or removed to the list of `User` founders for each `Geocache` object.  </li> <li> `submit_geocache(request)`: If accessed via `GET`, this method will return a `Geocache` submission form to the user. If data is sent via `POST`, a new `Geocache` and `DiscussionBoard` object will be created. The `DiscusisonBoard` object represents the hint and title used to generate the new `Geocache`. </li> <li> `discussion_board(request)`: This method will call `process_geocache()` and obtain a list of `Geocache` objects. The list will be further split into the 3 categories and a parsed timestamp field is generated. The final list will be passed and rendered via `discussion_board.html`. </li> <li> `geocache_discussion_post(request, geocache_id)`: If data is sent via `POST`, a new `DiscussionBoard` object is created. If accessed via `GET`, a form will be sent to the user. <li>`test_geoposition(request)`: This is a test function to practice interacting with the Google Maps API. </li> <li> `error(request)`: This is a method which returns a template (`error.html`), displaying an error message.  </li> 
| `models.py` | Contains the 3 data models used for this project. They are: <li> `User`: Represents a single user account. </li>  <li> `Geocache`: Represents a single geocache. Contains fields to store the GPS coordinates, geocache title, geocache hint, `Users` that have found the geocache and the timestamp. </li>  <li> `DiscussionBoard`: Represents a single comment made for any `Geocache`. </li>  |  </li></ul>| 
| `error.html` | Represents an error HTML page, with links that redirects back to the index. |
| `test_geoposition.html` | Represents a test HTML page which renders coordinates from the Google Maps API. |
| `layout.html` | Contains the layout page, which contains placeholder template for JavaScript, banner messages. CSS etc. |
| `login.html` | Represents the login page. |
| `register.html` | Represents the user account registration page. |
| `index.html` | Represents the home page. This page contains a textual description of what is Geocaching as well as a YouTube video describing it. There are 3 JavaScript functions which aims to obtain the user GPS coordinates and store it within the `localStorage`: <li> `setUserPosition(position)`: Obtains the GPS coordinates and stores into the `localStorage`. </li> <li> `handleLocationError(error)`: Used to handle the event where the user GPS coordinates cannot be obtained. </li> <li> `getLocation()`: Calls the previous 2 functions. </li> |
| `main_map.html` | Represents a Google Maps rendered page. The HTML will display the Google Maps image as well as legends for the icons used. There are 4 JavaScript functions which are used: <li> `addMarker(lat, lng, title, contentString, icon_url)`: Used to add a marker to a Google Maps. Will require the GPS coordinates, title, HTML content string and icon URL to display on the map itself. </li> <li> `updateGeocaches(geocaches_input, geocache_id, status)`: Used to change the global JSON array of `Geocaches` when the button (which is within the HTML content of each marker) is clicked. </li>  <li> `toggleFound(event, geocache_id)`: This function is attached to the button defined in the Google Map pop-up HTML div content (`contentString`). The aim is to toggle the found/not found status for a Geocache and sends the request asynchronously to the backend.  </li> <li> `initializeMap()`: Used to initialize the Google Maps instance, when the page is loaded. This function will create all the markers and its associated contents. </li>  |
| `submit_geocache.html` | Contains a submission form, with a Google Maps instance rendered below. The purpose of the Google Maps instance is so that the user can click on the map, which will auto-populate the GPS coordinate fields of the form. There is 1 JavaScript function, `initializeMap()` which |
| `geocache_discussion_post.html` | This page represents the discussion regarding a `Geocache`. It uses the static Google Maps API, which only uses the `<img>` tag. At the top of the page, there are 4 buttons. Each button will toggle the views for each type of static image ie: roadmap, satellite, hybrid, terrain. The JavaScript function attached to each button is `toggle_terrain(terrain_type)`, which just changes the image source being displayed. |
| `discussion_board.html` | This page will display all the Geocaches, according to their 3 categories.  | 

For the full write-up of all the files in the directories, please refer to the [Folder Directory Contents](#folder-contents)

## Django Models

There are 3 data models used in this project: `Users`, `Geocache` and `DiscussionBoard`. 

### `Users`
The standard `User` model is used, to create new accounts. 

### `Geocache`
`Geocache` represents the geocache object itself. There are fields to store the latitude and longitude GPS coordinates, character fields to store the hints and titles as well as timestamps. The `User` fields are used to store the owner of the geocache and keep track of `Users` that have found the field. 

The other remaining fields are not currently in use. 

### `DiscussionBoard`
`DiscussionBoard` represents a single discussion forum post. There are fields to contain the comment itself (character and image field) as well as keeping track of the referenced `Geocache`, the `User` that created the post and the timestamp. 

## How Does This Application Help Geocachers? 

Using this application, users can log in and do the following: 
- Mark geocache locations via Google Maps 
- View all nearby geocaches near their location 
- Discuss with other users regarding a geocache

## Google Maps integration
What makes this project unique is that there are extensive interactions with the Google Maps API to render the maps and get inputs from the user. 
There are 3 webpages that interact with the Google Maps API. Their features are detailed below. 
- `submit_geocache.html`: This page renders an interactable map using the Google Maps JavaScript API. To submit a geocache, a user needs to either manually supply the latitude and longitude coordinates or click on the map. This will auto populate the input fields with the coordinates. 

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

## Viewing Nearby Geocaches

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

To get to the discussion page, the user can either click the link in the pop up above (Fig. 6) or navigate to the `Discussion` section of the navigation bar. 

At the `Discussion` section, the user will be able to see a consolidated list of all the geocaches, separated into the 3 previous categories.

<figure>
<img src="https://raw.githubusercontent.com/AhmadHatziq/cs50w/main/Project%205%20-%20Capstone/capstone/assets/discussion_board.png"  alt="Discussion Board View">
<figcaption align = "left"><b>Fig. 7 - Discussion board of all geocaches.</b></figcaption>
</figure>

The user will be able to click on any of the geocache titles to access the discussion for a single geocache. 

In the discussion page, users can discuss with each other regarding finding the geocache. The application accepts image uploads to facilitate  the discussion. 

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
│   │───api_key
│   │       GOOGLE_MAPS_API.txt - Contains the API key needed to interact with Google Maps
│   │
│   ├───migrations
│   │ 
│   │───static
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
│   │                                  JavaScript is also used to automatically retrieve the coordinates based on mouseClick events. 
│   │           main_map.html - Renders a Google map instance to the user using JavaScript. Inside the map, the markers are added as well as 
│   │                           their relevant contents. When the user marks a geocache as found/unfound, an asynchronous request is sent to
│   │                           the back-end while the front-end content is also updated.      
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

The list of dependencies can be found in [`requirements.txt`](https://github.com/AhmadHatziq/cs50w/blob/main/Project%205%20-%20Capstone/capstone/pip_requirements.txt). 

They can be installed with the command: 

`pip install -r pip_requirements.txt`

The application was developed using a Windows 11 64-bit machine running Anaconda and Python version 3.9.12.  

# How To Run The Application 

Before running the application, ensure that all dependencies are installed and a valid Google Maps API key is obtained. The Google Maps API key can be obtained [here](https://developers.google.com/maps/documentation/javascript/get-api-key).

Please save your API key in a text file inside the [`/api_key`](https://github.com/AhmadHatziq/cs50w/tree/main/Project%205%20-%20Capstone/capstone/geocache/api_key) directory. 

As per usual Django projects, navigate to the folder with the file `manage.py` and run the following commands to make migrations.

`python manage.py makemigrations`

`python manage.py migrate`

And to run the server: 

`python manage.py runserver`

The loaded Google Maps API key should be printed in the console, as well as the local address of the index page. 

# Demo Video Link 

Please click on the image below to be redirected to the demo video. 

<a href="https://youtu.be/RQH51yzz_PM">
<img src="https://raw.githubusercontent.com/AhmadHatziq/cs50w/main/Project%205%20-%20Capstone/capstone/assets/video_thumbnail.png" alt="YouTube Demo Video" width="600" height = "350">
</a>
