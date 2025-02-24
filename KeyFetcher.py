from bs4 import BeautifulSoup #Til at scrape og identificere elementerne i HTML-koden.
import requests as req #Requests for at skabe en forbindelse til siden.
import re #RegEx
from collections import defaultdict #I stedet for at skulle tjekke om nøgler eksisterer i forvejen.

class KeyFetcher:
    """
    Skal anvendes i det endelige dokument til at indsamle nøglerne og sende dem 
    videre til en anden del af programmet som tager dem og interagerer med siden.
    """
    def __init__(self):
        self.base_url = "https://ufst-my.github.io/CyberShield/keycollector/"
        self.htmls = defaultdict(list) #To nøgler 'groups' og 'cells', baseret på hvad vi undersøgte.
        self.keys = set()

    def get_script_code(self,page_nos):
        """
        page_nos er en liste af værdier af siderne man ønsker.

        Opdaterer self.htmls med HTML-koden i <scripts> på sider med koderne
        man ønsker.
        """
        self.htmls = defaultdict(list) #For at være sikker på at vi ikke overskriver den flere gange.
        make_url = lambda page_no: self.base_url + f"page{page_no}.html" #Lille funktion til at lave URL
        page_nos = [x for x in page_nos if 1 <= x and x <= 10] #Filtrere værdier udenfor rækkevidde.
        for page_no in page_nos:
            url = make_url(page_no)
            html = BeautifulSoup(req.get(url).content, 'html.parser')
            as_str = str(html.find_all("script").pop()) #Vi har kun brug for <script> delen, nok til at identificere.
            identifier = re.findall(r"document.getElementById\(\"container\"\)",as_str) #For at se om de er grupperede.
            key = 'groups' if identifier else 'cells'
            self.htmls[key].append(as_str)
    
    def treat_groups(self):
        """
        Vi skal finde dem for både groups og cells, så jeg skriver en metode for hver.

        Givet en groups script html skal den finde koderne og returnere dem.
        """
        html_script_code = self.htmls['groups']
        RegEx_loops = r"for \(.*{"
        RegEx_from_to = r". \+?<?=? \d*"
        RegEx_If = r". % \d* === \d*"
        for script_code in html_script_code:
            loops = re.findall(RegEx_loops, script_code)
            outer_loop = loops[0] #inner_loops = loops[1], hvis der skal mere fleksibilitet. Men alle værdier tjekkes i det indre loop.
            outer_from, outer_to, step = [int(element.split()[-1]) for element in re.findall(RegEx_from_to, outer_loop)]
            If = re.findall(RegEx_If,script_code).pop() #Man kan blive ved med at gøre det mere fleksibelt, men nu laver jeg det kun til modulus.
            modulus = lambda x: x % int(If.split(" ")[2]) == int(If.split(" ")[-1])
            for value in range(outer_from, outer_to+1): #Her har vi naturligvis antaget at vi tjekker alle værdierne imellem outer_from og outer_to, hvilket vi jo også gør!
                if modulus(value):
                    self.keys.add(value)
    
    def treat_cells(self):
        """
        Vi skal finde dem for både groups og cells, så jeg skriver en metode for hver.

        Givet et cells script html skal den finde koderne og returnere dem.
        """
        html_script_code = self.htmls['cells']
        RegEx_loops = r"for \(.*{"
        RegEx_from_to = r"[a-zA-Z] <?=? \d*"
        RegEx_If = r". % \d* === \d*"
        for script_code in html_script_code:
            loop = re.findall(RegEx_loops, script_code)[0]
            From, To = [int(element.split()[-1]) for element in re.findall(RegEx_from_to, loop)]
            If = re.findall(RegEx_If,script_code).pop() #Man kan blive ved med at gøre det mere fleksibelt, men nu laver jeg det kun til modulus.
            modulus = lambda x: x % int(If.split(" ")[2]) == int(If.split(" ")[-1])
            for value in range(From, To+1):
                if modulus(value):
                    self.keys.add(value)
    
    def get_keys(self,page_nos):
        """
        Bruger de andre metoder til at finde nøglerne.
        """
        self.get_script_code(page_nos)
        self.treat_groups()
        self.treat_cells()


#Bare til at teste løbende.
#        
#keyfetcher = KeyFetcher()
#htmls = keyfetcher.get_script_code([i+1 for i in range(10)])
#keyfetcher.get_keys([i+1 for i in range(10)])
#print(sorted(keyfetcher.keys))



