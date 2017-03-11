import requests as r
from bs4 import BeautifulSoup


class assessor:
    endpointSearch = 'http://www.hcnv.us:1401/cgi-bin/asw100'
    headersSearch = {
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
        'Origin': 'http://www.hcnv.us:1401',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Referer': 'http://www.hcnv.us:1401/cgi-bin/asw100',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'en-US,en;q=0.8'
    }
    dataSearch = {
        'srchsort': '1',  # Sort by Parcel num by default (1:Parcel, ??
        'srchdist1': 'All',  # District (All, 1.0, 2.0, 3.0); Also appears in results
        'CGIOption': 'Search',
        'srchluc1': '',  # Land-Use-Code Start
        'srchluc2': '',  # Land-Use-Code End
        'srchluci1': '',  # Specific LUC #1
        'srchluci2': '',  # Specific LUC #2
        'srchluci3': '',  # Specific LUC #3
        'srchluci4': '',  # Specific LUC #4
        'srchacr1': '',  # Acreage Minimum
        'srchacr2': '',  # Acreage Maximum
        'srchval1': '',  # Net Assessed Value min
        'srchval2': '',  # Net Assessed Value max

        'srchpar1': '',  # Parcel number start
        'srchpar2': '',  # Parcel number end; inclusive
        'srchname': '',  # Partial Owner Name
        'srchlocn': '',  # Partial Location
        'srchaorl': 'A'  # Name Type, Assesed or Legal (A:Assesed, L:Legal)
    }

    def search(self, queryParams):

        # Map 'nicer' names to the required names
        cleanQueryParams = {}
        cleanQueryParams['srchpar1'] = queryParams['parcelNum']
        cleanQueryParams['srchpar2'] = queryParams['parcelNumRange']
        cleanQueryParams['srchname'] = queryParams['ownerName']
        cleanQueryParams['srchlocn'] = queryParams['location']

        try:
            return self._getResultTable(cleanQueryParams)
        except r.ConnectionError as e:
            raise e
        except r.Timeout as e:
            raise e

    def _getResultTable(self, cleanQueryParams, pageStart=0):
        try:
            tmp = r.post(self.endpointSearch,
                         dict(self.dataSearch.items() + [(k, v) for k, v in cleanQueryParams.items() if v is not None]),
                         headers=self.headersSearch,
                         timeout=10.0)

            soup = BeautifulSoup(tmp.content, 'html.parser')
            results = []
            for table in soup.find_all('table'):
                if 'Search' in table.get_text() and 'Results' in table.get_text():
                    # print table
                    for tr in table.find_all('tr')[2:-1]:
                        cols = tr.find_all('td')

                        results.append({
                            'county': '1',  # Humboldt
                            'parcelNum': cols[0].string,
                            'ownerName': cols[1].string,
                            'location': cols[2].string,
                            'district': cols[3].string,
                            'useCode': cols[4].string,
                            'acreage': cols[5].string,
                            'netValue': cols[6].string
                        })
            if results[0]['ownerName'] == '*** No results found ***':
                return []
            return results

        except r.ConnectionError as e:
            raise e
        except r.Timeout as e:
            raise e

