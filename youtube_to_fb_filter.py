""" Zapier Module that Processes two Regex Patterns as Paths, and Sends a YouTube Video to One Page or Another Based on Regex Patterns of Title of Video. Useful if you have Two Facebook Pages for Two Churches, but have one YouTube Channel for your Charge """

# Import necessary libraries
import json
import re
import requests

# Defining a function to post video to Correct Page by Title of Video
def post_video_to_page(input_data):

    # Define Regex Patterns
    video_title = input_data['video_title']
    video_url = input_data['video_url']
  
    pattern_1 = input_data['pattern_1']
    pattern_2 = input_data['pattern_2']

    # Define the URL for the Facebook Graph API endpoint to publish a post
    url_1 = f"https://graph.facebook.com/v14.0/{input_data['page_id_1']}/feed"
    url_2 = f"https://graph.facebook.com/v14.0/{input_data['page_id_2']}/feed"

  if re.match(pattern_1, video_title)
      return publish_facebook_post(input_data, input_data['text'], url, input_data["page_token_1"], page_url_1)
  else if re.match(pattern_2, video_title)
      return publish_facebook_post(input_data, input_data['text'], url, input_data["page_token_2"], page_url_2)

def publish_facebook_post(input_data, text, url, fb_page_token, page_url):
    # Define the access token for the Facebook Graph API
    access_token = input_data.get("access_token")

    # Define the headers for the HTTP request
    headers = {
        "Authorization": f"Bearer {fb_page_token}",  # Include the access token in the Authorization header
        "Content-Type": "application/json",  # Specify the content type as JSON
    }

    # Define the data for the HTTP request
    data = {
        "message": f'{text}',  # Include the message for the post
        "link": url,  # Include the URL for the post
    }

    # Send a POST request to the Facebook Graph API endpoint to publish the post
    response = requests.post(page_url, headers=headers, data=json.dumps(data))

    # Print the response from the API
    print(response.text)

    # Define the output as a dictionary with the key "response" and the value as the response from the API
    return {"response": response.text}
  
# Publish to Facebook
response = post_video_to_page(input_data)
output = {"response": response}
