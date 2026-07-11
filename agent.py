import requests
from bs4 import BeautifulSoup
from openai import OpenAI
from pydantic import BaseModel, Field


class ExtractionPlan(BaseModel):
    page_type: str
    title_selector: str
    content_selector: str
    confidence: float = Field(ge=0, le=1)


client = OpenAI()

url = (
    # "http://blog.rei.com/camp/how-to-introduce-your-indoorsy-friend-to-the-outdoors/"
    "https://www.cnn.com/2025/09/23/tech/google-study-90-percent-tech-jobs-ai"
)

headers = {
    "User-Agent": (
           "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Safari/537.36"
    )
}


def crawl_article(url: str) -> dict:

    response = requests.get(url, headers=headers, timeout=60)
    response.raise_for_status()

    html = response.text
    soup = BeautifulSoup(html, "lxml")

    simple_html = ""

    for tag in soup.find_all(["h1", "h2", "article", "main", "section", "div", "p"]):
        text = tag.get_text(" ", strip=True)

        if text:
            simple_html += str(tag)[:1000] + "\n"

    simple_html = simple_html[:100000]

    ai_response = client.responses.parse(
        model="gpt-5-mini",
        input=f"""
    You are an HTML content extraction agent.

    Analyze the HTML and return:

    1. Page type
    2. CSS selector for the main title
    3. CSS selector for the main content

    Exclude navigation, footer, advertisements, comments,
    recommendations, and related articles.

    HTML:

    {simple_html}
    """,
        text_format=ExtractionPlan,
    )

    plan = ai_response.output_parsed

    if plan is None:
        raise RuntimeError("AI did not return a valid extraction plan.")

    title_tag = soup.select_one(plan.title_selector)
    content_tag = soup.select_one(plan.content_selector)
    title = (
        title_tag.get_text(" ", strip=True)
        if title_tag
        else ""
    )
    content = (
        content_tag.get_text(" ", strip=True)
        if content_tag
        else ""
    )

    return  {
            "url": url,
            "page_type": plan.page_type,
            "title": title,
            "content": content,
            "title_selector": plan.title_selector,
            "content_selector": plan.content_selector,
            }

# print(json.dumps(result, indent=2, ensure_ascii=False))