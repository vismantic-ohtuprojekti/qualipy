import flickrapi
import json
import urllib
import os
import sys


def get_original_url(photo, original_secret):
    img_farm = str(photo[unicode('farm')])
    img_server = str(photo[unicode('server')])
    img_id = str(photo[unicode('id')])
    img_secret = str(photo[unicode('secret')])
    print 'downloading original image'
    return 'https://farm' + img_farm + '.staticflickr.com/' + img_server + '/' + img_id + '_' + original_secret + '_o' + '.jpg'

def download_image(url, local_file_name):
    print 'downloading ', local_file_name, '...'
    urllib.urlretrieve(url, local_file_name)

if __name__ == '__main__':
    number_of_images = sys.argv[1]
    tags_to_use = sys.argv[2]
    save_directory = sys.argv[3]
    download_originals = True
    
    api_key = unicode('')
    api_secret = unicode('')

    flickr = flickrapi.FlickrAPI(api_key, api_secret, format='json')
    response_json = flickr.photos_search(tags=tags_to_use, per_page=str(number_of_images))
    response = json.loads(response_json.decode('utf-8'))

    for photo in response['photos'][unicode('photo')]:
        try:
            img_id = str(photo[unicode('id')])
            img_secret = str(photo[unicode('secret')])
            
            response_info_json = json.loads(flickr.photos.getInfo(photo_id=img_id))
            
            if download_originals and 'originalsecret' in response_info_json['photo']:
                url = get_original_url(photo, str(response_info_json['photo'][unicode('originalsecret')]))
                image_path = os.path.join(save_directory, img_id + '_' + img_secret + '.jpg')
                download_image(url, image_path)
        except:
            print 'Failed to download image'
