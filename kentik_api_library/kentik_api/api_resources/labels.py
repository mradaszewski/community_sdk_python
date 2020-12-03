from typing import Optional

from kentik_api.api_calls import labels
from kentik_api.api_resources.query import KentikQuery
from kentik_api.requests_payload import labels_payload

class Labels:
    """ Exposes Kentik API operations related to device labels """

    def __init__(self, query: KentikQuery) :
        self._query = query

    def get_all(self) -> labels_payload.GetAllResponse:
        apicall = labels.get_labels()
        response = self._query.send(apicall)
        return labels_payload.GetAllResponse.from_json(response.text)

    def get(self, label_id : int) -> labels_payload.GetResponse:
        apicall = labels.get_label_info(label_id)
        response = self._query.send(apicall)
        return labels_payload.GetResponse.from_json(response.text)

    def create(self, name: str, color: str) -> labels_payload.CreateResponse:
        apicall = labels.create_label()
        payload = labels_payload.CreateRequest(name, color).__dict__
        response = self._query.send(apicall, payload)
        return labels_payload.CreateResponse.from_json(response.text)

    def update(self, label_id: int, name: str, color: Optional[str] = None) -> labels_payload.UpdateResponse:
        apicall = labels.update_label(label_id)
        payload = labels_payload.UpdateRequest(name, color).__dict__
        response = self._query.send(apicall, payload)
        return labels_payload.UpdateResponse.from_json(response.text)

    def delete(self, label_id: int) -> labels_payload.DeleteResponse:
        apicall = labels.delete_label(label_id)
        response = self._query.send(apicall)
        return labels_payload.DeleteResponse.from_json(response.text)
