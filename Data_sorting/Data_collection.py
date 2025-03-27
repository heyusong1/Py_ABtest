from lib2to3.pgen2.tokenize import group

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

# 过滤tag对应的id_list
def data_tag(ab_url, ab_payload, ab_cookie):
    ab_tag = get_ab_data(ab_url, ab_payload, ab_cookie)
    data = ab_tag.get('data').get('idList')
    group_new_data = []
    for group_data in data:
        if group_data.get('tag') is not None:
            tag = group_data.get('tag').replace('|', '')
            id_list = group_data.get('id_list')
            group_name = group_data.get('group_name')
            name = group_data.get('name')
            group_dict = {tag:id_list}
            group_new_data.append(group_dict)
    return group_new_data




if __name__ == '__main__':
    tag_id = ['A140|', 'A141|']
    # production_id = "5b18faf53e70cb00010315f6"  # android
    production_id = "5b18ed819c560300013ddf24" #ios
    url = f"https://work.learnings.ai/abtest/test/v5/cms/matrix/abtest/ids/{production_id}?production_id={production_id}"
    payload = {"production_id": production_id}
    cookie = '_ga=GA1.1.630718862.1736761800; _tea_utm_cache_1229=undefined;learnings-passport=jyzs_fIBxVOU5VhB13opp5GInoJ6SX2EidzrVd7nr50ki0R2FmWwtQqGFQweXl11;learnings-user=TlD9Gf8zXYCciyz7NTwPa4LrFyOP82H6iaaw149aollJN0yJAaDo67zdpSplbR9U1KSqv3KtXcAOOB5ZBAdjb2wW_TAXOs47t4OIR3yf4Li6dSo0u-gLHAOOYS4pI-JARkMF-TjuIhltp9TBK_Op5RpR_IBIqLcOKWZJe7F0GhzCz8H90AejGSsm9BIFbHqU83pStLc0jkOkCLDG66Ra4xCR2enfGVBTQklEtTzc0G0pF6yjgQ34toWU08MUe-bzXzCskfqPnJtCOw9tEWnEjlnYqlcq_auYNMMkpINOsmmhhsTuYWWO2KlbfPUJ7nt_8kLR8mtDmFCYNlffxzmQYD0823yEjg4SyZDQDRHuUOgiiLhAAruVWC0OZWEO-kKTciCfz2b6mrXSZAjRicNh1sitECV6aCj6xh4cNwDrN2Sjeso9q2z65luekH-3ZAC0y8TVyTaOvtC5DegKcNdktjcXUCD-b70RYguugot6tFikej8JhinVdtzbBsO2CTtDvqx5PV4WWWP4RY-HqyHx2JvAkiqiMe1aSQyhpdMOXG4ZQHjQSifHYjLekl_JnVfgjhuO0oreU38-2vPnakbHoSwCYczutnqulUvk03zgFX8_B9Qb5YCs_1RMjce99mSbNwqDKtpYsr9pqXrKwMMcitnerb-8uB1-CL5Qos_cje5oVKWLtv9Idp0iu8pK3lRR'
    print(data_tag(url, payload, cookie))
