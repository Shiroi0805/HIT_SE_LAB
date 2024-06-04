import my_graph as mg

def menu():

    print('\n\n功能选择：')
    print('1. 展示图并保存')
    print('2. 查询桥接词')
    print('3. 根据bridge word生成新文本')
    print('4. 计算并展示两个单词之间的最短路径')
    print('5. 随机游走')
    print('0. 退出程序')


def main():
    # input path
    path = input('请输入图的路径：(留空则使用默认路径)')
    if not path:
        graph = mg.Graph()
    else:
        graph = mg.Graph(path)
    
    while True:
        menu()
        choice = input('请输入功能编号：')
        if choice == '0':
            break
        elif choice == '1':
            graph.showDirectedGraph()
        elif choice == '2':
            word1 = input("请输入第一个单词: ").lower()
            word2 = input("请输入第二个单词: ").lower()
            print(graph.queryBridgeWords(word1, word2))
        elif choice == '3':
            text = input("请输入一段话: ").lower()
            graph.generateNewText(text)
        elif choice == '4':
            word1 = input("请输入第一个单词: ").lower()
            word2 = input("请输入第二个单词: ").lower()
            shortest_path, path_length = graph.calcShortestPath(word1, word2)
            if isinstance(shortest_path, list):
                print(f"最短路径为: {'→'.join(shortest_path)}")
                print(f"路径长度（所有边权值之和）为: {path_length}")
            else:
                print(shortest_path)
        elif choice == '5':
            graph.randomWalk()

if __name__ == '__main__':
    main()