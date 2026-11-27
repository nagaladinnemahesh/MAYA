import webbrowser
import re
from urllib.parse import urlencode, urlsplit
from config.websites import WEBSITES


class WebTools:

    def __init__(self):
        self.websites = WEBSITES

    def resolve_website(self, website_name):
        website_name = website_name.lower().strip()

        for key, website in self.websites.items():

            if (
                website_name == key
                or website_name in website["aliases"]
            ):
                return website

        return None

    def open_website(self, website_name):

        website = self.resolve_website(website_name)

        if website is None:
            return (
                f"Sir, {website_name} is not "
                "registered in my website registry."
            )

        try:
            opened = webbrowser.open(
                website["url"],
                new=2
            )

            if opened:
                return f"Opening {website['name']}, sir."

            return (
                f"Sir, I was unable to open "
                f"{website['name']}."
            )

        except (webbrowser.Error, OSError) as error:
            print(f"Browser launch error: {error}")

            return (
                f"Sir, an error occurred while "
                f"opening {website['name']}."
            )
        
    def search_google(self, query):

        query = query.strip()

        if not query:
            return "Sir, please provide a search query."

        parameters = urlencode({"q": query})

        search_url = (
            f"https://www.google.com/search?{parameters}"
        )

        try:
            opened = webbrowser.open(search_url, new=2)

            if opened:
                return f"Searching Google for {query}, sir."

            return "Sir, I was unable to open Google search."

        except (webbrowser.Error, OSError) as error:
            print(f"Google search error: {error}")

            return (
                "Sir, an error occurred while "
                "performing the Google search."
            )
        
    def search_youtube(self, query):

        query = query.strip()

        if not query:
            return "Sir, please provide a YouTube search query."

        parameters = urlencode({"search_query": query})

        search_url = (
            f"https://www.youtube.com/results?{parameters}"
        )

        try:
            opened = webbrowser.open(search_url, new=2)

            if opened:
                return f"Searching YouTube for {query}, sir."

            return "Sir, I was unable to open YouTube search."

        except (webbrowser.Error, OSError) as error:
            print(f"YouTube search error: {error}")

            return (
                "Sir, an error occurred while "
                "performing the YouTube search."
            )
        
    def validate_url(self, url):

        url = url.strip()

        if not url:
            return None

        if any(
            character.isspace()
            or ord(character) < 32
            or character == "\\"
            for character in url
        ):
            return None

        if "://" not in url:
            url = f"https://{url}"

        try:
            parsed_url = urlsplit(url)

            if parsed_url.scheme not in ["http", "https"]:
                return None

            if not parsed_url.hostname:
                return None

            if (
                parsed_url.username is not None
                or parsed_url.password is not None
            ):
                return None

            hostname = parsed_url.hostname

            domain_pattern = (
                r"(?=.{1,253}$)"
                r"(?:[a-zA-Z0-9]"
                r"(?:[a-zA-Z0-9-]{0,61}"
                r"[a-zA-Z0-9])?\.)+"
                r"[a-zA-Z]{2,63}"
            )

            if not re.fullmatch(domain_pattern, hostname):
                return None

            # Accessing port validates its format and range.
            _ = parsed_url.port

            return url

        except ValueError:
            return None
        
    def open_url(self, url):

        validated_url = self.validate_url(url)

        if validated_url is None:
            return (
                "Sir, the provided URL is invalid "
                "or unsupported."
            )

        try:
            opened = webbrowser.open(
                validated_url,
                new=2
            )

            if opened:
                return f"Opening {validated_url}, sir."

            return "Sir, I was unable to open the website."

        except (webbrowser.Error, OSError) as error:
            print(f"URL opening error: {error}")

            return (
                "Sir, an error occurred while "
                "opening the website."
            )