# LSB Steganography

This project implements a steganographic method, which consists in hiding messages in the lower bits of the image (png or bmp formats).
This method can be used to hide information in images saved in bmp, png format

##### Installation
```bash
pip3 install -r requirements.txt
```

#### A little bit about the algorithm
Random pixels of the image are used to hide the text. To obtain a sequence of pixels, a random generator (numpy.random) is initialized with a seed obtained by taking the first 4 bytes of the sha256 hash from the password.

The hidden message itself is represented as a sequence of bits. Three bits from the message are written to the next pixel, one in each channel.
