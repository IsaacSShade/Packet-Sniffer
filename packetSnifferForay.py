"""
 * Code was created to learn network code and made alongside thenewboston's series: https://www.youtube.com/watch?v=WGJC5vT5YJo&ab_channel=thenewboston
 * Thought it was possible for a bit to unpack the ethernet frame on Windows using this approach but it's not, leaving me stuck for a bit
 * A good image to keep in mind on how packets work is with https://faculty.cs.niu.edu/~berezin/330/N/frame.html 
 *
 * PROGRAM FUNCTION: Sniffs packets and displays the IP address it's going to, where it came from, and the protocol used (if not UDP or TCP it's a number)
 * TO RUN THIS PROGRAM: it must be run in the cmd with administrator permissions
"""



import socket
import struct
import textwrap
import binascii

def main():

    host = socket.gethostbyname(socket.gethostname())
    print('IP: {}'.format(host)) #for debugging

    conn = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_IP) 

    # create a raw socket and bind it to the public interface
    conn.bind((host, 0))
    # Include IP headers
    conn.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
    #receives all packets
    conn.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)
    

    while True:

        raw_data, address = conn.recvfrom(65536)
        destination, source, protocol, data = IpFrame(raw_data)
        print('\nIPv4 Frame: ')
        #Uses placeholders in the print function just for easy printing
        print('Destination: {}, Source: {}, Protocol: {}'.format(destination, source, protocol))

# Unpacks ethernet frame
def IpFrame(data):
    #Unpacking the Ipv4 header and separating the header and the frame.
    headerLength = data[0]
    ttl, protocol, source, target = struct.unpack('! 8x B B 2x 4s 4s', data[:20]) 
    #x = no value, B = unsigned char, s = char[]
    protocolStr = ""

    if protocol == 6:
        protocolStr = "TCP"
    elif protocol == 17:
        protocolStr = "UDP"
    else:
        protocolStr = str(protocol)

    return ipv4(target), ipv4(source), protocolStr, data[headerLength:]
    #socket.htons() just converts the data flowing through's binary to computer binary

#Returns properly formatted IPv4 Packet
def ipv4(address):
    return '.'.join(map(str, address))

main()