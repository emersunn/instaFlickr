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
    with open(file_path, 'rb') as f:
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
    json_files = glob.glob(os.path.join(archive_path, 'media', 'json', '*.json'))

    for json_file in json_files:
        with open(json_file, 'r') as f:
            data = json.load(f)

        media_path = os.path.join(archive_path, 'media', data['path'])
        title = data['caption'][:100] if data['caption'] else ''
        description = data['caption']
        tags = ' '.join([tag.strip('#') for tag in data['tags']])

        if os.path.exists(media_path):
            response = upload_to_flickr(media_path, title, description, tags)
            print(f"Uploaded {media_path} to Flickr: {response}")
        else:
            print(f"File not found: {media_path}")

if __name__ == '__main__':
    process_instagram_archive(INSTAGRAM_ARCHIVE_PATH)
