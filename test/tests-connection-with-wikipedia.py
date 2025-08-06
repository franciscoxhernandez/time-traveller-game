import requests
import re
from bs4 import BeautifulSoup
from categories import CATEGORY_TITLES

WIKI_BASE_URL = "https://en.wikipedia.org"


def fetch_wiki_page(url): # safe way to download a Wikipedia page as HTML text.
    try:
        response = requests.get(url, timeout=7) # Tries to send an HTTP GET request to the given url. timeout=7 means: if the server doesn’t respond in 7 seconds, stop waiting
        response.raise_for_status() # Checks if the request was successful, if the server returns an error this line will raise an exception
        return response.text
    except requests.exceptions.RequestException:
        return None


def generate_question_from_infobox(title):
    """
    Check's the Wikipedia infobox for a date label and year.
    Returns (question, year, url).
    """
    url = f"{WIKI_BASE_URL}/wiki/{title}"
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

    for row in infobox.find_all("tr"): #tr table rows contains data like html <tr> <th>Born</th> <td>14 March 1879</td> </tr>
        header = row.find("th") #th gets the header like Born, released
        data = row.find("td") #td get the actual date

    #     < tr >
    #       < th > Born < / th >
    #       < td > 14 March 1879 < / td >
    #     < / tr >

        if header and data:
            label = header.get_text(strip=True)
            if any(keyword in label for keyword in labels_to_look_for):
                text = data.get_text()
                match = re.search(r'\b(\d{3,4})\s*(BC|AD)?', text, re.IGNORECASE)
                # Uses regex to search for a 3- or 4-digit year (\d{3,4}) in the text A RegEx, or Regular Expression,
                # is a sequence of characters that forms a search pattern. RegEx can be used to check if a string contains the specified search pattern
                if match:
                    label_text = label
                    year = int(match.group(1))
                    if match.group(2) and match.group(2).upper() == 'BC':
                        year = -year
                    break

    if year is None or label_text is None:
        return None

    readable_title = title.replace("_", " ")
    question = f"In the Wikipedia article titled \"{readable_title}\", what year is listed for: \"{label_text}\"?"

    return question, year, url


#test which element is corrected retrived from wikipedia
if __name__ == "__main__":
    for category, titles in CATEGORY_TITLES.items():
        print(f"\n🔍 Checking category: {category}") # I can check a specific category for example {category} --> {"history"} and it will only check history
        for title in titles:
            result = generate_question_from_infobox(title)
            if result:
                question, year, url = result
                print(f"\n🟢 Success for: {title}")
                print(f"Question: {question}")
                print(f"Year: {year}")
                print(f"URL: {url}")
            else:
                print(f"\n🔴 Failed to extract info for: {title}")

#














