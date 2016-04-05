import requests, re, json
from bs4 import BeautifulSoup

def extractHiddenFields(formParmas, soup):
    for inputType in soup.find_all('input'):
        formParams[inputType.get('name')] = inputType.get('value')
    return formParams

def setDefaultFormFields(formParams):
    formParams['RdlSearch'] = 0
    formParams['__EVENTARGUMENT'] = ''
    formParams['__EVENTTARGET'] = 'ddlDistricts'
    formParams['__LASTFOCUS'] = ''

    # District Code of Faizabad
    formParams['ddlDistricts'] = 67
    return formParams

# Get the inital page
response = requests.get("http://164.100.180.4/searchengine/SearchEngineEnglish.aspx")
soup = BeautifulSoup(response.text, 'lxml')

# Prepare for inital Post Request to get the form which will contain the input field to enter EPIC No
formParams = {}
formParams = extractHiddenFields(formParams, soup)
formParams = setDefaultFormFields(formParams)

# Get the page to enter EPIC No
selectedDistrictForm = requests.post('http://164.100.180.4/searchengine/SearchEngineEnglish.aspx', data = formParams)
selectedDistrictSoup = BeautifulSoup(selectedDistrictForm.text, 'lxml')

# Check if previous request was successful or not
if len(selectedDistrictSoup.body.findAll(text=re.compile('EPIC'))) > 0:
    # Yo, first request was a success
    pass
else:
    # error quit the program
    pass

# Prepare for final request to get the required information
finalFormParams = {}
finalFormParams = extractHiddenFields(finalFormParams, selectedDistrictSoup)
finalFormParams =  setDefaultFormFields(finalFormParams)
finalFormParams['txtEPICNo'] = 'ANB1882687'
finalFormParams['RdlSearchBy'] = 0
getVoterDetails = requests.post('http://164.100.180.4/searchengine/SearchEngineEnglish.aspx', data = finalFormParams)
finalDetailsSoup = BeautifulSoup(getVoterDetails.text, 'lxml')

dateTable = finalDetailsSoup.findChildren('table', {'id': 'gvSearchResult'})[0]
dataRow = dateTable.findChildren(['tr'])[1]

dataCell = dataRow.findChildren('td')
for cell in dataCell:
    value = cell.string
    print "The value in this cell is %s" % value

# Save it to csv