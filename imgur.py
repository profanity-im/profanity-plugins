"""
Requires imgur API
    pip install imgurpython


"""

import prof

from imgurpython import ImgurClient
from imgurpython.helpers.error import ImgurClientError

client_id = '19c4ba3fc2c26ef'
client_secret = 'dd5b0918a2f5d36391d574bd2061c50b47bade63'
client = ImgurClient(client_id, client_secret)


def _cmd_imgur(arg):
    try:
        data = client.upload_from_path(arg, config=None, anon=True)
        prof.send_line(data['link'])
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
