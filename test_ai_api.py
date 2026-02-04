import requests

def test_ai_chat_api():
    """测试AI聊天API是否正常工作"""
    try:
        print("🧪 测试AI聊天API...")
        
        # 构建测试数据
        test_data = {
            "temp": "19.0",
            "humidity": "18.0",
            "weather_temp": "3",
            "weather_hum": "59",
            "weather_text": "阴",
            "alarm": "正常"
        }
        
        # 测试AI聊天接口
        ai_payload = {
            "message": "我应该开窗还是关窗？",
            "environment": test_data
        }
        
        ai_response = requests.post(
            'http://localhost:5000/api/ai_chat',
            json=ai_payload,
            timeout=15
        )
        
        if ai_response.status_code == 200:
            ai_result = ai_response.json()
            print("✅ AI聊天API调用成功！")
            print(f"🤖 AI建议: {ai_result.get('response', '')}")
            return True
        else:
            print(f"❌ AI聊天API调用失败: {ai_response.status_code}")
            print(f"💬 错误信息: {ai_response.text}")
            return False
            
    except Exception as e:
        print(f"❌ 测试AI聊天API时出错: {e}")
        return False

if __name__ == "__main__":
    test_ai_chat_api()