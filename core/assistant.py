# 机器狗核心类
import time
import json
import pyaudio
from threading import Lock, Thread
from config.settings import SAMPLE_RATE, CHUNK_SIZE, ECHO_DURATION, MIN_INPUT_LEN, MAX_INPUT_LEN
from core.recognizer import init_vosk_recognizer
from core.tts import get_tts_engine
from core.api import call_doubao_api
from utils.filters import is_valid_command

class MachineDogVoiceAssistant:
    def __init__(self):
        print("正在初始化机器狗语音助手...")
        # 初始化Vosk
        self.recognizer = init_vosk_recognizer()
        # 初始化TTS
        self.tts_engine = get_tts_engine()
        print("✅ Windows TTS初始化成功（语速=1，优先慧慧语音）")
        # 控制配置
        self.processing_lock = Lock()
        self.is_processing = False
        self.last_tts_end_time = 0
        print("✅ 所有模块初始化完成！")
        print("="*80)

    def is_echo(self, text):
        """判断是否为TTS回音"""
        return time.time() - self.last_tts_end_time < ECHO_DURATION

    def process_command(self, text):
        """处理有效指令"""
        with self.processing_lock:
            if self.is_processing:
                return
            self.is_processing = True

        try:
            print(f"\n📢 [你说] {text}")
            # 调用API
            start_time = time.time()
            dog_reply = call_doubao_api(text)
            cost_time = round(time.time() - start_time, 2)
            # 打印回复信息
            print(f"🤖 [机器狗] 耗时{cost_time}秒 | {dog_reply}")
            print(f"📏 回复长度：{len(dog_reply)}字")
            # 播放回复
            self.tts_engine.speak(dog_reply)
            self.last_tts_end_time = time.time()
        finally:
            with self.processing_lock:
                self.is_processing = False

    def validate_and_process(self, text):
        """验证并处理指令"""
        if not self.is_echo(text) and is_valid_command(text, MIN_INPUT_LEN, MAX_INPUT_LEN):
            self.process_command(text)

    def start_listening(self):
        """启动麦克风监听"""
        print("🎤 机器狗语音助手已成功启动！")
        print(f"👉 支持{MIN_INPUT_LEN}-{MAX_INPUT_LEN}字中文指令")
        print("👉 退出方式：按下 Ctrl+C 即可关闭")
        print("="*80)

        # 初始化PyAudio
        pa = pyaudio.PyAudio()
        stream = pa.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=SAMPLE_RATE,
            input=True,
            frames_per_buffer=CHUNK_SIZE
        )

        try:
            while True:
                data = stream.read(CHUNK_SIZE)
                if self.recognizer.AcceptWaveform(data):
                    result = json.loads(self.recognizer.Result())
                    text = result.get("text", "").strip()
                    if text:
                        Thread(target=self.validate_and_process, args=(text,), daemon=True).start()
                self.recognizer.PartialResult()
                time.sleep(0.001)
        except KeyboardInterrupt:
            print("\n\n👋 正在关闭机器狗语音助手...")
        finally:
            stream.stop_stream()
            stream.close()
            pa.terminate()
            print("✅ 机器狗语音助手已关闭！")