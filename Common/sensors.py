"""
Get Environmental Sensor Data.
"""

import External.lnetatmo as lnetatmo


def get_netatmo_temperature(station='zBox Room'):
    """
    Get Netatmo Temperature Data.

    @param: station - Name of sensor to poll [String]
    @return: temperature - Temperature (Celsius) [Float]
    @return: epoch - Unix Timestamp (Seconds) [Float]
    """

    # Load Credentials
    with open('userpass_netatmo', 'r') as f:
        line = f.readline()
        line = line.strip().split(',')
        clientId = line[0]
        clientSecret = line[1]
        username = line[2]
        password = line[3]

    # Auth to Netatmo API
    authorization = lnetatmo.ClientAuth(clientId = clientId, \
                                        clientSecret = clientSecret, \
                                        username = username, \
                                        password = password)
    devList = lnetatmo.DeviceList(authorization)

    # Get Data
    temperature = devList.lastData()[station]['Temperature']
    epoch = devList.lastData()[station]['When']

    return temperature, epoch