#
# from colorama import init, Fore, Back, Style
# init(autoreset=True)
# import random
# from categories import CATEGORY_TITLES
# import requests
# import re
# from bs4 import BeautifulSoup
#
# WIKI_BASE_URL = "https://en.wikipedia.org"
# categories = ["history", "famous_people", "sports", "music_releases", "movies", "random"]
# score_counter = 0
#
#
# def welcome():
#     messages = [
#
#         "",
#         "WELCOME",
#         "TO THE",
#         "TIME TRAVELER",
#         "GAME",
#
#         "",
#     ]
#
#     max_width = 23
#     max_msg_length=max(len(msg) for msg in messages)
#     padding=4
#     total_width =max_msg_length+padding*2
#     border="*"*(total_width+4)
#     print(Fore.YELLOW+border)
#     for msg in messages:
#         centered_msg = msg.center(max_width)
#         print(Fore.YELLOW + "*" + Fore.GREEN + centered_msg + Fore.YELLOW + "*")
#     print(Fore.YELLOW+border)
#     input("Press Enter to continue...")
#
# # def welcome():
#     messages = [
#         "",
#         "",
#         "WELCOME",
#         "TO THE",
#         "TIME TRAVELER",
#         "GAME",
#         "",
#         "",
#         "",
#         "",
#     ]
#
#     max_width = 30  # Adjust for overall width
#
#     for i in range(len(messages)):
#         stars = "*" * (i + 1 if i < len(messages) // 2 else len(messages) - i)
#         message = messages[i]
#         padding = max_width - len(stars) * 2 - len(message)
#         left_space = padding // 2
#         right_space = padding - left_space
#         print(stars + " " * left_space + message + " " * right_space + stars)
#     input("Press Enter to continue...")
#
# def rules_and_scores_of_the_game():
#     #print("\n--- Welcome to the Time Traveler Wiki Game! ---")
#     print()
#     print("Guess the year associated with key facts pulled live from Wikipedia!")
#     print()
#     print("Think you know history? Put your knowledge to the test in Guess the Year! \nIn this fun and educational game, you're given a famous event — your challenge \nis to guess the year it happened. Get instant feedback after each guess: \nwere you too early, too late, or spot on? \nLearn new facts, improve your memory, and compete for the highest score. \nPerfect for history buffs, \ntrivia fans, or anyone who loves a challenge!")
#     print()
#     input("Press Enter to continue...")
#     print("Game Rules (Multiplayer Game):\n -Choose the number of rounds (1 to 3)\n -Each player  selects a category: sports, history, famous people, music releases, movies and random \n -The player receives a question and must guess the year.\n -The system provides a Wikipedia article with the correct answer")
#
#     print("\nScoring:")
#     print("  - Exact guess: 100 points")
#     print("  - Within 10 years: 50 points")
#     print("  - Within 50 years: 20 points")
#     print("  - Otherwise: 0 points")
#     print("\nInput must be a full year (e.g., 1945), or negative for BC (e.g., -753).")
#     print("----------------------------------------------------\n")
#     input("Press Enter to start the game 🎮...")
#
# def number_and_name_of_players():
#     try:
#         num_player = int(input("How many players would you like to play? (1 to 3) "))
#         if num_player < 1 or num_player > 3:
#             print("Please enter a number between 1 and 3")
#             return number_and_name_of_players()
#         list_of_players = []
#         for i in range(num_player):
#             player_name = input(f"Please enter the name of Player {i + 1} : ")
#             list_of_players.append(player_name)
#         return list_of_players
#     except ValueError:
#         print("Please enter a number.")
#         return number_and_name_of_players()
#
# def get_number_of_rounds():
#     try:
#         rounds = int(input("How many rounds would you like to play? (between 1-3): "))
#         if rounds < 1 or rounds > 3:
#             print("Please enter a number between 1 and 3")
#             return get_number_of_rounds()
#         return rounds
#     except ValueError:
#         print("Please enter a number.")
#         return get_number_of_rounds()
#
#
# def get_topic_from_user():
#     while True:
#         print("\n1. History\n2. Famous People\n3. Sports\n4. Music Releases\n5. Movies\n6. Random\n")
#         topic = input("Which topic do you want the quiz to be about? (1-6) " )
#         if topic in ["1","2","3","4","5"]:
#             return categories[int(topic) - 1]
#         elif topic == "6":
#             return categories[random.randint(0,5)]
#         else:
#             print("Please enter a number from 1 to 6")
#
# # beautiful_soup_integration:
#
# def fetch_wiki_page(url):
#     try:
#         response = requests.get(url, timeout=7)
#         response.raise_for_status()
#         return response.text
#     except requests.exceptions.RequestException:
#         return None
#
#
# def generate_question_from_infobox(title):
#     """
#     Check's the Wikipedia infobox for a date label and year.
#     Returns (question, year, url).
#     """
#     random_article = random.choice(title)
#     url = f"{WIKI_BASE_URL}/wiki/{random_article}"
#
#     html = fetch_wiki_page(url)
#     if not html:
#         return None
#
#     soup = BeautifulSoup(html, "html.parser")
#     infobox = soup.find("table", class_="infobox")
#     if not infobox:
#         return None
#
#     labels_to_look_for = [
#         "Born", "Founded", "Established", "Released", "Opening", "Release date",
#         "First awarded", "Date", "Formed", "Created", "Launched", "Start", "Period"
#     ]
#
#     year = None
#     label_text = None
#
#     for row in infobox.find_all("tr"):
#         header = row.find("th")
#         data = row.find("td")
#         if header and data:
#             label = header.get_text(strip=True)
#             if any(keyword in label for keyword in labels_to_look_for):
#                 text = data.get_text()
#                 match = re.search(r'\b(\d{3,4})\s*(BC|AD)?', text, re.IGNORECASE)
#                 if match:
#                     label_text = label
#                     year = int(match.group(1))
#                     if match.group(2) and match.group(2).upper() == 'BC':
#                         year = -year
#                     break
#
#     if year is None or label_text is None:
#         return None
#
#     #readable_title = title.replace("_", " ")
#     question = f"In the Wikipedia article titled \"{random_article}\", what year is listed for: \"{label_text}\"?"
#
#     return question, year
#
#
#
# def get_user_guess():
#     try:
#         user_guess = int(input("Please enter your guess: "))
#         return user_guess
#     except ValueError:
#         print("Please enter a number.")
#         return get_user_guess()
#
#
# def calculate_difference(user_guess, year):
#     return abs(user_guess - year)
#
# def calculate_points(difference):
#     if difference == 0:
#         print("🍾-Well done! You receive 100 points-🍾")
#         return 100
#     elif difference <= 20:
#         print("🎯-You are pretty close and receive 50 points-🎯")
#         return 50
#     elif difference <= 50:
#         print("📏-You are not that far away and receive 20 points-📏")
#         return 20
#     else:
#         print("❌-You are way off! No points for you in this round-❌")
#         return 0
#
# def show_winner(player_scores):
#     best_player = max(player_scores, key = player_scores.get)
#     highest_score = player_scores[best_player]
#     print(f"{best_player} won the game with {highest_score} points!")
#     input("\nPress enter to go back to the main menu")
#     main()
#
# def main():
#     welcome()
#     rules_and_scores_of_the_game()
#     list_of_players = number_and_name_of_players()
#     number_of_rounds = get_number_of_rounds()
#     category = get_topic_from_user()
#
#     player_scores = {}
#     for player in list_of_players:
#         player_scores[player] = 0
#
#
#     for player in range(len(list_of_players)):
#         player_name = list_of_players[player]
#         print()
#         print(f"--------------------👨‍💻-Player:-{player_name}-👩‍💻--------------")
#         for j in range(number_of_rounds):
#             score = 0
#             print(f"-------------------🎮-Round Nr-{j + 1}-🎮-----------------------")
#             print()
#             question, year = generate_question_from_infobox(CATEGORY_TITLES[category])
#             print(question)
#             user_guess = get_user_guess()
#             print("------------------------------------------------------")
#             if abs(user_guess - year) == 0:
#                 print(f"☑️-You are absolutely correct! The correct answer is {year}.")
#             else:
#                 print(f"⚠️-The difference is {abs(user_guess - year)} years. The correct answer is {year}")
#             print("------------------------------------------------------")
#             difference = calculate_difference(user_guess, year)
#             print("------------------------------------------------------")
#             score = calculate_points(difference)
#             player_scores[player_name] += score
#     print()
#     print()
#     print("--------------------🏆-FINAL SCORE-🏆-----------------------")
#     for name in list_of_players:
#         print(f"{name}: {player_scores[name]} points")
#
#     show_winner(player_scores)
#
#
# if __name__ == "__main__":
#     main()