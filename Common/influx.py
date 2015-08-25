"""
InfluxDB Interaction.
"""

import requests


def post_data(data):
    """
    Post Data to Server.

    @param: data - String of data to post.
    """

    # Load Userpass CSV File (InfluxDB)
    # Format: server,port,db,user,pass
    with open('userpass_influx', 'r') as f:
        line = f.readline()
        line = line.strip().split(',')
        host = line[0]
        port = line[1]
        db   = line[2]
        user = line[3]
        pswd = line[4]

    # Post
    url = "http://%s:8086/write?db=%s&precision=s" % (host, db)
    auth = requests.auth.HTTPBasicAuth("%s" % user, "%s" % pswd)
    r = requests.post("%s" % url, auth=auth, data="%s" % data)

    # Debug
    # print r.status_code
    # print r.headers
    # print r.content
