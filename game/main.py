from colorama import init, Fore, Back, Style
init(autoreset=True)
import random
from categories import CATEGORY_TITLES
import requests
import re
from bs4 import BeautifulSoup

WIKI_BASE_URL = "https://en.wikipedia.org"
categories = ["history", "famous_people", "sports", "music_releases", "movies", "random"]
score_counter = 0

def welcome():
    """Display welcome screen."""
    messages = [
        "",
        "",
        "WELCOME",
        "TO THE",
        "TIME TRAVELER",
        "GAME",
        "",
        "",
        "",
        "",
    ]

    max_width = 30  # Adjust for overall width

    for i in range(len(messages)):
        stars = "*" * (i + 1 if i < len(messages) // 2 else len(messages) - i)
        message = messages[i]
        padding = max_width - len(stars) * 2 - len(message)
        left_space = padding // 2
        right_space = padding - left_space
        print(Fore.CYAN + stars + " " * left_space +Fore.MAGENTA + message + Fore.CYAN + " " * right_space + stars)

    input("Press Enter to continue...")


def rules_and_scores_of_the_game():
    """Display the game description and rules"""
    print()
    print(Fore.BLACK + Back.LIGHTBLUE_EX + "-----------------------GAME DESCRIPTION-----------------------------")
    print("Guess the year associated with key facts pulled live from Wikipedia!")
    print()
    print("Think you know history? Put your knowledge to the test in Guess the Year! \nIn this fun and educational game,"
          " you're given a famous event — your challenge \nis to guess the year it happened. Get instant feedback after "
          "each guess: \nwere you too early, too late, or spot on? \nLearn new facts, improve your memory, and compete "
          "for the highest score. \nPerfect for history buffs, \ntrivia fans, or anyone who loves a challenge!")
    print()
    input("Press Enter to continue...")
    print()
    print(Fore.BLACK + Back.LIGHTBLUE_EX + "-----------------------GAME RULES:-----------------------------")
    print("-Choose the number of rounds (1 to 3)\n-Each player  selects a category: sports, history, famous people, "
          "music releases, movies and random \n-The player receives a question and must guess the year.\n-The system "
          "provides a Wikipedia article with the correct answer")
    print()
    print("\nHINT:Input must be a full year (e.g., 1945), or negative for BC (e.g., -753).")
    print()
    print(Fore.BLACK + Back.LIGHTBLUE_EX + "-----------------------SCORINGSYSTEM:-------------------------")
    print("  - Exact guess: 100 points")
    print("  - Within 10 years: 50 points")
    print("  - Within 50 years: 20 points")
    print("  - Otherwise: 0 points")

    print("----------------------------------------------------\n")
    input("Press Enter to start the game 🎮...")
    print()
    print()

def number_and_name_of_players():
    """Ask the user how many players are going to play and their names"""
    try:
        num_player = int(input(Fore.LIGHTBLUE_EX +"How many players would you like to play? (1 to 3) "))
        print()
        if num_player < 1 or num_player > 3:
            print(Fore.LIGHTBLUE_EX +"Please enter a number between 1 and 3")
            print()
            return number_and_name_of_players()
        list_of_players = []
        for i in range(num_player):
            player_name = input(Fore.LIGHTBLUE_EX+ f"Please enter the name of Player {i + 1} : ")
            print()
            list_of_players.append(player_name)
        return list_of_players
    except ValueError:
        print(Fore.LIGHTBLUE_EX +"Please enter a number.")
        print()
        return number_and_name_of_players()

def get_number_of_rounds():
    """Ask the user to enter the number of rounds"""
    try:
        rounds = int(input(Fore.LIGHTBLUE_EX +"How many rounds would you like to play? (between 1-3): "))
        print()
        if rounds < 1 or rounds > 3:
            print(Fore.LIGHTBLUE_EX+"Please enter a number between 1 and 3")
            return get_number_of_rounds()
        return rounds
    except ValueError:
        print(Fore.LIGHTBLUE_EX+ "Please enter a number.")
        return get_number_of_rounds()


def get_topic_from_user():
    """Ask the user to select one topic the topic"""
    while True:
        print("\n1. History\n2. Famous People\n3. Sports\n4. Music Releases\n5. Movies\n6. Random\n")
        topic = input(Fore.LIGHTBLUE_EX + "Which topic do you want the quiz to be about? (1-6) " )
        if topic in ["1","2","3","4","5"]:
            return categories[int(topic) - 1]
        elif topic == "6":
            random_category = categories[random.randint(0,5)]
            return random_category
        else:
            print(Fore.LIGHTBLUE_EX+ "Please enter a number from 1 to 6")

def fetch_wiki_page(url):
    try:
        response = requests.get(url, timeout=7)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException:
        return None

def generate_question_from_infobox(title):
    """
    Check's the Wikipedia infobox for a date label and year.
    Returns (question, year, url).
    """
    random_article = random.choice(title)
    url = f"{WIKI_BASE_URL}/wiki/{random_article}"

    html = fetch_wiki_page(url)
    if not html:
        return None

    soup = BeautifulSoup(html, "html.parser")
    infobox = soup.find("table", class_="infobox")
    if not infobox:
        return None

    labels_to_look_for = [
        "Born", "Founded", "Established", "Released", "Opening", "Release date",
        "First awarded", "Date", "Formed", "Created", "Launched", "Start", "Period"
    ]

    year = None
    label_text = None

    for row in infobox.find_all("tr"):
        header = row.find("th")
        data = row.find("td")
        if header and data:
            label = header.get_text(strip=True)
            if any(keyword in label for keyword in labels_to_look_for):
                text = data.get_text()
                match = re.search(r'\b(\d{3,4})\s*(BC|AD)?', text, re.IGNORECASE)
                if match:
                    label_text = label
                    year = int(match.group(1))
                    if match.group(2) and match.group(2).upper() == 'BC':
                        year = -year
                    break

    if year is None or label_text is None:
        return None

    question = f"In the Wikipedia article titled \"{random_article}\", what year is listed for: \"{label_text}\"?"

    return question, year

def get_user_guess():
    """Ask the user to guess the question"""
    try:
        user_guess = int(input(Fore.LIGHTYELLOW_EX +"Please enter your guess: "))
        return user_guess
    except ValueError:
        print(Fore.LIGHTYELLOW_EX + "Please enter a number.")
        return get_user_guess()

def calculate_difference(user_guess, year):
    """Calculate the difference between the user's guess and the year"""
    return abs(user_guess - year)

def calculate_points(difference):
    """Calculate the amount of points"""
    if difference == 0:
        print("🧠-BIG BRAIN MODE (EXACT GUESS: 100 POINTS)")
        return 100
    elif difference <= 10:
        print("😬 CRINGE FACE (WITHIN 10 YEARS: 50 POINTS)")
        return 50
    elif difference <= 50:
        print("🦖 DINOSAUR (WITHIN 50 YEARS: 20 POINTS)")
        return 20
    else:
        print("📡 SATELLITE DISH (OTHERWISE: 0 POINTS)")
        return 0

def show_winner(player_scores):
    """Display the winner"""
    highest_score = max(player_scores.values())
    best_player = max(player_scores, key = player_scores.get)

    top_players = []
    for player, score in player_scores.items():
        if score == highest_score:
            top_players.append(player)
    if len(top_players) == 1:
        print(f"{best_player} won the game with {highest_score} points!\n")
    else:
        names = " and ".join(top_players)
        print(f"{names} tied with {highest_score} points!\n")

def play_again_or_quit():
    """Ask the user to play again or quit the game"""
    again_or_quit = input("Press 'A' to play again or 'Q' to quit...")
    if again_or_quit.lower() != "a" and again_or_quit.lower() != "q":
        print("Please enter either 'A' or 'Q'.\n")
        play_again_or_quit()
    elif again_or_quit.lower() == "a":
        main()
    elif again_or_quit.lower() == "q":
        print("Thank you for playing.\n")

def main():
    welcome()
    rules_and_scores_of_the_game()
    list_of_players = number_and_name_of_players()
    number_of_rounds = get_number_of_rounds()
    category = get_topic_from_user()

    player_scores = {}
    for player in list_of_players:
        player_scores[player] = 0

    for player in range(len(list_of_players)):
        player_name = list_of_players[player]
        print()
        print(f"--------------------👨‍💻-Player:-{player_name}-👩‍💻--------------")
        for j in range(number_of_rounds):
            score = 0
            print(f"-------------------🎮-Round Nr-{j + 1}-🎮-----------------------")
            print()
            question, year = generate_question_from_infobox(CATEGORY_TITLES[category])
            print(question)
            user_guess = get_user_guess()
            print("------------------------------------------------------")
            if abs(user_guess - year) == 0:
                print(f"☑️-You are absolutely correct! The correct answer is {year}.")
            else:
                print(f"⚠️-The difference is {abs(user_guess - year)} years. The correct answer is {year}")
            print("------------------------------------------------------")
            difference = calculate_difference(user_guess, year)
            print("------------------------------------------------------")
            score = calculate_points(difference)
            player_scores[player_name] += score
    print()
    print()
    print(Fore.BLACK + Back.MAGENTA + "--------------------🏆-FINAL SCORE-🏆-----------------------")
    for name in list_of_players:
        print(f"{name}: {player_scores[name]} points")

    show_winner(player_scores)
    play_again_or_quit()

if __name__ == "__main__":
    main()
