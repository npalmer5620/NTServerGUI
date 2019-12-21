import time
import logging
import datetime

# from netifaces import interfaces, ifaddresses, AF_INET
from networktables import NetworkTables

logging.basicConfig(level=logging.DEBUG)

'''
def get_ip():
    for face in interfaces():
        addresses = [i['addr'] for i in ifaddresses(face).setdefault(AF_INET, [{'addr': 'No IP addr'}])]
        print('%s: %s' % (face, ', '.join(addresses)))
'''


class NTBackend:
    mode: int
    address: str
    port: int
    log_list: list

    def __init__(self, address='', port=1735, window=None):
        self.mode = 0
        self.address = address
        self.port = port
        self.log_list = []
        self.window = window

    def to_log(self, text, nl=True, tag='INFO'):
        st = datetime.datetime.fromtimestamp(time.time()).strftime('%H:%M:%S')
        text = '[' + st + '] ' + ' [' + tag + ']  ' + text
        self.log_list.append(text)
        if nl:
            self.window['log'].update('\n'.join(str(e) for e in self.log_list))
        else:
            self.window['log'].update(''.join(str(e) for e in self.log_list))
        self.window.read(timeout=100)

    def initialize(self, ip=None, port=None):
        if type(ip) is str and ip.strip().lower() != '':
            self.address = ip
        if type(port) is int:
            self.port = port

        if self.mode == 1:
            self.to_log('NetworkTables already initialized')
            return True
        self.to_log('NetworkTables initializing...')
        if NetworkTables.startServer(listenAddress=self.address, port=self.port):
            time.sleep(1)
            self.mode = NetworkTables.getNetworkMode()
            if self.mode == 1:
                self.to_log('NetworkTables initialized in server mode')
                if self.address is '' or None:
                    self.to_log('Listening on  ' + str(self.port), tag='DEBUG')
                else:
                    self.to_log('Listening on ' + self.address + ':' + str(self.port), tag='DEBUG')
                return True

        self.to_log('Could not start NetworkTables instance', tag='ERROR')
        self.to_log('NT_NET MODE ' + str(self.mode), tag='ERROR')
        return False

    def shutdown(self):
        if self.mode == 0:
            self.to_log('NetworkTables already stopped')
            return True

        self.to_log('NetworkTables Stopping...')
        NetworkTables.stopServer()

        time.sleep(1)

        self.mode = NetworkTables.getNetworkMode()
        if self.mode == 0:
            self.to_log('Stopped')
            return True
        self.to_log('Could not stop NetworkTables instance', tag='ERROR')
        self.to_log('NT_NET MODE ' + str(self.mode), tag='ERROR')

    def flush(self):
        if self.mode == 0:
            self.to_log('NetworkTables is stopped')
            return False

        NetworkTables.flush()
        self.to_log('NetworkTables flushed')
        return True

    def set_identity(self, ide):
        if self.mode == 0:
            self.to_log('NetworkTables is stopped')
            return False

        NetworkTables.setNetworkIdentity(ide)
        self.to_log('Network identity set to: ' + ide)
        return True


if __name__ == '__main__':
    # get_ip()
    be = NTBackend()
    be.initialize()
    time.sleep(1)
