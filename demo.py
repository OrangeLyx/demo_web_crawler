import requests
from bs4 import BeautifulSoup
import pyperclip
from openai import OpenAI
from pydantic import BaseModel, Field

header={"User-Agent": 
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Safari/537.36"
    }
response=requests.get("http://blog.rei.com/camp/how-to-introduce-your-indoorsy-friend-to-the-outdoors/",headers=header)

# response=requests.get("https://www.cnn.com/2025/09/23/tech/google-study-90-percent-tech-jobs-ai",headers=header)

response.raise_for_status()
html=response.text 


# 验证
# pyperclip.copy(html)

soup = BeautifulSoup(html, "lxml")

# 下面是需要通过ai请求实现的
prompt=prompt = f"""
You are an HTML content extraction agent. Analyze the following HTML structure and identify:
1. The page type: article, product, homepage, listing, or other meta data.
2. A CSS selector for the main page title.
3. A CSS selector for the primary content container.
The content selector must exclude navigation, footer, advertisements, related articles, comments, and recommendations.

Return valid JSON only:

{{
  "page_type": "article",
  "title_selector": "h1",
  "content_selector": "article .content",
  "confidence": 0.95
}}

HTML:

{html}
"""

# openai 
# 设定密钥

# 检查返回值

# 组合生成meta data 

# 返回给前端

title = soup.title.get_text(strip=True)
content_tag = soup.find(
    "section",
    attrs={"itemprop": "articleBody"}
)
content = (
    content_tag.get_text(" ", strip=True)
    if content_tag
    else ""
)

# 返回给前端
# meta data
print("Title:")
print(title)
print("\nContent:")
print(content)



# soup = BeautifulSoup(html, "lxml")

# title = (
#     soup.title.get_text(strip=True)
#     if soup.title
#     else ""
# )

# content_tag = soup.find(
#     class_="article__content"
# )

# content = (
#     content_tag.get_text(" ", strip=True)
#     if content_tag
#     else ""
# )

# print("Title:")
# print(title)

# print("\nContent:")
# print(content)
