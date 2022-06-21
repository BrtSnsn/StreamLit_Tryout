import influxdb_client

class InfluxQuery:
    def __init__(self, line, start, stop):
        """
        Dit is standaard: influx connectie opzetten
        line : string
        start: datetime formatn .isoformat('T') + 'Z'
        stop: datetime format .isoformat('T') + 'Z'
        """
        self.org = "testorac"
        token = "FfFelQxbFycdHBx430FMZ1lB13mUtxUCau7Cu-LF-dRVT1OvWPTQcLI5tjcsrPfs9uU9TwFMGmngIHZuPKNb4g=="

        url = "http://influxdbv2:8086"
        client = influxdb_client.InfluxDBClient(
            url=url,
            token=token,
            org=self.org,
            timeout=10_000)

        self.query_api = client.query_api()
        self.bucket = "orac_bucket"
        self.line_parm = Rf"/{line.upper()}/"
        self.data_point = "value"

        self.start = start
        self.stop = stop


    def bruteforce(self):
        """
        Simple query to gather all data from one line
        """
        # dit is de standaard query om 1 voor 1 te bevragen zonder de "laatste" waarde
        query_string = \
            f'from(bucket: "{self.bucket}")' \
            f'|> range(start:{self.start}, stop: {self.stop})' \
            f'|> filter(fn: (r) => r._measurement =~ {self.line_parm} ' \
            f'and r._field == "{self.data_point}")'\
            f'|> truncateTimeColumn(unit: 1s)' \
            f'|> timedMovingAverage(every: 15s, period: 5m)' \
            f'|> pivot(rowKey: ["_time"], columnKey: ["_measurement"], valueColumn: "_value")'
        result = self.query_api.query_data_frame(org=self.org, query=query_string)  # uitlezen als Pandas
        result = result.set_index('_time')
        result = result.sort_index(ascending=True)
        result = result.drop(columns=['result', 'table', '_start', '_stop', '_field'])

        return result

"""
<This is the query directly from de influxDB query builder editor>
from(bucket: "orac_bucket")
  |> range(start:-5h, stop: -4h)
  |> filter(fn: (r) => r._measurement =~ /EL05/ and r._field == "value")
  |> truncateTimeColumn(unit: 1s)
  |> timedMovingAverage(every: 15s, period: 5m)
  |> pivot(rowKey: ["_time"], columnKey: ["_measurement"], valueColumn: "_value")
"""