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
    device = obj.add_object(config.get("device").get("id"), config.get("device").get("name"))
    
    # add node
    nodes = config.get("nodes")
    for node in nodes:
        idx = node.get("register")
        globals()['node'+str(idx)] = device.add_variable(node.get("id"), node.get("name"),  ua.Variant(0, ua.VariantType.Float))
        eval('node'+str(idx)).set_writable()

    # start opc ua server
    server.start()

    try:
        # plc modbus connection
        client = ModbusTcpClient(config.get("plc"))
        if not client:
           server.stop()

        # Load saver 
        saver = saver.data_sheet()

        # Scheduling
        schedule.every().day.at("00:00").do(saver.create_file)
        schedule.every().second.do(saver.wirte_data)

        while client:
            datas = []
            datas.append(time.strftime('%Y%m%d %H:%M:%S'))
            for node in nodes:
                try:
                    raw = client.read_holding_registers(node.get("register"), 1)
                    data = raw.registers[0] # int type
                    # Set opc ua server value
                    nodeName = node.get("name").split("_")[1]
                    if nodeName == "A" or nodeName == "Hz":
                        data = float(data) * 0.1
                        data = round(data, 2)
                    
                    idx = node.get("register")
                    eval('node'+str(idx)).set_value(data)
                except:
                    break

                datas.append(data)

            saver.row = datas
            schedule.run_pending()
            # time.sleep(2)
        
    finally:
        client.close()
        server.stop()