## The following script scrapes the identifier of the latest VRT NWS radio bulletin and fetches the stream url.
## To do so, you first need a player token in order to request the stream.


import requests
from bs4 import BeautifulSoup

def extract_media_id(url):
    try:
        # Fetch webpage content
        response = requests.get(url)
        #print(response.content)
        if response.status_code == 200:
            # Parse HTML content using BeautifulSoup
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Find the div with the specified class
            div_element = soup.find('div', {'class': 'vrt-card vrt-card-news'})
            
            if div_element:
                # Extract the value of data-media-id attribute
                media_id = div_element.get('data-media-id')
                media_id = media_id.replace('vrtmediareference://', '')
                return media_id
            else:
                return "Div element with specified class not found."
        else:
            return f"Failed to fetch webpage. Status code: {response.status_code}"
    except requests.RequestException as e:
        return f"Request Exception: {e}"

def get_vrt_player_token():
    url = "https://media-services-public.vrt.be/vualto-video-aggregator-web/rest/external/v1/tokens"
    headers = {"Content-Type": "application/json"}

    try:
        response = requests.post(url, headers=headers)
        if response.status_code == 200:
            json_response = response.json()
            vrt_player_token = json_response.get('vrtPlayerToken')
            return vrt_player_token
        else:
            return f"Failed to fetch token. Status code: {response.status_code}"
    except requests.RequestException as e:
        return f"Request Exception: {e}"

def get_hls_url_from_json(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            json_data = response.json()
            target_urls = json_data.get('targetUrls', [])
            for target_url in target_urls:
                if target_url.get('type') == 'hls':
                    hls_url = target_url.get('url')
                    return hls_url
            return "No HLS URL found in the response."
        else:
            return f"Failed to fetch data. Status code: {response.status_code}"
    except requests.RequestException as e:
        return f"Request Exception: {e}"


# URL of the webpage to fetch
url = "https://www.vrt.be/vrtnws/nl/luister/programma-s/"

# Call the function and print the extracted media ID
vrtmediareference = extract_media_id(url)

# Get the vrtPlayerToken
vrtPlayerToken = get_vrt_player_token()

# Construct get stream info URL
mediaAggregatorUrl = "https://media-services-public.vrt.be/media-aggregator/v2/media-items/" + vrtmediareference + "?vrtPlayerToken=" + vrtPlayerToken + "&client="

# Get the HLS URL from the JSON response
hls_url = get_hls_url_from_json(mediaAggregatorUrl)
print(hls_url)