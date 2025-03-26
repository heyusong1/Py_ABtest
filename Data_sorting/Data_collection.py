from Api.Api_requests import *
import re

# 过滤掉对照组和空白基线组
def data_integration(ab_url, ab_payload, ab_cookie):
    ab_data = get_ab_data(ab_url, ab_payload, ab_cookie)
    code = ab_data.get('data', {}).get('idList', [])
    result = []
    for i in code:
        group_name = i.get('group_name')
        if group_name != "对照组" and group_name != "对照组-空白基线组":
            # print(i)
            name_parts = i.get('name', '').split()
            if len(name_parts) < 2:  # 确保名称格式正确
                continue
            version, ab_name = name_parts[0], ' '.join(name_parts[1:])
            id_list = i.get('id_list', [])
            data = f"{version} {ab_name}_{group_name} {id_list}"
            result.append(data)
    return result

# 解析列表字符串，并返回一个整数列表
def safe_parse_list(list_str: str) -> list[int]:
    # 彻底清理非法字符：去除所有非数字和逗号的字符（保留负号）
    cleaned = re.sub(r'[^\d,-]', '', list_str)
    # 分割并过滤空值
    elements = [x.strip() for x in cleaned.split(',') if x.strip()]
    try:
        return [int(x) for x in elements]
    except ValueError:
        print(f"解析列表失败: {list_str}")
        return []
