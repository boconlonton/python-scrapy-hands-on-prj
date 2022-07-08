import base64
import json

import scrapy
from scrapy import Spider

_COMPANY_LIST = ['6306682', '6306706', '6306707',
                 '6306708', '167267', '154407',
                 '128171', '128176', '128180',
                 '128178', '291702', '226530',
                 '158776', '128177', '137265',
                 '128191', '137264', '128192',
                 '163467', '128190', '128189',
                 '128188', '169642', '128185',
                 '128186', '128184', '128182',
                 '167266', '128181', '128179',
                 '128174', '128175', '128173',
                 '128172', '128169', '128168',
                 '229282', '128167', '128166',
                 '128170']


class CompassGroupSpider(Spider):
    name = "compass_group_spider"

    USERNAME = 'oliviaapi'
    PASSWORD = 'RKXGaKXUPVf74h^+'
    SFSF_COMPANY_ID = "CGNA"

    def _prepare_query(self, brand_id: int):
        filter_list = [
            f'filter11/id eq {brand_id}',
            'deleted eq 0',
            "internalStatus eq 'Approved'",
            "jobReqPostings/boardId eq '_external'",
            "status/externalCode eq 'reqStatus_Open'",
            "(jobReqPostings/postingStatus eq 'Success' or jobReqPostings/postingStatus eq 'Updated')",
            "(legalEntity_obj/externalCode eq 'CGUSA' or filter3/id eq '4066')"
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
        return (f"https://api8.successfactors.com/odata/v2/JobRequisition?"
                f"{self._build_query_string(brand_id)}")

    def _build_headers(self):
        auth = base64.b64encode(f"{self.USERNAME}@{self.SFSF_COMPANY_ID}:{self.PASSWORD}".encode("ASCII"))
        self.logger.info(auth.decode("utf-8"))
        return {
            'Authorization': f'Basic {auth.decode("utf-8")}'
        }

    def start_requests(self):
        for brand_id in _COMPANY_LIST:
            yield scrapy.Request(url=self._build_url(brand_id),
                                 headers=self._build_headers())

    def parse(self, response, *args, **kwargs) -> None:
        data = json.loads(response.text)
        if data.get('d'):
            jobs = data['d'].get('results')
            for job in jobs:
                description = [
                    job['jobReqLocale']['results'][0]['extJobDescHeader'],
                    job['jobReqLocale']['results'][0]['externalJobDescription'],
                    job['jobReqLocale']['results'][0]['extJobDescFooter']
                ]
                concat_description = "".join(description)
                if "XXX" in concat_description:
                    yield {
                        'rid': job.get('jobReqId'),
                        'description': concat_description,
                        'extJobDescHeader': job['jobReqLocale']['results'][0]['extJobDescHeader'],
                        'original_data': job
                    }
            next_url = data['d'].get('__next')
            if next_url:
                yield scrapy.Request(url=next_url,
                                     headers=self._build_headers())
        return
