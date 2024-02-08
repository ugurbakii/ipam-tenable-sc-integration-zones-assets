import requests
import json
import csv
import os
from datetime import date
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

os.environ['REQUESTS_CA_BUNDLE'] = os.path.join(
    '/etc/ssl/certs/',
    '/usr/local/share/ca-certificates')
def userToken():

	url = "https://ipam.domain.com/api/?app_id=app&controller=user"

	payload  = {}
	headers = {
	  'Content-Type': 'application/json',
	  'Authorization': 'Basic xxx='
	}

	response = requests.request("POST", url, headers=headers, data = payload, verify=False)
	j = response.json()
	i=json.dumps(j)
	response_data = json.loads(i)
	my_data=response_data['data']['token']
	return str(my_data)
	

	
	
#MAIN




def vlans(token,deger):
	import requests

	url = "https://ipam.domain.com/api/app/vlan/all"
	x=0
	allData=""
	ODM=""
	payload = {}
	headers = {
	  'token': token
	}
	response = requests.request("GET", url, headers=headers, data = payload, verify=False)
	j = response.json()
	i=json.dumps(j)
	response_data = json.loads(i)
	for item in response_data['data']:
	    nme=item['name'].split("-")
	    allData=str(item['vlanId'])+"-"+str(item['name'])+"-"+str(item['description'])
	    if deger in allData:
	        try: 
	            gotdata=str(nme[1])
	            gotdata2=str(nme[5]) 
	            #print(allData)
	            #print(gotdata,gotdata2)
	            ODM+=subnets(token,str(item['vlanId']))
	            
	        except IndexError: 
	            gotdata='null'
	        continue
	    else:
	        continue
	print(ODM)
	return ODM
	

def subnets(token,gotdata):
	import requests

	url = "https://ipam.domain.com/api/app/vlan/"+str(gotdata)+"/subnets"
	x=0
	allData=""
	payload = {}
	headers = {
	  'token': token
	}
	hata=""
	response = requests.request("GET", url, headers=headers, data = payload, verify=False)
	j = response.json()
	i=json.dumps(j)
	response_data = json.loads(i)
	if response_data['code']==200:
	    if 'data' in response_data:
	        for item in response_data['data']:
	            allData=str(item['subnet'])+"/"+str(item['mask'])+","
	            #try: 
	               # print(gotdata,allData)
	            #except IndexError: 
	                #gotdata='null'
	            #continue
	    else:
	        print("No data in the response")
	#else:
	    #print("response code:",str(gotdata),response.status_code,response.text)
	return allData
	

def zoneList(deger):
    url = "https://nessus/rest/zone"
    allData=""
    payload = {}
    headers = {
      'Content-Type': 'application/json',
      'x-apikey': 'accessKey=x;secretKey=y'
    }
    response = requests.request("GET", url, headers=headers, data = payload,verify=False)
    j = response.json()
    i=json.dumps(j)
    response_data = json.loads(i)
    for item in response_data['response']:
        if deger in item['name']:
            allData+=str(item['id'])+"*-*"+str(item['description'])+"*-*"+str(item['ipList'])
        else:
            continue
    print(allData)
    ortak(allData)
    return allData

def ortak(allData):
    nme=allData.split("*-*")
    print(nme)
    ne=str(vlans(userToken(),"ODM"))
    allDesc=str(nme[1])+"----------------------------------------------"+ne
    zoneUpdate(str(nme[0]),str(allDesc),str(nme[2]))
    
def zoneUpdate(ID,description,ip):
    url = "https://nesus/rest/zone/"+str(ID)
    payload = ("{\r\n        \"description\": \""+description+"\",\r\n        \"ipList\": \""+str(ip)+"\"\r\n}").encode('utf8')
    print(payload)
    headers = {
      'Content-Type': 'application/json',
      'x-apikey': 'accessKey=x;secretKey=y'
    }
    response = requests.request("PATCH", url, headers=headers, data=payload, verify=False)
    print(response.text.encode('utf8'),ID)


def jsontoCsv(json_file):
	f = open('data.csv','w')
	csv_file = csv.writer(f)
	for item in json_file:
	    f.writerow(item.values())  # ← changed
	f.close()


def zoneListAllName():
    url = "https://nessus/rest/zone"
    allData=""
    x=0
    payload = {}
    headers = {
      'Content-Type': 'application/json',
      'x-apikey': 'accessKey=x;secretKey=y'
    }
    response = requests.request("GET", url, headers=headers, data = payload,verify=False)
    j = response.json()
    i=json.dumps(j)
    response_data = json.loads(i)
    for item in response_data['response']:
        allData=str(item['id'])+"*-*"+str(item['name'])
        tex=str((item['name']).replace("_"," "))
        tex2=str(tex.replace("-"," ")).split(" ")
        print(tex2)
            #for x in range(len(tex)):
                #if type(tex[x])==str:
                    #det=vlans(userToken(),tex[x])
                    #print(allData)
                    #print(det)
    return tex2



def vlansList(token):
	import requests

	url = "https://ipam.domain.com/api/siberapp/vlan/all"
	x=0
	allData=""
	tex3=[]
	ODM=list()
	payload = {}
	headers = {
	  'token': token
	}
	response = requests.request("GET", url, headers=headers, data = payload, verify=False)
	j = response.json()
	i=json.dumps(j)
	response_data = json.loads(i)
	for item in response_data['data']:
	    nme=item['name'].split("-")
	    allData=str(item['vlanId'])+"-"+str(item['name'])
	    #tex=str((allData).replace("_"," "))
	    tex2=str(allData).split("-")
	    tex3.append(tex2)
	return tex3


def ortakList(vlanArray,token):
    zonesListesi=["ODM"]
    allData=""
    for item in range(len(zonesListesi)):
        for s in range(len(vlanArray)):
            for t in range(len(vlanArray[s])):
                if(zonesListesi[item]==vlanArray[s][t]):
                    #print(zonesListesi[item])
                    print(vlanArray[s])
                    test=subnets(token,str(vlanArray[s][0])).replace(",","")
                    if(test==vlanArray[s][len(vlanArray[s])-1]):
                        allData+=test+"\n"
                        break;
                    elif isinstance(vlanArray[s][len(vlanArray[s])-1], str):
                        continue;
                    else:
                        allData+=test+"\n"
                        allData+=vlanArray[s][len(vlanArray[s])-1]+"\n"
                        break;
                    #print(test)
                    #print(vlanArray[s][len(vlanArray[s])-1]) 
            #vlans(userToken(),zonesListesi[item])
    print(allData)
        


ortakList(vlansList(userToken()),userToken())
#zoneListAllName()

#zoneUpdate("98")
    #zoneList("Single_Nessus")
#vlans(userToken(),"ODM")
#subnets(userToken(),"161")
#jsontoCsv(ugur)

