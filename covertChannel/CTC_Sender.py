import random
import socket
import string
import time
from abc import ABC, abstractmethod


class SendStrategy(ABC):
    destination_ip = "localhost"
    destination_port = 12345

    @abstractmethod
    def send(self,message):
        pass
    @abstractmethod
    def encode_message(self, message):
        pass

    def generate_random_payload(self, length):
        payload = ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))
        print(payload)
        return payload


class BitBasedSendStrategy(SendStrategy):
    def __init__(self):
        self.zero_interval = 60
        self.one_interval = 120

    def encode_message(self,message):
        #convert char to decimal then binary and remove 0b from the start and fill the leftside with zero
        return ''.join( bin(ord(c))[2:] .zfill(8) for c in message)

    def send(self,message):
        msg_sequence = self.encode_message(message)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((self.destination_ip,self.destination_port))
        sock.sendall('start'.encode('utf-8'))
        start_time = time.time()
        for  digit in msg_sequence:
            if digit=='0':
                time.sleep(self.zero_interval/1000)
            else:
                time.sleep(self.one_interval/1000)
            payload = self.generate_random_payload(random.randint(1, 50))
            sock.sendall(payload.encode('utf-8'))
        ending_time = time.time()
        self.sending_peiod = ending_time - start_time
        print(f"bit rate is {len(msg_sequence)/round(ending_time-start_time,3)}")
        print(msg_sequence)


class CharBasedSendStrategy(SendStrategy):

    def __init__(self, ):
        self.sending_peiod = 0
        self.letter_mapping = {
            'a': [1000, 1010, 1020, 1030, 1040],
            'b': [1050, 1060, 1070, 1080, 1090],
            'c': [1100, 1110, 1120, 1130, 1140],
            'd': [1150, 1160, 1170, 1180, 1190],
            'e': [1200, 1210, 1220, 1230, 1240],
            'f': [1250, 1260, 1270, 1280, 1290],
            'g': [1300, 1310, 1320, 1330, 1340],
            'h': [1350, 1360, 1370, 1380, 1390],
            'i': [1400, 1410, 1420, 1430, 1440],
            'j': [1450, 1460, 1470, 1480, 1490],
            'k': [1500, 1510, 1520, 1530, 1540],
            'l': [1550, 1560, 1570, 1580, 1590],
            'm': [1600, 1610, 1620, 1630, 1640],
            'n': [1650, 1660, 1670, 1680, 1690],
            'o': [1700, 1710, 1720, 1730, 1740],
            'p': [1750, 1760, 1770, 1780, 1790],
            'q': [1800, 1810, 1820, 1830, 1840],
            'r': [1850, 1860, 1870, 1880, 1890],
            's': [1900, 1910, 1920, 1930, 1940],
            't': [1950, 1960, 1970, 1980, 1990],
            'u': [2000, 2010, 2020, 2030, 2040],
            'v': [2050, 2060, 2070, 2080, 2090],
            'w': [2100, 2110, 2120, 2130, 2140],
            'x': [2150, 2160, 2170, 2180, 2190],
            'y': [2200, 2210, 2220, 2230, 2240],
            'z': [2250, 2260, 2270, 2280, 2290],
            ' ': [2300, 2310, 2320, 2330, 2340],
            '.': [2350, 2360, 2370, 2380, 2390],
            '?': [2400, 2410, 2420, 2430, 2440],
            '>': [2450, 2460, 2470, 2480, 2490],
            '<': [2500, 2510, 2520, 2530, 2540],
            '}': [2550, 2560, 2570, 2580, 2590],
            '{': [2600, 2610, 2620, 2630, 2640],
            ']': [2650, 2660, 2670, 2680, 2690],
            '[': [2700, 2710, 2720, 2730, 2740],
            '-': [2750, 2760, 2770, 2780, 2790],
            ')': [2800, 2810, 2820, 2830, 2840],
            '(': [2850, 2860, 2870, 2880, 2890],
            '*': [2900, 2910, 2920, 2930, 2940],
            '&': [2950, 2960, 2970, 2980, 2990],
            '%': [3000, 3010, 3020, 3030, 3040],
            '$': [3050, 3060, 3070, 3080, 3090],
            '#': [3100, 3110, 3120, 3130, 3140],
            '@': [3150, 3160, 3170, 3180, 3190],
            '_': [3200, 3210, 3220, 3230, 3240],
            '+': [3250, 3260, 3270, 3280, 3290],
            '=': [3300, 3310, 3320, 3330, 3340],
            '/': [3350, 3360, 3370, 3380, 3390],
            '\\': [3400, 3410, 3420, 3430, 3440],
            '!': [3450, 3460, 3470, 3480, 3490],
            ',': [3500, 3510, 3520, 3530, 3540]
        }

    def encode_message(self,message):
        encoded_sequence = []
        for letter in message.lower():
            if letter in self.letter_mapping:
                # print(letter)
                encoded_sequence.extend(self.letter_mapping[letter])
                encoded_sequence.append(10)  # append the sixth packet delay which is 10 milli seconds
        # print(len(encoded_sequence))
        return encoded_sequence

    def send(self,message):
        # creates a UDP socket, socket.SOCK_DGRAM specifies that the
        # socket object is used for udp communication and socket.AF_INET
        # specifies the adress family which is ipv4
        msg_sequence = self.encode_message(message)
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.sendto('start'.encode('utf-8'), (self.destination_ip, self.destination_port))  # send a udp packet
        start_time = time.time()
        for i, interval in enumerate(msg_sequence):
            if i == len(msg_sequence) - 1:
                payload = 'done'
            else:
                payload = self.generate_random_payload(random.randint(1, 100))
            # print(payload)
            time.sleep(interval / 1000)
            sock.sendto(payload.encode('utf-8'), (self.destination_ip, self.destination_port))  # send a udp packet
        ending_time = time.time()
        self.sending_peiod = ending_time - start_time

class Sender:
    def __init__(self):
        self.send_strategy = None

    def set_send_strategy(self, send_strategy):
        self.send_strategy = send_strategy

    def send_data(self, data):
        if self.send_strategy:
            self.send_strategy.send(data)
        else:
            raise ValueError("No send strategy set.")

sender = Sender()
sender.set_send_strategy(BitBasedSendStrategy())
sender.send_data("Hello, TCP secret!")


