# author: a5892731
# date: 01.06.2022
# last update: 14.06.2022
# version: 1.0

# description: This is REST API GET function for MOXA ioLogik E1212 device

'''
source:
https://github.com/zentec/moxa-iologic-1200-monitor/blob/master/monitor.py

'''

from requests import get
from json import loads

from time import sleep, time



class GetRequestData():
    def __init__(self, address = "http://192.168.127.254"):
        self.address = address

        self.connection_error = None # True if there is no connection for more than 1 s
        self.data_error = None
        self.replay_status_code = None # connection statuses = 200; 404 etc
        self.reply = None # request response
        self.json_data = None # converted response to json
        """downloaded data >>>"""
        self.deviceUpTime = None

        self.DO = None
        self.DI = None

        self.start_time = time() # for testing
        self.last_get_time = time()

    def get_sysInfo(self):
        self.get_data(api_address_extension = "/api/slot/0/sysInfo/device")
        if not self.connection_error:
            self.convert_received_data()
            self.deviceUpTime = self.json_data['sysInfo']['device'][0]['deviceUpTime']

    def get_DI(self):
        self.get_data(api_address_extension="/api/slot/0/io/di")
        if not self.connection_error:
            self.convert_received_data()
            self.DI = self.json_data['io']['di']

    def get_DO(self):
        self.get_data(api_address_extension="/api/slot/0/io/do")
        if not self.connection_error:
            self.convert_received_data()
            self.DO = self.json_data['io']['do']

    def run(self):
        # get device status
        self.get_sysInfo()

        # get digital inputs
        self.get_DI()

        # get digital outputs
        self.get_DO()

    def get_data(self, api_address_extension = "/api/slot/0/io/do"):
        try:
            self.reply = get(self.address + api_address_extension,
                             {"rel_rhy": "network"},
                             headers={"Content-Type": "application/json", "Accept": "vdn.dac.v1"},
                             timeout=0.1,
                            )

            self.replay_status_code = self.reply.status_code
            self.connection_error = False
            self.last_get_time = time()

        except:
            self.connection_error = True

    def convert_received_data(self):
        if not self.connection_error:
            try:
                json_blob = loads(self.reply.content.decode('utf-8'))
                self.json_data = json_blob

                self.data_error = False

            except ValueError:
                self.data_error = True



if __name__ == "__main__":
    data = GetRequestData()

    while True:
        data.run()

        sleep(0.1)
        print(data.deviceUpTime)
        print("di {}".format(data.DO))

        print("do {}".format(data.DO))