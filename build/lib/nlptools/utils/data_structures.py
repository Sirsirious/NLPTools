from collections import defaultdict

class TrieNode:

    def __init__(self, char, root=False):
        self.children = defaultdict()
        self.root = root
        self.char = char
        self.terminating = False

class Trie:
    """
    Inspired by: https://towardsdatascience.com/implementing-a-trie-data-structure-in-python-in-less-than-100-lines-of-code-a877ea23c1a1
    
    """

    def __init__(self):
        self.root = self.get_node(root=True)

    def get_node(self, char='', root=False):
        return TrieNode(char, root)

    def get_index(self, ch):
        return ord(ch) - ord('a')

    def insert(self, word):
        root = self.root
        len1 = len(word)
        for i in range(len1):
            index = self.get_index(word[i])

            if index not in root.children:
                root.children[index] = self.get_node(char=word[i])
            root = root.children.get(index)

        root.terminating = True

    def search(self, word):
        root = self.root
        len1 = len(word)
        for i in range(len1):
            index = self.get_index(word[i])
            if not root:
                return False
            root = root.children.get(index)

        return True if root and root.terminating else False

    def findall(self, prefix):
        root = self.root
        len1 = len(prefix)
        for i in range(len1):
            index = self.get_index(prefix[i])
            if not root:
                return []
            root = root.children.get(index)
        words = []
        word = prefix
        if root:
            if self.search(word):
                words.append(word)
            for children in root.children:
                new_prefix = word+root.children[children].char
                words = words + self.findall(new_prefix)
        return words
