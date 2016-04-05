import requests, re, json, re, time
import unicodecsv as csv
from multiprocessing.pool import ThreadPool as Pool
from bs4 import BeautifulSoup

# Default Values
start_time = time.time()
iterator = 1
notFoundCount = 0
headerList = ['AC No', 'Part No', 'Section No', 'Serial No', 'First Name', 'Name (Hindi)', 'Father/ Husband\'s Name', 'Father/ Husband\'s Name (Hindi)', 'Age', 'Gender', 'EPIC No']

'''
    This function extracts the hidden input fields injected by ASP.net
'''
def extractHiddenFields(formParmas, soup):
    for inputType in soup.find_all('input'):
        formParams[inputType.get('name')] = inputType.get('value')
    return formParams

'''
    This function sets extra form fields required for ASP form submissions
'''
def setDefaultFormFields(formParams):
    formParams['RdlSearch'] = 0
    formParams['__EVENTARGUMENT'] = ''
    formParams['__EVENTTARGET'] = 'ddlDistricts'
    formParams['__LASTFOCUS'] = ''
    # District Code of Faizabad
    formParams['ddlDistricts'] = 67
    return formParams

def parseData(epicNo):
    global iterator, formParams, headerList, notFoundCount
    print "Finding data for Epic No", epicNo
    response = requests.get("http://164.100.180.4/searchengine/SearchEngineEnglish.aspx")
    soup = BeautifulSoup(response.text, 'lxml')

    # Prepare for inital Post Request to get the form which will contain the input field to enter EPIC No
    formParams = {}
    formParams = extractHiddenFields(formParams, soup)
    formParams = setDefaultFormFields(formParams)

    # Get the page to enter EPIC No
    selectedDistrictForm = requests.post('http://164.100.180.4/searchengine/SearchEngineEnglish.aspx', data = formParams)
    selectedDistrictSoup = BeautifulSoup(selectedDistrictForm.text, 'lxml')

    # Prepare for final request to get the required information
    finalFormParams = {}
    finalFormParams = extractHiddenFields(finalFormParams, selectedDistrictSoup)
    finalFormParams =  setDefaultFormFields(finalFormParams)
    finalFormParams['txtEPICNo'] = epicNo
    finalFormParams['RdlSearchBy'] = 0
    getVoterDetails = requests.post('http://164.100.180.4/searchengine/SearchEngineEnglish.aspx', data = finalFormParams)
    finalDetailsSoup = BeautifulSoup(getVoterDetails.text, 'lxml')

    with open('data.csv', 'a') as csvWriterFile:
        csvWriter = csv.writer(csvWriterFile)

        if(len(finalDetailsSoup.findChildren('table', {'id': 'gvSearchResult'}))) > 0:
            dateTable = finalDetailsSoup.findChildren('table', {'id': 'gvSearchResult'})[0]
            dataRow = dateTable.findChildren(['tr'])[1]
            dataCell = dataRow.findChildren('td')

            dataList = []
            dataCell.pop(0)
            for cell in dataCell:
                value = "" + cell.string 
                dataList.append(cell.string)
            print dataList
            csvWriter.writerow(dataList)
        else:
                 notFoundCount += 0
                 notFound   = ["Not Found"] * 10
                 notFound.append(epicNo)
                 csvWriter.writerow(notFound)

with open("epicNoList.txt", "r") as filestream:
    for line in filestream:
        epicNoList = line.split(",")

pool_size = 8
pool = Pool(pool_size)

with open('data.csv', 'w') as csvHeaderWriterFile:
        csvHeaderWriter = csv.writer(csvHeaderWriterFile)
        csvHeaderWriter.writerow(headerList)

for epicNo in epicNoList:
    pool.apply_async(parseData, (epicNo,))
        # parseData(epicNo)

print("--- %s seconds ---" % round(time.time() - start_time, 2))
print "Accuracy :", 100 * float(notFoundCount)/float(len(epicNoList))
pool.close()
pool.join()

