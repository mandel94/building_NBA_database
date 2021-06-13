# Import libraries
import re 
import requests
import re
import pandas as pd
from bs4 import BeautifulSoup





def make_soup(html):
    """Returns a BeautifulSoup object"""
    soup = BeautifulSoup(html, "html.parser")
    return soup

def extract_address(url):
    url = url[0:url.index(".com") + 4]
    return url

def extract_table(soup, table_id):
    """Extract from soup object the href for a certain season"""
    table = soup.find("table", id=table_id)
    return table

def extract_season_href(table, season):
    """Extract href of specified season from table soup object"""
    href_season = table.find(string=season).parent.get("href")
    return href_season

def missing_stats_index(game: object) -> object:
    """Detect the position of missing stats inside game"""
    indexes = []
    for i, child in enumerate(game.find_all(attrs={"data-stat": True})):
        if child.string is None:
            indexes.append(i)
    return indexes

def are_30_stats(stats):
    """Check if the game is described by exactly 30 stats"""
    if len(stats) != 30:
        return False
    else:
        return True

def separate_data(data, index, sep, columns):
    """ Separate data in the index column of df according to the separator and assign splitting result to as many columns as the names provided to columns.
    Supported separator are '_', '-', '.', '(', '[' '{'
    """
    df = data.copy(deep=True)
    to_separate = df.iloc[:, index]
    df.drop(df.columns[index], axis=1, inplace=True)
    idx_values = to_separate.index
    if sep in ["(", "[", "{"]:
        if sep == "(":
            mirror_sep = ")"
        elif sep == "[":
            mirror_sep = "]"
        elif sep == "{":
            mirror_sep = "}"
        map_step_1 = list(map(lambda x: re.split("\\" + sep + "|" + "\\" + mirror_sep, x), to_separate))
        map_step_2 = list(map(lambda x: [elem for elem in x if elem != ""], map_step_1))
        col_1 = [elem[0] for elem in map_step_2]
        col_2 = [elem[1] for elem in map_step_2]
        df.insert(loc=index, column=columns[0], value=col_1)
        df.insert(loc=index, column=columns[1], value=col_2)
    else:
        map_step = list(map(lambda x: re.split(sep, x), to_separate))
        col_1 = [elem[0] for elem in map_step]
        col_2 = [elem[1] for elem in map_step]
        df.insert(loc=index, column=columns[0], value=col_1)
        df.insert(loc=index, column=columns[1], value=col_2)
    return df


def concatenate_href(root_url, href, remove_last_dir=True):
    """concatenate root_url to ref.

    Args:
        - root_url: string.
        - href: string. It will be appended to `root_url`.
        - remove_last_dir: bool. Choose if the last directory in `root_url` should be removed.
    """

    if remove_last_dir:
        splitted_root = root_url.split("/")[:-2]
        root_url = "/".join(splitted_root)
    return root_url + href


def is_roster_descendant(tag):
    """Is the tag a descendant of the roster table?"""

    for parent in tag.parents:
        if parent.has_attr("id"):
            return parent.get("id") == "roster"

def are_there_unicode_nbsp(string_):
    """Are there unicode non-breaking whitespaces in the provided string?"""

    nbsp_detected = re.search(u"\xa0", string_)
    return nbsp_detected

def clean_list_TW(list):
    """Drop elements of list if they contain the string 'TW'."""

    cleaned_list = [el for el in list if not re.search("TW", el)]
    return cleaned_list


def create_soup_from_url(url):
    """"Create a soup object for the page accessed by url."""

    req = requests.get(url)
    soup = BeautifulSoup(req.content, "html.parser")
    return soup


def is_player_active(player_soup):
    """Returns True if the player is still active."""
    _search = player_soup.find_all("strong", text="Experience:")
    if len(_search) == 0:
        return False
    else:
        return True
    

def inspect(df, max_rows, max_cols):
    """Display `max_rows` rows and `max_cols` cols of a pandas dataframes"""
    
    with pd.option_context('display.max_rows', max_rows, 
                           'display.max_columns', max_cols): 
        print(df)
    
    

# class ScrapyHub():
#     """
#     Central hub for directing scraping activity.
#
#     Let's define some architectural aspects of the scrapy package.
#     The scraping activity is performed by one or more scrapers (Scraper class). Each scraper can be assigned a scraping task at a time.
#     Once the scraper is deployed, its task will be to retrieve data from HTML language, reformatting that data into a programmable structure.
#     [??Once a raw output of the scraping task is delivered by the deployed scraper, that raw output will need to be further processed. This is the task of cleaners (Cleaner class).??]
#     How is a scraping task defined?
#     Scraping tasks are assigned through a central hub (ScrapyHub class). In general, a ScrapyHub object allows to organize the whole scraping activiy.
#     A ScrapyHub objects's main tasks are:
#     -   invoke new scrapers.
#     -   prepare scraping tasks to be assigned to scrapers.
#     -   deploying commissioned scrapers.
#     -   receive the output of scrapers.
#     -   invoke cleaner.
#     -   assigning cleaning tasks to cleaners.
#     What's the structure of a task? A task contains all the information that the scraper needs to perform its recovery commission.
#     Its structure is that of a dictionary, with the following key: value pairs:
#     - urls: list of pair-tuples, containing all the urls on which some action needs to be performed, together with the action to be performed. [(url, action),...,]
#
#     HOW TO REFERENCE AN ELEMENT? TWO ALTERNATIVE WAYS:
#     1) Use a dictionary containing the key-value pairs for accessing an element or a collection of elements (example: {tag: "a", class: "class_name", id = "id"}).
#     2) Provide directly the stringified version of the element (ex., <a href="/teams/BRK/2021.html" title="Brooklyn Nets">BRK</a>), or the list containing the stringified version of the elements to be referenced.
#
#     Two types of references:
#     - "reference"
#     - "multiple-reference"
#     Actions are performed on all referenced elements. This means that if more than one element is referenced, the same action is performed on each element.
#     Tasks can be concatenated, so that the output of a task can be passed as input to the immediately subsequent task. T
#     Once a sequence of tasks is defined, those tasks can be concatenated by passing them as a tuple to the commissioned scraper. The tasks of the so-formed chain will be performed in the same order with which they appear in the tuple.
#
#
#
#     REFERENCING OPTIONS
#     The API provides optional arguments for building references in a more complex manner.
#     For multiple-referencing:
#     level = "same" | "siblings"
#     limit = int, at most limit references will be collected. References are collected in the order referencing requirements are met, or stringified versions of elements are given.
#
#
#
#     Allowed actions:
#     - "access" --> takes the href of the selected links, returning for each a beautiful soup object of the accessed page.
#     - "extract_string" --> takes the string content of the element.
#     - "extract_child"
#     - "extract_parent"
#     -
#     - change_string="new_string" --> changes the string content of the referenced element.
#     -
#
#     TASKS SYNTAX:
#     dict={action: reference/s, options: {},
#
#
#     """
#     def __init__(self, name=None, url=None):
#         self.website_name = website_name
#         self.name = None
#         self.url = None
#
#
#
#     if self.website_name == "basketball-reference":
#         self.url = "https://www.basketball-reference.com/"
#         def create_NBA_task(self, task_name):
#
#

