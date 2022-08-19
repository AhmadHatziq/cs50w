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
<img src="https://raw.githubusercontent.com/AhmadHatziq/cs50w/main/Project%205%20-%20Capstone/capstone/assets/submission_form.png" width="600" height = 350 alt="Submission Form Image">
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

# Folder Contents 

# How To Run The Application 

# Python Package Dependencies & Setup

# Demo Video Link 



