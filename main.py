from KeyFetcher import KeyFetcher
from BrowserInteraction import KeyInserter

page = "https://ufst-my.github.io/CyberShield/" #URL til selve siden.
browser_name = "chrome" #Vigtigt at man har browseren tilgængelig.
page_nos = [i+1 for i in range(10)]

keyfetcher = KeyFetcher()
keyfetcher.get_keys(page_nos)
keys = keyfetcher.keys
keyinserter = KeyInserter(browser_name,page,keys)

