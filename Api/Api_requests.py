import requests

# 配置常量
AUTHORIZATION = 'bb4253071b934690b900267425b1a9b2'
REFERER = 'https://work.learnings.ai/frontend_pm/'

# 获取AB数据id
def get_ab_data(ab_url, ab_payload, ab_cookie):
    try:
        headers = {
            'accept': 'application/json, text/plain, */*',
            'authorization': AUTHORIZATION,
            'if-none-match': '"09e2ec0b71dae356b828cc2d12fe42bb147d0718"',
            'referer': REFERER,
            'cookie': ab_cookie
        }
        response = requests.request("GET", ab_url, headers=headers, data=ab_payload)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"请求失败: {e}")
        return e
