import os
import re
import webbrowser

import vk
from vk.exceptions import VkAPIError


def get_user_id_and_access_token() -> list:
    with open(SECRET_FILE, 'r') as file:
        return file.readline().split(";")


SECRET_FILE = os.path.join(
    os.path.normpath(
        os.path.dirname(os.path.abspath(__file__)) + os.sep + os.pardir
    ),
    "secret"
)


def check_secret_file():
    if not os.path.exists(SECRET_FILE):
        with open(SECRET_FILE, 'w') as file:
            file.write("-1;-1;-1;-1")


class VkProvider:
    def __init__(self):
        self.session = None
        self.api = None
        (self.app_token,
         self.user_id,
         self.access_token,
         self.app_id) = get_user_id_and_access_token()
        vk.api.access_token = self.app_token
        self.session = vk.AuthSession(scope='wall', app_id=self.app_id)
        self.api = vk.API(self.session)

    def has_accessed(self):
        pass

    def try_get_access(self):
        my_request = 'https://oauth.vk.com/authorize?client_id={}' \
                     '&redirect_uri={}' \
                     '&scope={}' \
                     '&display={}' \
                     '&response_type={}'\
            .format(
                self.app_id,
                "https://oauth.vk.com/blank.html", "wall", "popup", "token"
            )
        webbrowser.open(my_request, new=1)

    def send_post_with(self, text: str) -> bool:
        try:
            self.api.wall.post(
                owner_id=self.user_id,
                message=text,
                v="5.70",
                access_token=self.access_token
            )
        except VkAPIError:
            return False
        return True

    @staticmethod
    def save_user_id_and_access_token_by(url: str):
        a = re.findall(r'access_token=(.+)&.+user_id=(\d+)', url)
        if a is None or a[0] is None or len(a[0]) != 2:
            return
        VkProvider.save_user_id_and_access_token(a[0][0], a[0][1])

    @staticmethod
    def save_user_id_and_access_token(user_id: str, token: str):
        key = get_user_id_and_access_token()[0]
        app_id = get_user_id_and_access_token()[3]
        with open(SECRET_FILE, 'w') as file:
            file.write(key + ";" + token + ";" + user_id + ";" + app_id)
