import re
from collections import defaultdict
from Data_sorting.Data_collection import data_integration,safe_parse_list

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


