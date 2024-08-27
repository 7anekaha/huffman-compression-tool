import sys
from huffman import HuffmanCompression

if __name__ == '__main__':
    path = sys.argv[1]

    huffman_compression = HuffmanCompression(path)

    # encode
    encoded_text = huffman_compression.encode()
    # print(encoded_text)
    huffman_compression = HuffmanCompression(path)
    decoded_text = huffman_compression.decode(path + '.huffman')
    # print(decoded_text)
    print('done')
