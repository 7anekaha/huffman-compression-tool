from pathlib import Path
from collections import Counter
from heapq import heapify, heappop, heappush
from typing import Dict, Tuple
from tree import Node


class HuffmanTree:

    @staticmethod
    def construct(path: Path) -> Node:
        """Construct hoffman tree from file"""
        freq = Counter()
        with open(path, mode="r") as file:
            for line in file.readlines():
                for ch in line:
                    freq[ch] += 1
        nodes = [Node(k, v, is_leaf=True) for k, v in freq.items()]
        heapify(nodes)

        pq = nodes
        while len(pq) > 1:
            left, right = heappop(pq), heappop(pq)
            root = Node(None, left.freq + right.freq, left, right)
            heappush(pq, root)

        return pq[0]  # root

    @staticmethod
    def generate_table(root: Node) -> Dict[str, str]:
        """Generate hoffman table from hoffman tree - character: code"""

        table = {}
        stack = [(root, "")]
        while stack:
            node, seq = stack.pop()

            if node.is_leaf:
                table[node.ch] = seq
                continue
            if node.right:
                stack.append((node.right, seq + "1"))

            if node.left:
                stack.append((node.left, seq + "0"))

        return table


class HuffmanCompression:
    @staticmethod
    def encode(path: Path, output_path: Path = Path("encoded.bin")):
        def _encode(table: Dict[str, str], path: Path) -> Tuple[bytearray, int]:
            encoded_text = bytearray()
            padding = 0
            current_sequence = ""
            with open(path, mode="r") as file:
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
                encoded_text.append(int(current_sequence + "0" * padding, 2))

            return encoded_text, padding

        # construct hoffman tree
        root: Node = HuffmanTree.construct(path)

        # generate hoffman table
        table: Dict[str, str] = HuffmanTree.generate_table(root)

        # encode text - sequence of bits in bitsarray - store padding
        content, padding = _encode(table, path)

        # write to file
        #   - length of tree as string
        #   - tree as string
        #   - padding
        #   - sequence of bits
        # file = len tree(4bytes) \n tree \n padding (1byte) \n sequence of bits
        tree_serialized = root.serialize_tree()
        len_tree_serialized = len(tree_serialized).to_bytes(4, byteorder="big")
        padding = padding.to_bytes(1, byteorder="big")

        with open(output_path, mode="wb") as file:
            file.write(len_tree_serialized)
            file.write(b"\n")
            file.write(tree_serialized.encode())
            file.write(b"\n")
            file.write(padding)
            file.write(b"\n")
            file.write(content)

        print("encoding done")

    @staticmethod
    def decode(input_path: Path, output_path: Path = Path("decoded.txt")):

        padding = 0
        with open(input_path, mode="rb") as file, open(
            output_path, mode="w"
        ) as output_file:
            # read len tree
            len_tree = int.from_bytes(file.read(4), byteorder="big")

            # read jump line
            file.read(1)

            # read tree
            tree = file.read(len_tree).decode()

            # convert tree to node
            root = Node.deserialize_tree(tree)

            # read jump line
            file.read(1)

            # read padding
            padding = int.from_bytes(file.read(1), byteorder="big")

            # read jump line
            file.read(1)

            # read sequence of bits
            sequence = f'{int.from_bytes(file.read(1), "big"):08b}'

            node = root
            while True:
                current = file.read(1)
                if not current:
                    sequence = sequence[: len(sequence) - padding]
                    break

                while sequence:
                    ch = sequence[0]
                    sequence = sequence[1:]
                    node = node.left if ch == "0" else node.right
                    if node.is_leaf:
                        output_file.write(node.ch)
                        node = root

                sequence += f'{int.from_bytes(current, "big"):08b}'

            while sequence:
                ch = sequence[0]
                sequence = sequence[1:]
                node = node.left if ch == "0" else node.right
                if node.is_leaf:
                    output_file.write(node.ch)
                    node = root
