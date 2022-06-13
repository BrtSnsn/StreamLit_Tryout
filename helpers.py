import json
from collections import OrderedDict
import paho.mqtt.client as mqtt
from PIL import Image

# Global parameters that will be used in all pages
class Param():
    def __init__(self):
        self.extr_lines_be = [f'EL{x:02d}' for x in range(1, 11)]
        self.LINES = ['_'] + self.extr_lines_be
        self.SCRAP_REASONS = ['_', 'line', 'H20', 'scratch', 'other']

        self.logo = Image.open(R"Icons/getsitelogo.png")
        self.oracicon = Image.open(R"Icons/logo.ico")
        self.hot = Image.open(R"Icons/Burning.png")
        pass


# Christophe has a more bug-free version of this class (implement once he is 'done')
class Mqtt():
    def __init__(self, clientid):
        # read config files
        cnf_version = self.config_version()
        self.config = self.read_jsonconfig(cnf_version)

        # define Paho Mqtt client:
        self.client = mqtt.Client(
            client_id=clientid,
            clean_session=True,
            userdata=None,
            protocol=mqtt.MQTTv311,
            transport="tcp"
            )


    def read_jsonconfig(self, extension):
            with open(f'mqtt_config{extension}.json') as jsonfile:
                return json.load(jsonfile, object_pairs_hook=OrderedDict)


    def config_version(self):
        with open('config.ini') as f:
            line = f.readline()
            return line


    def make_connection(self):
        # make connection
        if self.config['broker_login'] != "":
            self.client.username_pw_set(username=self.config['broker_login'], password=self.config['broker_password'])
        
        self.client.connect(
            host=self.config['broker_ip'], 
            port=self.config['broker_port'],
            # keepalive=6000
            )

