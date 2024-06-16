# Lab3 代码评审与单元测试

## python代码评审

- pylint
- flake8
- bandit

### pylint

- 安装：`pip install pylint`
- 使用：`pylint [file_name.py]`
- 优点是可以打分，正反馈较强（
- 要求给每个文件、每个模块都写一个注释，每行代码100字符

### flake8

- 安装：`pip install flake8`
- 使用：`flake8 [file_name.py]`
- 每行代码最多79字符

### bandit

- 安装：`pip install bandit`
- 使用：`bandit -r examples/ --format custom`
  - `-r` 递归查找目录
  - `--format custom` 自定义输出格式


## 单元测试

- pytest
- unittest
- coverage.py

### pytest

pytest是python的单元测试框架
- 安装：`pip install pytest`
- 使用：`pytest [测试文件.py]` 
- `pytest -s test.py` 支持输入

### unittest

unittest是python的单元测试框架
- 安装：`pip install unittest`

### coverage.py

coverage.py可以统计代码的覆盖率

- 安装：`pip install coverage`
- 使用：`coverage run test.py`
  `coverage report` 查看覆盖率
  `coverage html`
