import asyncio
import csv
from urllib.parse import urlencode, urljoin
import math
import httpx
from parsel import Selector
import json
import re
from typing_extensions import TypedDict
from typing import List, Optional


class Preview(TypedDict):
    """Type hint container for business preview data."""
    name: str
    url: str
    links: List[str]
    phone: str
    categories: List[str]
    address: str
    location: str
    rating: str
    rating_count: str
    email: Optional[str]  # Added email field
    facebook: Optional[str]  # Added Facebook field


def extract_email(response_text):
    """Extract email address from HTML text using regular expressions."""
    email_regex = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    email_matches = re.findall(email_regex, response_text)
    return email_matches[0] if email_matches else None


async def parse_search(response) -> List[Preview]:
    """Parse yellowpages.com search page for business preview data"""
    sel = Selector(text=response.text)
    parsed = []
    base_url = "https://www.yellowpages.com"
    for result in sel.css(".organic div.result"):
        links = {}
        for link in result.css("div.links>a"):
            name = link.xpath("text()").get()
            url = link.xpath("@href").get()
            links[name] = url
        first = lambda css: result.css(css).get("").strip()
        
        # Extract email address from the business's website
        website_url = first("a.business-name::attr(href)")
        print("Website URL:", website_url)  # Debugging statement
        if website_url:
            website_url = urljoin(base_url, website_url)  # Convert to absolute URL
            async with httpx.AsyncClient() as client:
                website_response = await client.get(website_url)
                website_email = extract_email(website_response.text)
        else:
            website_email = None
        
        # Extract Facebook page link
        facebook_page = first("div.links a[href*=facebook]::attr(href)")

        parsed.append(
            {
                "name": first("a.business-name ::text"),
                "url": urljoin(base_url, first("a.business-name::attr(href)")),
                "links": links,
                "phone": first("div.phone::text"),
                "categories": [value.strip() for value in result.css(".categories>a::text").getall()],
                "address": first(".adr .street-address::text"),
                "location": first(".adr .locality::text"),
                "rating": first(".ratings .rating div::attr(class)").split(" ", 1)[-1],
                "rating_count": first(".ratings .rating span::text").strip("()"),
                "email": website_email,  # Include extracted email address
                "facebook": facebook_page,  # Include Facebook page link
            }
        )
    return parsed


async def search(query: str, location: Optional[str] = None) -> List[Preview]:
    """Search yellowpages.com for business preview information."""
    async with httpx.AsyncClient() as client:
        def make_search_url(page):
            base_url = "https://www.yellowpages.com/search?"
            parameters = {"search_terms": query, "geo_location_terms": location, "page": page}
            return base_url + urlencode(parameters)

        first_page = await client.get(make_search_url(1))
        sel = Selector(text=first_page.text)
        total_results = int(sel.css(".pagination>span::text ").re(r"of (\d+)")[0])
        total_pages = int(math.ceil(total_results / 30))
        print(f'{query} in {location}: scraping {total_pages} pages of business previews')
        previews = await parse_search(first_page)
        for result in await asyncio.gather(*[client.get(make_search_url(page)) for page in range(2, total_pages + 1)]):
            previews.extend(await parse_search(result))
        print(f'{query} in {location}: scraped {len(previews)} total business previews')
        return previews


async def main():
    results = await search("BBQ Restaurants", "Chattanooga, TN")
    with open('businesses.csv', mode='w', newline='') as file:
        fieldnames = results[0].keys()
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for result in results:
            writer.writerow(result)
    print("Data written to businesses.csv")


if __name__ == "__main__":
    asyncio.run(main())
