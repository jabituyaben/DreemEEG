from bluepy import btle
from bluepy.btle import AssignedNumbers

class MyDelegate(btle.DefaultDelegate):
    def __init__(self, handle):
        btle.DefaultDelegate.__init__(self)
        self.handle = handle
        print ("Created delegate for handle", self.handle)
        # ... more initialise here

    def handleNotification(self, cHandle, data):
        print(str(data))
        if(cHandle == self.handle):
            f.write(data)
            f.flush()
        else:
            print(str(data)	)
# Initialisation  -------

f=open("binfile.bin","wb")
f.close()
f=open("binfile.bin","ab")

#you'll have to replace with your devices MAC address
p = btle.Peripheral( '8C:45:00:4A:93:95' )
    
svc = p.getServiceByUUID( '0000d300-0000-1000-8000-00805f9b34fb' )
EEGChar = svc.getCharacteristics('0000d301-0000-1000-8000-00805f9b34fb')[0]
print ("EEGChar", EEGChar, EEGChar.propertiesToString());

p.setDelegate(MyDelegate(157));

desc = EEGChar.getDescriptors(AssignedNumbers.client_characteristic_configuration);
configHandle = desc[0].handle

writeResponse = p.writeCharacteristic(9, b"\x02\x00", withResponse=True)
print(writeResponse)
#write device UUID
writeResponse = p.writeCharacteristic(85, b"\x38\x63\x30\x65\x33\x64\x63\x30\x2d\x37\x63\x62\x61\x2d\x34\x64\x66\x39\x2d\x39\x30\x39\x63\x2d\x37\x62\x36\x33\x63\x66\x38\x32\x39\x61\x31\x39", withResponse=True)
#Write location info
print(writeResponse)
writeResponse = p.writeCharacteristic(88, b"\x6d\x35\x09\x62\x45\x75\x72\x6f\x70\x65\x2f\x4c\x6f\x6e\x64\x6f\x6e", withResponse=True)
print(writeResponse)
#write server and API URLs - I tried changing these already but you get errors
writeResponse = p.writeCharacteristic(83, b"\x59\x00\x00\x00\x7b\x22\x75\x73\x65\x72\x5f\x61\x70\x69\x5f\x75\x72\x6c\x22\x3a\x22\x68\x74\x74\x70\x73\x3a\x2f\x2f\x61\x70\x69\x2e\x72\x79\x74\x68\x6d\x2e\x63\x6f\x2f\x76\x31\x2f\x64\x72\x65\x65\x6d\x22\x2c\x22\x75\x73\x65\x72\x5f\x61\x75\x74\x68\x5f\x75\x72\x6c\x22\x3a\x22\x68\x74\x74\x70\x73\x3a\x2f\x2f\x6c\x6f\x67\x69\x6e\x2e\x72\x79\x74\x68\x6d\x2e\x63\x6f\x22\x7d", withResponse=True)
print(writeResponse)
#bunch of other random writes, I don't know if you need these really
writeResponse = p.writeCharacteristic(47, b"\x00\x00\x00\x00", withResponse=True)
print(writeResponse)
writeResponse = p.writeCharacteristic(59, b"\xdc\x01\x00\x00\x02\x00\x00\x00", withResponse=True)
print(writeResponse)
writeResponse = p.writeCharacteristic(107, b"\x6b\x00\x00\x00", withResponse=True)
print(writeResponse)
#finally write to client characteristic config to receive notifications. Not sure how much of the above is required but if you try skipping some of it you likely won't retain a connection for very long
writeResponse = p.writeCharacteristic(configHandle, b"\x01\x00", withResponse=True)
print(writeResponse)

print ("Waiting for notifications...")

while True:
    if p.waitForNotifications(1.0):
        # handleNotification() was called
        continue

    print ("Waiting...")
