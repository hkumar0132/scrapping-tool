# Web Scraper

A Python and FastAPI based web scraper designed for extracting product information from an e-commerce website. This scraper retrieves product titles, prices, and image URLs, and stores the data in a specified format.

## Features

- Scrapes multiple pages of products and extracts product titles, prices, and image URLs
- Implements a retry mechanism for failed requests
- Abstraction:
    - Follows OOP principles and SOLID design principles
    - Utilizes Observer, Factory, and Decorator design patterns
- Notification service setup for alerts and updates
- Uses Redis for caching to minimize frequent updates to storage
- Stores data in a JSON file, easily extensible to SQL/NoSQL databases
- Configurable scrape settings, including the number of pages to scrape

## Requirements

- Python 3.x
- Required Libraries:
```bash
    fastapi
    uvicorn
    beautifulsoup4
    requests
    pydantic
    python-dotenv
    pytest
    redis
    aiohttp
```

You can install the required libraries using pip:

```bash
    pip install -r requirements.txt
```

## Initiating the Scraping Process

1. Set a static token to access the endpoint. Update the SECRET_TOKEN value in the config.py file or set the SECRET_TOKEN variable in your environment.

2. Start the FastAPI project using command:

```bash
    uvicorn app:app --host 0.0.0.0 --port <PORT> --reload
```

3. Setup redis on local server and update the URL in config.py

4. Make and API request to start scrapping:

```bash
    curl --location 'http://localhost:<PORT>/scrape?token=<SECRET_TOKEN>' \
    --header 'Content-Type: application/json' \
    --data '{
        "proxy": "<proxy_server_url>",
        "limit": <number_of_pages_to_scrape>
    }'
```

Replace <SECRET_TOKEN> with your actual token, <proxy_server_url> with your proxy server URL, and <number_of_pages_to_scrape> with the desired number of pages.# scrapping-tool
# scrapping-tool
