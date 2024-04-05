""" Zapier Module that Process RCL Calendar Description to retrieve Non-Psalter Old Testament Reading and Gospel Reading as well as URL of Lectionary Week """

# Import necessary libraries
import json
import re
import requests

def get_pages(user_token):
    # This code Is "Better" But requires too much time for the Zapier 1 second time limit due to latency. 
    #url = f'https://graph.facebook.com/v19.0/me/accounts?access_token={user_token}'
    #print(url)
    #response = requests.get(url)
    #return response.json()['data']

    # Unfortunately hardcode your access_tokens for each page here with their ids so you can loop through them
    response = [{"id": 123, "access_token": 'abc123'}, {"id": 321, "access_token": "cba321"}] 
    return response

# Defining a function to process the text with a regular expression
def process_text_with_regex(text):
    # The regular expression pattern to match the year in the text
    # It looks for a word boundary, followed by a capital letter 'Y', followed by a colon, 
    # followed by a space, and then captures one or more word characters as a group
    pattern = r"(?:\** *)((?:[\d ]*[a-zA-Z]+(?: \d*:\d*)?)(?:(?: - )| | (?:-))?(?:(?:(?:\d* )?[a-zA-Z]+ )?\d*(?:[:-]+\d*)?))(?: +)(?:((?:[\d ]*[a-zA-Z]+(?: \d*:\d*)?)(?:(?: - )| |(?:-))?(?:(?:(?:\d* )?[a-zA-Z]+ )?\d*(?:[:-]+\d*)?))(?:(?:(?: +)or(?:[\d ]*[a-zA-Z]+(?: \d*:\d*)?)(?:(?: - )| |(?:-))?(?:(?:(?:\d* )?[a-zA-Z]+ )?\d*(?:[:-]+\d*)?))?))(?: +)((?:[\d ]*[a-zA-Z]+(?: \d*:\d*)?)(?:(?: - )| |(?:-))?(?:(?:(?:\d* )?[a-zA-Z]+ )?\d*(?:[:-]+\d*)?))(?: +)((?:[\d ]*[a-zA-Z]+(?: \d*:\d*)?)(?:(?: - )| |(?:-))?(?:(?:(?:\d* )?[a-zA-Z]+ )?\d*(?:[:-]+\d*)?))(?: +)(https?:\/\/(?:www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b(?:[-a-zA-Z0-9()@:%_\+.~#?&//=]*))"

    # Using the re.search function to find the first occurrence of the pattern in the text
    text = text.replace('\n', ' ').replace('\r', '')
    match = re.search(pattern,  text)

    # Checking if a match was found
    if match:
        print(match)
        # If a match was found, returning the matched group (the year)
        return f"{match.group(1)}, {match.group(4)}", match.group(5)
    else:
        # If no match was found, returning None
        return None, None

def publish_facebook_post(input_data, readings, access_token, url, page_url):
    # Define the headers for the HTTP request
    headers = {
        "Authorization": f"Bearer {access_token}",  # Include the access token in the Authorization header
        "Content-Type": "application/json",  # Specify the content type as JSON
    }

    # Define the data for the HTTP request
    data = {
        "message": f'{input_data["message"]} \n{readings}',  # Include the message for the post
        "link": url,  # Include the URL for the post
    }

    # Send a POST request to the Facebook Graph API endpoint to publish the post
    try:
        # Add Timeout to beat Zapier 1 second limit since regex takes a little bit. We just need to fire off a submit successfully.
        response = requests.post(page_url, headers=headers, data=json.dumps(data),timeout=(None, 0.3))
    except requests.exceptions.Timeout:
      print("Timeout occurred")

    # Define the output as a dictionary with the key "response" and the value as the response from the API
    return {"response": "Some Response"}

# Getting the text from the input data
text = input_data["text"]

# Calling the function to process the text with the regular expression
#print(text)
readings, url = process_text_with_regex(text)

# Printing the processed text
#print(readings, url)

fb_pages = get_pages(input_data['system_user_token'])

responses = []
for page in fb_pages:
    page_url = f"https://graph.facebook.com/v19.0/{page['id']}/feed"
    response = publish_facebook_post(input_data, readings, page['access_token'], url, page_url)
    responses.append(fb_pages)

output = {"readings": readings, "url": url, "responses": responses}
