"""
Requires imgur API
    pip install imgurpython


"""

import prof
from os import path

from imgurpython import ImgurClient
from imgurpython.helpers.error import ImgurClientError

client_id = '19c4ba3fc2c26ef'
client_secret = 'dd5b0918a2f5d36391d574bd2061c50b47bade63'
client = ImgurClient(client_id, client_secret)


def _cmd_imgur(img_path):
    try:
        expanded_path = path.expanduser(img_path)
        data = client.upload_from_path(expanded_path, config=None, anon=True)
        prof.send_line(data['link'])
    except IOError as ioe:
        prof.cons_show('Could not find file at ' + expanded_path)
    except ImgurClientError as e:
        prof.log_error('Could not upload to Imgur - ' + e.error_message)
        prof.log_error('Imgur status code - ' + e.status_code)


def prof_init(version, status, account_name, fulljid):
    synopsis = [
        "/imgur <file>"
    ]
    description = "Upload an image to imgur and send the link"
    args = [
        [ "<file>",  "full path to image file" ]
    ]
    examples = [
        "/imgur ~/images/cats.jpg"
    ]

    prof.register_command("/imgur", 1, 1, synopsis, description, args, examples, _cmd_imgur)
