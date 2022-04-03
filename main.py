from art import logo
import pandas as pd
import random
import requests
from bs4 import BeautifulSoup

def generate_character(dataframe):
    class_pick = random.choice(dataframe["Class"][:15])
    location_pick = random.choice(dataframe["Location"][:22])
    weapon_pick = random.choice(dataframe["Weapon"])
    print(f"You are a {class_pick} from {location_pick} who wields the {weapon_pick}.")

def run_program():
    ds_data = pd.read_csv("DarkSoulsData.csv")
    print(logo)
    generate_character(ds_data)
    game_running = True
    while game_running:
        run_again = input("Would you like to generate another character? Type Y or N: ").lower()
        if run_again == "y":
            generate_character(ds_data)
        elif run_again == "n":
            print("Thanks for playing!")
            game_running = False
        else:
            print("Sorry, that's not a valid input. Please type only Y or N.")

try:
    run_program()
except FileNotFoundError:
    game_list = ["Dark_Souls", "Dark_Souls_II", "Dark_Souls_III"]
    base_url = "https://darksouls.fandom.com/wiki/"
    location_list = []
    class_list = []
    weapon_list = []

    # Extract Locations
    for game in game_list:
        response = requests.get(f"{base_url}Category:{game}:_Mentioned_Locations")
        data = response.text
        location_soup = BeautifulSoup(data, "html.parser")
        location_data = location_soup.find_all(class_="category-page__member-link")
        for location in location_data:
            if location.get("title") not in location_list:
                location_list.append(location.get("title"))

    # Extract DS1 Classes
    response = requests.get(f"{base_url}Classes_({game_list[0]})")
    data = response.text
    class_soup = BeautifulSoup(data, "html.parser")
    class_data = class_soup.find_all(class_="mw-headline")
    for class_name in class_data[2:]:
        if class_name.get("id") not in class_list:
            class_name = class_name.get("id").lower()
            class_list.append(class_name)

    # Extract DS2 and DS3 Classes
    for game in game_list[1:]:
        response = requests.get(f"{base_url}Classes_({game})")
        data = response.text
        class_soup = BeautifulSoup(data, "html.parser")
        class_data = class_soup.find_all(name="b")
        classes = class_data[1:8]
        for item in classes:
            class_name = item.text.lower()
            if class_name not in class_list:
                class_list.append(class_name)

    # Extract DS1 Weapons
    response = requests.get(f"{base_url}Weapons_({game_list[0]})")
    data = response.text
    weapon_soup = BeautifulSoup(data, "html.parser")
    weapon_soup = weapon_soup.find_all("li")
    for item in weapon_soup:
        weapon = item.find('a')
        try:
            if 'title' in weapon.attrs:
                weapon = weapon.text
                if weapon not in weapon_list:
                    weapon_list.append(weapon)
        except AttributeError:
            pass
    weapon_list = weapon_list[:140]

    # Extract DS2 Weapons
    response = requests.get(f"{base_url}Weapons_({game_list[1]})")
    data = response.text
    weapon_soup = BeautifulSoup(data, "html.parser")
    for item in weapon_soup.find_all('li'):
        weapon = item.find('a')
        try:
            if 'title' in weapon.attrs:
                weapon = weapon.text
                if ":" not in weapon and "\n" not in weapon and weapon not in weapon_list:
                    weapon_list.append(weapon)
        except AttributeError:
            pass
    weapon_list = weapon_list[:329]
    # Extract DS3 Weapons
    response = requests.get(f"{base_url}Weapons_({game_list[2]})")
    data = response.text
    weapon_soup = BeautifulSoup(data, "html.parser")
    for item in weapon_soup.find_all('li'):
        weapon = item.find('a')
        try:
            if 'title' in weapon.attrs:
                weapon = weapon.text
                if ":" not in weapon and "\n" not in weapon and weapon not in weapon_list:
                    weapon_list.append(weapon)
        except AttributeError:
            pass
    weapon_list = weapon_list[:469]

    ds_dict = {"Class": class_list, "Location": location_list, "Weapon": weapon_list}
    ds_df = pd.DataFrame.from_dict(ds_dict, orient="index")
    ds_df = ds_df.transpose()
    ds_df.to_csv("DarkSoulsData.csv")
