import os
import re


def clean_str(s, platform="both"):
    """
    清洗字符串以符合 Windows 和 Linux 的文件命名规范。

    参数:
        s (str): 原始文件名字符串
        platform (str): 目标平台 ('windows', 'linux', 'both')，默认为 'both'

    返回:
        str: 清洗后的合法文件名
    """

    # 根据平台定义非法字符的正则模式
    if platform == "windows":
        illegal_pattern = r'[\\/:*?"<>|]'
    elif platform == "linux":
        illegal_pattern = r"/"
    else:  # 'both' 或其他情况
        illegal_pattern = r'[\\/:*?"<>|/]'

    # 替换非法字符为下划线
    cleaned = re.sub(illegal_pattern, "_", s)

    # 剥离首尾空格和点
    cleaned = cleaned.strip(" .")

    # 若清洗后为空，返回默认名称
    if not cleaned:
        return "unnamed"

    # 分割文件名和扩展名
    base_name, ext = os.path.splitext(cleaned)

    # 处理 Windows 保留名（仅适用于 Windows 或 both）
    if platform != "linux":
        b_upper = base_name.upper()
        reserved_names = {
            "CON",
            "PRN",
            "AUX",
            "NUL",
            "COM1",
            "COM2",
            "COM3",
            "COM4",
            "COM5",
            "COM6",
            "COM7",
            "COM8",
            "COM9",
            "LPT1",
            "LPT2",
            "LPT3",
            "LPT4",
            "LPT5",
            "LPT6",
            "LPT7",
            "LPT8",
            "LPT9",
        }
        if b_upper in reserved_names:
            base_name += "_"

    # 重新组合 base_name 和扩展名
    new_filename = base_name + ext

    # 再次去除首尾空格和点，确保最终结果合法
    new_filename = new_filename.strip(" .")

    # 若最终仍为空，返回默认名称
    if not new_filename:
        new_filename = "unnamed"

    return new_filename


def mkdir(dir_path):
    if not dir_path:
        return -1
    if not os.path.exists(dir_path):
        os.mkdir(dir_path)
    return 0


if __name__ == "__main__":
    dict1 = {"aa": 66}
    print(dict1.get("aa", 0))
    print(dict1.setdefault("aa", 0))
    print(dict1)
