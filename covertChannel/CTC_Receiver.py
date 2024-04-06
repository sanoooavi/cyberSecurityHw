import socket
import time
from abc import ABC, abstractmethod


class ReceiverStrategy(ABC):
    IP = "localhost"
    PORT = 12345

    @abstractmethod
    def receive(self):
        pass


class BitBasedReceiver(ReceiverStrategy):
    def __init__(self):
        self.zero_interval = 60
        self.one_interval = 120

    def decode_message(self, binary_text):
        secret = ''
        for i in range(0, len(binary_text), 8):
            binary_chunk = binary_text[i:i + 8]
            secret += chr(int(binary_chunk, 2))
        return secret

    def receive(self):
        server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_sock.bind((self.IP, self.PORT))
        server_sock.listen()
        client_socket, client_adress = server_sock.accept()
        encrypted = ""
        while True:
            t1 = time.time()
            data ,_= client_socket.recvfrom(1024)
            t2 = time.time()
            # print(data.decode('utf-8'))
            if data.decode('utf-8') == 'start':
                continue
            if not data:
                break
            if round(t2 - t1,3) >= (self.one_interval / 1000):
                encrypted += '1'
            else:
                encrypted += '0'
        decoded_message = self.decode_message(encrypted)
        print(f"The secret message is: {decoded_message}")
        return decoded_message



class CharBasedReceiver(ReceiverStrategy):

    def __init__(self):
        # Mapping of letters to sequences of five numbers (representing inter-arrival times in milliseconds)
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

    def receive(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind(('', self.PORT))
        received_intervals = []
        while True:
            t1 = time.time()
            data, _ = sock.recvfrom(1024)
            t2 = time.time()
            # print(round(t2 - t1, 4))
            print(data.decode('utf-8'))
            # if not data:
            #     break
            if data.decode('utf-8') == 'start':
                continue
            received_intervals.append(round(t2 - t1, 4) * 1000)
            # print(received_intervals)
            if data.decode('utf-8') == 'done':
                break
        # print("done getting the data")
        decoded_message = self.decode_message(received_intervals)
        print(f"The secret message is: {decoded_message}")
        return decoded_message

    def decode_message(self, received_intervals):
        decoded_message = []
        # print(len(received_intervals))
        for i in range(0, len(received_intervals), 6):  # Interval for each letter plus the expected packet
            interval_sequence = received_intervals[i:i + 5]
            # print(interval_sequence)
            if len(interval_sequence) != 5:
                raise RuntimeError("The data was not received correctly")
                break
            decoded_letter = self.decode_interval_sequence(interval_sequence, received_intervals[i + 5])
            decoded_message.append(decoded_letter)
        return ''.join(decoded_message)

    def decode_interval_sequence(self, interval_sequence, lateness):
        min_diff = float('inf')
        maximum_overall_lateness = lateness * len(interval_sequence)
        most_likely_letter = None
        for letter, sequence in self.letter_mapping.items():
            diffs = [abs(interval - seq) for interval, seq in zip(interval_sequence, sequence)]
            avg_diff = sum(diffs) / len(diffs)
            if avg_diff < min_diff and sum(diffs) < maximum_overall_lateness:
                min_diff = avg_diff
                most_likely_letter = letter
        return most_likely_letter

class Receiver:
    def __init__(self):
        self.receive_strategy = None

    def set_receive_strategy(self, receive_strategy):
        self.receive_strategy = receive_strategy

    def receive_data(self):
        if self.receive_strategy:
            self.receive_strategy.receive()
        else:
            raise ValueError("No receive strategy set.")

rcv = Receiver()
rcv.set_receive_strategy(BitBasedReceiver())
rcv.receive_data()
