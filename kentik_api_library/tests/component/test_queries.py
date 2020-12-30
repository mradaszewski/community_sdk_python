from http import HTTPStatus

from kentik_api.api_resources.query_api import QueryAPI
from kentik_api.api_calls.api_call import APICallMethods
from kentik_api.public.saved_filter import Filters, FilterGroups, Filter
from kentik_api.public.query_object import (
    QueryObject,
    QueryArrayItem,
    Query,
    ImageType,
    Aggregate,
    AggregateFunctionType,
    FastDataType,
    MetricType,
    DimensionType,
    ChartViewType,
    TimeFormat,
)
from tests.component.stub_api_connector import StubAPIConnector


def test_query_data_success() -> None:
    # given
    query_response_payload = """
    {
        "results": [
            {
                "bucket": "Left +Y Axis",
                "data": [
                    {
                        "key": "Total",
                        "avg_bits_per_sec": 19738.220765027323,
                        "p95th_bits_per_sec": 22745.466666666667,
                        "max_bits_per_sec": 25902.533333333333,
                        "name": "Total",
                        "timeSeries": {
                            "both_bits_per_sec": {
                                "flow": [
                                    [
                                        1608538980000,
                                        20751.333333333332,
                                        60
                                    ],
                                    [
                                        1608539040000,
                                        16364.133333333333,
                                        60
                                    ],
                                    [
                                        1608539100000,
                                        19316.933333333334,
                                        60
                                    ]
                                ]
                            }
                        }
                    }
                ]
            }
        ]
    }"""
    connector = StubAPIConnector(query_response_payload, HTTPStatus.OK)
    query_api = QueryAPI(connector)

    # when
    agg1 = Aggregate(name="avg_bits_per_sec", column="f_sum_both_bytes", fn=AggregateFunctionType.average, raw=True)
    agg2 = Aggregate(name="p95th_bits_per_sec", column="f_sum_both_bytes", fn=AggregateFunctionType.percentile, rank=95)
    agg3 = Aggregate(name="max_bits_per_sec", column="f_sum_both_bytes", fn=AggregateFunctionType.max)
    query = Query(
        dimension=[DimensionType.Traffic],
        cidr=32,
        cidr6=128,
        metric=MetricType.bytes,
        topx=8,
        depth=75,
        fastData=FastDataType.auto,
        outsort="avg_bits_per_sec",
        lookback_seconds=3600,
        hostname_lookup=True,
        all_selected=True,
        aggregates=[agg1, agg2, agg3],
    )
    query_item = QueryArrayItem(query=query, bucket="Left +Y Axis")
    query_object = QueryObject(queries=[query_item])
    result = query_api.data(query_object)

    # then request properly formed
    assert connector.last_url == "/query/topXdata"
    assert connector.last_method == APICallMethods.POST
    assert connector.last_payload is not None
    assert len(connector.last_payload["queries"]) == 1
    assert connector.last_payload["queries"][0]["bucket"] == "Left +Y Axis"
    query0 = connector.last_payload["queries"][0]["query"]
    assert len(query0["dimension"]) == 1
    assert query0["dimension"][0] == "Traffic"
    assert query0["cidr"] == 32
    assert query0["cidr6"] == 128
    assert query0["metric"] == "bytes"
    assert query0["topx"] == 8
    assert query0["depth"] == 75
    assert query0["fastData"] == "Auto"
    assert query0["outsort"] == "avg_bits_per_sec"
    assert query0["lookback_seconds"] == 3600
    assert query0["hostname_lookup"] == True
    assert query0["device_name"] == []
    assert query0["all_selected"] == True
    assert query0["descriptor"] == ""
    assert len(query0["aggregates"]) == 3
    assert query0["aggregates"][0]["name"] == "avg_bits_per_sec"
    assert query0["aggregates"][0]["column"] == "f_sum_both_bytes"
    assert query0["aggregates"][0]["fn"] == "average"
    assert query0["aggregates"][0]["raw"] == True
    assert query0["aggregates"][1]["name"] == "p95th_bits_per_sec"
    assert query0["aggregates"][1]["column"] == "f_sum_both_bytes"
    assert query0["aggregates"][1]["fn"] == "percentile"
    assert query0["aggregates"][1]["rank"] == 95
    assert query0["aggregates"][2]["name"] == "max_bits_per_sec"
    assert query0["aggregates"][2]["column"] == "f_sum_both_bytes"
    assert query0["aggregates"][2]["fn"] == "max"

    # and response properly parsed
    assert len(result.results) == 1
    assert result.results[0]["bucket"] == "Left +Y Axis"
    assert result.results[0]["data"] is not None


