from collections import Counter
from heapq import heapify, heappop, heappush
import sys
from typing import Dict


class Node:
    def __init__(self, ch, freq, left=None, right=None, is_leaf=False):
        self.ch = ch
        self.freq = freq
        self.left, self.right = left, right
        self.is_leaf = is_leaf

    def __lt__(self, other):
        return self.freq < other.freq
    
    def __str__(self):
        return self.serialize_tree()

    def serialize_tree(self):
        def preorder(root):
            if not root:
                return 'None'
            return f'{root.ch} ##{root.freq}-{root.is_leaf},,{preorder(root.left)},,{preorder(root.right)}'
        return preorder(self)

    @staticmethod    
    def deserialize_tree(serialized: str):
        values = serialized.split(',,')
        idx = 0
        def preorder():
            nonlocal idx
            if values[idx] == 'None':
                idx += 1
                return None
            print(f'values[idx]={values[idx]}')
            ch, freq = values[idx].split(' ##')
            freq, is_leaf = freq.split('-')
            print(f'{ch=}, {freq=}')
            node = Node(ch, int(freq), is_leaf = is_leaf == 'True')
            idx += 1
            node.left = preorder()
            node.right = preorder()
            return node
        
        return preorder()

class HuffmanCompression:
    def __init__(self, path: str):
        self.path = path

    def _construct_hoffman_tree(self, path: str):
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

        self.root = pq[0]
        return self.root



    def _generate_hoffman_code(self, root: Node):
        def dfs(node, code):
            if not node:
                return

            # leaf
            if not node.left and not node.right:
                table[node.ch] = code

            dfs(node.left, code + '0')
            dfs(node.right, code + '1')

        table = {}
        dfs(root, '')
        self.code = table
        return self.code

    
    def encode(self, output_path: str = None):
        self.root: Node = self._construct_hoffman_tree(path)
        self.code = self._generate_hoffman_code(self.root)

        text = []
        with open(self.path, mode='r') as file:
            for line in file.readlines():
                for ch in line:
                    text.append(self.code.get(ch))

        if output_path is None:
            output_path = self.path + '.huffman'
            
        with open(output_path, mode='w') as file:
            # write header (tree)
            file.write(str(self.root))
            Node.deserialize_tree(str(self.root))
            print('all good')
            
            file.write('\n')
            file.write('\n')
            
            # write sequence of bits
            file.write(''.join(text))


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
            
            code = self._generate_hoffman_code(root_node)
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
