# Needed for core operation
import requests
from bs4 import BeautifulSoup
import json
from time import sleep
from os import system

# Required for optional features
import pyttsx3
from playsound import playsound

# Extra files 
import text_style_functions as tsf

# TODO : Implement features to add/remove, news sources, view news from all sources, select sources, or one source. 
# TODO : Implement features to modify presentation features.
# TODO PRIORITY: Create class method to handle modification of the config file
# TODO LATER : Create a module that allows for easier menu creation. 
# TODO LATER : See if possible to scrape articles from links. i.e. without hardcoding.

class headliner_app():
    def __init__(self):
        self.source_information = self.recall_sources("config.json")
        self.headlines = self.prepare_headlines()
        self.presentation_options = self.recall_presentation_options("config.json")

    def recall_sources(self, source_file) -> dict:
        """Summary --> Retrieves news source data from config.json. Returns information as a list of dictionaries.
            Returns --> (list(dicts)) : A list containing key word pairs relating to the attributes of in use news sources"""
        with open(source_file) as json_file:
            config_information = json.load(json_file)
            return config_information["sources"]
        
    def recall_presentation_options(self, source_file) -> dict:
        """Summary --> Retrieves presentation preferences from config.json. Returns data as a dictionary.
            Returns --> (dict) : A set of key word pairs indicating the current option selection."""
        with open(source_file) as json_file:
            config_information = json.load(json_file)
            return config_information["presentation_options"]

    def scrape_page_data(self, URL:str) -> list:
        """Summary --> Accepts target site as URL. Retrieves raw HTML. Parses with bs4. Discovers post details from remaining text. Returns list of posts in dictionary form
            Arguments --> URL (str) : String version of target URL
            Returns --> posts_clean_list (list) : List of Post data in dicts. Includes title, description, link, and date."""

        page = requests.get(URL)
        soup = BeautifulSoup(page.text)

        match URL:
            case 'https://thehackernews.com':
            
                posts_raw_html = [data for data in soup.find_all('div', class_ = "body-post clear")]
                posts_clean_list = []

                for post in posts_raw_html:
                    post_title = post.find_all('h2', class_ = 'home-title')[0].text
                    post_desc = post.find_all('div', class_ = 'home-desc')[0].text
                    post_link = post.find_all('a', class_ = 'story-link')[0].get('href')
                    post_date = post.find_all('span', class_ = 'h-datetime')[0].text[1::]

                    posts_clean_list.append({
                        "title" : post_title,
                        "description" : post_desc,
                        "link" : post_link,
                        "date" : post_date
                    })

                return posts_clean_list
            
    def prepare_headlines(self) -> dict:
        """Summary --> Returns a dictionary, headlines, of news headlines from news sources. 
            Returns --> headlines (dict) : Dictionary where keys are equal to the name of a given news source. Values are lists of posts in dict formating."""
        headlines = {}
        for source in self.source_information:
            headlines[source["News_Source_Name"]] = self.scrape_page_data(source["News_Source_Link"])
        return headlines

    # NOTE : Don't bother worrying about the stupid number of display_X functions right now. Get this bitch working first. Later, after hitting version 1.0, work on a menu module.
    def display_headliner_logo(self):
        with open("headliner_logo.txt", "r") as file:
            lines = file.read().splitlines()
            for line in lines:
                print(line)
            file.close()

    def display_main_menu(self):
        system('cls')
        self.display_headliner_logo()
        menu_options = ["Show News", "Change Settings", 'Exit']
        menu_bar = ''.join(['_' for _ in range(73)])+"\n"
        
        print(menu_bar)
        for option in menu_options:
            print(f" [{option[0]}] {option}")
        print(menu_bar)
        
        
        menu_selection = ''
        while (menu_selection not in [option[0].upper() for option in menu_options]):
            menu_selection = str(input('Selection : ')).upper()
            
        match menu_selection:
            case 'S':
                self.display_headlines()
            case 'C':
                self.display_settings_menu()
            case 'E':
                exit()
                
    def display_settings_menu(self):
        system('cls')
        menu_options = ["Presentation Settings", "Feed Settings", "Back"]
        menu_bar = ''.join(['_' for _ in range(73)])+"\n"
        
        print(menu_bar)
        for option in menu_options:
            print(f" [{option[0]}] {option}")
        print(menu_bar)
        
        menu_selection = ''
        while (menu_selection not in [option[0].upper() for option in menu_options]):
            menu_selection = str(input('Selection : ')).upper()
            
        match menu_selection:
            case 'P':
                self.display_presentation_menu()
            case 'F':
                # TODO : Create Feed Menu
                # self.display_feed_menu()
                print("I havent made this section yet.")
            case 'B':
                self.display_main_menu()
    
    def display_presentation_menu(self):
        system('cls')
        menu_bar = ''.join(['_' for _ in range(73)])+"\n"
        menu_options = [option for option in self.presentation_options]
        menu_options.append("b")
        
        print(menu_bar)
        for option in menu_options:
            if option == "b":
                print(" [B] Back")
            else:
                print(f" {option} : {self.presentation_options[option]}")
        print(menu_bar)
        
        menu_selection = ''
        while (menu_selection not in [option.lower() for option in menu_options]):
            menu_selection = str(input('Selection : ')).lower()
            
        match menu_selection:
            case 'toggle tts':
                if self.presentation_options["Toggle TTS"] == False:
                    print("Current configuration is 'False'. Changing configuration to 'True'.")
                else:
                    print("Current configuration is 'True'. Changing configuration to 'False'.")
            case 'toggle automatic continuation':
                if self.presentation_options["Toggle Automatic Continuation"] == False:
                    print("Current configuration is 'False'. Changing configuration to 'True'.")
                else:
                    print("Current configuration is 'True'. Changing configuration to 'False'.")
            case 'number of articles displayed':
                article_display_number = 0
                while article_display_number not in range(1,11):
                    article_display_number = int(input("How many articles would you like displayed : "))
                print(f"Changing number of displayed articles to {article_display_number}")
            case 'b':
                self.display_settings_menu()
                

    def display_headlines(self):
        """Summary --> Recalls self.headlines, which contains news source and headlining article information. Displays news source preceding each sources articles.  Displays data from headline articles."""

        for news_source in self.headlines:
            source_message = (f"Now presenting the headlines from {tsf.style_text(news_source, 'f96b49')}")
            length_news_source = len(news_source)
            
            source_break_line_color = tsf.style_text(''.join(['_' for _ in range(length_news_source)]), 'f96b49')
            source_break_line_white = ''.join(['_' for _ in range(len(source_message)-12-length_news_source)])
            source_break_line = source_break_line_white + source_break_line_color

            print(f"\n{tsf.style_text(source_break_line, 'f97b49')}\n{tsf.style_text(source_message, 'f97b49U')}\n")

            source_articles = self.headlines[news_source]
            articles_to_be_read = [article for article in source_articles if source_articles.index(article) >= 5]

            for article in articles_to_be_read:
                header = (f"{article['title']} | {article['link']} | {article['date']}")
                body = (f"{article['description']}...")
                break_line = ''.join(['_' for _ in range(len(header))])

                print(f"\n{header}\n{break_line}\n{body}\n")
                
                if self.presentation_options["Toggle TTS"] == True:
                    self.read_to_me_im_lazy(article["title"])
                    sleep(.5)
                    self.read_to_me_im_lazy(body)

                if self.presentation_options["Toggle Automatic Continuation"] == False:
                    self.handle_progression_of_articles()
                
    def handle_progression_of_articles(self):
        print("\nWould you like to know more...")
        if self.presentation_options["Toggle TTS"] == True:
            playsound('./would_you_like_to_know_more.mp3')
        # TODO: Figure out some choices
        input()
    
    def read_to_me_im_lazy(self,message:str):
        """Summary --> Function for Text-to-Speech option. Initializes tts engine and reads provided message.
            Arguments --> message (str) : Message to be read."""
        engine = pyttsx3.init()
        engine.say(message)
        engine.runAndWait()
    
def main():
    Headliner = headliner_app()
    Headliner.display_main_menu()
    # print(Headliner.source_information)

if __name__ == "__main__":
    main()
    