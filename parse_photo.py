import requests
import json

def parse_photo(url):
    start_json_template = "window._cianConfig['frontend-offer-card'] = (window._cianConfig['frontend-offer-card'] || []).concat("
    photos = []
    try:
        response = requests.get(url)
    except requests.ConnectionError:
        return -1

    html = response.text
    if start_json_template in html:
        start = html.index(start_json_template) + len(start_json_template)
        end = html.index('</script>', start) - 2
        json_raw = html[start:end].strip()[:-1]
        json_ = json.loads(json_raw)
        for item in json_:
            if item['key'] == 'defaultState':
                description = item['value']['offerData']['offer']['description']
                flat_id = item['value']['offerData']['offer']['cianId']
                area = item['value']['offerData']['offer']['totalArea']
                floor = item['value']['offerData']['offer']['floorNumber']
                price = item['value']['offerData']['offer']['bargainTerms']['price']
                title1 = item['value']['offerData']['seoData']['socialNetworksTitle']['full']
                title2 = item['value']['offerData']['seoData']['mainTitle']
                currency = item['value']['offerData']['offer']['bargainTerms']['currency']
                for photo in item['value']['offerData']['offer']['photos']:
                    photos.append(photo['fullUrl'])
                break
    if photos:
        return flat_id, title1, title2, description, photos
    else:
        return -2
