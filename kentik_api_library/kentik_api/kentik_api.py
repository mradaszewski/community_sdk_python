# Local application imports
from kentik_api.public.query import KentikQuery
from kentik_api.api_resources.device_labels_api import DeviceLabelsAPI


class KentikAPI:
    """ Root object for operating KentikAPI """

    API_VERSION = "v5"

    def __init__(self, query: KentikQuery) -> None:
        self.labels = DeviceLabelsAPI(query)
        # self.devices =
        # self.users =
        # self.tags =
        # ...

    @classmethod
    def from_url_email_token(cls, api_url: str, auth_email: str, auth_token: str):
        versioned_api_url = api_url + "/" + KentikAPI.API_VERSION
        query = KentikQuery(versioned_api_url, auth_email, auth_token)
        return cls(query)


def for_com_domain(auth_email: str, auth_token: str) -> KentikAPI:
    """ Handy kentik api client constructor for COM domain """
    return KentikAPI.from_url_email_token(KentikQuery.BASE_API_COM_URL, auth_email, auth_token)

def for_eu_domain(auth_email: str, auth_token: str) -> KentikAPI:
    """ Handy kentik api client constructor for EU domain """
    return KentikAPI.from_url_email_token(KentikQuery.BASE_API_EU_URL, auth_email, auth_token)