# 火山方舟API调用模块
from config.settings import ARK_BASE_URL, ARK_API_KEY, DOUBAO_MODEL, REPLY_MAX_LEN
from utils.filters import remove_emoji
from volcenginesdkarkruntime import Ark

def call_doubao_api(user_input):
    """调用火山方舟API，带异常处理和兜底"""
    try:
        # 初始化客户端+封装输入
        client = Ark(base_url=ARK_BASE_URL, api_key=ARK_API_KEY)
        api_input = [
            {
                "role": "user",
                "content": [{"type": "input_text", "text": user_input}]
            }
        ]
        # 调用接口
        response = client.responses.create(
            model=DOUBAO_MODEL,
            input=api_input,
            thinking={"type": "disabled"},
        )

        # 提取回复内容
        raw_reply = ""
        if hasattr(response, 'output') and response.output:
            output_0 = response.output[0]
            if hasattr(output_0, 'content') and output_0.content:
                content_0 = output_0.content[0]
                if hasattr(content_0, 'text'):
                    raw_reply = str(getattr(content_0, 'text', "")).strip()

        # 兜底+过滤+截断
        if not raw_reply:
            raw_reply = "你好呀～我收到你的指令啦，很高兴为你服务～"
        return remove_emoji(raw_reply)[:REPLY_MAX_LEN]

    except Exception as e:
        print(f"[API调用异常] 详细原因：{str(e)}")
        if "401" in str(e) or "403" in str(e):
            return "API密钥失效了，麻烦检查一下密钥是否正确～"
        elif "timeout" in str(e):
            return "网络有点慢，连接服务器超时了，再试一次吧～"
        elif "model" in str(e):
            return "模型ID不对，麻烦检查一下模型配置～"
        else:
            return "我有点小迷糊，但收到你的指令啦，再跟我说一次吧～"