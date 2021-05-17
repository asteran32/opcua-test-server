import uuid
import time
import threading
import schedule

import driver
import saver
import config

from opcua import ua, Server
from opcua.ua import NodeId, NodeIdType

if __name__ == "__main__":
    # load configurations
    c = config.OPCUAServerConfig()
    # setup our server
    server = Server()
    server.set_endpoint(c.ENDPOINT)
    # server.set_security_policy([
    #             ua.SecurityPolicyType.NoSecurity,
    #             ua.SecurityPolicyType.Basic256Sha256_SignAndEncrypt,
    #             ua.SecurityPolicyType.Basic256Sha256_Sign])

    # setup our own namespace, not really necessary but should as spec
    uri = c.URI
    server.register_namespace(uri)

    # create a new node type we can instantiate in our address space
    obj = server.get_objects_node()
    root_folder = obj.add_folder(c.FOLDER['id'], c.FOLDER['name'])
    device = root_folder.add_object(c.DEVICE['id'], c.DEVICE['name'])
    
    # add node
    hz = device.add_variable(c.NODE_HZ['id'],c.NODE_HZ['name'], 0, ua.VariantType.Float)
    hz.set_writable()

    volt = device.add_variable(c.NODE_VOLT['id'],c.NODE_VOLT['name'], 0, ua.VariantType.Float)
    volt.set_writable()

    rpm = device.add_variable(c.NODE_RPM['id'],c.NODE_RPM['name'], 0, ua.VariantType.Float)
    rpm.set_writable()

    gforce = device.add_variable(c.NODE_GFORCE['id'],c.NODE_GFORCE['name'], 0, ua.VariantType.Float)
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
        saver = saver.data_sheet()

        # Scheduling
        schedule.every().day.at("00:00").do(saver.createCSV)
        schedule.every().minute.do(saver.wirteCSV)
        schedule.every(15).minutes.do(saver.uploadCSV)

        while plc.client:
            v = plc.readRegister(c.NODE_VOLT['register'])
            if v is not None:
                volt.set_value(v)
            
            h = plc.readRegister(c.NODE_HZ['register'])
            if h is not None:
                hz.set_value(h)
            
            r = plc.readRegister(c.NODE_RPM['register'])
            if r is not None:
                rpm.set_value(r)

            g = plc.readRegister(c.NODE_GFORCE['register'])
            if g is not None:
                gforce.set_value(g)

            data_list = [time.strftime('%Y-%m-%d %H:%M'), v, h, r, g]
            saver.row = data_list
            schedule.run_pending()

            time.sleep(1)
        
    finally:
        plc.disconncet()
        server.stop()