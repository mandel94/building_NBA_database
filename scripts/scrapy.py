# Import libraries
import re 
import requests
import re
import pandas as pd
from bs4 import BeautifulSoup



# =============================================================================
# New functions
# =============================================================================


def map_find(tags, tag, attr):
    """Map-apply find_all search to a list of BeautifulSoup tags.
    
        Args:
            - tags: list of 'bs4.BeautifulSoup' objects.
            - tag: string. Html tag.
            - attr: string. CSS atribute.
        Returns:
            A list (of detected tags) of lists (one for each tag in 'tag_list'). 
    """
    
    map_find = lambda t: t.find_all(tag, attrs={attr:True})
    to_return = list(map(map_find, tags))
    
    return to_return





# =============================================================================






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
    
 
    
 
