import network, esp, socket, machine, ure, ubinascii, bmp180,time, neopixel
from machine import Pin, I2C
from bmp180 import BMP180
def wifiAP():
    ap_if = network.WLAN(network.AP_IF)
    essid = b"MicroPython-%s" % ubinascii.hexlify(ap_if.config("mac")[-3:])
    ap_if.config(essid=essid, authmode=network.AUTH_WPA_WPA2_PSK, password=b"micropythoN")
def connect_to_wifi():
    wlan = network.WLAN(network.STA_IF) 
    wlan.active(True)       
    wlan.isconnected()     
    wlan.connect('xx', 'XXXXX',timeout=100) 
    wlan.config('mac')     
    print ("Check if internet Connected")
    addr = socket.getaddrinfo('za.pycon.org', 80)[0][-1]

def web_server():
    try:
        pins = [machine.Pin(i, machine.Pin.OUT) for i in (0, 2, 4, )]
        #pins.extend([machine.Pin(i, machine.Pin.IN) for i in (5, 12, 13, 14, 15)])
        [p.low() for p in pins]
        html = """<!DOCTYPE html><html>
            <head> <title>PyConZA IOT Demo</title> </head>
            <body> <h1>PyConZA IOT Demo</h1> <h2>BMP Sensor Output</h2>
                    <h2>Temp: %s</h2><h2>Pressure: %s</h2><h2>Altitude: %s</h2>
            <h1>ESP8266 Pins</h1>
                <table border="1"> <tr><th>Pin</th><th>Value</th><th>Change Value</th></tr> %s </table>
            </body>
        </html>
        """
        addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
        s = socket.socket()
        s.bind(addr)
        s.listen(5)
        print('listening on', addr)
        while True:
            i2c = I2C(scl=Pin(14), sda=Pin(12))
            bmp180 = BMP180(i2c)
            bmp180.oversample_sett = 2
            bmp180.baseline = 101325
            temp = bmp180.temperature
            pressure = bmp180.pressure
            altitude = bmp180.altitude
            print ("Temp: %s Pressure: %s Altitude: %s" %(temp,pressure,altitude))
            conn, addr = s.accept()
            print('client connected from', addr)
            data = conn.recv(100)
            if "Pin" in data:
                r = str(data,'utf-8').split("/Pin(")[1].split(")")[0]
                print ("Match ", r)
                new_pin = machine.Pin(int(r))
                if new_pin.value() == 1:
                    new_pin.value(0)
                    #new_pin.toggle()
                    print (new_pin.value())
                else:
                    new_pin.value(1)
            conn_file = conn.makefile('rwb', 0)
            while True:
                line = conn_file.readline()
                if not line or line == b'\r\n':
                    break
                print ("")
            rows = ['<tr><td>%s</td><td>%d</td><td><a href="http:/%s"><button>Change</button></td></a></tr>' % (str(p), p.value(), str(p)) for p in pins]
            response = html % (temp,pressure,altitude,'\n'.join(rows))
            conn.send(response)
            conn.close()
    except KeyboardInterrupt:
        s.close()
        print ("Keyboard interrupt")
def main():
    wifiAP()
    web_server()
main()
