import csv
import threading
import sys
import time
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
from geopy.exc import GeocoderTimedOut, GeocoderServiceError, GeocoderQueryError, GeocoderUnavailable

def main():
    route = get_route("uscities.csv")
    print("After a long and magical night of worldwide travel, Santa has arrived in the USA!")
    time.sleep(4)
    print("You can follow Santa and his sleigh across the United States by entering your location below.")
    travel_thread = threading.Thread(target=travel, args=(route,), daemon=True)
    travel_thread.start()
    time.sleep(3)
    while True:
        validated = validate_location()
        coded = geocode(*validated)
        if coded == None:
            print("Could not get location, try again")
        else:
            print(format_santa(coded))
            break
    track_loop(coded)

def get_route(file):
    cities = []
    gifts_per_second = 150000
    try:
        with open(file, "r") as original:
            reader = csv.DictReader(original)
            for row in reader:
                if int(row["population"]) != 0 and float(row["lng"]) < 0:
                    seconds = f"{(int(row["population"]) / gifts_per_second):.3f}"
                    cities.append({
                                    "city_name": row["city"],
                                    "state": row["state_name"],
                                    "population": int(row["population"]),
                                    "latitude": float(row["lat"]),
                                    "longitude": float(row["lng"]),
                                    "delivery_time": seconds
                                    })
    except FileNotFoundError:
        print("Couldn't get Santa's travel route")
    else:
        cities = sorted(cities, key=lambda city: city["longitude"], reverse=True)

    return cities

def travel(route):
    with open("visited.csv", "w") as visited:
        fieldnames = route[0].keys()
        writer = csv.DictWriter(visited, fieldnames=fieldnames)
        writer.writeheader()

        for stop in route:
            writer.writerow(stop)
            visited.flush()
            time.sleep(float(stop["delivery_time"]))

def validate_location():
    while True:
        try:
            user_city, user_state = input("Current location (city, state): ").split(",")
            if user_state == "":
                raise ValueError
        except ValueError:
            print("Invalid input")
        else:
            return user_city, user_state

def geocode(user_city, user_state):
    geolocator = Nominatim(user_agent="santa_tracker")

    try:
        coded = geolocator.geocode(user_city + "," + user_state)
        if coded:
            if coded.raw["addresstype"] not in ["city","town","suburb"]:
                raise ValueError
            else:
                full_address = coded.address.split(",")
                country = full_address[-1].strip()
                if "United States" not in country:
                    raise ValueError
        else:
            raise GeocoderUnavailable

    except (ValueError, GeocoderTimedOut, GeocoderServiceError, GeocoderQueryError, GeocoderUnavailable):
        return None
    else:
        return coded


def track_loop(coded):
    while True:
        choice = input("1: Track again 2: Enter a new location 3: Gifts delivered 4: exit ")

        if choice == "1":
            print(format_santa(coded))
        elif choice == "2":
            while True:
               validated = validate_location()
               coded = geocode(*validated)
               if coded == None:
                  print("Could not get location, try again")
               else:
                  print(format_santa(coded))
                  break
        elif choice == "3":
            print(get_gifts())
        elif choice == "4":
            sys.exit("See you next time!")

def format_santa(coded):
    user_location = coded.address.split(",")
    user_coordinates = (coded.latitude, coded.longitude)
    santa_location = track()
    santa_coordinates = (santa_location["latitude"], santa_location["longitude"])
    distance = f"{geodesic(user_coordinates, santa_coordinates).miles:.3f}"

    if check_visited(user_location) == True:
        return f"Santa has already visited {user_location[0]}! Santa is currently {distance} mi away in {santa_location["city_name"]}, {santa_location["state"]}."
    elif float(distance) > 20:
        return f"Santa is currently {distance} mi away delivering gifts in {santa_location["city_name"]}, {santa_location["state"]}."
    else:
        return f"Santa is currently in {santa_location["city_name"]}, {santa_location["state"]}!"

def check_visited(user_location):
    try:
        with open("visited.csv", "r") as visited:
            reader = csv.DictReader(visited)
            for row in reader:
                if row["city_name"] in user_location and row["city_name"] != track()["city_name"]:
                    return True
    except FileNotFoundError:
        print("Santa hasn't left the North Pole yet!")

def track():
        city = {}
        try:
            with open("visited.csv", "r") as visited:
                reader = visited.readlines()
                santa_location = reader[-1].strip().split(",")
                keys = ["city_name", "state", "population", "latitude", "longitude", "delivery_time"]

                for i in range(len(santa_location)):
                    city[keys[i]] = santa_location[i]
        except FileNotFoundError:
            print("Santa hasn't left the North Pole yet!")
        else:
            return city

def get_gifts():
    gifts_delivered = 0
    try:
        with open("visited.csv") as visited:
            reader = csv.DictReader(visited)
            previous_row = None
            for row in reader:
                if previous_row:
                    gifts_delivered += int(previous_row["population"])
                previous_row = row
    except FileNotFoundError:
        print("Santa hasn't delivered any gifts yet!")
    else:
        return f"{gifts_delivered:,} gifts have been delivered!"


if __name__ == "__main__":
    main()

























