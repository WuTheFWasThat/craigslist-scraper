import csv
import bs4
import requests

def find_one(x, type, filters=None, none_okay=False):
    divs = x.findAll(type, filters)
    if not len(divs) and none_okay:
        return None
    assert len(divs) == 1
    return divs[0]


def get_craigslist_info(url):
    print(url)
    res = requests.get(url)

    r = bs4.BeautifulSoup(res.text)
    if find_one(r, "span", {"id": "has_been_removed"}, none_okay=True):
        return dict(url=url, title='POSTING REMOVED')

    title = find_one(r, "span", {"id": "titletextonly"}).text
    price = find_one(r, "span", {"class": "price"}).text
    body = find_one(r, "section", {"id": "postingbody"}).text
    body = body.strip()
    assert body.startswith("QR Code Link to This Post")
    body = body[len("QR Code Link to This Post"):]
    body = body.strip()
    try:
        address = find_one(r, "div", {"class": "mapaddress"}).text
    except AssertionError:
        address = ""
    try:
        address_link = find_one(find_one(r, "p", {"class": "mapaddress"}), "a").get("href")
    except AssertionError:
        address_link = ""
    attrs = []
    for x in r.findAll("p", {"class": "attrgroup"}):
        for y in x.findAll("span"):
            attrs.append(y.text)

    return dict(
        url=url,
        title=title,
        price=price,
        body=body,
        address=address,
        address_link=address_link,
        attrs=attrs,
    )


urls = [
    "https://sfbay.craigslist.org/eby/apa/d/berkeley-furnished-1-br-in-north/7137487034.html",
    "https://sfbay.craigslist.org/eby/apa/d/berkeley-furnished-1-br-in-north/7137487034.html",
    "https://sfbay.craigslist.org/eby/apa/d/berkeley-amazing-one-bedroom-north/7140765366.html",
    "https://sfbay.craigslist.org/eby/apa/d/berkeley-minutes-away-from-the/7143220440.html",
    "https://sfbay.craigslist.org/eby/apa/d/berkeley-1-bedroom-walk-to-cal-campus/7135035937.html",
    "https://sfbay.craigslist.org/sfc/apa/d/berkeley-bright-unit/7131106245.html",
    "https://sfbay.craigslist.org/eby/apa/d/berkeley-gourmet-ghetto-apartment/7143749427.html",
    "https://sfbay.craigslist.org/eby/apa/d/berkeley-welcome-home-great-lighting/7138379260.html",
    "https://sfbay.craigslist.org/eby/apa/d/berkeley-1-bedroom-with-berkeley-hills/7134234964.html",
    "https://sfbay.craigslist.org/eby/apa/d/berkeley-renovated-and-modern-one/7143092203.html",
    "https://sfbay.craigslist.org/eby/apa/d/berkeley-1-2-block-to-uc-sunny-1-2br/7141703241.html",
    "https://sfbay.craigslist.org/eby/apa/d/berkeley-pet-friendly-2-bedroom-near/7138377630.html",
    "https://sfbay.craigslist.org/eby/apa/d/berkeley-charming-location-newly/7141123102.html",
    "https://sfbay.craigslist.org/eby/apa/d/berkeley-schedule-tour-and-save-2000/7142839969.html",
    "https://sfbay.craigslist.org/eby/apa/d/berkeley-beautifully-remodeled-brand/7135416324.html",
    "https://sfbay.craigslist.org/eby/apa/d/berkeley-1-2-block-to-uc-sunny-1-2br/7122059628.html",
    "https://sfbay.craigslist.org/eby/apa/d/berkeley-1-bedroom-walk-to-cal-campus/7135035937.html",
    "https://sfbay.craigslist.org/eby/apa/d/berkeley-lovely-2-bedroom-apartment/7138032412.html",
    "https://sfbay.craigslist.org/eby/apa/d/berkeley-modern-spacious-with-open/7125373080.html",
]

with open("apartments.csv", 'w') as f:
    w = csv.DictWriter(f, ['url', 'price', 'attrs', 'title', 'body', 'address', 'address_link'])
    w.writeheader()

    for url in urls:
        d = get_craigslist_info(url)
        if d is None:
            continue
        w.writerow(d)
