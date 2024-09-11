Comic Scraper 🖼️
Comic Scraper Script
Overview

This Python script allows you to scrape comic images from a website (like readallcomics.com), download them, and package the images into a zip file. The script supports downloading comics by issue numbers and tries different years if an issue is not found for the initially provided year. It also includes robust error handling, retries, and a comprehensive summary report at the end.
Features

    Year Fallback Logic: If a comic page is not found for the provided year, the script will automatically increment the year up to the current year and retry.
    Download Images with Size Constraints: Optionally set a minimum size for images to filter out small unwanted files.
    Retry Mechanism: The script retries downloading images and scraping pages up to 3 times if a request fails or times out.
    Detailed Logging: Logs detailed information for each comic and image, including status codes for failed requests and retries.
    Clean-up: After downloading and zipping the images, the script automatically cleans up the image folders.
    Comprehensive Summary: At the end of the script, a summary is displayed showing:
        How many comics were processed successfully.
        How many comics were skipped due to errors.
        A list of missing comics.
        The start and end time of the process.

Usage
Prerequisites

    Python 3.x
    Required Python packages:
        requests
        beautifulsoup4

You can install these using pip:

bash

    pip install requests beautifulsoup4

windows cmd

    pip install requests beautifulsoup4

Script Execution

To run the script, use the following command:

bash

    python comic_scraper.py

Windows (Tested)

    I open the file through idle and then run (F5) from there.

Input Prompts

The script will prompt you for several inputs:

    URL Pattern:
        Enter the base URL pattern where the comic issues are hosted. Use {n} for the issue number and {year} for the year.
        Example: https://readallcomics.com/scooby-apocalypse-{n}-{year}/

    Starting and Ending Issue Numbers:
        Enter the range of issue numbers you want to scrape.

    Starting Year:
        Enter the starting year to search for the comic. If left blank, the current year will be used.

    Zip File Name Format:
        Provide a name format for the zip file. Use {n} for the issue number and {year} for the year.
        Example: scooby-apocalypse-{n}-{year}

    Leading Zeroes for Issue Numbers:
        Specify how many digits the issue number should have. For example, 001 has 3 digits.

    Minimum Image Size:
        Optionally enter a minimum size (in KB) for images. Leave blank for no size constraint.

Example Input

text

Enter the URL pattern (use {n} for the number and {year} for the year, e.g., 'https://readallcomics.com/scooby-apocalypse-{n}-{year}/'): https://readallcomics.com/scooby-apocalypse-{n}-{year}/
Enter the starting number: 1
Enter the ending number: 5
Enter the starting year (leave blank if there is no year): 2017
Enter the custom zip name format (use {n} for the number and {year} for the year, e.g., 'scooby-apocalypse-{n}-{year}'): scooby-apocalypse-{n}-{year}
How many digits should the issue number have? (Enter 1 for no zero padding, 2 for 01, 3 for 001): 3
Enter the minimum image size in KB (leave blank for no size constraint): 100

Output

After processing, the script will output a summary that looks like this:

text

    === SUMMARY ===
    Processed 4/5 comics successfully.
    Missing comics: 003, 005
    Started at: 2024-09-11 12:00:00
    Ended at: 2024-09-11 12:10:35
    ===============

Features Breakdown
Year Fallback Logic

If a comic page isn't found for the specified year, the script will attempt to find the comic by incrementing the year up to the current year. This ensures that even if the year is incorrect or missing, the script will keep trying to find the comic.
Retry Mechanism

If an image or page fails to load, the script will retry up to 3 times before skipping it. This helps prevent temporary network issues from stopping the scraping process.
Logging

For every request, the script logs:

    The status code of the request.
    Detailed error messages when an image or page cannot be loaded.
    A retry message if the page or image failed to load.

Cleanup

The script creates a folder for each comic issue and downloads the images into it. Once the images are zipped into the desired file format, the script automatically deletes the image folder to keep your workspace clean.
Summary Report

At the end of the script, a summary is provided that includes:

    How many comics were successfully processed.
    A list of any comics that were skipped or missing.
    The start and end times of the scraping process.

Troubleshooting

    Comic Not Found or Skipped:
        If a comic is skipped, check the URL pattern and year. Ensure that the comic issue and year exist on the website.
        The script will attempt different years if the comic is not found for the given year, up to the current year.

    Status Codes:
        Status codes for each request are logged. If the script logs a status code of 404, it means the page was not found on the server.
        For status codes like 403, the site may have blocked access or is preventing scraping.

License

This project is licensed under the MIT License.
