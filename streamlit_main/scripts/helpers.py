import json
from collections import OrderedDict
import paho.mqtt.client as mqtt
from PIL import Image

# docker = False
docker = True

if not docker:
    local_string = R"streamlit_main/"
else:
    local_string = ""

# Global parameters that will be used in all pages
class Param():
    def __init__(self):
        self.extr_lines_be = [f'EL{x:02d}' for x in range(1, 11)]
        self.LINES = ['_'] + self.extr_lines_be
        self.SCRAP_REASONS = ['_', 'line', 'H20', 'scratch', 'other']

        self.logo = Image.open(Rf"{local_string}Icons/getsitelogo.png")
        self.oracicon = Image.open(Rf"{local_string}Icons/logo.ico")
        self.hot = Image.open(Rf"{local_string}Icons/Burning.png")

        self.bg = Rf"{local_string}Icons/background.png"
        self.quick = Rf"{local_string}Icons/Quickness.png"

        self.status_text = {
            '0': '_',
            '1': 'Opwarmen',
            '2': 'Startup',
            '3': 'Production',

            '5': 'Heropstart',

            '10': 'Cold Die',
            '20': 'Hot Die',

            '50': 'Wissel Opbouw', 
            '51': 'Wissel Afbouw',

            '99': 'Error'
        }

        self.inv_status_text = {v: k for k, v in self.status_text.items()}

        self.status_color = {
            '0': '#e8e8e8',
            '1': '#e0e000',
            '2': '#b8c282',
            '3': '#00a80b',

            '5': '#b8c282',

            '10': '#5279fa',
            '20': '#a952fa',

            '50': '#e09900', 
            '51': '#e09900',

            '99': 'Error'
        }
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
            with open(Rf"{local_string}mqtt_config{extension}.json") as jsonfile:
                return json.load(jsonfile, object_pairs_hook=OrderedDict)


    def config_version(self):
        with open(Rf"{local_string}config.ini") as f:
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

