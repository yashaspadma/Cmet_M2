class MockModbusClient:
    """Mock Modbus client for development testing"""
    def __init__(self):
        self.client = self
        self.connected = True
        self.mock_coils = {0: False}
        self.mock_registers = {0: 0}

    def connect(self):
        return self.connected

    def close(self):
        self.connected = False

    def read_coils(self, address, count):
        return MockResponse([self.mock_coils.get(address, False)])

    def read_holding_registers(self, address, count):
        return MockResponse([self.mock_registers.get(address, 0)])

    def write_coil(self, address, value):
        self.mock_coils[address] = value
        return MockResponse([value])

    def write_register(self, address, value):
        self.mock_registers[address] = value
        return MockResponse([value])

class MockResponse:
    def __init__(self, values):
        self.bits = values
        self.registers = values

    def isError(self):
        return False