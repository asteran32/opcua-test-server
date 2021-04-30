import uuid
import time
import threading
import schedule

import driver
import saver

from opcua import ua, Server
from opcua.ua import NodeId, NodeIdType

# Const 
REQUEST_DELAY = 1

# UA Config
ENDPOINT = "opc.tcp://192.168.10.15:49320/test"
URI = "FINE_Test_Server"

# Node Address 
NODE_VOLT = 114
NODE_GFORCE = 54
NODE_HZ = 74
NODE_RPM = 104

if __name__ == "__main__":
    # setup our server
    server = Server()
    server.set_endpoint(ENDPOINT)
    # server.set_security_policy([
    #             ua.SecurityPolicyType.NoSecurity,
    #             ua.SecurityPolicyType.Basic256Sha256_SignAndEncrypt,
    #             ua.SecurityPolicyType.Basic256Sha256_Sign])

    # setup our own namespace, not really necessary but should as spec
    uri = URI
    server.register_namespace(uri)

    # create a new node type we can instantiate in our address space
    obj = server.get_objects_node()
    root_folder = obj.add_folder('ns=2;s="FINE"', "FINE")
    device = root_folder.add_object('ns=2;s="FINE.FSC300"', "FSC300")
    
    # add node
    hz = device.add_variable('ns=2;s="FINE.FSC300.hz"',"hz", 0, ua.VariantType.Float)
    hz.set_writable()

    volt = device.add_variable('ns=2;s="FINE.FSC300.volt"', "volt", 0, ua.VariantType.Float)
    volt.set_writable()

    rpm = device.add_variable('ns=2;s="FINE.FSC300.rpm"', "rpm", 0, ua.VariantType.Float)
    rpm.set_writable()

    gforce = device.add_variable('ns=2;s="FINE.FSC300.gfor"', "gforce", 0, ua.VariantType.Float)
    gforce.set_writable()

    # uuid
    # guid = device.add_variable(NodeId(uuid.UUID('1be5ba38-d004-46bd-aa3a-b5b87940c698'), idx, NodeIdType.Guid), 'MyStringVariableWithGUID', 'NodeId type is guid')

    # starting server Thread
    server.start()

    try:
        # PLC modbus connection
        plc = driver.Slave()
        if not plc.connect():
            server.stop()
        
        # Load data saver 
        saver = saver.data_sheet("./data/")

        # Scheduling
        schedule.every().day.at("00:00").do(saver.createCSV)
        schedule.every().minute.do(saver.wirteCSV)

        while plc.client:
            v = plc.readRegister(NODE_VOLT)
            if v is not None:
                volt.set_value(v)
            
            h = plc.readRegister(NODE_HZ)
            if h is not None:
                hz.set_value(h)
            
            r = plc.readRegister(NODE_RPM)
            if r is not None:
                rpm.set_value(r)

            g = plc.readRegister(NODE_GFORCE)
            if g is not None:
                gforce.set_value(g)

            data_list = [time.strftime('%Y-%m-%d %H:%M'), v, h, r, g]
            saver.row = data_list
            schedule.run_pending()

            time.sleep(REQUEST_DELAY)
        

    finally:
        plc.disconncet()
        server.stop()
        print("Closing the Server", ENDPOINT)