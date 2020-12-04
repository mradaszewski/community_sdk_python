from typing import Optional, List

from kentik_api.api_calls import labels
from kentik_api.public.query import KentikQuery
from kentik_api.public.device_label import DeviceLabel
from kentik_api.requests_payload import labels_payload

class DeviceLabelsAPI:
    """ Exposes Kentik API operations related to device labels """

    def __init__(self, query: KentikQuery) -> None:
        self._query = query

    def get_all(self) -> List[DeviceLabel]:
        apicall = labels.get_labels()
        response = self._query.send(apicall)
        return labels_payload.GetAllResponse.from_json(response.text).to_device_labels()

    def get(self, label_id : int) -> DeviceLabel:
        apicall = labels.get_label_info(label_id)
        response = self._query.send(apicall)
        return labels_payload.GetResponse.from_json(response.text).to_device_label()

    def create(self, device: DeviceLabel) -> DeviceLabel:
        apicall = labels.create_label()
        payload = labels_payload.CreateRequest(device.name, device.color).__dict__
        response = self._query.send(apicall, payload)
        return labels_payload.CreateResponse.from_json(response.text).to_device_label()

    def update(self, label_id: int, device: DeviceLabel) -> DeviceLabel:
        apicall = labels.update_label(label_id)
        payload = labels_payload.UpdateRequest(device.name, device.color).__dict__
        response = self._query.send(apicall, payload)
        return labels_payload.UpdateResponse.from_json(response.text).to_device_label()

    def delete(self, label_id: int) -> bool:
        apicall = labels.delete_label(label_id)
        response = self._query.send(apicall)
        return labels_payload.DeleteResponse.from_json(response.text).success
