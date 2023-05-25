# hash_tableのItemの順序を管理する

class TimeItem:
    def __init__(self, url):
        self.url = url
        self.prev = None
        self.next = None

# 双方向連結リスト


class DoubleLinkedList:
    def __init__(self):
        self.head = TimeItem(None)  # ダミーの先頭ノード/新しいデータ
        self.tail = TimeItem(None)  # ダミーの末尾ノード/古いデータ
        self.head.next = self.tail
        self.tail.prev = self.head

    def add_node(self, node):  # 先頭ノードの直後にノードを挿入
        node.prev = self.head
        node.next = self.head.next
        self.head.next = node
        node.next.prev = node

    def remove_node(self, node):  # ノードを削除
        node.prev.next = node.next
        node.next.prev = node.prev

    def move_to_head(self, node):  # ノードを先頭に移動．つまりノードを削除し先頭に追加
        self.remove_node(node)
        self.add_node(node)

    # 最も古いアクセス記録を消去し、そのURL
    def remove_tail_item(self):
        removed_url = self.tail.prev.url
        self.remove_node(self.tail.prev)
        return removed_url
