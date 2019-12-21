import PySimpleGUI as sg

from ntbackend import NTBackend


class FrontendUI:
    version_tag: str
    app: NTBackend
    windows: sg.Window

    def __init__(self, version_tag="0.1"):
        self.version_tag = version_tag
        self.layout = [[sg.Text('', size=(127, 30), font='Helvetica 12', key='log', background_color='black',
                                text_color='lime')],
                       [sg.Button('Start', button_color=('black', 'lime'), key='start_button'),
                        sg.Button('Flush', button_color=('black', 'magenta'), key='flush_button'),
                        sg.Button('Set Identity', button_color=('black', 'cyan'), key='identity_button'),
                        sg.Button('Stop', button_color=('black', 'red'), key='stop_button')]]

        sg.change_look_and_feel('DarkBlue3')
        self.window = sg.Window('NetworkTables Server GUI v' + self.version_tag, self.layout,
                                default_element_size=(30, 2),
                                font=('Helvetica', ' 13'),
                                default_button_element_size=(8, 2),
                                no_titlebar=False)
        self.app = NTBackend(window=self.window)

    def run(self):
        while True:  # Event Loop
            event, values = self.window.read(timeout=100)
            if event in (None, 'EXIT'):
                break
            elif event == 'start_button':
                ip = sg.PopupGetText('Host IP', 'Please enter a host IP', default_text='127.0.0.1', keep_on_top=True,
                                     no_titlebar=False)
                if type(ip) is str and ip.strip().lower() != '':
                    self.app.initialize(ip=ip.strip().lower())
                else:
                    self.app.initialize()
            elif event == 'stop_button':
                self.app.shutdown()
            elif event == 'flush_button':
                self.app.flush()
            elif event == 'identity_button':
                identity = sg.PopupGetText('Set Network Identity',
                                           'Please enter a new network identity',
                                           keep_on_top=True,
                                           no_titlebar=False)
                if type(identity) is str and identity.strip().lower() != '':
                    self.app.set_identity(identity.strip().lower())

        self.window.close()


if __name__ == '__main__':
    my_gui = FrontendUI()
    my_gui.run()
