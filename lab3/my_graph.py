# /lab3/my_graph.py
"""
这个模块提供了用于处理和分析文本生成图的功能，包括读取文本数据，生成有向图，
以及展示图形，查询桥接词，生成基于桥接词的新文本，计算最短路径和进行随机游走。

主要包含两个类: Text 和 Graph，分别用于文本处理和图的操作。
"""
import re
import string
import random
import matplotlib.pyplot as plt
import networkx as nx
from networkx.algorithms.shortest_paths.weighted import _weight_function
from heapq import heappush, heappop
from itertools import count


# 词语，类即中间操作
class Text :
    """
    处理和储存文本数据的类。

    属性:
        text (str): 原始文本字符串。
        words (list): 分割后的单词列表。

    方法:
        split: 对输入的文本进行清洗和分词。
        __add__: 实现两个Text实例的相加，合并文本。
    """
    def __init__(self, text):
        """
        初始化Text实例，保存原始文本并进行分词。

        参数:
            text (str): 输入的原始文本。
        """
        self.text = text
        self.words = self.split(self.text)

    # 功能: 清理文本、分割单词
    def split(self, text):
        """
        清洗文本并按空白字符分词。

        参数:
            text (str): 需要被处理的文本。

        返回:
            list: 包含文本中所有单词的列表。
        """
        text = re.sub(f'[{string.punctuation}]', '', text)
        words = text.split()
        return words

    # 相加
    def __add__(self, other):
        return Text(self.text + other.text)

# 图
class Graph:
    """
    基于文本生成有向图，并提供图操作的功能。

    属性:
        path (str): 文件路径。
        file (Text): Text类实例，包含文件文本和单词列表。
        graph (networkx.DiGraph): 表示文本的有向图。

    方法:
        read: 从文件中读取文本。
        createGraph: 根据单词列表创建有向图。
        showDirectedGraph: 展示有向图。
        queryBridgeWords: 查询两个单词间的桥接词。
        generateNewText: 根据桥接词生成新文本。
        calcShortestPath: 计算两单词间的最短路径。
        randomWalk: 在图上进行随机游走。
    """
    def __init__(self, path = 'input.txt'): # D:/[study]/[studying]/软件工程/lab/lab1/input.txt
        """
        初始化Graph实例。

        参数:
            path (str): 文件路径，默认为'input.txt'。
        """
        self.path = path
        self.file = Text(self.read(self.path))
        self.graph = self.createGraph(self.file.words)

    # 功能: 读取文件
    def read(self, file_path):
        """
        从文件中读取文本并转换为小写。

        参数:
            file_path (str): 文件路径。

        返回:
            str: 读取并转换为小写的文本内容。
        """
        with open(file_path, 'r', encoding='utf-8') as file:
            text = file.read().lower()
        return text

    # 功能: 创建有向图
    def createGraph(self, words):
        """
        根据单词列表创建有向图。

        参数:
            words (list): 单词列表。

        返回:
            networkx.DiGraph: 创建的有向图。
        """
        graph = nx.DiGraph()
        for i in range(len(words) - 1):
            if graph.has_edge(words[i], words[i+1]):
                graph[words[i]][words[i+1]]['weight'] += 1
            else:
                graph.add_edge(words[i], words[i+1], weight=1)
        return graph

    # 功能: 用plt绘制有向图
    def showDirectedGraph(self):
        """
        展示有向图。
        """
        pos = nx.spring_layout(self.graph)
        edge_labels = nx.get_edge_attributes(self.graph, 'weight')
        nx.draw(self.graph, pos, with_labels=True, node_size=1500,
                node_color='lightblue', font_size=8)
        nx.draw_networkx_edge_labels(self.graph, pos, edge_labels=edge_labels, font_color='red')
        plt.savefig("./out/graph.png") # {self.file.file_path}
        plt.show()

    # 功能: 查询桥接词 word1 -> word3 -> word2
    def queryBridgeWords(self, word1, word2):
        """
        查询两个单词间的桥接词。

        参数:
            word1 (str): 起始词。
            word2 (str): 终止词。

        返回:
            str: 包含桥接词的字符串。
        """
        if word1 not in self.graph or word2 not in self.graph:
            return f"No {word1} or {word2} in the graph!"
        bridge_words = [word3 for word3 in self.graph if self.graph.has_edge(word1, word3)
                        and self.graph.has_edge(word3, word2)]
        if not bridge_words:
            return f"No bridge words from {word1} to {word2}!"
        return f"The bridge words from {word1} to {word2} is: " + ', '.join(bridge_words) + "."

    # 根据bridge word生成新文本
    # 先分解为词列表，遍历查询, 如果存在桥接词，随机插入
    def generateNewText(self, text):
        """
        根据桥接词生成新文本。

        参数:
            text (str): 输入的文本。
        """
        words = Text(text)
        # 句首词首字母大写 待完成
        new_text = words.words[0]
        for i in range(len(words.words) - 1):
            bridge_words = [word3 for word3 in self.graph
                            if self.graph.has_edge(words.words[i], word3)
                            and self.graph.has_edge(word3, words.words[i+1])]
            if bridge_words:
                bridge_word = random.choice(bridge_words)
                new_text += ' ' + bridge_word
            new_text += ' ' + words.words[i+1]
        print(new_text)

    # 计算两个单词之间的最短路径
    def calcShortestPath(self, word1, word2):
        """
        计算两个单词之间的最短路径。

        参数:
            word1 (str): 起始词。
            word2 (str): 终止词。

        返回:
            tuple: 包含最短路径和路径长度。
        """
        try:
            # 计算最短路径
            path_length, shortest_path = dijkstra(self.graph, source=word1, target=word2,
                                                  weight='weight')

            # 原图
            pos = nx.spring_layout(self.graph)
            nx.draw(self.graph, pos, with_labels=True, node_color='lightblue', font_size=8)

            # 突出
            path_edges = list(zip(shortest_path[:-1], shortest_path[1:]))
            nx.draw_networkx_nodes(self.graph, pos, nodelist=shortest_path, node_color='red')
            nx.draw_networkx_edges(self.graph, pos, edgelist=path_edges, edge_color='red', width=2)
            plt.show()

            return shortest_path, path_length
        except nx.NetworkXNoPath:
            return "这两个单词不可达。"

    #功能: 游走
    def randomWalk(self):
        """
        在图上进行随机游走。
        """
        # 随机选择节点
        current_node = random.choice(list(self.graph.nodes))
        visited_edges = set()
        walk = [current_node]

        #遍历节点出边
        while True:
            neighbors = list(self.graph[current_node])
            if not neighbors or all((current_node, neighbor) in visited_edges
                                    for neighbor in neighbors):
                break

            # 随机访问
            next_node = random.choice([neighbor for neighbor in neighbors
                                       if (current_node, neighbor) not in visited_edges])
            visited_edges.add((current_node, next_node))
            walk.append(next_node)
            current_node = next_node

            if input("按Enter键继续遍历，输入任何内容后按Enter键停止遍历: ").strip():
                print("遍历停止。")
                break

        print("遍历的节点:", walk)
        write_walk_to_file(walk, './out/random_walk.txt')
        print("遍历的节点已写入文件 'random_walk.txt'。")

