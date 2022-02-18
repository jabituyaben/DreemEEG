from bitstring import ConstBitStream, BitArray
import matplotlib.pyplot as plt

dict = {
    "x190": [],
    "x191": [],
    "x192": [],
    "x193": [],
    "x194": [],
    "x195": [],
    "x196": [],
    "x197": [],
    "x198": [],
    "x199":[],
    "x200":[],
    "x186":[],
    "x187":[],
    "x186":[],
    "x188":[],
    "x189":[],
    "x59":[],
    "x60":[],
    "x61":[],
    "x62": [],
    "x63": [],
    "x64": [],
    "x65": [],
    "x66": [],
    "x67": [],
    "x68": [],
    "x69": [], 
    "x70": [],
    "x71": []
}

f=open("binfile.bin","rb")
bArray = BitArray(f)
print(len(bArray))

EOF = len(bArray)-32

x = ConstBitStream(bArray)

i = 0

while i == 0:
    x.pos += 8
    i = x.read('uintle:8')

x.pos -= 16

breakloop = False

while x.pos < EOF:
    val = []
    for index in range(3):
        val.append(x.read('uintle:8'))
    channelNumber = x.read('uintle:8')
    channel = 'x' + str(channelNumber)
    if channel != "x0":
        dict[channel].extend(val)
    elif channelNumber == 0:
        while channelNumber == 0:
            if x.pos >= EOF:
                breakloop = True
                break
            else:
                x.pos += 8
        if breakloop == True:
            break
        else:
            x.pos -= 16
    else:
        print("missing channel")
        print(channel)
        break

vals = dict.items()
for Channel in vals:
    print(Channel[0] + " " + str(len(Channel[1])))

plt.specgram(dict['x195'], Fs=150, cmap='Spectral_r')
#plt.plot(dict['x195'])
plt.show()
