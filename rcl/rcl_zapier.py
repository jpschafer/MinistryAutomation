""" Zapier Module that Process RCL Calendar Description to retrieve Non-Psalter Old Testament Reading and Gospel Reading as well as URL of Lectionary Week """

# Import necessary libraries
import json
import re
import requests


# Defining a function to process the text with a regular expression
def process_text_with_regex(text):
    # The regular expression pattern to match the year in the text
    # It looks for a word boundary, followed by a capital letter 'Y', followed by a colon, 
    # followed by a space, and then captures one or more word characters as a group
    pattern = r"((?:[\d ]*[a-zA-Z]+(?: \d*:\d*)?)(?:(?: - )| )?(?:(?:(?:\d* )?[a-zA-Z]+ )?\d*(?:[:-]+\d*)?))(?: +)(?:((?:[\d ]*[a-zA-Z]+(?: \d*:\d*)?)(?:(?: - )| )?(?:(?:(?:\d* )?[a-zA-Z]+ )?\d*(?:[:-]+\d*)?))(?: +)(?:or (?:(?:[\d ]*[a-zA-Z]+(?: \d*:\d*)?)(?:(?: - )| )?(?:(?:(?:\d* )?[a-zA-Z]+ )?\d*(?:[:-]+\d*)?))?))(?: +)((?:[\d ]*[a-zA-Z]+(?: \d*:\d*)?)(?:(?: - )| )?(?:(?:(?:\d* )?[a-zA-Z]+ )?\d*(?:[:-]+\d*)?))(?: +)((?:[\d ]*[a-zA-Z]+(?: \d*:\d*)?)(?:(?: - )| )?(?:(?:(?:\d* )?[a-zA-Z]+ )?\d*(?:[:-]+\d*)?))(?: +)(https?:\/\/(?:www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b(?:[-a-zA-Z0-9()@:%_\+.~#?&//=]*))"

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
        return None

def publish_facebook_post(input_data, readings, url, fb_page_token, page_url):
    # Define the access token for the Facebook Graph API
    access_token = input_data.get("access_token")

    # Define the headers for the HTTP request
    headers = {
        "Authorization": f"Bearer {fb_page_token}",  # Include the access token in the Authorization header
        "Content-Type": "application/json",  # Specify the content type as JSON
    }

    # Define the data for the HTTP request
    data = {
        "message": f'{input_data["message"]} \n{readings}',  # Include the message for the post
        "link": url,  # Include the URL for the post
    }

    # Send a POST request to the Facebook Graph API endpoint to publish the post
    response = requests.post(page_url, headers=headers, data=json.dumps(data))

    # Print the response from the API
    print(response.text)

    # Define the output as a dictionary with the key "response" and the value as the response from the API
    return {"response": response.text}

# Getting the text from the input data
text = input_data["text"]

# Calling the function to process the text with the regular expression
print(text)
readings, url = process_text_with_regex(text)

# Printing the processed text
print(readings, url)

# Define the URL for the Facebook Graph API endpoint to publish a post
url_1 = f"https://graph.facebook.com/v14.0/{input_data['page_id_1']}/feed"
url_2 = f"https://graph.facebook.com/v14.0/{input_data['page_id_2']}/feed"

# Publish to Facebook
response_1 = publish_facebook_post(input_data, readings, url, input_data["page_token_1"], page_url_1)
response_2 = publish_facebook_post(input_data, readings, url, input_data["page_token_2"], page_url_2)

output = {"readings": readings, "url": url, "response_1", response_1 "response_2", response_2}
