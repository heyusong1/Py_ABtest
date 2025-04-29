import re
from collections import defaultdict
from Data_sorting.Data_collection import data_integration, safe_parse_list, data_tag

REGEX_PATTERN = r'(\d+\.\d+\.\d+)\s+([^$$]+?)\s+\[(.*)$$'

# 对列表数据处理，并返回正交实验组数据
def data_out(ab_url, ab_payload, ab_cookie):
    data = data_integration(ab_url, ab_payload, ab_cookie)
    parsed = []
    for line in data:
        match = re.match(REGEX_PATTERN, line)
        if not match:
            print(f"无效数据行: {line}")
            continue
        version_str = match.group(1)
        feature = match.group(2).strip()
        list_str = match.group(3)
        parsed.append({
            "version": tuple(map(int, version_str.split('.'))),
            "version_str": version_str,
            "feature": feature,
            "list": safe_parse_list(list_str)
        })

    if not parsed:
        print("无有效数据可供处理")
        return
    max_version = max(item["version"] for item in parsed)
    max_items = [item for item in parsed if item["version"] == max_version]
    results = {}
    for max_item in max_items:
        max_name = f"{max_item['version_str']} ({max_item['feature']})"
        high_counts = defaultdict(int)
        low_counts = defaultdict(int)
        comparisons = []
        for other_item in parsed:
            if max_item["feature"] == other_item["feature"]:
                continue

            common = sorted(set(max_item["list"]) & set(other_item["list"]))
            if not common:
                continue

            other_name = f"{other_item['version_str']} ({other_item['feature']})"
            is_high_version = other_item["version"] == max_version
            comparisons.append({
                "对比需求": other_name,
                "交集ID": common,
                "是否高版本对比": is_high_version
            })

            for num in common:
                if is_high_version:
                    high_counts[num] += 1
                else:
                    low_counts[num] += 1

        common_lists = [set(comp["交集ID"]) for comp in comparisons]
        secondary_common = sorted(set.intersection(*common_lists)) if common_lists else []

        candidates = []
        all_ids = set(high_counts.keys()).union(set(low_counts.keys()))
        for num in all_ids:
            candidates.append((
                num,
                high_counts.get(num, 0),
                low_counts.get(num, 0)
            ))

        candidates.sort(key=lambda x: (-x[1], -x[2], -x[0]))
        most_common_id = candidates[0][0] if candidates else None

        results[max_name] = {
            "对比结果": comparisons,
            "二次交集": secondary_common,
            "最高频ID": most_common_id,
            "high_counts": high_counts,
            "low_counts": low_counts
        }

    print("===== 每个高版本的交集及优先级结果 =====")
    for name, data in results.items():
        print(f"\n高版本需求: {name}")

        if data["二次交集"]:
            print(f"二次交集ID: {data['二次交集']}")
        else:
            if data["最高频ID"] is not None:
                involved = [
                    comp["对比需求"]
                    for comp in data["对比结果"]
                    if data["最高频ID"] in comp["交集ID"]
                ]
                print(f"按优先级选择最高频ID: {data['最高频ID']}")
                print("涉及的需求对比:")
                for req in involved:
                    print(f"  - {req}")
            else:
                print("无任何交集ID")


def tag_quite(ab_url, ab_payload, ab_cookie):
    """
    调用 data_tag 并返回其结果。
    :param ab_url: 请求的 URL
    :param ab_payload: 请求的 payload 数据
    :param ab_cookie: 请求的 cookie 数据
    :return: data_tag 的返回值
    """
    try:
        group_data = data_tag(ab_url, ab_payload, ab_cookie)
        if not isinstance(group_data, list):
            raise ValueError("data_tag 的返回值必须是列表")
        return group_data
    except NameError:
        raise RuntimeError("data_tag 函数未定义，请确保其已正确定义")


def validate_and_collect_tags(tag_list, data_list):
    """
    检查标签是否全部存在于 data_list 中，并返回所有存在的标签及其对应数据。
    :param tag_list: 标签列表
    :param data_list: 数据列表
    :return: 存在的标签及其对应数据的字典
    """
    if not isinstance(tag_list, list) or not all(isinstance(tag, str) for tag in tag_list):
        raise ValueError("标签列表必须是非空字符串列表")
    if not isinstance(data_list, list) or not all(isinstance(data, dict) for data in data_list):
        raise ValueError("数据列表必须是非空字典列表")

    existing_tags = {}
    all_keys = {key for data in data_list for key in data.keys()}

    missing_tags = [tag for tag in tag_list if tag not in all_keys]
    if missing_tags:
        print(f"以下标签不存在: {missing_tags}")
        return None

    # 收集所有存在的标签及其对应数据
    for data in data_list:
        for tag in tag_list:
            if tag in data:
                if not isinstance(data[tag], list):
                    raise ValueError(f"标签 {tag} 的数据格式不正确，应为列表")
                existing_tags.setdefault(tag, set()).update(data[tag])
    return existing_tags


def calculate_sets(existing_tags, tag_list):
    """
    计算标签的交集和非交集。
    :param existing_tags: 存在的标签及其对应数据的字典
    :param tag_list: 标签列表
    :return: 包含交集和非交集的结果字典
    """
    if len(tag_list) < 2:
        raise ValueError("至少需要两个标签来计算交集和非交集")

    sets = {tag: existing_tags[tag] for tag in tag_list}
    intersection = set.intersection(*sets.values())

    non_intersections = {}
    total_non_inter = set()
    for tag, s in sets.items():
        non_inter = s - intersection
        non_intersections[f"{tag}的非交集"] = sorted(non_inter)[0]
        total_non_inter.update(non_inter)

    result = {
        "交集": sorted(intersection),
        **non_intersections
    }
    return result


