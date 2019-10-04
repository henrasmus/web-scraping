"""
Rasmus Hen
Python 3.6.2
Windows 10
"""

from bs4 import BeautifulSoup
import urllib.request
import re

def main():
    url_1 = "https://dsv.su.se/utbildning/alla-utbildningar/kandidatprogram"#Variable with the origin URL
    texturl_x = find_and_extract(open_and_read(url_1))#Variable with the content of the origin URL
    all_links = find_link(open_and_read(url_1))#Variable with all links from the origin URL
    selected_links = all_links[:5]#Variable with 5 links selected through slicing
    """
    for-loop that iterates through the five links in "selected_links" and puts the content i the variable "texturl_x"
    that already contains the content from the origin URL as well as any content from earlier iterations
    """
    for i in range(0, 5):
        texturl_x += find_and_extract(open_and_read(selected_links[i]))

    #List of all valid characters
    valid_characters = ("a","b","c","d","e","f","g","h","i","j","k","l","m","n",\
                  "o","p","q","r","s","t","u","v","w","x","y","z","å","ä","ö"," ")
    #Creates a new variable to iterate through the gathered contents of the websites and add all the valid characters from "valid_characters" in it as a string
    all_text = ""
    for i in texturl_x:
        if i in valid_characters:
            all_text += i

    #Splits the string into a new list with all of the words that are separated by empty spaces       
    words_list = all_text.split(" ")

    #List of all invalid words that are not to be counted
    invalid_words = ("i", "och", "att", "det", "som", "en", "på", "är", "av", "för",\
                     "med", "till", "den", "har", "de", "inte", "om", "ett", "han", "men",\
                     "the", "be", "and", "of", "a", "in", "to", "have", "it", "i", "that",\
                     "for", "you", "he", "with", "on", "do", "say", "this", "they", "")
    #Creates a new list and iterates through "word_list" to remove all of the invalid words
    valid_list = []
    for i in words_list:
        if i not in invalid_words:
            valid_list.append(i)

    """
    Creates a dictionary and iterates through "valid_list": If the word is not in the dictionary it is added as a key with a value of 1
    if the word is in the dictionary already the value of that key is added by 1
    """
    word_count = {}
    for i in valid_list:
        if i in word_count:
            word_count[i] += 1
        else:
            word_count[i] = 1

    #Prints the whole dictionary "word_count" and then top 10 most common words on the six websites combined
    print(word_count)
    print("Lista över de vanligast förekommande orden på de givna hemsidorna i sjunkande ordning:")
    for i in range(1, 11):
        print(str(i) + "." + max(word_count, key = word_count.get).upper() + ", som förekom " + str(max(word_count.values())) + " gånger.")
        del word_count[max(word_count, key = word_count.get)]

    #Function to open and read code from a given URL
def open_and_read(url):
    website = urllib.request.urlopen(url)
    html = website.read()
    soup = BeautifulSoup(html, "html.parser")
    return soup

    #Function that finds and extracts text from given HTML tags: p and h1-h6
def find_and_extract(soup):
    tags = soup.findAll("p")
    tags += soup.findAll("h1")
    tags += soup.findAll("h2")
    tags += soup.findAll("h3")
    tags += soup.findAll("h4")
    tags += soup.findAll("h5")
    tags += soup.findAll("h6")

    text_string = get_text(tags)
  
    return text_string

    #Function that gets texts from the different tags and removes the tags themselves
def get_text(tag_list):
    text_string = ""
    for tag in tag_list:
        text = tag.text.lower()
        text_string = text_string + " " + text

    return text_string
    
"""
This function is from Pythonspot. It goes through the different href links in all of the <a> tags in the HTML code and searches for the pattern "https//:dsv.su.se" to put these
in the list "links". It then removes all doubles with "set()"
"""
def find_link(soup):
    links = []

    for link in soup.findAll('a', attrs={'href': re.compile("https://dsv.su.se")}):
        links.append(link.get('href'))

    links = list(set(links))
 
    return links

#Starts the program    
main()
