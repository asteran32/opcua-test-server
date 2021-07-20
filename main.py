import time
import json
import saver
import schedule

from opcua import ua, Server
from pymodbus.client.sync import ModbusTcpClient

if __name__ == "__main__":
    # load json config
    file = open("config.json")
    config = json.load(file)

    server = Server()
    server.set_endpoint(config.get("endpoint"))
    # server.set_security_policy([
    #             ua.SecurityPolicyType.NoSecurity,
    #             ua.SecurityPolicyType.Basic256Sha256_SignAndEncrypt,
    #             ua.SecurityPolicyType.Basic256Sha256_Sign])
    # setup our own namespace, not really necessary but should as spec
    server.register_namespace(config.get("uri"))

    # create a new node type we can instantiate in our address space
    obj = server.get_objects_node()
    root_folder = obj.add_folder(config.get("root").get("id"), config.get("root").get("name"))
    device = root_folder.add_object(config.get("device").get("id"), config.get("device").get("name"))
    
    # add node
    nodes = config.get("nodes")
    for node in nodes:
        i = node.get("register")
        globals()['node_{}'.format(i)] = device.add_variable(node.get("id"), node.get("name"), 0, ua.VariantType.Float).set_writable()
    # starting server Thread
    server.start()

    try:
        # PLC modbus connection
        client = ModbusTcpClient(config.get("plc"))
        if not client:
            server.stop()

        print("Start to listen plc address {}".format(config.get("plc")))
       
        # Load data saver 
        saver = saver.data_sheet()

        # Scheduling
        schedule.every().day.at("00:00").do(saver.createCSV)
        schedule.every().minute.do(saver.wirteCSV)

        while client:
            datas = []

            datas.append(time.strftime('%Y%m%d %H:%M'))
            for node in nodes:
                num = node.get("register")
                try:
                    node = client.read_holding_registers(num, 1)
                    data = node.registers[0] #error
                except:
                    break

                # globals()['node_{}'.format(i)].set_value(data)
                datas.append(data)

            saver.row = datas
            schedule.run_pending()
            time.sleep(5)
        
    finally:
        client.close()
        server.stop()

# if __name__ == "__main__":
#     # load json config
#     c = config.OpcuaServer()
#     # setup our server
#     server = Server()
#     server.set_endpoint(c.ENDPOINT)
#     # server.set_security_policy([
#     #             ua.SecurityPolicyType.NoSecurity,
#     #             ua.SecurityPolicyType.Basic256Sha256_SignAndEncrypt,
#     #             ua.SecurityPolicyType.Basic256Sha256_Sign])

#     # setup our own namespace, not really necessary but should as spec
#     uri = c.URI
#     server.register_namespace(uri)

#     # create a new node type we can instantiate in our address space
#     obj = server.get_objects_node()
#     root_folder = obj.add_folder(c.FOLDER['id'], c.FOLDER['name'])
#     device = root_folder.add_object(c.DEVICE['id'], c.DEVICE['name'])
    
#     # add node
#     hz = device.add_variable(c.BowlMoter['id'],c.BowlMoter['name'], 0, ua.VariantType.Float)
#     hz.set_writable()

#     # uuid
#     # guid = device.add_variable(NodeId(uuid.UUID('1be5ba38-d004-46bd-aa3a-b5b87940c698'), idx, NodeIdType.Guid), 'MyStringVariableWithGUID', 'NodeId type is guid')

#     # starting server Thread
#     server.start()

#     try:
#         # PLC modbus connection
#         plc = driver.Slave()
#         if not plc.connect():
#             server.stop()
        
#         # Load data saver 
#         saver = saver.data_sheet()

#         # Scheduling
#         schedule.every().day.at("00:00").do(saver.createCSV)
#         schedule.every().minute.do(saver.wirteCSV)

#         while plc.client:
#             h = plc.readRegister(c.NODE_HZ['register'])
#             if h is not None:
#                 hz.set_value(h)

#             data_list = [time.strftime('%Y %m %d %H:%M'), h]
#             saver.row = data_list
#             schedule.run_pending()

#             time.sleep(1)
        
#     finally:
#         plc.disconncet()
#         server.stop()