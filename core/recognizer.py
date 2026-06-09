# vosk语音识别初始化
import vosk
from config.settings import VOSK_MODEL_PATH, SAMPLE_RATE
from pathlib import Path

def init_vosk_recognizer():
    """初始化Vosk语音识别器，带路径校验"""
    if not Path(VOSK_MODEL_PATH).exists():
        raise FileNotFoundError(f"❌ Vosk模型路径不存在：{VOSK_MODEL_PATH}")
    vosk_model = vosk.Model(VOSK_MODEL_PATH)
    recognizer = vosk.KaldiRecognizer(vosk_model, SAMPLE_RATE)
    print("✅ Vosk中文语音识别初始化成功")
    return recognizer