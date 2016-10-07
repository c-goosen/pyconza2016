def connect_to_wifi():
    wlan = network.WLAN(network.STA_IF) 
    wlan.active(True)       
    wlan.isconnected()     
    wlan.connect('xx', 'xxxxxx',timeout=100) 
    wlan.config('mac')     
    print ("Check if internet Connected")
    addr = socket.getaddrinfo('za.pycon.org', 80)[0][-1]
