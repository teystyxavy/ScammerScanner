import requests
import time
from app.config import Config

class VirusTotalService:
    def __init__(self):
        self.api_key = Config.VT_API_KEY
        self.base_url = "https://www.virustotal.com/api/v3"
        self.malicious = False

    def scan_url(self, url) -> bool:
        """
        Scans URL, returns true if successful
        """
        headers = {
            "accept": "application/json",
            "x-apikey": self.api_key,
            "content-type": "application/x-www-form-urlencoded"
        }
        
        payload = f"url={url}"

        max_wait_time = 60
        wait_time = 10
        elapsed_time = 0
        response = requests.post(f"{self.base_url}/urls", headers=headers, data=payload)
        if response.status_code == 200:
            url_scan_link = response.json()['data']['links']['self']
            while elapsed_time < max_wait_time:
                url_analysis_report = requests.get(url_scan_link, headers=headers)
                if url_analysis_report.status_code == 200:
                    url_analysis_report_json = url_analysis_report.json()
                    total_number_of_vendors = len(url_analysis_report_json['data']['attributes']['results'].keys())
                    url_scan_stats = url_analysis_report_json['data']['attributes']['stats']
                    malicious_stats = url_scan_stats['malicious']
                    if total_number_of_vendors > 0:
                        if malicious_stats > 0:
                            self.malicious = True
                        else:
                            self.malicious = False
                        
                        return True
                    else:
                        # Scan still in progress
                        time.sleep(wait_time)
                        elapsed_time += wait_time
                        wait_time = 5

        else:
            return False
        
    def is_malicious(self) -> bool:
        return self.malicious


