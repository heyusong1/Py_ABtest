import logging
from Data_sorting.Data_processing import data_out,tag_out_data

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# 输入校验
def validate_inputs(url, payload, cookie):
    """
    校验输入参数是否合法。
    :param url: 请求的目标 URL
    :param payload: 请求的数据
    :param cookie: 请求的 Cookie
    :return: 如果校验通过则返回 True，否则抛出 ValueError
    """
    if not isinstance(url, str) or not url.startswith(('http://', 'https://')):
        raise ValueError("Invalid URL format")
    if not isinstance(payload, dict):
        raise ValueError("Payload must be a dictionary")
    if not isinstance(cookie, str):
        raise ValueError("Cookie must be a string")
    return True

# 核心逻辑-版本号筛选
def handle_data_output(url, payload, cookie):
    """
    封装 data_out 的调用，并处理异常。
    :param url: 请求的目标 URL
    :param payload: 请求的数据负载
    :param cookie: 请求的 Cookie
    """
    try:
        data_out(url, payload, cookie)
    except Exception as e:
        logging.error(f"Error occurred while calling data_out: {e}")
        raise

# 核心逻辑-tag筛选
def tag_data_output(url,production_id,payload,cookie,tag_id):
    """
    封装 data_out 的调用，并处理异常。
    :param url: 请求的目标 URL
    :param payload: 请求的数据负载
    :param cookie: 请求的 Cookie
    """
    try:
        tag_out_data(url,payload,cookie,tag_id)
    except Exception as e:
        logging.error(f"Error occurred while calling data_out: {e}")
        raise


# 运行主程序
def run(url, payload, cookie,tag_id):
    """
    执行数据输出操作。
    :param url: 请求的目标 URL
    :param payload: 请求的数据负载
    :param cookie: 请求的 Cookie
    """
    # 参数校验
    try:
        validate_inputs(url, payload, cookie)
    except ValueError as ve:
        logging.error(f"Input validation failed: {ve}")
        raise

    # 调用核心逻辑-按照tag筛选
    tag_out_data(url, payload, cookie, tag_id)
    # 调用核心逻辑-按照版本号筛选
    # handle_data_output(url, payload, cookie)


