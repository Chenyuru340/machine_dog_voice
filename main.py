# 主程序入口
from core.assistant import MachineDogVoiceAssistant

if __name__ == "__main__":
    try:
        # 初始化并启动
        dog_assistant = MachineDogVoiceAssistant()
        dog_assistant.start_listening()
    except FileNotFoundError as e:
        print(f"\n❌ 启动失败：{e}")
        print(f"📌 解决：修改 config/settings.py 中的Vosk模型路径")
    except ImportError as e:
        print(f"\n❌ 启动失败：缺少依赖 → {e}")
        print("📌 解决：执行 pip install -r requirements.txt")
    except Exception as e:
        print(f"\n❌ 启动失败：未知错误 → {str(e)}")
        print("📌 排查方向：1. 麦克风可用 2. 网络正常 3. API密钥/模型ID正确")