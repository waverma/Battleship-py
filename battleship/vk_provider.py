import re
import webbrowser
import vk


def get_user_id_and_access_token() -> list:
    with open(SECRET_FILE, 'r') as file:
        return file.readline().split(";")


APP_SECRET_KEY = "KAlJPYqbltkCatYOaVQS"
SECRET_FILE = r"F:\MyProgProject\battleship\resources\secret"


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
        except Exception:
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
        id = get_user_id_and_access_token()[3]
        with open(SECRET_FILE, 'w') as file:
            file.write(key + ";" + token + ";" + user_id + ";" + id)
