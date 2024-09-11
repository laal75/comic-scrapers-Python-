Comic Scraper 🖼️

This repository contains two Python scripts designed to scrape and download images (comics) from a website, with options to download a single page or a series of pages. Both scripts offer the ability to zip the downloaded images and filter out files below a certain size.
Scripts Overview
1. comic_scraper_single_getter_v1.py

This script scrapes images from a single webpage and saves them to a zip file. It provides a simple interface for downloading and zipping images from one URL.

Features:

    Downloads all images from the provided URL.
    Skips images below 500 KB.
    Saves images into a zip file with a user-specified name.

Usage:

    Run the script.
    Enter the URL from which to scrape the images.
    Enter the desired name for the zip file.

bash

python comic_scraper_single_getter_v1.py

Example:

python

Enter the URL of the website to scrape images from: https://readallcomics.com/comic-name-1/
Enter the name for the zip file (e.g., 'comic.zip'): my_comic_images.zip

The images will be scraped and zipped into the specified file.
2. comic_scraper_series_getter_v1.py

This script scrapes images from a series of webpages, allowing you to specify a URL pattern with a placeholder for the page number (e.g., comic-name-{n}) and a range of numbers to scrape. Each page is scraped separately and saved in a unique zip file.

Features:

    Scrapes images from a series of pages based on a URL pattern (e.g., comic-name-{n}).
    Downloads images larger than 500 KB.
    Zips images from each page into a separate zip file, with the file name format customizable by the user.

Usage:

    Run the script.
    Enter the URL pattern, using {n} to represent the page number (e.g., https://readallcomics.com/comic-name-{n}-2022/).
    Enter the starting and ending numbers for the series.
    Enter the desired name format for each zip file.

bash

python comic_scraper_series_getter_v1.py

Example:

rust

Enter the URL pattern (use {n} for the number, e.g., 'https://readallcomics.com/comic-name-{n}-2022/'): https://readallcomics.com/comic-name-{n}-2022/
Enter the starting number: 1
Enter the ending number: 5
Enter the custom zip name format (use {n} for the number, e.g., 'comic-{n}'): comic-{n}

This will scrape comics from comic-name-1 to comic-name-5 and save the images into zip files named comic-1.zip, comic-2.zip, etc.
Requirements

    Python 3.x
    Packages: requests, beautifulsoup4, zipfile

Install the required packages:

bash

pip install requests beautifulsoup4

License

This project is licensed under the MIT License.
