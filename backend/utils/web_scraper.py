import requests
from bs4 import BeautifulSoup
import os

def scrape_dress_images(url):
    """
    Scrapes 360° images of a dress from the provided URL.
    
    Args:
        url (str): The URL of the dress page to scrape.
        
    Returns:
        list: A list of URLs for the 360° dress images.
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36"
    }

    try:
        # Send an HTTP GET request to fetch the page content
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an exception for HTTP errors
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find the 360° images - adjust the selector based on the website's structure
        # Example: Assume images are stored in <img> tags with class "dress-360"
        image_tags = soup.find_all('img', class_='dress-360')

        if not image_tags:
            raise ValueError("No 360° images found on the page. Verify the URL or selector.")

        # Extract image URLs
        image_urls = [tag['src'] for tag in image_tags if 'src' in tag.attrs]

        # Validate and return absolute URLs
        image_urls = [requests.compat.urljoin(url, img_url) for img_url in image_urls]
        return image_urls

    except Exception as e:
        raise RuntimeError(f"Error scraping images: {str(e)}")

# Example usage
if __name__ == '__main__':
    dress_url = "https://example.com/dress-page"
    try:
        images = scrape_dress_images(dress_url)
        print("360° Images Found:")
        for img in images:
            print(img)
    except Exception as e:
        print(f"Error: {e}")
