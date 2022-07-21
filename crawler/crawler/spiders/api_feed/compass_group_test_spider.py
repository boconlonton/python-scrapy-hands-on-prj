import base64
import json

import scrapy
from scrapy import Spider

_COMPANY_LIST = ['3949681', '3949609', '3949616',
                 '3949624', '3949625', '187531',
                 '119707', '110213', '116707',
                 '121974', '110223', '119667',
                 '110236', '110227', '110234',
                 '110220', '110244', '114514',
                 '110243', '110211', '110228',
                 '110239', '110233', '110237',
                 '188238', '121975', '110235',
                 '110222', '116007', '119827',
                 '126807', '110231', '121907',
                 '110224', '110210', '126246',
                 '110217', '110221', '110230',
                 '110242', '119407', '110240',
                 '110216', '119347', '110240'
                 ]


class CompassGroupSpider(Spider):
    name = "compass_group_test_spider"

    USERNAME = 'oliviaapi_scr'
    PASSWORD = 'compass_scr456!'
    SFSF_COMPANY_ID = "CGNAtest"

    def _prepare_query(self, brand_id: int):
        filter_list = [
            f"filter11%2fid+eq+%27{brand_id}%27+and+deleted+eq+0+and"
            f"+internalStatus+eq+%27Approved%27+and+jobReqPostings%2fboardId"
            f"+eq+%27_external%27+and+status%2fexternalCode+eq"
            f"+%27reqStatus_Open%27+and+("
            f"jobReqPostings%2fpostingStatus+eq+%27Success%27+or"
            f"+jobReqPostings%2fpostingStatus+eq+%27Updated%27)+and+("
            f"legalEntity_obj%2fexternalCode+eq+%27CGUSA%27+or+filter3%2fid"
            f"+eq+%274066%27) "
        ]

        expand_list = [
            "mfield1",
            "hiringManager",
            "recruiter",
            "filter3",
            "filter2",
            "filter2/picklistLabels",
            "filter1",
            "filter1/picklistLabels",
            "filter11",
            "filter10",
            "jobReqLocale",
            "custFlsa",
            "req_classification",
            "custFlsa/picklistLabels",
            "req_classification/picklistLabels",
            "hiringManagerTeam"
        ]

        select_list = [
            "hiringManager/email",
            "recruiter",
            "jobReqId",
            "appTemplateId",
            "req_streetAddress",
            "mfield1/id",
            "filter11/id",
            "filter10/id",
            "filter2/picklistLabels/label",
            "filter1/picklistLabels/label",
            "city",
            "deleted",
            "country",
            "internalStatus",
            "jobReqLocale/externalTitle",
            "jobReqLocale/externalJobDescription",
            "jobReqLocale/extJobDescFooter",
            "jobReqLocale/extJobDescHeader",
            "postalcode",
            "jobClassTitle",
            "custFlsa/picklistLabels/label",
            "req_classification/picklistLabels/label",
            "Cust_clntAcName",
            "hiringManagerTeam/email"
        ]

        return {
            '$format': 'json',
            '$filter': " and ".join(filter_list),
            '$expand': ",".join(expand_list),
            '$select': ",".join(select_list)
        }

    def _build_query_string(self, brand_id):
        query = self._prepare_query(brand_id)
        return '&'.join(
            [f'{k}={v}' for k, v in query.items()]
        )

    def _build_url(self, brand_id):
        return (f"https://api8preview.sapsf.com/odata/v2/JobRequisition?"
                f"{self._build_query_string(brand_id)}")

    def _build_headers(self):
        auth = base64.b64encode(f"{self.USERNAME}@{self.SFSF_COMPANY_ID}"
                                f":{self.PASSWORD}".encode("ASCII"))
        self.logger.info(auth.decode("utf-8"))
        return {
            'Authorization': f'Basic {auth.decode("utf-8")}'
        }

    def start_requests(self):
        for brand_id in _COMPANY_LIST:
            yield scrapy.Request(url=self._build_url(brand_id),
                                 headers=self._build_headers())

    def parse(self, response, *args, **kwargs) -> None:
        self.logger.info(response)
        data = json.loads(response.text)
        if data.get('d'):
            jobs = data['d'].get('results')
            for job in jobs:
                hiring_manager = job.get('hiringManagerTeam')['results']
                if hiring_manager:
                    yield {
                        'hiring': hiring_manager
                    }
            next_url = data['d'].get('__next')
            if next_url:
                yield scrapy.Request(url=next_url,
                                     headers=self._build_headers())
        return
