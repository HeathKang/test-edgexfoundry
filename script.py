import random
import struct

from pymodbus.server.sync import StartTcpServer
from pymodbus.datastore import ModbusSequentialDataBlock, ModbusSparseDataBlock
from pymodbus.device import ModbusDeviceIdentification
from pymodbus.datastore import ModbusSlaveContext, ModbusServerContext

import logging
FORMAT = ('%(asctime)-15s %(threadName)-15s'
          ' %(levelname)-8s %(module)-15s:%(lineno)-8s %(message)s')
logging.basicConfig(format=FORMAT)
log = logging.getLogger()
log.setLevel(logging.DEBUG)

def simulate_env() -> [float]:
    """
    generate random temperature and humidity
    """
    temperature = random.uniform(16.0, 20.0)
    humidity = random.uniform(0.41, 0.61)
    return [temperature, humidity]

def turn_float_int(float_data) -> [int]:
    """
    turn float num to int
    """
    log.debug(float_data)
    data_handle_bytes = struct.pack(">2f",*float_data)
    log.debug(data_handle_bytes)
    data_handle = struct.unpack(">8B", data_handle_bytes)
    log.debug(data_handle)
    return list(data_handle)

def run_server():
    data_list = turn_float_int(simulate_env())
    log.debug("register data is {}".format(data_list))
    store = ModbusSlaveContext(
        di=ModbusSequentialDataBlock(0, [17]*100),
        co=ModbusSequentialDataBlock(0, [17]*100),
        hr=ModbusSequentialDataBlock(0, [17] + data_list), ## start at index 1 not 0
        # hr=ModbusSequentialDataBlock(0, [20.1,20.1,20.1,20.1,20.1]),
        ir=ModbusSequentialDataBlock(0, [17]*100))

    context = ModbusServerContext(slaves=store, single=True)

    identity = ModbusDeviceIdentification()
    identity.VendorName = 'Pymodbus'
    identity.ProductCode = 'PM'
    identity.VendorUrl = 'http://github.com/riptideio/pymodbus/'
    identity.ProductName = 'Pymodbus Server'
    identity.ModelName = 'Pymodbus Server'
    identity.MajorMinorRevision = '1.5'

    StartTcpServer(context, identity=identity, address=("192.168.0.110", 5020))

def main():
    run_server()


if __name__ == '__main__':
    main()