# pylint: disable=redefined-outer-name
"""
Examples of using the typed labels API
"""

import os
import sys
import json
import logging
from typing import Tuple
from requests import Response
from kentik_api.api_calls import labels
from kentik_api.client import API, BASE_API_COM_URL
from kentik_api.requests_payload import labels_payload


class APIClient():

    # @MM: for testing requests with: nc -l -p 9999
    # URL_V5 : str = "http://localhost:9999/v5"

    URL_V5 : str = BASE_API_COM_URL + "/v5"

    class Labels:
        def __init__(self, api: API) :
            self._api = api 
            # @MM: for testing requests
            # logging.basicConfig(level=logging.DEBUG)

        def get_all(self) -> labels_payload.GetAllResponse:
            apicall = labels.get_labels()
            response = self._api.send_query(apicall)   
            return labels_payload.GetAllResponse.from_json(response.text)     

        def get(self, label_id : int) -> labels_payload.GetResponse:
            apicall = labels.get_label_info(label_id)
            response = self._api.send_query(apicall)
            return labels_payload.GetResponse.from_json(response.text) # add http error handling here

        # Dedicated response type here
        def create(self, name: str, color: str) -> labels_payload.CreateResponse:
            apicall = labels.create_label()
            payload = labels_payload.CreateRequest(name, color).__dict__
            response = self._api.send_query(apicall, payload)
            return labels_payload.CreateResponse.from_json(response.text) # add http error handling here

        # Dedicated response type here
        def update(self, label_id: int, name: str, color: str) -> labels_payload.UpdateResponse:
            apicall = labels.update_label(label_id)
            payload = labels_payload.UpdateRequest(name, color).__dict__
            response = self._api.send_query(apicall, payload)
            return labels_payload.UpdateResponse.from_json(response.text) # add http error handling here

        def delete(self, label_id: int) -> labels_payload.DeleteResponse:
            apicall = labels.delete_label(label_id)
            response = self._api.send_query(apicall)
            return labels_payload.DeleteResponse.from_json(response.text) # add http error handling here

    def __init__(self, email: str, token: str):
        api = API(APIClient.URL_V5, email, token)
        self.labels = APIClient.Labels(api)




def get_auth_email_token() -> Tuple[str, str]:
    try:
        email = os.environ['KTAPI_AUTH_EMAIL']
        token = os.environ['KTAPI_AUTH_TOKEN']
        return email, token
    except KeyError:
        print('You have to specify KTAPI_AUTH_EMAIL and KTAPI_AUTH_TOKEN first')
        sys.exit(1)

def pretty_print_response(response: Response) -> None:
    print(response.status_code)
    if response.status_code == 200:
        json_object = json.loads(response.text)
        print(json.dumps(json_object, indent=2))
    else:
        print(response.text)

def run_crud():
    """
    Expected response is like:

    ### CREATE
    CreateResponse(id=2794, name='apitest-label-1', color='#0000FF', user_id='144319', company_id='74333', devices=[], created_date='2020-12-02T14:39:46.686Z', updated_date='2020-12-02T14:39:46.686Z')

    ### UPDATE
    UpdateResponse(id=2794, name='apitest-label-one', color='#FF0000', user_id='144319', company_id='74333', devices=[], created_date='2020-12-02T14:39:46.686Z', updated_date='2020-12-02T14:39:46.686Z')

    ### GET
    GetResponse(id=2794, name='apitest-label-one', color='#FF0000', user_id='144319', company_id='74333', devices=[], created_date='2020-12-02T14:39:46.686Z', updated_date='2020-12-02T14:39:46.686Z')

    ### DELETE
    DeleteResponse(success=True)
    """


    email, token = get_auth_email_token()
    client = APIClient(email, token)


    print("### CREATE")
    created = client.labels.create("apitest-label-1", "#0000FF")
    print(created)
    print()

    print("### UPDATE")
    updated = client.labels.update(created.id, "apitest-label-one", "#FF0000")
    print(updated)
    print()

    print("### GET")
    got = client.labels.get(created.id)
    print(got)
    print()

    print("### DELETE")
    deleted = client.labels.delete(created.id)
    print(deleted)


if __name__ == "__main__":
    run_crud()
