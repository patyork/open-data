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
		   'srchsort' : '1', # Sort by Parcel num by default (1:Parcel, ??
		   'srchdist1' : 'All', # District (All, 1.0, 2.0, 3.0); Also appears in results
		   'CGIOption' : 'Search'
	    }

	def search(self, queryParams):
	    try:
		   tmp = r.post(self.endpointSearch,
		                dict(queryParams, **self.dataSearch),
		                headers=self.headersSearch)
	    except r.ConnectionError:
		   print r.ConnectionError
	    
	    soup = BeautifulSoup(tmp.content, 'html.parser')
	    results = []
	    for table in soup.find_all('table'):
		   if 'Search' in table.get_text() and 'Results' in table.get_text():
		       #print table
		       for tr in table.find_all('tr')[2:-1]:
		           cols = tr.find_all('td')
		           
		           results.append( {
		               'parcelNum' : cols[0].string,
		               'ownerName' : cols[1].string,
		               'location' : cols[2].string,
		               'district' : cols[3].string,
		               'useCode' : cols[4].string,
		               'acreage' : cols[5].string,
		               'netValue' : cols[6].string
		           })
	    return results
		   
