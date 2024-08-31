# Build your own compression tool (Coding Challenges)
This is a coding challenge found: [https://codingchallenges.fyi/challenges/challenge-huffman/|https://codingchallenges.fyi/challenges/challenge-huffman/]

## How to run
1. Clone the repository
2. Create a virtual environment
3. Install the requirements
4. Run the main.py file or install the package with pip install -e .

## How to use
To compress a file:
```bash
huff-zip compress --input sample.txt --output sample.bin
```

To decompress a file:
```bash
huff-zip decompress --input sample.bin --output sample-decoded.txt
```

## How it works
### Compression
1. Read the file and count the frequency of each character
2. Create a priority queue with the frequency of each character
3. Create a binary tree with the priority queue (huffman tree)
4. Create a dictionary with the binary code of each character
5. Encode the file using the dictionary
6. Write the binary code to a file

### Decompression
1. Read the file and decode the binary code using the huffman tree
2. Write the decoded file to a new file
