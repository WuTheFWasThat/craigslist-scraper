import csv
import bs4
import requests

def find_one(x, type, filters=None):
    divs = x.findAll(type, filters)
    assert len(divs) == 1
    return divs[0]


def get_craigslist_info(url):
    res = requests.get(url)

    r = bs4.BeautifulSoup(res.text)

    title = find_one(r, "span", {"id": "titletextonly"}).text
    body = find_one(r, "section", {"id": "postingbody"}).text
    address = find_one(r, "div", {"class": "mapaddress"}).text
    address_link = find_one(find_one(r, "p", {"class": "mapaddress"}), "a").get("href")
    attrs = []
    for x in r.findAll("p", {"class": "attrgroup"}):
        for y in x.findAll("span"):
            attrs.append(y.text)

    return dict(
        url=url,
        title=title,
        body=body,
        address=address,
        address_link=address_link,
        attrs=attrs,
    )


with open("apartments.csv") as f:
    w = csv.DictWriter(f, ['url', 'title', 'body', 'address', 'address_link', 'attrs'])
    w.writeheader()

    url = "https://sfbay.craigslist.org/eby/apa/d/berkeley-furnished-1-br-in-north/7137487034.html"
    w.writerow(get_craigslist_info(url))
