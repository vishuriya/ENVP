import base64
from requests import Session
from requests.auth import HTTPBasicAuth  # or HTTPDigestAuth, or OAuth1, etc.
from zeep import Client
from zeep.transports import Transport


# pdf =  
# #Enter PDF file path

# xl = #Enter excel file path


# data1 = open(pdf, 'rb').read()
# base64_encoded_pdf = base64.b64encode(data1).decode('UTF-8')

# data2 = open(xl, 'rb').read()
# base64_encoded_xl = base64.b64encode(data2).decode('UTF-8')

base64_encoded_pdf = 'test.pdf'
base64_encoded_xl = 'test.xlsx'


session = Session()
session.auth = HTTPBasicAuth("chintang", "Ey@123456789")
client = Client('http://euwdrh201fl01.SPRADV.SBP.LOCAL:8001/sap/bc/srt/wsdl/flv_10002A111AD1/bndg_url/sap/bc/srt/rfc/sap/zeyocr_upload_files_name/200/zeyocr_upload_files_name/zeyocr_upload_files_name?sap-client=200',
    transport=Transport(session=session))

print(client.service.ZEYOCR_UPLOAD_FILES_NAME(base64_encoded_pdf,base64_encoded_xl))
