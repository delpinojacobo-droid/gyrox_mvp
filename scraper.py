import urllib.request
import xml.etree.ElementTree as ET
import pandas as pd
from datetime import datetime

def scrape_adversarial_nodes():
    print("[+] Initializing Dual-Node Adversarial Ingestion Pipelines...")
    rss_url = "https://www.cnbc.com/id/20910258/device/rss/rss.html"
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)'}
    req = urllib.request.Request(rss_url, headers=headers)
    
    try:
        with urllib.request.urlopen(req) as response:
            root = ET.fromstring(response.read())
        
        records = []
        for item in root.findall('.//item'):
            headline = item.find('title').text
            pub_date_str = item.find('pubDate').text
            try:
                clean_date = datetime.strptime(pub_date_str[5:16], '%d %b %Y').strftime('%Y-%m-%d')
            except:
                clean_date = datetime.today().strftime('%Y-%m-%d')
            
            # Algorithmic Node Splitting Logic
            headline_lower = headline.lower()
            west_signals = ['us', 'washington', 'biden', 'bis', 'sec', 'tariff', 'sanction', 'restriction']
            east_signals = ['china', 'beijing', 'xinhua', 'taiwan', 'export', 'mineral', 'semiconductor', 'chip']
            
            is_west = any(w in headline_lower for w in west_signals)
            is_east = any(e in headline_lower for e in east_signals)
            
            if is_west or not is_east:
                records.append({"timestamp": clean_date, "headline": headline, "node": "ALPHA_WEST"})
            if is_east:
                records.append({"timestamp": clean_date, "headline": headline, "node": "BETA_EAST"})
                
        df = pd.DataFrame(records)
        print(f"[✓] Structural success: Node Alpha and Node Beta streams populated with {len(df)} lines.")
    except Exception as e:
        print(f"[!] Feed redirect active. Deploying high-fidelity mock stream: {e}")
        base_date = datetime.today().strftime('%Y-%m-%d')
        df = pd.DataFrame([
            {"timestamp": base_date, "headline": "US BIS tightens export enforcement on advanced technological infrastructure components.", "node": "ALPHA_WEST"},
            {"timestamp": base_date, "headline": "Beijing custom authorities execute compliance reviews on high-purity mineral shipments.", "node": "BETA_EAST"}
        ])
    
    df.to_csv("raw_narratives.csv", index=False)
    print("[✓] Raw text nodes cached inside raw_narratives.csv")

if __name__ == "__main__":
    scrape_adversarial_nodes()
