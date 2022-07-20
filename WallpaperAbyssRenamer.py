from bs4 import BeautifulSoup
import requests
import os, re
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

def is_int(val):
    try:
        num = int(val)
    except ValueError:
        return False
    return True

dir = "D:\My Personal Files\Προσωρινά Αρχεία\Downloads\\"
dir = "D:\My Personal Files\Software\Αρχεία Προγραμμάτων\Προγραμματισμός\Python\WallpaperAbyssImageParser\Images\\"
dir = "D:\My Personal Files\Πολυμέσα\Εικόνες\Φόντα\\"
dir2 = "Cannot_rename\\"
dir = "Temp\\"
regex8 = r'<strong>(.*?)</strong>'

files = os.listdir(dir) # dir is your directory path
NumberOfImages = len(files)
ParsedImages = 0

for filename in os.listdir(dir):
    ParsedImages = ParsedImages + 1
    print("{:.2f} %".format((ParsedImages/NumberOfImages)*100))
    if (is_int(filename[0:-4])):
        ID = filename[0:-4]
        extension = filename[-3:]
        #print("ID : ", ID , "Extension : ",extension)
        Website = "https://wall.alphacoders.com/big.php?i=" + ID
        r = requests.get(Website)
        soup = BeautifulSoup(r.text, "html.parser")
        if ("That Image doesn't exist anymore" in r.text):
            print("Could not rename", filename)
            continue

        new_filename = soup.select(".wallpaper-name")

        if (new_filename == []):
            tags = soup.select(".tag-element")
            tags = list(dict.fromkeys(tags)) # Delete duplicate tags
            if (tags == []):
                words = re.findall(regex8, soup.select(".floatright").__str__())
                if (words == []):
                    words = re.findall(r'">(.*?)</a>',soup.select("#page_container").__str__())
                    if (words == []):
                        print("Could not rename", filename)
                        continue
                    new_filename = ""
                    for x, word in enumerate(words):
                        if (x >= 2):  # Too many tags
                            break
                        if (word == '') or (word == 'Share/Embed') or (word == 'Submission Info') or (word == '" + width + "x" + height + " Cropped') or (word == '" + width + "x" + height + " Stretched'):
                            continue
                        new_filename = new_filename + "_" + word.lower()
                else:
                    new_filename = ""
                    for x,word in enumerate(words):
                        if (x >= 2):  # Too many tags
                            break
                        new_filename = new_filename + "_" + word.lower()
            else:
                new_filename = ""
                for x,tag in enumerate(tags):
                    if (x >= 2): # Too many tags
                        break
                    new_filename = new_filename + "_" + tag.get_text().strip()
        else:
            new_filename = new_filename[0].get_text()

        new_filename = new_filename.replace("/", '_')
        new_filename = new_filename.replace("+", '_')
        new_filename = new_filename.replace("-", '_')
        new_filename = new_filename.replace("(", '_')
        new_filename = new_filename.replace(")", '_')
        new_filename = new_filename.replace(",", '_')
        new_filename = new_filename.replace("?", '_')
        new_filename = new_filename.replace("...", '_')
        new_filename = new_filename.replace(" ", '_')
        new_filename = new_filename.replace("'", '_')
        new_filename = new_filename.replace("|", '_')
        new_filename = new_filename.replace(":", '_')
        new_filename = new_filename.replace("___", '_')
        new_filename = new_filename.replace("__", '_')
        new_filename = new_filename.replace("\n", '')
        new_filename = new_filename.replace(r'"', '')
        new_filename = new_filename.lower()
        new_filename = new_filename.strip('_')
        new_filename = new_filename.strip()

        words = new_filename.split('_')
        words = list(dict.fromkeys(words))

        new_filename = ""
        for word in words:
            new_filename = new_filename + "_" + word

        new_filename = new_filename.strip('_')
        new_filename = new_filename.strip()
        if (new_filename == "newest_wallpapers_recently_popular"):
            print("Could not rename", filename)
            continue

        full_filename = new_filename + "." + extension

        if (os.path.exists(dir + full_filename)):
            cnt = 1

        while (os.path.exists(dir + full_filename)):
            final_name = new_filename + "_" + str(cnt)
            full_filename = final_name + "." + extension
            cnt = cnt + 1

        print("Old file name:", filename, "|| New file name:", full_filename)
        os.rename(dir + filename,dir + full_filename)