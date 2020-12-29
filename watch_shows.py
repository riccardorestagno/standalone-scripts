from bs4 import BeautifulSoup, SoupStrainer
from google import google
import requests
import webbrowser
import dryscrape
from timedinput import *

global show_name
show_name = ""


def show_name_exceptions():
    global show_name
    if show_name.lower().startswith("lot"):
        show_name = show_name.replace("lot", "DC's Legends of Tomorrow")
    elif show_name.lower().startswith("twd"):
        show_name = show_name.replace("twd", "The Walking Dead")
    elif show_name.lower().startswith("htgawm"):
        show_name = show_name.replace("htgawm", "how to get away with murder")
    return show_name


def link_to_use():
    if not show_name_exceptions():
        pass
    else:
        show_name = show_name_exceptions()

    if show_name.endswith("all eps"):
        show_name = show_name.replace(" all eps", "")
    else:
        pass
    search_results = google.search(
        "ewatchseries .to " + show_name)  # in case WatchSeries changes their URL, this might need modifications
    for url in search_results:
        link_found = url.link
        break
    if "season" in link_found:
        link_found, season = link_found.rsplit('/', 1)
        link_found = link_found.replace('.to/',
                                        '.to/serie/')  # in case WatchSeries changes their URL, this might need modifications
        return link_found
    else:
        return link_found


while True:
    # try:
    if show_name == "":
        show_name = input('Enter a show that you want to watch the latest episode of.\n' \
                          'End the shows title with "all eps" if you would like a list of all episodes\n')
    session = requests.Session()

    main_link = link_to_use()
    tv_show_home = session.get(link_to_use())
    strainer1 = SoupStrainer('div', attrs={'class': 'latest-episode'})
    strainer2 = SoupStrainer('tr', attrs={'class': 'download_link_gorillavid.in '})
    strainer3 = SoupStrainer('div', attrs={'style': 'float:left; text-align:center;'})

    if show_name.endswith("all eps"):
        webbrowser.open(main_link, new=2, autoraise=True)
        show_name = timed_input("Enter another show that you want to watch the latest episode of.\n", 20)
        if show_name != "":
            continue
        break

    else:
        # Parse 1: Gets the latest episode link
        page1 = tv_show_home
        soup = BeautifulSoup(page1.content, 'html.parser', parse_only=strainer1)
        not_needed, show_name = link_to_use().rsplit('/', 1)
        show_name = show_name.replace("_", " ")

        for a in soup.find_all('a', href=True):
            print("Now loading " + a.text + " of " + show_name.title())
            page2 = session.get(a['href'])
            break
        page1.close()

        # Parse 2: Gets the first gorillavid link (the one filled with big add)
        soup = BeautifulSoup(page2.content, 'html.parser', parse_only=strainer2)
        for a in soup.find_all('a', href=True):
            page3 = a['href']
            break
        page2.close()

        # Parse 3 (using dryscrape): Gets the main gorillavid link by scraping the javascript of the previous link
        dry_session = dryscrape.Session()
        dry_session.visit(page3)
        response = dry_session.body()
        soup = BeautifulSoup(response, 'lxml', parse_only=strainer3)
        # print(response)
        for a in soup.find_all('a', href=True):
            print(a['href'])
            webbrowser.open(a['href'], new=2, autoraise=True)
            break

        show_name = timed_input("Enter another show that you want to watch the latest episode of.\n", 20)
        if show_name != "":
            continue
        break
# except:
# print("""There's an error in your search due to one of the folowing:
# 1. Google flagged this script as a bot due to too many uses.
# 2. The url for WatchSeries has changed.
# 3. The shows name is spelled incorrectly.""")
# try_again = timed_input("Try again?\n",15)
# if try_again.lower() == 'yes':
# continue
# else:
# break
