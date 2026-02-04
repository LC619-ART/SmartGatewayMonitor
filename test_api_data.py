import requests

def test_api_data():
    """测试API返回的数据结构"""
    try:
        print("🧪 测试API返回的数据...")
        response = requests.get('http://localhost:5000/api/data', timeout=10)
        if response.status_code == 200:
            data = response.json()
            print("✅ API调用成功！")
            print(f"📊 完整数据: {data}")
            print(f"🌡️  本地温度: {data.get('temp')}")
            print(f"💧  本地湿度: {data.get('humidity')}")
            print(f"☀️  室外温度: {data.get('weather_temp')}")
            print(f"☁️  天气状况: {data.get('weather_text')}")
            return data
        else:
            print(f"❌ API调用失败: {response.status_code}")
            return None
    except Exception as e:
        print(f"❌ 测试API时出错: {e}")
        return None

if __name__ == "__main__":
    test_api_data()