class TrieNode:
    MAX_CHILDREN = 26

    def __init__(self, value: str) -> None:
        self.value = value
        self.isWord = False
        self.children = [None] * TrieNode.MAX_CHILDREN
    