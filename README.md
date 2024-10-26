# scrapping-tool

A Python and FastAPI based web scraper designed for extracting product information from an e-commerce website. This scraper retrieves product titles, prices, and image URLs, and stores the data in a specified format.

```Result has been written to scrapped_result folder after scrapping all 119 pages on https://dentalstall.com/shop/```

## Features

- Scrapes multiple pages of products and extracts product titles, prices, and image URLs
- Implements a retry mechanism for failed requests
- Abstraction:
    - Follows OOPs and SOLID principles
    - Utilizes Observer, Factory, Decorator and Singleton design patterns
- Notification service setup for alerts and updates
- Uses Redis for caching to minimize frequent updates to storage
- Stores data in a JSON file, easily extensible to SQL/NoSQL databases
- Configurable scrape settings, including the number of pages to scrape
- Logging

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

4. Make an API request to start scrapping:

```bash
    curl --location 'http://localhost:<PORT>/scrape?token=<SECRET_TOKEN>' \
    --header 'Content-Type: application/json' \
    --data '{
        "proxy": "<proxy_server_url>",
        "limit": <number_of_pages_to_scrape>
    }'
```

Replace <SECRET_TOKEN> with your actual token, <proxy_server_url> with your proxy server URL, and <number_of_pages_to_scrape> with the desired number of pages.

## Project structure

```bash
/scrapping-tool
|── main.py
|── /scrapper
|   |── base_scrapper.py
|   |── web_scrapper.py         
|   |── page_fetcher.py         
|   |── product_parser.py
|   |── scrapper_factory.py
|── /models
|   |── product.py
|   |── scrape_settings.py
|── /notification
|   |── base_notifier.py
|   |── console_notifier.py
|   |── email_notifier.py
|   |── notification_factory.py
|── /notification
|   |── base_notifier.py
|── /services
|   |── image_downloader.py
|── /repository
    |── /cache
    |   |── base_cache.py
    |   |── redis_cache.py
    |   |── cache_factory.py
    |── /storage
    |   |── base_storage.py
    |   |── json_storage.py
    |   |── storage_factory.py
    |── product_sync_manager.py
|── /tests    
    |   |── test_page_fetcher.py
    |   |── test_product_parser.py
    |   |── test_product_repository_manager.py
|── /utils
|   |── retry.py
|── README.md
|── requirements.txt

```