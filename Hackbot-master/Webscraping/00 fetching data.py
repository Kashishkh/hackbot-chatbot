import requests

url= "https://devpost.com/hackathons"

def fetchAndSaveToFile(url, path) :
    r = requests.get(url)
    with open (path, "w") as f:
        f.write(r.text)

fetchAndSaveToFile(url, './data/devpost.html') 