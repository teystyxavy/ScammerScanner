import re
from app.services import VirusTotalService
from spellchecker import SpellChecker

class ScamFirstCheckService:
    def __init__(self, text:str) -> None:
        self.spell_checker = SpellChecker()

        punctuation_regex = r'[,.:!+-]'
        email_regex = r'[a-zA-Z0-9._]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
        url_regex = r'(https?://[^\s]+)'

        # Get all emails and urls, remove from text
        self.emails = re.findall(email_regex, text)
        self.urls = re.findall(url_regex, text)

        for item in self.emails + self.urls:
            text = text.replace(item,'')

        # Remove punctuation from text (will confuse spellchecker)
        cleaned_text = re.sub(punctuation_regex,' ',text)
    
        self.text = cleaned_text
        pass

    def check_spelling(self) -> bool:
        """
        Spell Checking using PySpellChecker
        Check for percentage characters of misspelled words since longer words tend to be
        more prone to errors, 
        hence we get (characters in misspelled words) / (character in total words)
        """
        misspelled = self.spell_checker.unknown(self.text.split())

        misspelled_char_count = 0
        for word in misspelled:
            misspelled_char_count += len(word)

        total_char_count = len(self.text)

        return (misspelled_char_count / total_char_count) > 0.05
    
    def check_urls(self) -> bool:
        """
        Uses VirusTotal API to scan urls attached
        Returns true if malicious
        """
        virustotal_tool = VirusTotalService()
        for url in self.urls:
            if virustotal_tool.scan_url(url):
                if virustotal_tool.is_malicious():
                    return True
        
        # Return false for harmless/unable to scan url
        return False

    def check_scam(self) -> bool:
        """
        Runs check spelling and check urls
        Returns true if scam
        """
        if self.check_spelling():
            return True

        if len(self.urls) > 0:
            if self.check_urls():
                return True
        
        return False