def split(text):
    """
    清洗文本并按空白字符分词。

    参数:
        text (str): 需要被处理的文本。

    返回:
        list: 包含文本中所有单词的列表。
    """
    text = re.sub(f'[{string.punctuation}]', '', text)
    words = text.split()
    return words

def write_walk_to_file(walk, file_name):
    """
    将随机游走的节点写入文件。

    参数:
        walk (list): 随机游走的节点列表。
        file_name (str): 文件路径。
    """
    with open(file_name, 'w', encoding='utf-8') as file:
        file.write(' '.join(walk))

def dijkstra(graph, source_node, target_node, weight="weight"):
    """
    计算图graph中从源节点source_node到目标节点target_node的最短路径。

    参数:
        graph (networkx.Graph): 输入图。
        source_node (node): 起始节点。
        target_node (node): 终止节点。
        weight (str or function): 边的权重。

    返回:
        tuple: 包含最短路径和路径长度。
    """
    if source_node not in graph or target_node not in graph:
        message = f"Either source {source_node} or target {target_node} is not in graph"
        raise nx.NodeNotFound(message)

    if source_node == target_node:
        return (0, [source_node])

    weight_func = _weight_function(graph, weight)
    push = heappush
    pop = heappop
    distances = [{}, {}]
    paths = [{source_node: [source_node]}, {target_node: [target_node]}]
    fringe = [[], []]
    seen = [{source_node: 0}, {target_node: 0}]
    counter = count()
    push(fringe[0], (0, next(counter), source_node))
    push(fringe[1], (0, next(counter), target_node))
    if graph.is_directed():
        neighbors = [graph._succ, graph._pred]
    else:
        neighbors = [graph._adj, graph._adj]
    final_path = []
    direction = 1
    while fringe[0] and fringe[1]:
        direction = 1 - direction
        (distance, _, vertex) = pop(fringe[direction])
        if vertex in distances[direction]:
            continue
        distances[direction][vertex] = distance
        if vertex in distances[1 - direction]:
            return (final_distance, final_path)

        for neighbor, edge_data in neighbors[direction][vertex].items():
            if direction == 0:
                vw_length = distances[direction][vertex] + weight_func(vertex, neighbor, edge_data)
            else:
                vw_length = distances[direction][vertex] + weight_func(neighbor, vertex, edge_data)
            if neighbor in distances[direction]:
                if vw_length < distances[direction][neighbor]:
                    raise ValueError("Contradictory paths found: negative weights?")
            elif neighbor not in seen[direction] or vw_length < seen[direction][neighbor]:
                seen[direction][neighbor] = vw_length
                push(fringe[direction], (vw_length, next(counter), neighbor))
                paths[direction][neighbor] = paths[direction][vertex] + [neighbor]
                if neighbor in seen[0] and neighbor in seen[1]:
                    total_distance = seen[0][neighbor] + seen[1][neighbor]
                    if final_path == [] or final_distance > total_distance:
                        final_distance = total_distance
                        reverse_path = paths[1][neighbor][:]
                        reverse_path.reverse()
                        final_path = paths[0][neighbor] + reverse_path[1:]
    raise nx.NetworkXNoPath(f"No path between {source_node} and {target_node}.")
