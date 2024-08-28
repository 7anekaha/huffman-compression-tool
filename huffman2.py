from collections import Counter
from heapq import heapify, heappop, heappush
from typing import Dict, Tuple
from tree import Node

class HuffmanCompression:
    def __init__(self, path: str = None):
        self.path = path
            
    def encode(self):
        
        path = self.path
        
        # construct hoffman tree
        root: Node = self._construct_hoffman_tree()
        # generate hoffman table
        table: Dict[str, str] = self._generate_hoffman_table(root)
        
        # encode text - sequence of bits in bitsarray - store padding
        content, padding = self._encode(table, path)
        
        # write to file
        #   - length of tree as string
        #   - tree as string
        #   - padding
        #   - sequence of bits
        # file = len tree(4bytes) \n tree \n padding (1byte) \n sequence of bits
        tree_serialized = root.serialize_tree()
        len_tree_serialized = len(tree_serialized).to_bytes(4, byteorder='big')
        padding = padding.to_bytes(1, byteorder='big')
        print(len_tree_serialized)
        
        with open(path + '.huffman', mode='wb') as file:
            file.write(len_tree_serialized)
            file.write(b'\n')
            file.write(tree_serialized.encode())
            file.write(b'\n')
            file.write(padding)
            file.write(b'\n')
            file.write(content)
        
        print('done encoding')        

    def _construct_hoffman_tree(self):
        """ Construct hoffman tree from file """
        path = self.path
        freq = Counter()
        with open(path, mode='r') as file:
            for line in file.readlines():
                for ch in line:
                    freq[ch] += 1
        nodes = [Node(k, v, is_leaf = True) for k, v in freq.items()]
        heapify(nodes)

        pq = nodes
        while len(pq) > 1:
            left, right = heappop(pq), heappop(pq)
            root = Node(None, left.freq + right.freq, left, right)
            heappush(pq, root)

        
        return pq[0] # root



    def _generate_hoffman_table(self, root: Node) -> Dict[str, str]:
        """ Generate hoffman table from hoffman tree - character: code"""
        def preorder(node, code):
            if not node:
                return

            # leaf
            if not node.left and not node.right:
                table[node.ch] = code

            preorder(node.left, code + '0')
            preorder(node.right, code + '1')

        table = {}
        preorder(root, '')
        return table

    
    def _encode(self, table: Dict[str, str], path: str) -> Tuple[bytearray, int]:
        encoded_text = bytearray()
        left = 8
        current_sequence = ''
        with open(path, mode='r') as file:
            while True:
                block = file.read(64 * 1024)
                if not block:
                    break
                for ch in block:
                    sequence = table[ch]
                    current_sequence += sequence
                    while len(current_sequence) >= 8:
                        byte = int(current_sequence[:8], 2)
                        encoded_text.append(byte)
                        current_sequence = current_sequence[8:]
        
        if current_sequence:
            padding = 8 - len(current_sequence)
            encoded_text.append(int(current_sequence + '0' * padding, 2))
        
        return encoded_text, padding                        
                        

    def decode(self, input_path, output_path: str = None):
        if output_path is None:
            output_path = self.path + '.decoded'
        
        with open(input_path, mode='rb') as file, open(output_path, mode='w') as output_file:
            # read len tree
            len_tree = int.from_bytes(file.read(4), byteorder='big')
            
            # read jump line
            file.read(1)
            
            # read tree
            tree = file.read(len_tree).decode()
            
            # convert tree to node
            root = Node.deserialize_tree(tree)
            
            # read jump line
            file.read(1)
            
            # read padding
            padding = int.from_bytes(file.read(1), byteorder='big')
            
            # read jump line
            file.read(1)
            
            # read sequence of bits
            content = file.read()
            
            # remove padding
            content = content[:len(content) - padding]
            
            # decode
            sequence = ''
            node = root
            for b in content:
                sequence += f'{b:08b}'
                while len(sequence) >= 8:
                    ch = sequence[0]
                    sequence = sequence[1:]
                    node = node.left if ch == '0' else node.right
                    if node.is_leaf:
                        output_file.write(node.ch)
                        node = root
            
            while len(sequence) >= 8:
                ch = sequence[0]
                sequence = sequence[1:]
                node = node.left if ch == '0' else node.right
                if node.is_leaf:
                    output_file.write(node.ch)
                    node = root
                            
                    
                    
                



