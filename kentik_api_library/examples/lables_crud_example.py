# pylint: disable=redefined-outer-name
"""
Examples of using the typed labels API
"""

import os
import sys
import logging
from typing import Tuple
from kentik_api import kentik_api


logging.basicConfig(level=logging.INFO)


def get_auth_email_token() -> Tuple[str, str]:
    try:
        email = os.environ['KTAPI_AUTH_EMAIL']
        token = os.environ['KTAPI_AUTH_TOKEN']
        return email, token
    except KeyError:
        print('You have to specify KTAPI_AUTH_EMAIL and KTAPI_AUTH_TOKEN first')
        sys.exit(1)

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
    client = kentik_api.for_com_domain(email, token)

    print("### CREATE")
    created = client.labels.create("apitest-label-1", "#0000FF")
    print(created)
    print()

    print("### UPDATE")
    updated = client.labels.update(created.id, "apitest-label-one")
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
