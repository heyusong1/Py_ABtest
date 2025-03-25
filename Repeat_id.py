import re
from collections import defaultdict
from Data_all import *

REGEX_PATTERN = r'(\d+\.\d+\.\d+)\s+([^$$]+?)\s+\[(.*)$$'

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
                print(f"无共同交集，按优先级选择最高频ID: {data['最高频ID']}")
                print("涉及的需求对比:")
                for req in involved:
                    print(f"  - {req}")
            else:
                print("无任何交集ID")


if __name__ == '__main__':
    dev_id = "5b18faf53e70cb00010315f6" #android
    # dev_id = "5b18ed819c560300013ddf24" #ios
    url = f"https://work.learnings.ai/abtest/test/v5/cms/matrix/abtest/ids/{dev_id}?production_id={dev_id}"
    payload = {"production_id": dev_id}
    cookie = '_ga=GA1.1.630718862.1736761800; _tea_utm_cache_1229=undefined;learnings-passport=jyzs_fIBxVOU5VhB13opp5GInoJ6SX2EidzrVd7nr50ki0R2FmWwtQqGFQweXl11;learnings-user=TlD9Gf8zXYCciyz7NTwPa4LrFyOP82H6iaaw149aollJN0yJAaDo67zdpSplbR9U1KSqv3KtXcAOOB5ZBAdjb2wW_TAXOs47t4OIR3yf4Li6dSo0u-gLHAOOYS4pI-JARkMF-TjuIhltp9TBK_Op5RpR_IBIqLcOKWZJe7F0GhzCz8H90AejGSsm9BIFbHqU83pStLc0jkOkCLDG66Ra4xCR2enfGVBTQklEtTzc0G0pF6yjgQ34toWU08MUe-bzXzCskfqPnJtCOw9tEWnEjlnYqlcq_auYNMMkpINOsmmhhsTuYWWO2KlbfPUJ7nt_8kLR8mtDmFCYNlffxzmQYD0823yEjg4SyZDQDRHuUOgiiLhAAruVWC0OZWEO-kKTciCfz2b6mrXSZAjRicNh1sitECV6aCj6xh4cNwDrN2Sjeso9q2z65luekH-3ZAC0y8TVyTaOvtC5DegKcNdktjcXUCD-b70RYguugot6tFikej8JhinVdtzbBsO2CTtDvqx5PV4WWWP4RY-HqyHx2JvAkiqiMe1aSQyhpdMOXG4ZQHjQSifHYjLekl_JnVfgjhuO0oreU38-2vPnakbHoSwCYczutnqulUvk03zgFX8_B9Qb5YCs_1RMjce99mSbNwqDKtpYsr9pqXrKwMMcitnerb-8uB1-CL5Qos_cje5oVKWLtv9Idp0iu8pK3lRR'
    data_out(url, payload, cookie)

    # rel_id = "5b18faf53e70cb00010315f6" # android
    # rel_id = "5b18ed819c560300013ddf24" # ios
    # rel_url = f"https://work.learnings.ai/abtest/prod/v5/cms/matrix/abtest/ids/{rel_id}?production_id={rel_id}"
    # payload = {"production_id": rel_id}
    # rel_cookie = '_ga=GA1.1.630718862.1736761800; learnings-passport=jyzs_fIBxVOU5VhB13opp5GInoJ6SX2EidzrVd7nr50ki0R2FmWwtQqGFQweXl11; _ga_2Z4PFG28RG=GS1.1.1742888639.83.1.1742889210.33.0.0; learnings-user=Ou7DP0e3gj7hKCv6Vp_u07w6SJf2hZYK275qI9ZWNSturYC5LJ68pL9ZcBzqma-yy-4gjQCMeoo5Qme60vg_M_-aFGP1iybkXTAqLCW0mj1dYHFE_qaN07tBHoAwcZ_8_wAXTAK7QTZdsNg6LShmIsH76eVbo9Z_HZb0wh0H4r-97_ShvNERNXaZIdeEUx1sgIa3oVNuKc3qJh5bpcOuwxEIvL3uY-sYHEYy6EqS60rCF8hGWBpWcibny9BSdBSEfkW4Y2RVukQBJfPPm3p9VBYviE-feDIQem9zv0G6kJTihLvHsDN384PQ4JXrNtDLZidr7d5G4m_MYDPiOkl4CuXG3VtE6vhysronMHXc57SdEW9sb5f1sJLlWVojwDeq7btL4zXWVepE0MIncdLDLRrNAWyHnN-qhqnUCyFJLlEKPSQXL9SnkFktWr6n6ks4MEPqUcZJcdVxO94KUH0pF4gRqQgw4h0hrqxF8KWMe5RF5qhO_CXjwkjIL_QPaSFC9SetyojPAlyDMzkT47-tXq8sDWxwHfdtQ-EPfvVLjFloJW3VnvNcLYug9yXCp3p2vaxXiPudNbaMl0bZuBm6xXmg-kZS4dlqkfd41Hds9e4eZNm3GsSQwKnEKMlUlRv_JXodah1oqLYJu1rkZQAc4l3D-MzTnVMYduZfYw_yZLtSkCG4rhbg-tapEZ-I2MIq'
    # data_out(rel_url, payload, rel_cookie)
