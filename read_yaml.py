from ruamel.yaml import YAML
from jinja2 import Environment, FileSystemLoader


def pad_or_extend_list(lst, target_len):
    if len(lst) < target_len:
        if isinstance(lst, list):
            lst.extend([''] * (target_len - len(lst)))
        else:
            raise TypeError("yaml文件数据不是列表格式，请前往修改！")
    return lst


def to_data(file_path):

    with open(file_path, 'r', encoding='utf-8') as file:
        yaml = YAML(typ='safe')
        data = yaml.load(file)

    mid_data = data.keys().mapping
    # print(mid_data)

    row_num_list = []
    vals = list(data.values())
    for val in vals:
        num = len(val)
        row_num_list.append(num)
    row_num = max(row_num_list)  # td行数

    temp_data = []

    for val in mid_data.values():
        x = pad_or_extend_list(val, row_num)
        temp_data.append(x)
        # print(val)
    end_data = list(zip(*temp_data))
    th = tuple([key for key in mid_data.keys()])
    end_data.insert(0, th)
    # print(end_data)
    return end_data


def to_markdown(data: list, files_list: list):
    th = data[0]
    # print(th)
    tr = data[1:]
    # print(tr)

    # 创建一个模板加载器
    templateLoader = FileSystemLoader(searchpath="./")

    # 创建一个模板环境
    templateEnv = Environment(loader=templateLoader)

    # 指定模板文件名
    TEMPLATE_FILE = "readme_template.md"

    # 获取模板
    template = templateEnv.get_template(TEMPLATE_FILE)

    # 渲染模板
    for path in files_list:
        with open(path, 'w', encoding='utf-8') as f:
            result = template.render(ths=th, trs=tr)
            f.write(result)

        # 打印渲染后的结果
        # print(result)


if __name__ == '__main__':
    data = to_data(r'D:\repo\update_markdown_by_yaml\table_data.yaml')
    to_markdown(data, [r'D:\repo\update_markdown_by_yaml\last_readme.md',
                r'D:\repo\fenglingback\README.md'])
