# Import necessary libraries
import os
import asyncio
from firecrawl import FirecrawlApp
from datetime import datetime
from dotenv import load_dotenv

def scrape_data(url: str):
    load_dotenv()
    # Initialize the FirecrawlApp with your API key
    app = FirecrawlApp(api_key=os.getenv('FIRECRAWL_API_KEY'))
    
    # Scrape a single URL
    scraped_data = app.scrape_url(url,{'pageOptions':{'onlyMainContent': True}})
    
    # Check if 'markdown' key exists in the scraped data
    if 'markdown' in scraped_data:
        return scraped_data['markdown']
    else:
        raise KeyError("The key 'markdown' does not exist in the scraped data.")
    
def save_raw_data(raw_data, timestamp, output_folder='output'):
    # Ensure the output folder exists
    os.makedirs(output_folder, exist_ok=True)
    
    # Save the raw markdown data with timestamp in filename
    raw_output_path = os.path.join(output_folder, f'rawData_{timestamp}.md')
    with open(raw_output_path, 'w', encoding='utf-8') as f:
        f.write(raw_data)
    print(f"Raw data saved to {raw_output_path}")
    
def procedure(urls):
    for url in urls: 
        try:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
            raw_data = scrape_data(url)
            
            # Save raw data
            save_raw_data(raw_data, timestamp)
                
        except Exception as e:
            print(f"An error occurred while processing {url}: {e}")
            
if __name__ == "__main__":
    
        # Scrape a website:
        urls = ['https://www.friscoisd.org/departments/athletics/team-websites']
    
        procedure(urls)
