import random
import my_graph as mg

# 测试用例1: word1 和 word2 都在图中，并且存在一个桥接词
def test_single_bridge_word():
    G = mg.Graph()
    G.graph.add_edge('word1', 'bridge')
    G.graph.add_edge('bridge', 'word2')
    assert mg.Graph.query_bridge_words(G, 'word1', 'word2') == "The bridge words from word1 to word2 are: bridge."

# 测试用例2: word1 和 word2 都在图中，但没有桥接词
def test_no_bridge_word():
    G = mg.Graph()
    G.graph.add_node('word1')
    G.graph.add_node('word2')
    assert mg.Graph.query_bridge_words(G, 'word1', 'word2') == "No bridge words from word1 to word2!"

# 测试用例3: word1 不在图中
def test_word1_not_in_graph():
    G = mg.Graph()
    G.graph.add_node('word2')
    assert mg.Graph.query_bridge_words(G, 'word1', 'word2') == "No word1 or word2 in the graph!"

# 测试用例4: word2 不在图中
def test_word2_not_in_graph():
    G = mg.Graph()
    G.graph.add_node('word1')
    assert mg.Graph.query_bridge_words(G, 'word1', 'word2') == "No word1 or word2 in the graph!"

# 测试用例5: word1 和 word2 都不在图中
def test_neither_word_in_graph():
    G = mg.Graph()
    assert mg.Graph.query_bridge_words(G, 'word1', 'word2') == "No word1 or word2 in the graph!"

# 测试用例6: 图中有多个桥接词
def test_multiple_bridge_words():
    G = mg.Graph()
    G.graph.add_edge('word1', 'bridge1')
    G.graph.add_edge('bridge1', 'word2')
    G.graph.add_edge('word1', 'bridge2')
    G.graph.add_edge('bridge2', 'word2')
    assert mg.Graph.query_bridge_words(G, 'word1', 'word2') == "The bridge words from word1 to word2 are: bridge1, bridge2."



# 设置随机种子以确保测试的可重复性
random.seed(0)

# 创建一个图
G = mg.Graph()
G.graph.add_edges_from([('A', 'B'), ('B', 'C'), ('C', 'D'), ('D', 'A'), ('A', 'C')])

# 测试用例
def test_random_walk():
    # 执行 randomWalk 函数

    walk_result = mg.Graph.random_walk(G)
    # 验证 walk_result 是否为有效路径
    assert all(walk_result[i] in G.graph.neighbors(walk_result[i-1]) for i in range(1, len(walk_result)))

# 用于模拟用户输入的函数
def input(prompt):
    # 控制测试用例中的用户输入
    # 在第三次调用时停止遍历
    input.counter += 1
    if input.counter == 3:
        return 'stop'
    return ''

# 初始化计数器
input.counter = 0

if __name__ == '__main__':
    #main()
    #黑盒
    test_single_bridge_word()
    test_no_bridge_word()
    test_word1_not_in_graph()
    test_word2_not_in_graph()
    test_neither_word_in_graph()
    test_multiple_bridge_words()
    #白盒
    test_random_walk()
