"""Library to communicate with OREI UKM-404 USB switch over HTTP."""

import http.client
import json

_HOST = "192.168.1.178"
_SEND_CMD_ENDPOINT = "/cgi-bin/MMX32_Keyvalue.cgi"
_GET_PARAM_ENDPOINT = "/cgi-bin/MUH44TP_getsetparams.cgi"

def switch_usb_position(device: int, host: int):
  """Switch USB device to host.
  
  Devices are numbered 1, 2, 3, 4. Device 0 corresponds to all devices.
  Hosts are numbered 1, 2, 3, 4. Switching to host 0 disconnects the device.
  """
  assert 0 <= device <= 4
  assert 0 <= host <= 4
  cmd = '>SetUSB %02i:%02i' % (device, host)
  payload = '{CMD=%s\r\n' % cmd
  send_request(_SEND_CMD_ENDPOINT, payload)
  
def get_status():
  response = send_request(_GET_PARAM_ENDPOINT, 'lcc')
  response = response.replace('(', '')
  response = response.replace(')', '')
  response = response.replace('\'', '"')
  response_json = json.loads(response)
  # print("Formatted Response:", json.dumps(response_json, indent=2))
  # print(response_json['Outputbuttom'])
  # Returns the current device/host assignements as a string of numbers.
  # E.g. '2224' means that the first 3 devices are connected to host 2 and the 
  # 4th device is connected to host 4.
  return response_json['Outputbuttom'][:3]


def send_request(endpoint: str, payload: str):
  conn = http.client.HTTPConnection(_HOST, 80, timeout=1)
  headers = {"Content-Type": 'application/x-www-form-urlencoded; charset=UTF-8'}
  # print('Payload: %s' % payload)
  conn.request("POST", endpoint, body=payload, headers=headers)
  response = conn.getresponse()
  response_text = response.read().decode("utf-8")
  #print(f'Status: {response.status} Response: {response_text.strip()}')
  conn.close()
  return response_text