# 主逻辑封装到 main 函数中
def tag_out_data(url,payload,cookie,tag_id):
    try:
        # 步骤1：验证标签并收集数据
        id_lists = validate_and_collect_tags(tag_id, tag_quite(url, payload, cookie))
        if id_lists is None:
            print("由于缺少必要标签，无法继续计算。")
        else:
            # 步骤2：计算交集和非交集
            result = calculate_sets(id_lists, tag_id)
            return f"比对结果：{result}"
    except (ValueError, TypeError, RuntimeError) as e:
        print(f"发生错误: {e}")


# if __name__ == '__main__':
    # 定义必要变量
    # tag_id = ['A140', 'A150']
    # production_id = "5b18ed819c560300013ddf24"  # ios
    # url = f"https://work.learnings.ai/abtest/test/v5/cms/matrix/abtest/ids/{production_id}?production_id={production_id}"
    # payload = {"production_id": production_id}
    # cookie = '_ga=GA1.1.630718862.1736761800; _tea_utm_cache_1229=undefined;learnings-passport=jyzs_fIBxVOU5VhB13opp5GInoJ6SX2EidzrVd7nr50ki0R2FmWwtQqGFQweXl11;learnings-user=TlD9Gf8zXYCciyz7NTwPa4LrFyOP82H6iaaw149aollJN0yJAaDo67zdpSplbR9U1KSqv3KtXcAOOB5ZBAdjb2wW_TAXOs47t4OIR3yf4Li6dSo0u-gLHAOOYS4pI-JARkMF-TjuIhltp9TBK_Op5RpR_IBIqLcOKWZJe7F0GhzCz8H90AejGSsm9BIFbHqU83pStLc0jkOkCLDG66Ra4xCR2enfGVBTQklEtTzc0G0pF6yjgQ34toWU08MUe-bzXzCskfqPnJtCOw9tEWnEjlnYqlcq_auYNMMkpINOsmmhhsTuYWWO2KlbfPUJ7nt_8kLR8mtDmFCYNlffxzmQYD0823yEjg4SyZDQDRHuUOgiiLhAAruVWC0OZWEO-kKTciCfz2b6mrXSZAjRicNh1sitECV6aCj6xh4cNwDrN2Sjeso9q2z65luekH-3ZAC0y8TVyTaOvtC5DegKcNdktjcXUCD-b70RYguugot6tFikej8JhinVdtzbBsO2CTtDvqx5PV4WWWP4RY-HqyHx2JvAkiqiMe1aSQyhpdMOXG4ZQHjQSifHYjLekl_JnVfgjhuO0oreU38-2vPnakbHoSwCYczutnqulUvk03zgFX8_B9Qb5YCs_1RMjce99mSbNwqDKtpYsr9pqXrKwMMcitnerb-8uB1-CL5Qos_cje5oVKWLtv9Idp0iu8pK3lRR'
    # print(tag_out_data(url,payload,cookie,tag_id))
    # # data_out(url,payload,cookie)
    # tag_id = ['AAO1', 'AAK6', 'AALb']
    # production_id = "65967fd2c42f1245636a7410"  # android
    # # production_id = "65967fd2c42f1245636a7410" #ios
    # url = f"https://work.learnings.ai/abtest/test/v5/cms/matrix/abtest/ids/{production_id}?production_id={production_id}"
    # payload = {"production_id": production_id}
    # cookie = '_ga=GA1.1.824113639.1735788668; _ga_2Z4PFG28RG=deleted; learnings-passport=1ugsxa0PtN661XWycP9Ig70NzBDStWtW91m9drj_K35bsV3GHe76MJZG9d87Qfp6; _tea_utm_cache_1229=undefined; learnings-user=lVeSR6Ly9Mm2BcY9X2kZPbWZx8T4NnIGCIqRsz1qWLl7nQC7IlCF94HmXb4XJKj3n0XCR1ppS5wj4ArYWKL7e6YqLybfFlYp59c66ouyr0gbRA9hpSST1Ip1EadnFOF0xZh_0cwr54C3FpcBOxApRwUhy-8_kZdYsbhAgextuPDBgO7rBv8z9Ifd5YNy6Z2JAGWi166nxlzt3dlJ-8WLTDxaqGLnakGwyElRlVeOkjPZ70KYa4NEucWbQWM2UI3hnd8uZEWvWx2yiT7p-5Rv8sqLQbFnP-BeIxB9U_HvDRhCHxVAZYNqeu_WUolL23Hs4ptyZI4DioVhX2ONOzXrkcNabDVPb4FCQmrGO01mZt6PRriGSxX6QAdkTIghcAy_NVH84kY72d4NGD-o_YGGD7E2yG7y_qwZW8oFpO5tMmbJaoh0QshA2wUpBG3FsZecLdvoqObZHpnBkxLUJHrurYx-tM5A-3UbUPdXq5I7o7U3imqTT22Gl0VUkl4534tGXHj__3xOfNulIK7sfp4fblN5Tv3GVBzQQi6IPU1wvN8K9Dg6P6rUFP-JKMz9U3Q6ImGitvdnrnnARN2v02jsfLK3TfkHjmOg7xj3J5ew0nrJ-Padli-tD5rn84kyy2UxbagrOmb6cPw_FixqCNAZClyi_oTkpwdxPfkEoO08Wp4suTMETnPmzKKl4jTJI3A_; _ga_2Z4PFG28RG=GS1.1.1743129511.161.1.1743129516.55.0.0'
    # print(tag_out_data(url, payload, cookie, tag_id))