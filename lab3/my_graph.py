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
# from itertools import count


class Text:
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

        parameters:
            text (str): 输入的原始文本。
        """
        self.text = text
        self.words = self.split(self.text)

    def split(self, text):
        """
        清洗文本并按空白字符分词。

        parameters:
            text (str): 需要被处理的文本。

        return:
            list: 包含文本中所有单词的列表。
        """
        text = re.sub(f'[{string.punctuation}]', '', text)
        words = text.split()
        return words

    def __add__(self, other):
        return Text(self.text + other.text)


class Graph:
    """
    基于文本生成有向图，并提供图操作的功能。

    属性:
        path (str): 文件路径。
        file (Text): Text类实例，包含文件文本和单词列表。
        graph (networkx.DiGraph): 表示文本的有向图。

    方法:
        read: 从文件中读取文本。
        create_graph: 根据单词列表创建有向图。
        show_directed_graph: 展示有向图。
        query_bridge_words: 查询两个单词间的桥接词。
        generate_new_text: 根据桥接词生成新文本。
        calc_shortest_path: 计算两单词间的最短路径。
        random_walk: 在图上进行随机游走。
    """
    def __init__(self, path='input.txt'):  # D:/[study]/[studying]/软件工程/lab/lab1/input.txt
        """
        初始化Graph实例。

        parameters:
            path (str): 文件路径，默认为'input.txt'。
        """
        self.path = path
        self.graph = nx.DiGraph()
        if path is not None:
            self.file = Text(self.read(self.path))
            self.graph = self.create_graph(self.file.words)

    def read(self, file_path):
        """
        从文件中读取文本并转换为小写。

        parameters:
            file_path (str): 文件路径。

        return:
            str: 读取并转换为小写的文本内容。
        """
        with open(file_path, 'r', encoding='utf-8') as file:
            text = file.read().lower()
        return text

    def create_graph(self, words):
        """
        根据单词列表创建有向图。

        parameters:
            words (list): 单词列表。

        return:
            networkx.DiGraph: 创建的有向图。
        """
        graph = nx.DiGraph()
        for i in range(len(words) - 1):
            if graph.has_edge(words[i], words[i+1]):
                graph[words[i]][words[i+1]]['weight'] += 1
            else:
                graph.add_edge(words[i], words[i+1], weight=1)
        return graph

    def show_directed_graph(self):
        """
        展示有向图。
        """
        pos = nx.spring_layout(self.graph)
        edge_labels = nx.get_edge_attributes(self.graph, 'weight')
        nx.draw(self.graph, pos, with_labels=True, node_size=1500,
                node_color='lightblue', font_size=8)
        nx.draw_networkx_edge_labels(self.graph, pos, edge_labels=edge_labels, font_color='red')
        plt.savefig("./out/graph.png")  # {self.file.file_path}
        plt.show()

    def query_bridge_words(self, word1, word2):
        """
        查询两个单词间的桥接词。

        parameters:
            word1 (str): 起始词。
            word2 (str): 终止词。

        return:
            str: 包含桥接词的字符串。
        """
        if word1 not in self.graph or word2 not in self.graph:
            return f"No {word1} or {word2} in the graph!"
        bridge_words = [word3 for word3 in self.graph if self.graph.has_edge(word1, word3)
                        and self.graph.has_edge(word3, word2)]
        if not bridge_words:
            return f"No bridge words from {word1} to {word2}!"
        return f"The bridge words from {word1} to {word2} are: " + ', '.join(bridge_words) + "."

    def generate_new_text(self, text):
        """
        根据桥接词生成新文本。

        parameters:
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

    def calc_shortest_path(self, word1, word2):
        """
        计算两个单词之间的最短路径。

        parameters:
            word1 (str): 起始词。
            word2 (str): 终止词。

        return:
            tuple: 包含最短路径和路径长度。
        """
        try:
            # 计算最短路径
            # path_length, shortest_path = dijkstra(self.graph, source=word1, target=word2,
            #                                       weight='weight')
            path_length, shortest_path = nx.single_source_dijkstra(
                self.graph, source=word1, target=word2, weight='weight')

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

    def random_walk(self):
        """
        在图上进行随机游走。
        """
        # 随机选择节点
        current_node = random.choice(list(self.graph.nodes))
        visited_edges = set()
        walk = [current_node]

        # 遍历节点出边
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
        return walk


def split(text):
    """
    清洗文本并按空白字符分词。

    parameters:
        text (str): 需要被处理的文本。

    return:
        list: 包含文本中所有单词的列表。
    """
    text = re.sub(f'[{string.punctuation}]', '', text)
    words = text.split()
    return words


def write_walk_to_file(walk, file_name):
    """
    将随机游走的节点写入文件。

    parameters:
        walk (list): 随机游走的节点列表。
        file_name (str): 文件路径。
    """
    with open(file_name, 'w', encoding='utf-8') as file:
        file.write(' '.join(walk))
