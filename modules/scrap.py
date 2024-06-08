from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from os import path
from time import sleep
import platform
import json

from .tweet import Tweet
from .logger import Logger
from .telegram import SendMessage

class Scrap:
    def __init__(self, log: Logger):
        self.log = log

    def run(self):
        self.__load_conf()

        # i = 1
        while True:
            # Update Configurations
            self.__load_conf()
            self.open_driver()
            self.__load_users()

            # if i % 5 == 0:
            #     self.driver.quit()
            #     self.open_driver()

            # Start Script runnings
            for user in self.users:
                self.log.info(f"Checking >> {user}...")
                # i += 1
                while True:
                    try:
                        self.driver.get(f"https://twitter.com/{user}")
                        username = get_username(self.driver)
                    except TimeoutException:
                        self.log.warning("Timeout, maybe out of memory, retrying...")
                        # self.driver.refresh()
                        self.driver.quit()
                        self.open_driver()
                        continue
                    break

                sent_tweets = self.__get_sent_tweets(user)

                Ad = []
                # User already has a profile
                if sent_tweets:
                    while True:
                        tweet = Tweet(self.driver, self.log, Ad)

                        # No new tweets
                        if tweet.get_url() in sent_tweets:
                        #     self.log.info(f"A new tweet found {tweet.get_url()}")
                        #     SendMessage(tweet, username)
                        #     self.log.success(f"Message sent successfully")
                            break

                        # A new tweet posted
                        else:
                            self.log.info(f"A new tweet found {tweet.get_url()}")
                            SendMessage(tweet, username)
                            self.__record_new_tweet(tweet, user)
                            self.log.success(f"Message sent successfully")

                # No profile exist!- A recently added account -
                else:
                    self.log.info(f"Creating new profile >> {user}")
                    tweet = Tweet(self.driver, self.log, Ad)
                    self.__create_user_profile(tweet, user)

                sleep(10)

            self.log.info(f"Sleeping {self.conf['sleep']} sec...")
            self.driver.quit()
            sleep(self.conf["sleep"])
            self.log.info("Running again...")

    def open_driver(self):
        self.__open_driver()
        self.driver.get("https://twitter.com/")
        self.__set_token()

    def __get_sent_tweets(self, user):
        if path.isfile(f"./files/users/{user}.txt"):
            return open(f"./files/users/{user}.txt").read().splitlines()
        else:
            return []

    def  __create_user_profile(self, tweet: Tweet, user: str):
        self.__record_new_tweet(tweet, user)

    def __record_new_tweet(self, tweet: Tweet, user: str):
        with open(f"./files/users/{user}.txt", "a") as file:
            file.write(tweet.get_url() + "\n")

    def __open_driver(self):
        options = Options()

        options.add_argument('--log-level=3')
        options.add_argument('ignore-certificate-errors')

        if platform.system() != "Windows":
            options.add_argument("--headless=new")
            options.add_argument("--window-size=1920,1080")
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--headless')

        elif self.conf["headless"]:
            options.add_argument('--headless')

        options.add_argument(f"user-agent={self.conf['userAgent']}")

        self.driver = Chrome(options=options)
        self.driver.set_page_load_timeout(60)


    def __set_token(self):
        src = f"""
                let date = new Date();
                date.setTime(date.getTime() + (7*24*60*60*1000));
                let expires = "; expires=" + date.toUTCString();

                document.cookie = "auth_token={self.conf['token']}"  + expires + "; path=/";
            """
        self.driver.execute_script(src)

    def __load_conf(self):
        self.conf = json.load(open("./files/conf.json"))

    def __load_users(self):
        self.users = json.load(open("./files/users.json"))

def get_username(driver: Chrome):
    while not len(driver.find_elements(By.CSS_SELECTOR, "div[data-testid='UserName']")):
        continue
    return driver.find_element(By.CSS_SELECTOR, "div[data-testid='UserName']").find_element(By.CSS_SELECTOR, "span").get_attribute("innerText")

# if __name__ == "__main__":
#     Scrap()
