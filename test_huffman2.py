import tempfile
import pytest

from huffman2 import HuffmanCompression, HuffmanTree
from tree import Node


@pytest.fixture
def tmp_file():
    with tempfile.NamedTemporaryFile(mode='w') as file:
        file.write('hello')
        
        file.seek(0)
        
        yield file

@pytest.fixture
def tmp_root():
    with tempfile.NamedTemporaryFile(mode='w') as file:
        file.write('hello')
        
        file.seek(0)
        
        root : Node = HuffmanTree.construct(file.name)
        yield root
    
class TestHuffmanTree:
    
    def test_construct(self, tmp_file):
        """check if the tree is constructed correctly"""
        path = tmp_file.name
        root : Node = HuffmanTree.construct(path)
                
        assert root.serialize_tree() == 'None ##5-False,,None ##2-False,,o ##1-True,,None,,None,,e ##1-True,,None,,None,,None ##3-False,,h ##1-True,,None,,None,,l ##2-True,,None,,None'
        
        

    def test_generate_table(self, tmp_root):
        """check if codes are generated correctly"""
        root = tmp_root
        table = HuffmanTree.generate_table(root)
        
        assert table == {'o': '00', 'e': '01', 'h': '10', 'l': '11'}
        

class TestHuffmanCompression:
    def test_encode(self, tmp_file):
        path = tmp_file.name
        HuffmanCompression.encode(path)
        
        with open(path + '.huffman', mode='rb') as file:
            content = file.read()
                        
            assert content == b'\x00\x00\x00\x8e\nNone ##5-False,,None ##2-False,,o ##1-True,,None,,None,,e ##1-True,,None,,None,,None ##3-False,,h ##1-True,,None,,None,,l ##2-True,,None,,None\n\x06\n\x9f\x00'
            
    def test_decode(self, tmp_file):
        path = tmp_file.name
        HuffmanCompression.encode(path)
        
        HuffmanCompression.decode(path + '.huffman', path + '.huffman.decoded')
        
        with open(path + '.huffman.decoded', mode='r') as file:
            content = file.read()
            print(content)
            
            assert content == 'hello'
        
            
            
            
            