if __name__ == '__main__':
    # tag_id = ['A140', 'A150']
    # # production_id = "5b18faf53e70cb00010315f6"  # android
    # production_id = "5b18ed819c560300013ddf24" #ios
    # url = f"https://work.learnings.ai/abtest/test/v5/cms/matrix/abtest/ids/{production_id}?production_id={production_id}"
    # payload = {"production_id": production_id}
    # cookie = '_ga=GA1.1.630718862.1736761800; _tea_utm_cache_1229=undefined;learnings-passport=jyzs_fIBxVOU5VhB13opp5GInoJ6SX2EidzrVd7nr50ki0R2FmWwtQqGFQweXl11;learnings-user=TlD9Gf8zXYCciyz7NTwPa4LrFyOP82H6iaaw149aollJN0yJAaDo67zdpSplbR9U1KSqv3KtXcAOOB5ZBAdjb2wW_TAXOs47t4OIR3yf4Li6dSo0u-gLHAOOYS4pI-JARkMF-TjuIhltp9TBK_Op5RpR_IBIqLcOKWZJe7F0GhzCz8H90AejGSsm9BIFbHqU83pStLc0jkOkCLDG66Ra4xCR2enfGVBTQklEtTzc0G0pF6yjgQ34toWU08MUe-bzXzCskfqPnJtCOw9tEWnEjlnYqlcq_auYNMMkpINOsmmhhsTuYWWO2KlbfPUJ7nt_8kLR8mtDmFCYNlffxzmQYD0823yEjg4SyZDQDRHuUOgiiLhAAruVWC0OZWEO-kKTciCfz2b6mrXSZAjRicNh1sitECV6aCj6xh4cNwDrN2Sjeso9q2z65luekH-3ZAC0y8TVyTaOvtC5DegKcNdktjcXUCD-b70RYguugot6tFikej8JhinVdtzbBsO2CTtDvqx5PV4WWWP4RY-HqyHx2JvAkiqiMe1aSQyhpdMOXG4ZQHjQSifHYjLekl_JnVfgjhuO0oreU38-2vPnakbHoSwCYczutnqulUvk03zgFX8_B9Qb5YCs_1RMjce99mSbNwqDKtpYsr9pqXrKwMMcitnerb-8uB1-CL5Qos_cje5oVKWLtv9Idp0iu8pK3lRR'
    # run(url, production_id,payload, cookie,tag_id)
    # rel_url = f"https://work.learnings.ai/abtest/prod/v5/cms/matrix/abtest/ids/{rel_id}?production_id={rel_id}"
    # payload = {"production_id": rel_id}
    # rel_cookie = '_ga=GA1.1.630718862.1736761800; learnings-passport=jyzs_fIBxVOU5VhB13opp5GInoJ6SX2EidzrVd7nr50ki0R2FmWwtQqGFQweXl11; _ga_2Z4PFG28RG=GS1.1.1742888639.83.1.1742889210.33.0.0; learnings-user=Ou7DP0e3gj7hKCv6Vp_u07w6SJf2hZYK275qI9ZWNSturYC5LJ68pL9ZcBzqma-yy-4gjQCMeoo5Qme60vg_M_-aFGP1iybkXTAqLCW0mj1dYHFE_qaN07tBHoAwcZ_8_wAXTAK7QTZdsNg6LShmIsH76eVbo9Z_HZb0wh0H4r-97_ShvNERNXaZIdeEUx1sgIa3oVNuKc3qJh5bpcOuwxEIvL3uY-sYHEYy6EqS60rCF8hGWBpWcibny9BSdBSEfkW4Y2RVukQBJfPPm3p9VBYviE-feDIQem9zv0G6kJTihLvHsDN384PQ4JXrNtDLZidr7d5G4m_MYDPiOkl4CuXG3VtE6vhysronMHXc57SdEW9sb5f1sJLlWVojwDeq7btL4zXWVepE0MIncdLDLRrNAWyHnN-qhqnUCyFJLlEKPSQXL9SnkFktWr6n6ks4MEPqUcZJcdVxO94KUH0pF4gRqQgw4h0hrqxF8KWMe5RF5qhO_CXjwkjIL_QPaSFC9SetyojPAlyDMzkT47-tXq8sDWxwHfdtQ-EPfvVLjFloJW3VnvNcLYug9yXCp3p2vaxXiPudNbaMl0bZuBm6xXmg-kZS4dlqkfd41Hds9e4eZNm3GsSQwKnEKMlUlRv_JXodah1oqLYJu1rkZQAc4l3D-MzTnVMYduZfYw_yZLtSkCG4rhbg-tapEZ-I2MIq'
    # run(rel_url, payload, rel_cookie)

    tag_id = ['AAO1','AAK6','AALb']
    production_id = "65967fd2c42f1245636a7410"  # android
    # production_id = "65967fd2c42f1245636a7410" #ios
    url = f"https://work.learnings.ai/abtest/test/v5/cms/matrix/abtest/ids/{production_id}?production_id={production_id}"
    payload = {"production_id": production_id}
    cookie = '_ga=GA1.1.824113639.1735788668; _ga_2Z4PFG28RG=deleted; learnings-passport=1ugsxa0PtN661XWycP9Ig70NzBDStWtW91m9drj_K35bsV3GHe76MJZG9d87Qfp6; _tea_utm_cache_1229=undefined; learnings-user=lVeSR6Ly9Mm2BcY9X2kZPbWZx8T4NnIGCIqRsz1qWLl7nQC7IlCF94HmXb4XJKj3n0XCR1ppS5wj4ArYWKL7e6YqLybfFlYp59c66ouyr0gbRA9hpSST1Ip1EadnFOF0xZh_0cwr54C3FpcBOxApRwUhy-8_kZdYsbhAgextuPDBgO7rBv8z9Ifd5YNy6Z2JAGWi166nxlzt3dlJ-8WLTDxaqGLnakGwyElRlVeOkjPZ70KYa4NEucWbQWM2UI3hnd8uZEWvWx2yiT7p-5Rv8sqLQbFnP-BeIxB9U_HvDRhCHxVAZYNqeu_WUolL23Hs4ptyZI4DioVhX2ONOzXrkcNabDVPb4FCQmrGO01mZt6PRriGSxX6QAdkTIghcAy_NVH84kY72d4NGD-o_YGGD7E2yG7y_qwZW8oFpO5tMmbJaoh0QshA2wUpBG3FsZecLdvoqObZHpnBkxLUJHrurYx-tM5A-3UbUPdXq5I7o7U3imqTT22Gl0VUkl4534tGXHj__3xOfNulIK7sfp4fblN5Tv3GVBzQQi6IPU1wvN8K9Dg6P6rUFP-JKMz9U3Q6ImGitvdnrnnARN2v02jsfLK3TfkHjmOg7xj3J5ew0nrJ-Padli-tD5rn84kyy2UxbagrOmb6cPw_FixqCNAZClyi_oTkpwdxPfkEoO08Wp4suTMETnPmzKKl4jTJI3A_; _ga_2Z4PFG28RG=GS1.1.1743129511.161.1.1743129516.55.0.0'
    run(url, payload, cookie, tag_id)