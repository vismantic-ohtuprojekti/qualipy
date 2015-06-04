import flickrapi
import json
import urllib
import os
import sys


def get_url(photo):
    img_farm = str(photo[unicode('farm')])
    img_server = str(photo[unicode('server')])
    img_id = str(photo[unicode('id')])
    img_secret = str(photo[unicode('secret')])
    return 'https://farm' + img_farm + '.staticflickr.com/' + img_server + '/' + img_id + '_' + img_secret + '.jpg'


def download_image(url, local_file_name):
    print 'downloading ', local_file_name, '...'
    urllib.urlretrieve(url, local_file_name)


def create_exif_json(exif_json):
    if 'photo' not in exif_json:
        print 'Invalid exif'
        return 'invalid'

    final_json = '[{'
    for i, entry in enumerate(exif_json['photo']['exif']):
        final_json = final_json + '"' + entry['label'] + '"' +  ': ' + '"' + entry['raw']['_content'] + '"'

        if i != len(exif_json['photo']['exif']) - 1:
            final_json = final_json + ', '

    final_json = final_json + '}]'
    return final_json


def add_exif_to_image(exif_json, image_path):
    json_file = image_path.split('.')[0] + '_exif.json'

    exif_source = create_exif_json(exif_json)
    if exif_source == 'invalid':
        return

    with open(json_file, 'w') as outfile:
        outfile.write(exif_source.encode('UTF-8'))

    os.system('exiftool -overwrite_original -json=' + json_file + " " + image_path)
    os.unlink(json_file)


if __name__ == '__main__':
    number_of_images = sys.argv[1]
    tags_to_use = sys.argv[2]
    save_directory = sys.argv[3]

    api_key = unicode('')
    api_secret = unicode('')

    flickr = flickrapi.FlickrAPI(api_key, api_secret, format='json')
    response_json = flickr.photos_search(tags=tags_to_use, per_page=str(number_of_images))
    response = json.loads(response_json.decode('utf-8'))

    for photo in response['photos'][unicode('photo')]:
        try:
            img_id = str(photo[unicode('id')])
            img_secret = str(photo[unicode('secret')])
            url = get_url(photo)
            image_path = os.path.join(save_directory, img_id + '_' + img_secret + '.jpg')
            download_image(url, image_path)

            response_json_exif = flickr.photos.getExif(photo_id=img_id, photo_secret=img_secret)
            response_exif = json.loads(response_json_exif)
            add_exif_to_image(response_exif, image_path)
        except:
            print 'Failed to download image'
