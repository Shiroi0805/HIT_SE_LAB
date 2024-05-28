这是实验1的readme文件

功能 1 生成树
由命令行实现，在程序运行时规定输入文件为参数
input.txt # 输入文件, 手动输入

功能 2 生成图片
展示生成的有向图。
▪ 可选功能: 将生成的有向图以图形文件形式保存到磁盘，可以调用外部绘图库或绘图工具API自动生成有向图，但不能采用手工方式绘图。

功能需求3: 查询桥接词（bridge words）
▪ 在生成有向图之后，用户输入任意两个英文单词word1、word2，程序从图中查询它们的“桥接词”。
▪ word1、word2的桥接词word3: 图中存在两条边word1→word3, word3→word2。
▪ 输入的word1或word2如果不在图中出现，则输出“No word1 or word2 in the graph!”
▪ 如果不存在桥接词，则输出“No bridge words from word1 to word2!”
▪ 如果存在一个或多个桥接词，则输出“The bridge words from word1 to word2 are: xxx, xxx, and xxx.”

|---|---|---|
seek | to | No bridge words from ”seek” to ”to”!
to | explore | No bridge words from ”to” to ”explore”!
explore | new | The bridge words from ”explore” to ”new” is: strange
new | and | The bridge words from ”new” to ”and” is: life
and | exciting | No “exciting” in the graph!
exciting | synergies | No “exciting” and “synergies” in the graph!


功能需求4: 根据bridge word生成新文本
▪ 用户输入一行新文本，程序根据之前输入文件生成的图，计算该新文本中两两相邻的单词的bridge word，将bridge word插入新文本的两个
单词之间，输出到屏幕上展示。
– 如果两个单词无bridge word，则保持不变，不插入任何单词；
– 如果两个单词之间存在多个bridge words，则随机从中选择一个插入进去形成新文本。
▪ 例如用户输入: Seek to explore new and exciting synergies
▪ 则输出结果为: Seek to explore strange new life and exciting synergies