# 配置文件：所有可修改项都集中在这里，只需改这个文件
import os
from pathlib import Path

# ==================== 火山方舟配置 ====================
ARK_BASE_URL = "https://ark.cn-beijing.volces.com/api/v3"
ARK_API_KEY = "..."  # 其他人可以替换为自己的KEY
DOUBAO_MODEL = "ep-20260203161432-bvrtc"              # 替换为目标模型ID

# ==================== 文本/语音参数 ====================
REPLY_MAX_LEN = 500        # 回复最长字符数
MIN_INPUT_LEN = 2          # 输入最少字符数
MAX_INPUT_LEN = 30         # 输入最多字符数
SAMPLE_RATE = 16000        # Vosk固定采样率
CHUNK_SIZE = 1024          # 音频块大小
ECHO_DURATION = 2.5        # 防回音过滤时长（秒）
TTS_RATE = 1               # TTS语速

# ==================== 路径配置 ====================
# Vosk模型路径：其他成员修改为自己的路径（支持相对/绝对路径）
VOSK_MODEL_PATH = r"D:\\Models\\vosk-model-small-cn-0.22"
# 验证路径是否存在（可选，启动时会检查）
assert Path(VOSK_MODEL_PATH).exists(), f"Vosk模型路径不存在：{VOSK_MODEL_PATH}"
