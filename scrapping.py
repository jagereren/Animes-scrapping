from bs4 import BeautifulSoup
from bs4.element import SoupStrainer
import requests
import re

def scrapping(lien):
    HTMLFileToBeOpened = open(lien, "r",encoding="utf8")
    contents = HTMLFileToBeOpened.read()
    return BeautifulSoup(contents, 'lxml')

def parsing_titles(soup):
    s = soup.select('h2') 
    titles=[]
    for line in s :
        title_with_date_1 = re.split("[<>] ", line.get_text()) # get out titles from <h2 .. <a href etc in each occurence
        title_with_date_2 = "".join(map(str,title_with_date_1)).split("(") # transform into str and then split with the parenthesis of the date
        titles.append(title_with_date_2[0][:-1])
    return titles

def list_titles(titles):
    print("\nTous les animes : ")
    for e in titles:
        print(e)

def parsing_dates(soup):
    s = soup.select('h2') 
    dico_titles_dates = {}
    for line in s :
        title_with_date_1 = re.split("[<>] ", line.get_text()) # get out titles from <h2 .. <a href etc in each occurence
        title_with_date_2 = "".join(map(str,title_with_date_1)).split("(") # transform into str and then split with the parenthesis of the date
        title_with_date_2[1] = title_with_date_2[1].replace(")","") # delete the last parenthesis
        title_with_date_final = title_with_date_2.copy()

        dico_titles_dates[title_with_date_final[0]] = title_with_date_final[1] #adding to the dico
    return dico_titles_dates

def list_animes_per_date(dico):
    print("\nTous les animes selon la date de sortie : ")
    res=""
    date=input("Quelle date ? ")
    for e in range(len(dico)):
        if(list(dico.values())[e]==date):
            res += list(dico.keys())[e] + "\n"
    print(res)

# marche pas, en préparation
#def parsing_meilleurs(soup):
#    s = soup.find_all("p",class_="Text__SCText-sc-14ie3lm-0 ProductListItem__PollText-sc-ico7lo-11 dsSNGq ezNoIA")
#
#    for line in soup.find_all("div",class_="ProductListItem__Content-sc-ico7lo-5 hhzHdP"):
#        print(line.get_text().split("- ").pop(1))

def parsing_categories(soup):
    s = soup.find_all("span", {"data-testid": "genres"})
    res = ""
    dico_categories_animes = {}
    index_anime = 0
    for line in s:
        tab = re.split("[<>] ", line.get_text())
        inter = "".join(map(str,tab)).split(", ")
        for e in inter:
            if e not in dico_categories_animes.keys():
                dico_categories_animes[e] = [parsing_titles(soup)[index_anime]]
            else:
                dico_categories_animes[e].append(parsing_titles(soup)[index_anime])
        index_anime +=1
    return dico_categories_animes

def list_animes_per_categories(dico_categories_animes):
    print("\nTous les catégories disponibles : ")
    for e in dico_categories_animes:
        print(e)
    res = ""
    category = str(input("\nEntrez une catégorie : "))
    for e in range(len(dico_categories_animes)):
        if(list(dico_categories_animes.keys())[e]==category): # here we choose the category
            for anime in list(dico_categories_animes.values())[e] :
                res+=anime+"\n"
    print(res)
    
def main():
    print("\nBienvenue sur cette application vous permettant de récupérer des données sur 100 animes présents sur le site\n https://www.senscritique.com/top/resultats/les_meilleurs_animes_japonais/282242")
    soup = scrapping("animes/content.html")
    val = int(input("\nQue voulez-vous faire ?\n 1 - Afficher les titres des animes\n 2 - Afficher les animes selon une date de sortie\n 3 - Afficher les animes selon une catégorie\n 4 - Arrêter \n"))
    while(val != 4):
        if(val==1):
            list_titles(parsing_titles(soup))
        elif(val==2):
            list_animes_per_date(parsing_dates(soup))
        elif(val==3):
            list_animes_per_categories(parsing_categories(soup))
        else:
            break
        val = int(input("\nQue voulez-vous faire ?\n 1 - Afficher les titres des animes\n 2 - Afficher les animes selon une date de sortie\n 3 - Afficher les animes selon une catégorie\n 4 - Arrêter \n"))

main()
