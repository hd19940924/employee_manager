from django.test import TestCase

# Create your tests here.
import requests

url = "http://127.0.0.1:8000/login/"

payload = "-----011000010111000001101001\r\nContent-Disposition: form-data; name=\"username\"\r\n\r\nadmin\r\n-----011000010111000001101001\r\nContent-Disposition: form-data; name=\"password\"\r\n\r\n123456\r\n-----011000010111000001101001--\r\n\r\n"
headers = {"content-type": "multipart/form-data; boundary=---011000010111000001101001"}
payload_new={"username":"admin","password":"123456"}
print(type(payload_new))
#response = requests.request("POST", url, data=payload_new, headers=headers)
re=requests.request("POST",url,data=payload_new)

print(re.text)