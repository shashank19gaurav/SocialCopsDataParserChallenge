import re
epicNoList=[]
with open('output.txt', 'r') as myfile:
    data=myfile.read()
    epicNoList = re.findall(r'ANB[0-9]{7}', data)
    epicNoList = epicNoList + re.findall(r'GLT[0-9]{7}', data)
    epicNoList = epicNoList + re.findall(r'UP/[0-9]{2}/[0-9]{3}/[0-9]{7}', data)

print "Size of the list :", len(epicNoList)
print "Writing Epic Numbers to the file"
mylist = epicNoList
with open('epicNoList.txt','w') as epicNoListfile:
    epicNoListfile.write( ','.join( mylist ) )