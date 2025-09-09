import requests
import os
import hashlib
from urllib.parse import urlparse

def get_file_hash(content):
    """Generate a hash of the file content to detect duplicates."""
    return hashlib.sha256(content).hexdigest()

def main():
    print("Welcome to the Ubuntu Image Fetcher")
    print("A tool for mindfully collecting images from the web\n")
    
    # Get multiple URLs from user, separated by commas
    urls = input("Please enter one or more image URLs (separated by commas): ").split(",")
    urls = [url.strip() for url in urls if url.strip()]

    # Create directory if it doesn't exist
    os.makedirs("Fetched_Images", exist_ok=True)

    # Keep track of downloaded file hashes to prevent duplicates
    downloaded_hashes = set()

    for url in urls:
        try:
            # Fetch the image with headers
            response = requests.get(url, timeout=10, stream=True)
            response.raise_for_status()

            
            # Precaution 1: Validate content type
            
            content_type = response.headers.get("Content-Type", "")
            if not content_type.startswith("image/"):
                print(f"✗ Skipped {url} (not an image, Content-Type: {content_type})")
                continue

            
            # Precaution 2: Validate content length
            
            content_length = response.headers.get("Content-Length")
            if content_length and int(content_length) > 5 * 1024 * 1024:  # 5MB limit
                print(f"✗ Skipped {url} (file too large: {int(content_length) / 1024:.1f} KB)")
                continue

            # Read content safely
            content = response.content

            
            # Feature: Prevent duplicate images
            
            file_hash = get_file_hash(content)
            if file_hash in downloaded_hashes:
                print(f"✗ Skipped {url} (duplicate image detected)")
                continue
            downloaded_hashes.add(file_hash)

            # Extract filename from URL or generate one
            parsed_url = urlparse(url)
            filename = os.path.basename(parsed_url.path)
            if not filename:
                filename = f"downloaded_image_{len(downloaded_hashes)}.jpg"

            # Save the image
            filepath = os.path.join("Fetched_Images", filename)
            with open(filepath, 'wb') as f:
                f.write(content)

            print(f"✓ Successfully fetched: {filename}")
            print(f"✓ Image saved to {filepath}\n")
        
        except requests.exceptions.RequestException as e:
            print(f"✗ Connection error for URL: {url} → {e}")
        except Exception as e:
            print(f"✗ An error occurred for URL: {url} → {e}")

    print("All tasks completed. Connection strengthened. Community enriched.")

if __name__ == "__main__":
    main()

