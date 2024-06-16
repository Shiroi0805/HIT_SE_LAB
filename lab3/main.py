"""
这是用于图操作和探索的模块，提供了一个交互式命令行界面来展示图的不同功能。

该程序允许用户输入图的路径以初始化一个图对象，随后通过一系列菜单选项执行各种操作，包括展示图、查询桥接词、生成新文本、计算最短路径以及进行随机游走。

Functions:
    menu(): 显示菜单选项。
    main(): 程序的主入口，处理用户输入并调用相应功能。

Example:
    运行程序后，根据提示输入图的路径，然后根据需要选择不同的功能编号进行操作。

Notes:
    本模块依赖于 `my_graph` 模块，确保已正确安装该模块以及相关依赖。
"""
import my_graph as mg


def menu():
    """
    功能选择菜单
    """
    print('\n\n功能选择：')
    print('1. 展示图并保存')
    print('2. 查询桥接词')
    print('3. 根据bridge word生成新文本')
    print('4. 计算并展示两个单词之间的最短路径')
    print('5. 随机游走')
    print('0. 退出程序')


def main():
    """
    程序主入口
    """
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
        if choice == '1':
            graph.show_directed_graph()
        elif choice == '2':
            word1 = input("请输入第一个单词: ").lower()
            word2 = input("请输入第二个单词: ").lower()
            print(graph.query_bridge_words(word1, word2))
        elif choice == '3':
            text = input("请输入一段话: ").lower()
            graph.generate_new_text(text)
        elif choice == '4':
            word1 = input("请输入第一个单词: ").lower()
            word2 = input("请输入第二个单词: ").lower()
            shortest_path, path_length = graph.calc_shortest_path(word1, word2)
            if isinstance(shortest_path, list):
                print(f"最短路径为: {'→'.join(shortest_path)}")
                print(f"路径长度（所有边权值之和）为: {path_length}")
            else:
                print(shortest_path)
        elif choice == '5':
            graph.random_walk()
        else:
            print('输入错误，请重新输入！')


if __name__ == '__main__':
    main()
