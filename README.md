# Django Scrapy API Project

This project provides a comprehensive solution for web scraping and data extraction. It combines the power of Scrapy and Django to efficiently scrape data from the ACM and IEEE digital libraries and expose it through a user-friendly API. The Scrapy spiders extract relevant information such as titles, links, abstracts, citation counts, and author details, while the Django project provides a structured way to access and utilize this data through well-defined API endpoints.

## Scrapy Project: ACM & IEEE Spider

This project contains two Scrapy spiders that scrape research papers, titles, authors, abstracts, and citation counts from the **IEEE Xplore** and **ACM Digital Library** websites.

### Project Description

The **ACM & IEEE Spiders** are designed to scrape research paper metadata from their respective digital libraries. Both spiders handle dynamic content using `scrapy-splash` to ensure proper loading of JavaScript-rendered pages.

#### Spider Capabilities:
- Scrapes research paper titles, links, abstracts, citation counts, and author details.
- Handles JavaScript-rendered content using Splash.

### Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/yourusername/your-repo.git
   cd your-repo
   ```

2. **Install the Dependencies**
   Install Scrapy and the necessary libraries:
   ```bash
   pip install scrapy scrapy-splash
   ```

3. **Install Splash**
   Install Docker from [here](https://docs.docker.com/get-docker/) and run Splash to handle JavaScript rendering:
   ```bash
   docker run -p 8050:8050 scrapinghub/splash
   ```

4. **Ensure Splash is Running**
   Ensure Splash is running in Docker:
   ```bash
   docker run -p 8050:8050 scrapinghub/splash
   ```

#### Spiders Overview

##### `ieee_spider`
- **Description**: The IEEE spider scrapes research papers from IEEE Xplore. It extracts information like the paper title, link, abstract, citation count, and authors.
- **Command**: 
   ```bash
   scrapy crawl ieee_spider -a search_term="Your Search Term" -o results.json
   ```

##### `acm_spider`
- **Description**: The ACM spider scrapes research papers from ACM Digital Library. It extracts information like the paper title, link, abstract, citation count, and authors.
- **Command**:
   ```bash
   scrapy crawl acm_spider -a search_term="Your Search Term" -o results.json
   ```

### Example Output

After running the spiders, the output will be stored in a resule.json. Here’s an example structure:

```json
{
  "title": "Example Research Paper Title",
  "link": "https://example.com",
  "details":"Example details of publication",
  "abstract": "This is a sample abstract.",
  "authors": ["Author One", "Author Two"],
  "citation_count": 120
}
```
## Django Project: A Bridge to Scraped Data

The Django project acts as a gateway between users and the Scrapy spiders. It handles requests, interacts with the spiders, and processes the extracted data, providing a structured interface for accessing scraped information from ACM and IEEE.

### Project Setup

#### 1. Install Required Libraries

```
pip install django djangorestframework
```
#### 2. Start the Django Development Server

```
python manage.py runserver
```
#### 3. Access the API

The Django API is now running at http://localhost:8000/. You can use a web browser or an API testing tool to interact with the API endpoints.
