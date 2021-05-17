class OPCUAServerConfig():
    # UA Config
    #ENDPOINT = 'opc.tcp://192.168.0.20:49320/test'
    ENDPOINT = 'opc.tcp://192.168.0.20:4840'
    URI = 'FINE_Test_Server'
    
    # Root Folder
    FOLDER = {
        'id': 'ns=2;s="FINE"',
        'name': "FINE"
    }

    # PLC Device 
    DEVICE = {
        'id': 'ns=2;s="FINE.FSC300"',
        'name': "FSC300"
    }

    # Node
    NODE_VOLT = {
        'id': 'ns=2;s="FINE.FSC300.volt"',
        'name': 'voltage',
        'register': 114
    }

    NODE_GFORCE = {
        'id': 'ns=2;s="FINE.FSC300.gfor"',
        'name': 'gforce',
        'register': 54
    }

    NODE_HZ = {
        'id': 'ns=2;s="FINE.FSC300.hz"',
        'name': 'hz',
        'register': 74
    }

    NODE_RPM = {
        'id': 'ns=2;s="FINE.FSC300.rpm"',
        'name': 'rpm',
        'register': 104
    }

class DatabaseConfig():
    # db config
    DB_PATH = './db/plc_fs300.db'
    # csv file path
    CSV_PATH = './data/'
