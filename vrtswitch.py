import datetime
import requests
import hashlib


class VRTSwitchAPI(object):
    def __init__(self, version=3.3, server_key="13bc22628889ac02d14858a873af5e09"):
        self.version = str(version)
        self.server_key = server_key
        self.session = requests.Session()
        self.api_url = "https://switchserver.triangle-factory.be/api-" + self.version + "/"
        self.authorization_headers = {"switch_authorization": None}

    def create_headers(self):
        m = hashlib.md5()
        server_time = datetime.datetime.now()
        day = str(server_time.day).zfill(2)
        month = str(server_time.month).zfill(2)
        year = str(server_time.year)
        hours = str(server_time.hour-1).zfill(2)
        minutes = str(server_time.minute).zfill(2)
        seconds = str(server_time.second).zfill(2)
        server_time_formatted = day + month + year + hours + minutes + seconds
        server_token = server_time_formatted + self.server_key
        m.update(server_token.encode("utf-8"))
        return {
            "signature": m.hexdigest(),
            "signature-timestamp": server_time_formatted,
            "key": self.server_key
        }

    def create_user(self, username, birth_date, region="BE"):
        response = self.session.post(
            self.api_url + "users/create_user",
            headers=self.authorization_headers,
            data={
                "username": username,
                "region": region,
                "birth_date": birth_date,
                "character_info": None
            }
        )
        print(response.text)
        print(response.json)

    def authorize(self):
        headers = api.create_headers()
        response = self.session.get(
            self.api_url + "auth/register",
            headers=headers
        )

        if response.status_code == 200:
            self.authorization_headers["switch_authorization"] = response.headers["switch_authorization"]
            self.authorization_headers.update(headers)
            print(self.authorization_headers)
            return response.headers["switch_authorization"]
        else:
            return False


if __name__ == '__main__':
    api = VRTSwitchAPI()
    api.authorize()
    api.create_user("test5439", "06051995")
