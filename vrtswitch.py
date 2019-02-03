import datetime
import requests
import hashlib


class VRTSwitchAPI(object):
    def __init__(self, version=3.3, server_key="13bc22628889ac02d14858a873af5e09"):
        self.version = str(version)
        self.server_key = server_key

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

    def authorization_token(self):
        response = requests.get(
            "https://switchserver.triangle-factory.be/api-" + self.version + "/auth/register",
            headers=api.create_headers()
        )

        if response.status_code == 200:
            return response.headers["switch_authorization"]
        else:
            return False


if __name__ == '__main__':
    api = VRTSwitchAPI()
    print(api.authorization_token())
