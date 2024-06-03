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
    def __init__(self, text):
        self.text = text
        self.words = Text.split(self.text)
        
    # 功能：清理文本、分割单词
    def split(text):
        text = re.sub(f'[{string.punctuation}]', '', text)
        words = text.split()
        return words
    
    # 相加
    def __add__(self, other):
        return Text(self.text + other.text)
    
# 图
class Graph:
    def __init__(self, path = 'D:\[study]\[studying]\软件工程\lab\lab1\input.txt'): # input.txt
        self.path = path
        self.file = Text(Graph.read(self.path))
        self.graph = Graph.createGraph(self.file.words)

    # 功能：读取文件
    def read(file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            text = file.read().lower()
        return text

    # 功能：创建有向图
    def createGraph(words):
        graph = nx.DiGraph()
        for i in range(len(words) - 1):
            if graph.has_edge(words[i], words[i+1]):
                graph[words[i]][words[i+1]]['weight'] += 1
            else:
                graph.add_edge(words[i], words[i+1], weight=1)
        return graph
    
    # 功能：用plt绘制有向图
    def showDirectedGraph(self):
        pos = nx.spring_layout(self.graph)
        edge_labels = nx.get_edge_attributes(self.graph, 'weight')
        nx.draw(self.graph, pos, with_labels=True, node_size=1500, node_color='lightblue', font_size=8)
        nx.draw_networkx_edge_labels(self.graph, pos, edge_labels=edge_labels, font_color='red')
        plt.savefig(f"./out/graph.png") # {self.file.file_path}
        plt.show()
    
    # 功能：查询桥接词 word1 -> word3 -> word2
    def queryBridgeWords(self, word1, word2):
        if word1 not in self.graph or word2 not in self.graph:
            return f"No {word1} or {word2} in the graph!"
        bridge_words = [word3 for word3 in self.graph if self.graph.has_edge(word1, word3) and self.graph.has_edge(word3, word2)]
        if not bridge_words:
            return f"No bridge words from {word1} to {word2}!"
        return f"The bridge words from {word1} to {word2} is: " + ', '.join(bridge_words) + "."

    # 根据bridge word生成新文本
    # 先分解为词列表，遍历查询, 如果存在桥接词，随机插入
    def generateNewText(self, text):
        words = Text(text)
        # 句首词首字母大写 待完成
        new_text = words.words[0]
        for i in range(len(words.words) - 1):
            bridge_words = [word3 for word3 in self.graph if self.graph.has_edge(words.words[i], word3) and self.graph.has_edge(word3, words.words[i+1])]
            if bridge_words:
                bridge_word = random.choice(bridge_words)
                new_text += ' ' + bridge_word
            new_text += ' ' + words.words[i+1]
        print(new_text)
    
    # 计算两个单词之间的最短路径
    def calcShortestPath(self, word1, word2):
        try:
            # 计算最短路径
            path_length, shortest_path = dijkstra(self.graph, source=word1, target=word2, weight='weight')
            # shortest_path = nx.shortest_path(self.graph, source=word1, target=word2, weight='weight')

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
    
    #功能：游走
    def randomWalk(self):
        # 随机选择节点
        current_node = random.choice(list(self.graph.nodes))
        visited_edges = set()
        walk = [current_node]

        #遍历节点出边
        while True:
            neighbors = list(self.graph[current_node])
            if not neighbors or all((current_node, neighbor) in visited_edges for neighbor in neighbors):
                break

            # 随机访问
            next_node = random.choice([neighbor for neighbor in neighbors if (current_node, neighbor) not in visited_edges])
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
    text = re.sub(f'[{string.punctuation}]', '', text)
    words = text.split()
    return words

def write_walk_to_file(walk, file_name):
    with open(file_name, 'w', encoding='utf-8') as file:
        file.write(' '.join(walk))

def dijkstra(G, source, target, weight="weight"):
    if source not in G or target not in G:
        msg = f"Either source {source} or target {target} is not in G"
        raise nx.NodeNotFound(msg)

    if source == target:
        return (0, [source])

    weight = _weight_function(G, weight)
    push = heappush
    pop = heappop
    dists = [{}, {}]
    paths = [{source: [source]}, {target: [target]}]
    fringe = [[], []]
    seen = [{source: 0}, {target: 0}]
    c = count()
    push(fringe[0], (0, next(c), source))
    push(fringe[1], (0, next(c), target))
    if G.is_directed():
        neighs = [G._succ, G._pred]
    else:
        neighs = [G._adj, G._adj]
    finalpath = []
    dir = 1
    while fringe[0] and fringe[1]:
        dir = 1 - dir
        (dist, _, v) = pop(fringe[dir])
        if v in dists[dir]:
            continue
        dists[dir][v] = dist
        if v in dists[1 - dir]:
            return (finaldist, finalpath)

        for w, d in neighs[dir][v].items():
            if dir == 0:
                vwLength = dists[dir][v] + weight(v, w, d)
            else:
                vwLength = dists[dir][v] + weight(w, v, d)
            if w in dists[dir]:
                if vwLength < dists[dir][w]:
                    raise ValueError("Contradictory paths found: negative weights?")
            elif w not in seen[dir] or vwLength < seen[dir][w]:
                seen[dir][w] = vwLength
                push(fringe[dir], (vwLength, next(c), w))
                paths[dir][w] = paths[dir][v] + [w]
                if w in seen[0] and w in seen[1]:
                    totaldist = seen[0][w] + seen[1][w]
                    if finalpath == [] or finaldist > totaldist:
                        finaldist = totaldist
                        revpath = paths[1][w][:]
                        revpath.reverse()
                        finalpath = paths[0][w] + revpath[1:]
    raise nx.NetworkXNoPath(f"No path between {source} and {target}.")
