import os
import json
import glob
from flickrapi import FlickrAPI

# Replace with your own Flickr API keys
FLICKR_API_KEY = 'your_flickr_api_key'
FLICKR_API_SECRET = 'your_flickr_api_secret'
FLICKR_USER_ID = 'your_flickr_user_id'

# Replace with the path to your Instagram archive folder
INSTAGRAM_ARCHIVE_PATH = 'path_to_your_instagram_archive'

# Initialize the Flickr API client
flickr = FlickrAPI(FLICKR_API_KEY, FLICKR_API_SECRET, format='parsed-json')

def upload_to_flickr(file_path, title, description, tags):
    # Open the media file in binary mode
    with open(file_path, 'rb') as f:
        # Upload the media file to Flickr with the provided metadata
        response = flickr.upload(
            fileobj=f,
            title=title,
            description=description,
            tags=tags,
            format='rest',
            is_public=1
        )
    return response

def process_instagram_archive(archive_path):
    # Find all JSON files in the Instagram archive's media/json folder
    json_files = glob.glob(os.path.join(archive_path, 'media', 'json', '*.json'))

    # Iterate through each JSON file
    for json_file in json_files:
        # Open and load the JSON data
        with open(json_file, 'r') as f:
            data = json.load(f)

        # Construct the full path to the media file
        media_path = os.path.join(archive_path, 'media', data['path'])
        
        # Set the title to the first 100 characters of the caption (if available)
        title = data['caption'][:100] if data['caption'] else ''
        
        # Set the description to the full caption
        description = data['caption']
        
        # Extract tags from the Instagram post and remove the '#' symbol
        tags = ' '.join([tag.strip('#') for tag in data['tags']])

        # Check if the media file exists
        if os.path.exists(media_path):
            # Upload the media file to Flickr and print the response
            response = upload_to_flickr(media_path, title, description, tags)
            print(f"Uploaded {media_path} to Flickr: {response}")
        else:
            print(f"File not found: {media_path}")

if __name__ == '__main__':
    # Process the Instagram archive and upload media files to Flickr
    process_instagram_archive(INSTAGRAM_ARCHIVE_PATH)
