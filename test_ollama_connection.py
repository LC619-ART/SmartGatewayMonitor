import requests

def test_ollama_connection():
    """测试Ollama服务连接"""
    try:
        # 测试Ollama服务是否运行
        response = requests.get('http://localhost:11434/api/tags', timeout=10)
        if response.status_code == 200:
            data = response.json()
            print("✅ Ollama服务运行正常！")
            print(f"📦 可用模型: {[model['name'] for model in data.get('models', [])]}")
            return True
        else:
            print(f"❌ Ollama服务返回错误码: {response.status_code}")
            return False
    except requests.ConnectionError:
        print("❌ 无法连接到Ollama服务，请检查服务是否运行")
        return False
    except Exception as e:
        print(f"❌ 测试Ollama连接时出错: {e}")
        return False

def test_ai_model_directly():
    """直接测试AI模型调用"""
    try:
        print("\n🧪 直接测试AI模型调用...")
        
        # 构建测试提示词
        prompt = """你是一个智能环境控制助手，基于本地部署的 deepseek-r1:8b 模型。你的任务是根据当前的环境数据，判断是否应该开关窗。

当前环境数据：
- 本地温度：18℃
- 本地湿度：19%
- 室外温度：2℃
- 室外湿度：29%
- 天气状况：多云
- 报警状态：正常

决策规则（请严格遵循）：
1. 如果本地温度高于28℃，应该开窗降温
2. 如果本地温度低于15℃，应该关窗保暖
3. 如果室外温度高于30℃或低于5℃，应该关窗
4. 如果室外天气为雨、雪、雾、霾、沙尘暴等恶劣天气，应该关窗
5. 如果本地湿度高于70%，应该关窗
6. 如果本地有高温报警，应该开窗降温
7. 如果室外温度适宜（18-26℃）且天气良好，应该开窗通风

请根据以上数据和规则，判断是否应该开窗或关窗。
请只返回以下三种答案之一：
1. open - 表示应该开窗
2. close - 表示应该关窗
3. keep - 表示保持当前状态

请不要返回任何其他文字或解释。
"""
        
        # 直接调用Ollama API
        response = requests.post(
            'http://localhost:11434/api/generate',
            json={
                "model": "deepseek-r1:8b",
                "prompt": prompt,
                "stream": False
            },
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            ai_response = result.get('response', '').strip().lower()
            print("✅ AI模型调用成功！")
            print(f"🤖 AI建议: {ai_response}")
            return True
        else:
            print(f"❌ AI模型调用失败，错误码：{response.status_code}")
            print(f"💬 错误信息: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ 测试AI模型时出错: {e}")
        return False

if __name__ == "__main__":
    print("🧪 测试Ollama服务连接...")
    ollama_connected = test_ollama_connection()
    
    if ollama_connected:
        test_ai_model_directly()