def test_query_chart_success() -> None:
    # given
    query_response_payload = """{"dataUri": "data:image/png;base64,ImageDataEncodedBase64"}"""
    connector = StubAPIConnector(query_response_payload, HTTPStatus.OK)
    query_api = QueryAPI(connector)

    # when
    agg1 = Aggregate(name="avg_bits_per_sec", column="f_sum_both_bytes", fn=AggregateFunctionType.average, raw=True)
    agg2 = Aggregate(name="p95th_bits_per_sec", column="f_sum_both_bytes", fn=AggregateFunctionType.percentile, rank=95)
    agg3 = Aggregate(name="max_bits_per_sec", column="f_sum_both_bytes", fn=AggregateFunctionType.max)
    filter_ = Filter(filterField="dst_as", operator="=", filterValue="")
    filter_group = FilterGroups(connector="All", not_=False, filters=[filter_])
    filters = Filters(connector="", filterGroups=[filter_group])
    query = Query(
        viz_type=ChartViewType.stackedArea,
        show_overlay=False,
        overlay_day=-7,
        sync_axes=False,
        query_title="title",
        dimension=[DimensionType.Traffic],
        cidr=32,
        cidr6=128,
        metric=MetricType.bytes,
        topx=8,
        depth=75,
        fastData=FastDataType.auto,
        outsort="avg_bits_per_sec",
        lookback_seconds=0,
        starting_time="2020-10-20 10:15:00",
        ending_time="2020-10-21 10:15:00",
        hostname_lookup=False,
        device_name=["dev1", "dev2"],
        all_selected=False,
        filters_obj=filters,
        saved_filters=[],
        matrixBy=[DimensionType.src_geo_city.value, DimensionType.dst_geo_city.value],
        pps_threshold=1,
        time_format=TimeFormat.local,
        descriptor="descriptor",
        aggregates=[agg1, agg2, agg3],
    )
    query_item = QueryArrayItem(query=query, bucket="Left +Y Axis", isOverlay=False)
    query_object = QueryObject(queries=[query_item], imageType=ImageType.png)
    result = query_api.chart(query_object)

    # then request properly formed
    assert connector.last_url == "/query/topXchart"
    assert connector.last_method == APICallMethods.POST
    assert connector.last_payload is not None
    assert len(connector.last_payload["queries"]) == 1
    assert connector.last_payload["queries"][0]["bucket"] == "Left +Y Axis"
    query0 = connector.last_payload["queries"][0]["query"]
    assert query0["viz_type"] == "stackedArea"
    assert query0["show_overlay"] == False
    assert query0["overlay_day"] == -7
    assert query0["sync_axes"] == False
    assert query0["query_title"] == "title"
    assert len(query0["dimension"]) == 1
    assert query0["dimension"][0] == "Traffic"
    assert query0["cidr"] == 32
    assert query0["cidr6"] == 128
    assert query0["metric"] == "bytes"
    assert query0["topx"] == 8
    assert query0["depth"] == 75
    assert query0["fastData"] == "Auto"
    assert query0["outsort"] == "avg_bits_per_sec"
    assert query0["lookback_seconds"] == 0
    assert query0["starting_time"] == "2020-10-20 10:15:00"
    assert query0["ending_time"] == "2020-10-21 10:15:00"
    assert query0["hostname_lookup"] == False
    assert query0["device_name"] == ["dev1", "dev2"]
    assert query0["all_selected"] == False
    assert len(query0["filters_obj"]["filterGroups"]) == 1
    assert query0["filters_obj"]["filterGroups"][0]["connector"] == "All"
    # assert query0["filters_obj"]["filterGroups"][0]["not"] == False # TODO: uncomment once FilterGroups marshaling "not" as "not_" is fixed
    assert len(query0["filters_obj"]["filterGroups"][0]["filters"]) == 1
    assert query0["filters_obj"]["filterGroups"][0]["filters"][0]["filterField"] == "dst_as"
    assert query0["filters_obj"]["filterGroups"][0]["filters"][0]["operator"] == "="
    assert query0["filters_obj"]["filterGroups"][0]["filters"][0]["filterValue"] == ""
    assert query0["saved_filters"] == []
    assert query0["matrixBy"] == ["src_geo_city", "dst_geo_city"]
    assert query0["pps_threshold"] == 1
    assert query0["time_format"] == "Local"
    assert query0["descriptor"] == "descriptor"
    assert len(query0["aggregates"]) == 3
    assert query0["aggregates"][0]["name"] == "avg_bits_per_sec"
    assert query0["aggregates"][0]["column"] == "f_sum_both_bytes"
    assert query0["aggregates"][0]["fn"] == "average"
    assert query0["aggregates"][0]["raw"] == True
    assert query0["aggregates"][1]["name"] == "p95th_bits_per_sec"
    assert query0["aggregates"][1]["column"] == "f_sum_both_bytes"
    assert query0["aggregates"][1]["fn"] == "percentile"
    assert query0["aggregates"][1]["rank"] == 95
    assert query0["aggregates"][2]["name"] == "max_bits_per_sec"
    assert query0["aggregates"][2]["column"] == "f_sum_both_bytes"
    assert query0["aggregates"][2]["fn"] == "max"

    # and response properly parsed
    assert result.image_type == ImageType.png
    assert result.image_data_base64 == "ImageDataEncodedBase64"