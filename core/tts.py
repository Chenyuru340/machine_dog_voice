import comtypes.client
from config.settings import TTS_RATE

class WindowsTTS:
    def __init__(self):
        self.speaker = comtypes.client.CreateObject("SAPI.SpVoice")
        # 优先选择慧慧语音，无则用系统默认中文
        for voice in self.speaker.GetVoices():
            if "慧慧" in voice.GetDescription() or "中文" in voice.GetDescription():
                self.speaker.Voice = voice
                break
        self.speaker.Rate = TTS_RATE
        self.speaker.Volume = 100  # 音量最大

    def speak(self, text):
        """播放语音，捕获异常避免程序崩溃"""
        try:
            self.speaker.Speak(text)
        except Exception as e:
            print(f"[TTS播放异常] {str(e)}")

# 全局TTS单例（避免重复初始化）
_tts_engine = None
def get_tts_engine():
    global _tts_engine
    if _tts_engine is None:
        _tts_engine = WindowsTTS()
    return _tts_engine