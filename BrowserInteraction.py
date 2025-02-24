from splinter import Browser
import time

class KeyInserter:
    def __init__(self,browser_name,url,keys):
        """
        Kører ved oprettelse.
        """
        self.browser = Browser(browser_name)
        self.browser.visit(url)
        
        self.fill_boxes(keys)
        time.sleep(10)
        self.browser.quit()
    
    def fill_boxes(self,keys):
        """
        Det her har voldet flest problemer. Men det lykkedes at finde checkboksene
        v.h.a. deres værdi og gudskelov er der intet der overlapper.

        Finder derefter knappen hvilket er nemt fordi den har et tydeligt id.
        """
        elements = [self.browser.find_by_value(str(i)) for i in keys]
        for element in elements:
            element.click()
        button = self.browser.find_by_id('lockButton').pop()
        button.click()