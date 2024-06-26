### Char Based Strategy

- The `CharBasedSendStrategy` class is designed to send covert messages using timing channels in a network. This is achieved through encoding messages into specific time intervals and sending them over a UDP network.

    - Encoding
    The `encode_message` method converts a message into a sequence of time intervals based on the predefined character-to-timing mapping. Each character is represented by a unique series of time delays.
      ```self.letter_mapping = {
            'a': [1000, 1010, 1020, 1030, 1040],
            'b': [1050, 1060, 1070, 1080, 1090],
            'c': [1100, 1110, 1120, 1130, 1140],
            'd': [1150, 1160, 1170, 1180, 1190],
       }
        ```
    - Sending
    The `send` uses a UDP socket to send a message. It sends a 'start' packet to initiate the communication and a 'done' packet to signal the end of the message.
- The `CharBasedReceiver` decodes messages by analyzing the timing of incoming network packets.
    - `receive()`
     This method listens for incoming UDP packets on a specified port.It Records the intervals between packet arrivals and calls `decode_message` to convert the intervals into the original message.
     
    - `decode_interval_sequence(interval_sequence, lateness)`
     Compares the recorded interval sequence to each character's timing sequence.
    Determines the most likely character based on the smallest average difference in timing.



