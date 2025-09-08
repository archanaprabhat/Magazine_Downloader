import os
import requests
from PIL import Image
import re
from urllib.parse import urlparse
from datetime import datetime

def extract_page_number(url):
    """Extract page number from URL for proper sorting"""
    # Look for pattern like /5_01/, /5_02/, etc.
    match = re.search(r'/5_(\d+)/', url)
    if match:
        return int(match.group(1))
    return 0

def download_image(url, folder_path, filename):
    """Download a single image from URL"""
    try:
        print(f"Downloading: {filename}")
        
        # Send request with headers to avoid blocking
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()  # Raise an exception for bad status codes
        
        # Save the image
        filepath = os.path.join(folder_path, filename)
        with open(filepath, 'wb') as f:
            f.write(response.content)
        
        print(f"✓ Downloaded: {filename}")
        return True
        
    except requests.exceptions.RequestException as e:
        print(f"✗ Failed to download {filename}: {e}")
        return False
    except Exception as e:
        print(f"✗ Error saving {filename}: {e}")
        return False

def images_to_pdf(image_folder, pdf_filename):
    """Convert all images in folder to a single PDF"""
    try:
        # Get all image files
        image_files = []
        for filename in os.listdir(image_folder):
            if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                image_files.append(filename)
        
        if not image_files:
            print("No images found to convert to PDF!")
            return False
        
        # Sort files by page number
        image_files.sort(key=lambda x: int(re.search(r'page_(\d+)', x).group(1)) if re.search(r'page_(\d+)', x) else 0)
        
        print(f"Converting {len(image_files)} images to PDF...")
        
        # Convert images to PDF
        images = []
        for filename in image_files:
            img_path = os.path.join(image_folder, filename)
            try:
                img = Image.open(img_path)
                # Convert to RGB if needed (for PDF compatibility)
                if img.mode != 'RGB':
                    img = img.convert('RGB')
                images.append(img)
                print(f"✓ Processed: {filename}")
            except Exception as e:
                print(f"✗ Error processing {filename}: {e}")
        
        if not images:
            print("No valid images to convert!")
            return False
        
        # Save as PDF
        pdf_path = os.path.join(os.path.dirname(image_folder), pdf_filename)
        images[0].save(pdf_path, save_all=True, append_images=images[1:])
        
        print(f"✓ PDF created successfully: {pdf_filename}")
        return True
        
    except Exception as e:
        print(f"✗ Error creating PDF: {e}")
        return False

def main():
    """Main function to orchestrate the download and PDF creation"""
    
    # Define paths
    current_dir = os.getcwd()
    links_file = os.path.join(current_dir, "links.txt")
    download_folder = os.path.join(current_dir, "downloaded_pages")
    pdf_filename = "VANITHA_Magazine.pdf"
    
    print("=== VANITHA Magazine PDF Creator ===")
    print(f"Working directory: {current_dir}")
    
    # Check if links.txt exists
    if not os.path.exists(links_file):
        print(f"✗ Error: links.txt not found in {current_dir}")
        print("Please make sure links.txt is in the same folder as this script.")
        input("Press Enter to exit...")
        return
    
    # Create download folder if it doesn't exist
    if not os.path.exists(download_folder):
        os.makedirs(download_folder)
        print(f"✓ Created download folder: downloaded_pages")
    
    # Read links from file
    try:
        with open(links_file, 'r', encoding='utf-8') as f:
            urls = [line.strip() for line in f if line.strip()]
        
        if not urls:
            print("✗ No URLs found in links.txt")
            input("Press Enter to exit...")
            return
            
        print(f"✓ Found {len(urls)} URLs to download")
        
    except Exception as e:
        print(f"✗ Error reading links.txt: {e}")
        input("Press Enter to exit...")
        return
    
    # Sort URLs by page number for proper order
    urls.sort(key=extract_page_number)
    
    # Download all images
    print("\n--- Starting Downloads ---")
    successful_downloads = 0
    
    for i, url in enumerate(urls, 1):
        page_num = extract_page_number(url)
        filename = f"page_{page_num:03d}.jpg"  # 001, 002, 003, etc.
        
        if download_image(url, download_folder, filename):
            successful_downloads += 1
        
        # Show progress
        print(f"Progress: {i}/{len(urls)} ({(i/len(urls)*100):.1f}%)")
    
    print(f"\n--- Download Complete ---")
    print(f"Successfully downloaded: {successful_downloads}/{len(urls)} images")
    
    if successful_downloads == 0:
        print("✗ No images were downloaded. Cannot create PDF.")
        input("Press Enter to exit...")
        return
    
    # Create PDF
    print(f"\n--- Creating PDF ---")
    if images_to_pdf(download_folder, pdf_filename):
        print(f"\n🎉 SUCCESS! Your magazine PDF has been created!")
        print(f"📁 Location: {os.path.join(current_dir, pdf_filename)}")
        print(f"📄 Total pages: {successful_downloads}")
    else:
        print("✗ Failed to create PDF")
    
    print(f"\n--- Process Complete ---")
    input("Press Enter to exit...")

if __name__ == "__main__":
    main()