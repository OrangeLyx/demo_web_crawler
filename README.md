# Web Crawler

This repository contains a web crawler demo developed as a take-home interview assignment. The original requirement document is private, but the technical design and proposed system architecture are available in a Notion document.

## Deployment

The crawler API is deployed on an AWS EC2 instance. http://52.14.124.149:8000/ This proof of concept does not currently use a database, so previously generated JSON results are not stored.

## Current Implementation

The three provided test URLs are divided into two categories:

1. Product pages
2. Article pages

### Product Pages

Amazon may block direct requests from cloud servers or return CAPTCHA pages. To avoid unreliable direct crawling, this demo uses the [Canopy API](https://github.com/canopy-framework/canopy) to retrieve Amazon product information.

The extracted fields include: title, brand, price, rating, feature bullets, categories.

For a production system, the preferred next step would be to use an official Amazon API or obtain strict data access permission.

### Article Pages

For general article URLs, the crawler first downloads and parses the HTML. To overcome the dynamic extracting the content, I use an AI agent to analyzes the HTML structure and identifies CSS selectors for:

* The main page title
* The primary content container
* The page type

The crawler then uses BeautifulSoup and the generated selectors to extract the original article content while excluding navigation, advertisements, comments, related articles, and footer content.

## API Testing

A testing video is included in solution document. I use FAST API built-in testing page: http://52.14.124.149:8000/docs.  The request body contains the target URL:

```json
{
  "url": "https://example.com/article"
}
```

The server returns the extracted metadata and content in JSON format:

```json
{
  "success": true,
  "result": {
    "url": "https://example.com/article",
    "page_type": "article",
    "title": "Example Article",
    "content": "Extracted article content..."
  }
}
```

## Limitations

This version is intended as a proof of concept and has the following limitations. Future exploration is being strengthened to achieve improvements.

* Some websites may block requests from cloud-server IP addresses.
* Extracted results are not persisted in a database.
* The AI parsing extraction service is called for each general article page.
