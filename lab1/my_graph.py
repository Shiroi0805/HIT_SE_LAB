import re
from collections import defaultdict

def preprocess_text(text):
    # 替换掉非字母字符和标点为单个空格，将文本转化为小写
    cleaned_text = re.sub(r'[^a-zA-Z\s]', ' ', text).lower()
    cleaned_text = re.sub(r'\s+', ' ', cleaned_text).strip()
    return cleaned_text

def build_directed_graph(words):
    graph = defaultdict(lambda: defaultdict(int))
    for i in range(len(words) - 1):
        a, b = words[i], words[i + 1]
        graph[a][b] += 1
    return graph

def read_and_process_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()
        cleaned_text = preprocess_text(text)
        words = cleaned_text.split()
        graph = build_directed_graph(words)
        return graph

def print_graph(graph):
    for source in graph:
        for target in graph[source]:
            print(f"{source} -> {target} [权重: {graph[source][target]}]")

# 使用函数
file_path = 'd:\\[study]\\[studying]\\软件工程\\lab\\lab1\\task.md'
graph = read_and_process_file(file_path)
print_graph(graph)
