# Santa Tracker - CS50 Final Project

#### Video Demo: https://youtu.be/RP4jPomwwyA

# Introduction
This project is a Python version of a popular holiday game by NORAD (North American Aerospace Defense Command) called **"NORAD Tracks Santa".** Although the tradition has existed since 1955, a web-based version was developed in 1997 that visualizes Santa’s journey and allows users to track him as he travels. 

In the simulation, Santa leaves the North Pole on December 24th to fly around the globe delivering presents. Users can watch Santa travel in real time, following him on a map to see where he is in the world. Statistics such as “last seen”, “headed to” and the number of gifts that have been delivered so far are also available. 

Despite the popularity of the original NORAD version, the program now also has a service developed by Google in 2004 called “Google Santa Tracker” that contains many of the same features and capabilities.

# Description
For the CS50 final project, I created a more simple command line interface version of the simulation in Python. The project relies on `project.py` and `test_project.py`, where the main code and tests for its functions are stored. It also utilizes a CSV file downloaded from [SimpleMaps](https://simplemaps.com/data/us-cities) containing 30,000 cities in the United States that Santa “travels” to.

The file `project.py` contains the main code for the program which has ten functions including `main`. It is designed for the user to enter a location within the United States which will be geocoded using the Python library [geopy](https://pypi.org/project/geopy/). The program then prints how far away Santa is in miles and what city he’s currently in. After that, it starts a loop with a menu that allows the user to track Santa again with the same location, enter a new location, see the number of gifts that have been delivered or exit the program. 

This project also utilizes another file called `visited.csv` which keeps track of cities Santa has already been to. The program reads from the original `uscities.csv` file and restructures the data to create a route sorted by longitude so that Santa travels from east to west. A function called “travel” in `project.py` then writes each city to `visited.csv` one by one, pausing for a calculated “delivery time”, which is the amount of time in seconds it takes Santa to deliver gifts in that city based on its population.

# Limitations

Right away, I had to make a tough design choice to restrict Santa’s travel to only the United States due to the scope of my project. This was not the most ideal design as I wanted the program to mimic the web-based versions which follow Santa around the entire world. However, even when filtering out many cities due to small populations, the program would still need to iterate through tens of thousands of cities per country in order to accurately simulate real time travel. 

Even when limiting tracking capabilities to only within the United States, the program takes 45 minutes for Santa to cover the whole country. I decided it was reasonable for my final project to track Santa through one country instead of all of the countries in the world. This made error checking the geocoder and user input easier and ultimately made my code more functional and user friendly. 

In the future, I hope to explore alternative methods to simulating Santa's travel that don't rely on iteration and very large CSV files, allowing Santa's travel to expand globally.

I also made a choice to assign the value of 150,000 gifts per second to be the rate at which Santa delivers gifts. Although Santa files at almost 3 million miles per hour in order to deliver all gifts by Christmas Day according to Google, there is no official number from the online versions on how many gifts are delivered per second. 

I chose 150,000 somewhat arbitrarily, but the speed simulates real time relatively well and causes Santa to stop in each city long enough for the user to actually see where he currently is. Any faster and the delivery time is so small that Santa does not stay in one city for more than a fraction of a second at a time. A slower speed only takes longer to iterate through all 30,000 cities and causes the program to run for too long. 

Additionally, I chose not to organize the logic for tracking Santa into a class because there was no need to create instances of Santa with different attributes. Retrieving the most recent entry from `visited.csv` was sufficient for the user to be able to “track” Santa’s current location. Therefore the code in `project.py` is only functions, but they work well together to serve the user's needs and I did not feel it was necessary to complicate the program with a class if it wasn’t contributing to the functionality of the code.

# Acknowledgements

Thank you to David J. Malan and Harvard's [CS50: Introduction to Programming with Python](https://cs50.harvard.edu/python/) for creating the opportunity to develop this project. 

My completed CS50 certificate can be viewed [here](https://www.linkedin.com/in/rachael-johnson-61637a210) on my LinkedIn.





