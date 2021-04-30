from pymodbus.client.sync import ModbusTcpClient
# https://pymodbus.readthedocs.io/en/latest/source/library/pymodbus.client.html

#const 
PLC_IPADD = "192.168.10.11"

class Slave(object):
    def __init__(self):
        self.client = None
        self.serverAddress = PLC_IPADD

    # open connection
    def connect(self):
        c = ModbusTcpClient(self.serverAddress)
        if c :
            self.client = c
            return c
        return c

    # check connection is open or close
    def isopen(self):
        return self.client.is_socket_open()

    # get add data
    def readRegister(self, dataAdd): 
        if self.client:
            try:
                node = self.client.read_holding_registers(dataAdd, 1) 
                data = node.registers[0]
                return data
            except:
                self.disconncet()
                return
        return None

    # get datas start at add from count
    def readRegisters(self, dataAdd, cnt): 
        if self.client:
            try:
                node = self.client.read_holding_registers(dataAdd, cnt)
                datas = node.registers
                return datas    
            except:
                self.disconncet()
                return
        return None

    # close connection
    def disconncet(self):
        if self.client:
            self.client.close()
            self.client = None
