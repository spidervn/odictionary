from bs4 import BeautifulSoup
import urllib2


fr = urllib2.urlopen("https://en.oxforddictionaries.com/definition/odometry")
html = fr.read()
fr.close()
# page = requests.get("https://en.oxforddictionaries.com/definition/odometry")
soup = BeautifulSoup(html) # page.content, "html.parser")

print soup.title
print soup.p