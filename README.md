# cs50w
Repository for the CS50W lectures, projects etc. Taken in 2022.

Aside from the lecture material, there are 6 projects covered in this course. They are as follows: 

## Projects
- [Search](#search)
- [Wiki](#wiki)
- [Commerce](#commerce)
- [Mail](#mail)
- [Network](#network)
- [Capstone: Geocache](#capstone-geocache)

# [Search](https://github.com/AhmadHatziq/cs50w/tree/main/Project%200%20-%20Search) 

Simple website which aims to replicate the Google Search webpage. Uses HTML form tags and JavaScript to achieve the functionalities.

The functionalities are as follows: 
1. Users can input string queries and search using the normal Google search orGoogle image search. 
2. Users can do an advanced Google search. 
3. Users can access the `I'm Feeling Lucky` feature of Google search. 

Video demo can be found [here](https://www.youtube.com/watch?v=4mnQtnxfZWI). 

Code can be found [here](https://github.com/AhmadHatziq/cs50w/tree/main/Project%200%20-%20Search). 

# [Wiki](https://github.com/AhmadHatziq/cs50w/tree/main/Project%201%20-%20Wiki/wiki) 

Django website which aims to replicate Wikipedia. Entries are stored locally as `markdown` files which are rendered dynamically using the [Django template language (DTL)](https://docs.djangoproject.com/en/4.1/topics/templates/). 

The functionalities are as follows: 
1. Create: Users can create new `markdown` entries, which will be stored locally. 
2. Edit: Users can edit existing entries. 
3. Search: Users can search for corresponding entries with a standard string search. 
4. Random page: Users can opt to view a random entry. 

Video demo can be found [here](https://www.youtube.com/watch?v=jd25pUiqDRA). 

Code can be found [here](https://github.com/AhmadHatziq/cs50w/tree/main/Project%201%20-%20Wiki/wiki). 

# [Commerce](https://github.com/AhmadHatziq/cs50w/tree/main/Project%202%20-%20Commerce/commerce) 

An eBay-like e-commerce auction site built using Django and Django Models. 

The functionalities are as follows: 
1. Users can post auction listings. 
2. Users can place bids on listings. Bids must be ≥ the current bid amount. 
3. Users can comment on the listings. 
4. Users can add listings to a watchlist. 

Video demo can be found [here](https://www.youtube.com/watch?v=g1BGqi07Qnk). 

Code can be found [here](https://github.com/AhmadHatziq/cs50w/tree/main/Project%202%20-%20Commerce/commerce). 

# [Mail](https://github.com/AhmadHatziq/cs50w/tree/main/Project%203%20-%20Mail) 

A front-end email client, which renders everything on a single webpage. JavaScript is used to handle the front-end client and its interactions with the back-end, which is done via aynchronous API calls. 

All the functionalities is in a single JavaScript file, [`inbox.js`](https://github.com/AhmadHatziq/cs50w/blob/main/Project%203%20-%20Mail/mail/static/mail/inbox.js). 

The functionalities are as follows: 
1. Users can compose and send emails to other users. 
2. Users can view emails in their inbox and sentbox. 
3. Users can mark emails as `archive` or `unarchive`. 
4. Users can reply emails from their inbox. 

Video demo can be found [here](https://www.youtube.com/watch?v=pMrE-vUEKkU). 

Code can be found [here](https://github.com/AhmadHatziq/cs50w/tree/main/Project%203%20-%20Mail). 

# [Network](https://github.com/AhmadHatziq/cs50w/tree/main/Project%204%20-%20Network/project4) 

A Twitter-like social network website where users can make text-based posts, follow other users and like/unlike posts. 
There is a combination of asynchronous and standard POST requests made by the application to the back-end. 

The functionalities are as follows: 
1. Users can create text-based posts. 
2. Paginated view of all posts is shown on the index page. 
3. Users can view other user profiles, which shows the posts made by the specified user. 
4. Users can follow other users, which only shows posts made by their followed users. 
5. Users can edit posts that they had made. 
6. Users can `like` or `unlike` posts. There is a counter which shows the total number of likes. 

Video demo can be found [here](https://www.youtube.com/watch?v=BOW9xJOGtDk). 

Code can be found [here](https://github.com/AhmadHatziq/cs50w/tree/main/Project%204%20-%20Network/project4). 

# [Capstone: Geocache](https://github.com/AhmadHatziq/cs50w/tree/main/Project%205%20-%20Capstone/capstone)

A discussion-based website revolving around posts made on Google Maps. The purpose is to support Geocaching. 

JavaScript is extensively used to interact and render the Google Map instance. 

What is Geocaching? 
> Geocaching is an outdoor recreational activity, in which participants use a Global Positioning System device and other navigational techniques to hide and seek containers, called "geocaches" or "caches", at specific locations marked by GPS coordinates all over the world.

The functionalities are as follows: 
1. Users can add a geocache by clicking on the Google Map, which will automatically populate the input coordinates on the form. 
2. Users can view nearby geocaches to them on the map. 
3. Users can mark each geocache as `found` or `unfound` by interacting with the map markers. 
4. Users can discuss about each geocache on a discussion page. The inputs can be both text-based content or an image file. 

Video demo can be found [here](https://www.youtube.com/watch?v=RQH51yzz_PM). 

Code can be found [here](https://github.com/AhmadHatziq/cs50w/tree/main/Project%205%20-%20Capstone/capstone). 
