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
        tree_serialized = root.serialize_tree()
        len_tree_serialized = len(tree_serialized).to_bytes(4, byteorder='big')
        print(len_tree_serialized)
        
        with open(path + '.huffman', mode='wb') as file:
            file.write(len_tree_serialized)
            file.write(b'\n')
            file.write(tree_serialized.encode())
            file.write(b'\n')
            file.write(f'{padding}'.encode())
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
        
        with open(input_path, mode='r') as file, open(output_path, mode='w') as output_file:
            # read header
            idx = 0
            root = []
            while True:
                block = file.read(64 * 1024)
                if not block:
                    break
                root.append(block)
                for i, ch in enumerate(block):
                    if ch == '\n':
                        if i > 0 and block[i-1] == '\n':
                            idx = i-1
                            break
                        if i == 0 and root and root[-1] == '\n':
                            idx = 1
                            break
                
            root = ''.join(root)
            # print(f'{root[:idx]=}')
            root_node = Node.deserialize_tree(root[:idx])
            
            code = self._generate_hoffman_table(root_node)
            print(f'{code=}')
            
            node = root_node
            
            idx += 2
            if root[idx:]:
                for ch in root[idx:]:
                    print(f'{ch=}')
                    node = node.left if ch == '0' else node.right # type: ignore
                    print(f'{node=}')
                    if node.is_leaf: # type: ignore
                        output_file.write(node.ch)
                        node = root_node
                        print('done')
            
            # read sequence of bits - in 64kb blocks
            while True:
                block = file.read(64 * 1024)
                if not block:
                    break
                for ch in block:
                    node = node.left if ch == '0' else node.right # type: ignore
                    if node.is_leaf: # type: ignore
                        output_file.write(node.ch)
                        node = root_node
                





