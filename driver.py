from pymodbus.client.sync import ModbusTcpClient
# https://pymodbus.readthedocs.io/en/latest/source/library/pymodbus.client.html

class Slave:
    def __init__(self):
        self.client = None
        self.serverAddress = " "

    # open connection
    def connect(self, add):
        c = ModbusTcpClient(self.serverAddress)
        if c :
            self.client = c
            self.serverAddress = add
            return c
        return c

    # check connection is open or close
    def isopen(self):
        return self.client.is_socket_open()

    # get add data
    def readRegister(self, dataAdd): 
        if self.client:
            try:
                node = self.client.read_holding_registers(1000, 1) 
                data = node.registers[0]
                return data
            except:
                self.disconncet()
                return
        return " "

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
        return " "

    # close connection
    def disconncet(self):
        if self.client:
            self.client.close()
