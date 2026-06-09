# 文本过滤工具
import re


def remove_emoji(text):
    """过滤表情/特殊符号，避免TTS乱读"""
    filter_pattern = re.compile(
        r'[^\u4e00-\u9fa5a-zA-Z0-9\s，。！？：""''（）《》、·]',
        flags=re.UNICODE
    )
    clean_text = filter_pattern.sub(r'', text).strip()
    return clean_text if clean_text else "我收到你的指令啦～"

def is_valid_command(text, min_len=2, max_len=30):
    """校验指令是否有效：长度+内容合法性"""
    text_len = len(text)
    if text_len < min_len or text_len > max_len:
        print(f"[过滤无效指令] 长度不符合：{text_len}字（要求{min_len}-{max_len}字）")
        return False
    if text.isdigit() or all(not c.isalnum() for c in text):
        print(f"[过滤无效指令] 内容无效：纯数字/纯符号「{text}」")
        return False
    return True