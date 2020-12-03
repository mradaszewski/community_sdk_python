# Local application imports
from kentik_api.api_resources.labels import Labels
from kentik_api.api_resources.query import KentikQuery


class KentikApi:
    """ Root object for operating KentikAPI """

    API_VERSION = "v5"

    def __init__(self, api_url: str, auth_email: str, auth_token: str):
        versioned_api_url = api_url + "/" + KentikApi.API_VERSION
        query = KentikQuery(versioned_api_url, auth_email, auth_token)

        self.labels = Labels(query)
        # self.devices =
        # self.users =
        # self.tags =
        # ...


def for_com_domain(auth_email: str, auth_token: str) -> KentikApi:
    """ Handy kentik api client constructor for COM domain """
    return KentikApi(KentikQuery.BASE_API_COM_URL, auth_email, auth_token)

def for_eu_domain(auth_email: str, auth_token: str) -> KentikApi:
    """ Handy kentik api client constructor for EU domain """
    return KentikApi(KentikQuery.BASE_API_EU_URL, auth_email, auth_token)