import requests
import time

def test_ai_mode():
    """测试AI控制模式"""
    try:
        print("🧪 测试AI控制模式...")
        
        # 测试获取数据接口
        data_response = requests.get('http://localhost:5000/api/data', timeout=10)
        if data_response.status_code == 200:
            data = data_response.json()
            print("✅ 数据接口调用成功！")
            print(f"📊 当前环境数据: {data}")
        else:
            print(f"❌ 数据接口调用失败: {data_response.status_code}")
            return False
        
        # 测试AI聊天接口
        print("\n🧪 测试AI聊天接口...")
        ai_payload = {
            "message": "我应该开窗还是关窗？",
            "environment": data
        }
        
        try:
            ai_response = requests.post(
                'http://localhost:5000/api/ai_chat',
                json=ai_payload,
                timeout=30
            )
            
            if ai_response.status_code == 200:
                ai_result = ai_response.json()
                print("✅ AI聊天接口调用成功！")
                print(f"🤖 AI建议: {ai_result.get('response', '')}")
            else:
                print(f"❌ AI聊天接口调用失败: {ai_response.status_code}")
                print(f"💬 错误信息: {ai_response.text}")
                return False
        except requests.Timeout:
            print("❌ AI聊天接口调用超时，请检查Ollama服务")
            return False
        except Exception as e:
            print(f"❌ AI聊天接口调用异常: {e}")
            return False
            
        # 测试AI模式开关
        print("\n🧪 测试AI模式开关...")
        toggle_response = requests.post(
            'http://localhost:5000/api/send_cmd',
            json={"cmd": "ai_mode"},
            timeout=10
        )
        
        if toggle_response.status_code == 200:
            result = toggle_response.json()
            print("✅ AI模式开关测试成功！")
            print(f"📢 响应: {result.get('msg', '')}")
        else:
            print(f"❌ AI模式开关测试失败: {toggle_response.status_code}")
            return False
            
        # 等待几秒钟，让AI模式有时间执行
        print("\n⏳ 等待AI模式执行...")
        time.sleep(10)
        
        return True
            
    except Exception as e:
        print(f"❌ 测试AI模式时出错: {e}")
        return False

if __name__ == "__main__":
    test_ai_mode()