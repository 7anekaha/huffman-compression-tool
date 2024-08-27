
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