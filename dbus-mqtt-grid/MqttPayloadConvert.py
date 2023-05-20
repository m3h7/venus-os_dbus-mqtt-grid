class MqttPayloadConvert:
    def __init__(self, format: str):
        self._format = format

    def convert(self, jsonpayload):
        payload = { "grid": {} }

        if self._format == 'obis_0':
            phases = 0
            voltage_sum = 0
            for attr, value in jsonpayload.items():
                val_f = float(value)
                if attr == "1-0:1.8.0_255":
                    payload['grid']['energy_forward'] = val_f
                    continue

                if attr == "1-0:2.8.0_255":
                    payload['grid']['energy_reverse'] = val_f
                    continue
                
                if attr == "1-0:16.7.0_255":
                    payload['grid']['power'] = val_f
                    continue

                if attr == '1-0:32.7.0_255' or attr == '1-0:52.7.0_255' or attr == '1-0:72.7.0_255':
                    phases += 1
                    voltage_sum += val_f
                    continue
            
            if voltage_sum:
                payload['grid']['voltage'] = voltage_sum / phases
                payload['grid']['current'] = payload['grid']['power'] / payload['grid']['voltage']


        return payload

# 1-0:1.8.0_255: "10098.4976"
# 1-0:2.8.0_255: "254.3488"
# 1-0:16.7.0_255: "390"
# 1-0:32.7.0_255: "229.8"
# 1-0:52.7.0_255: "227.2"
# 1-0:72.7.0_255: "225.1"
# 1-0:31.7.0_255: "1.75"
# 1-0:51.7.0_255: "0.42"
# 1-0:71.7.0_255: "0.40"
# 1-0:81.7.1_255: "120"
# 1-0:81.7.2_255: "241"
# 1-0:81.7.4_255: "45"
# 1-0:81.7.15_255: "71"
# 1-0:81.7.26_255: "35"
# 1-0:14.7.0_255: "50.0"
# 1-0:1.8.0_96: "3.6"
# 1-0:1.8.0_97: "41.3"
# 1-0:1.8.0_98: "144.9"
# 1-0:1.8.0_99: "2252.0"
# 1-0:1.8.0_100: "10098.4"