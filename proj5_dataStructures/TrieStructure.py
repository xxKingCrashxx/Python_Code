
class TrieNode:

    def __init__(self, value: str) -> None:
        self.value = value
        self.is_leaf = False
        self.word_count = 0
        self.children = []
        
def insert(root: TrieNode, word: str):
    crawl_node = root
    word_lowercase = word.lower()

    for char in word_lowercase:
        if char in crawl_node.children:
            crawl_node = crawl_node.children[char]
        else:
            new_node = TrieNode(char)
            crawl_node.children[char] = new_node
            crawl_node = new_node
    crawl_node.is_leaf = True
    crawl_node.word_count += 1


def print_trie(root: TrieNode, word = ""):
    pass

def search_trie(root: TrieNode, word: str) -> list[str]:
    pass

def is_in_trie(root: TrieNode, word: str) -> bool:
    pass
       

root = TrieNode("")
#insert(root, "eldenring")
#insert(root, "Mother")
#insert(root, "python")

#print_trie(root)