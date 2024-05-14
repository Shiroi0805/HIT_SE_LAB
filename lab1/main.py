import argparse
import random
from collections import defaultdict
import re
import string

import networkx as nx
import matplotlib.pyplot as plt

# 解析命令行参数
parser = argparse.ArgumentParser(description='Process a text file to create and save a directed graph.')
parser.add_argument('file_path', type=str, help='The path to the text file.')
args = parser.parse_args()

# 功能：读取文件
def readFile(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read().lower()
    return text

# 功能：清理文本、分割单词
def split(text):
    text = re.sub(f'[{string.punctuation}]', '', text)
    words = text.split()
    return words

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
def drawGraph(graph, file_path):
    pos = nx.spring_layout(graph)
    edge_labels = nx.get_edge_attributes(graph, 'weight')
    nx.draw(graph, pos, with_labels=True, node_size=1500, node_color='lightblue', font_size=8)
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels, font_color='red')
    plt.savefig(f"{file_path}_graph.png")

# 功能：查询桥接词
def bridge(graph, word1, word2):
    if word1 not in graph or word2 not in graph:
        return f"No {word1} or {word2} in the graph!"
    bridge_words = [word3 for word3 in graph if graph.has_edge(word1, word3) and graph.has_edge(word3, word2)]
    if not bridge_words:
        return f"No bridge words from {word1} to {word2}!"
    return f"The bridge words from {word1} to {word2} are: " + ', '.join(bridge_words) + "."

# 功能：生吃新文本
def genWords(graph, text):
    words = split(text)
    new_text = words[0]
    for i in range(len(words) - 1):
        bridge_words = [word3 for word3 in graph if graph.has_edge(words[i], word3) and graph.has_edge(word3, words[i+1])]
        if bridge_words:
            bridge_word = random.choice(bridge_words)
            new_text += ' ' + bridge_word
        new_text += ' ' + words[i+1]
    return new_text


# 计算并展示最短路径
def show_shortest_path(graph, word1, word2):
    try:
        # 计算最短路径
        shortest_path = nx.shortest_path(graph, source=word1, target=word2, weight='weight')

        ####### 需要一个Dj 算法
        path_length = sum(graph[u][v]['weight'] for u, v in zip(shortest_path[:-1], shortest_path[1:]))

        # 原图
        pos = nx.spring_layout(graph)
        nx.draw(graph, pos, with_labels=True, node_color='lightblue', font_size=8)

        # 突出
        path_edges = list(zip(shortest_path[:-1], shortest_path[1:]))
        nx.draw_networkx_nodes(graph, pos, nodelist=shortest_path, node_color='red')
        nx.draw_networkx_edges(graph, pos, edgelist=path_edges, edge_color='red', width=2)
        plt.show()

        return shortest_path, path_length
    except nx.NetworkXNoPath:
        return "这两个单词不可达。"

#功能：游走
def random_walk(graph):
    # 随机选择节点
    current_node = random.choice(list(graph.nodes))
    visited_edges = set()
    walk = [current_node]

    #遍历节点出边
    while True:
        neighbors = list(graph[current_node])
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

    return walk

#辅助函数：将随机游走写入文本
def write_walk_to_file(walk, file_name):
    with open(file_name, 'w', encoding='utf-8') as file:
        file.write(' '.join(walk))




def main():
    file_path = args.file_path
    text = readFile(file_path)
    words = split(text)
    graph = createGraph(words)

    #画图
    drawGraph(graph, file_path)

    #查询桥接词
    word1 = input("Please Input word1: ").lower()
    word2 = input("Please Input word2: ").lower()


    # 生成新文本
    new_text = input("Please Input your sentence")
    print(genWords(graph, new_text))
    print(bridge(graph, word1, word2))

    word1 = input("请输入第一个单词: ").lower()
    word2 = input("请输入第二个单词: ").lower()

    # 计算并展示最短路径
    shortest_path, path_length = show_shortest_path(graph, word1, word2)
    if isinstance(shortest_path, list):
        print(f"最短路径为: {'→'.join(shortest_path)}")
        print(f"路径长度（所有边权值之和）为: {path_length}")
    else:
        print(shortest_path)

    # 执行随机遍历
    walk = random_walk(graph)
    print("遍历的节点:", walk)

    # 写入文件
    write_walk_to_file(walk, 'random_walk.txt')
    print("遍历的节点已写入文件 'random_walk.txt'。")

if __name__ == '__main__':
    main()
