from ruamel.yaml import YAML
from jinja2 import Environment, FileSystemLoader
import os


def extend_list(input_list, target_length):
    """
    将给定列表扩展到目标长度。

    如果列表长度小于目标长度，则通过追加空字符串将其扩展。
    如果输入不是列表类型，则抛出TypeError异常。

    参数:
    input_list (list): 需要扩展的列表。
    target_length (int): 目标长度。

    返回:
    list: 扩展后的列表。
    """
    # 检查输入是否为列表类型
    if not isinstance(input_list, list):
        raise TypeError("Input data is not of type list.")

    # 如果列表长度小于目标长度，则进行扩展
    if len(input_list) < target_length:
        input_list.extend([''] * (target_length - len(input_list)))

    return input_list


def format_data(file_path):
    """
    读取yaml文件，并转换为给jinja2渲染的数据
    :param file_path: yaml文件路径
    :return: 格式化后的数据，为一个可以供jinja2模板渲染使用的数据列表

    函数流程：
    1. 打开给定路径的yaml文件，并安全加载其内容；
    2. 将加载的数据转换为字典形式；
    3. 处理字典，使其每个值的长度相同，便于后续操作；
    4. 将处理后的数据转换为一个适用于jinja2渲染的格式，返回。
    """

    with open(file_path, 'r', encoding='utf-8') as file:
        yaml = YAML(typ='safe')
        data = yaml.load(file)

    # 获取数据字典的所有键，转换为mapping形式
    mid_data = data.keys().mapping

    # 计算每列数据的最大长度，以确保最终数据格式的一致性
    row_num_list = [len(val) for val in data.values()]
    row_num = max(row_num_list) if row_num_list else 0

    # 初始化存储最终数据的列表
    temp_data = []

    # 处理每列数据，确保其长度与最长列相等
    for val in mid_data.values():
        x = extend_list(val, row_num)
        temp_data.append(x)

    # 将处理后的所有列数据垂直打包成一个列表
    end_data = list(zip(*temp_data))

    # 添加表头，即原始数据字典的键
    th = tuple([key for key in mid_data.keys()])
    end_data.insert(0, th)

    # print(end_data)
    return end_data


def to_markdown(data: list, files_list: list):
    """
    提取接收的数据，使用jinja2加载模板进行渲染，生成markdown格式的文件
    :param data: 待渲染的数据，为一个列表，列表中的每个元素都是一行数据，列表中的每个元素都是一个元组，元组中的每个元素都是一个单元格数据
    :param files_list: 待渲染的文件列表，为一个列表，列表中的每个元素都是一个文件路径
    """

    # 提取表头
    th = data[0]

    # 提取数据行
    tr = data[1:]

    # 创建模板加载器，设置模板加载路径
    templateLoader = FileSystemLoader(searchpath="./update_markdown_by_yaml/templates")

    # 创建模板环境
    templateEnv = Environment(loader=templateLoader)

    # 指定使用的模板文件
    TEMPLATE_FILE = "readme_template.md"

    # 加载模板
    template = templateEnv.get_template(TEMPLATE_FILE)

    # 渲染模板，并将结果写入指定文件
    for path in files_list:
        with open(path, 'w', encoding='utf-8') as f:
            result = template.render(ths=th, trs=tr)
            f.write(result)

        # 打印渲染后的结果
        # print(result)


if __name__ == '__main__':
    # 打印当前工作目录，确保模板文件路径正确
    print(os.getcwd())
    data = format_data('./update_markdown_by_yaml/table_data.yml')
    to_markdown(data, ['./update_markdown_by_yaml/last_readme.md',
                './fenglingback/README.md'])
