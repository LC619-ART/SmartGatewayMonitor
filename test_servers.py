import requests

def test_frontend_server():
    """测试前端服务器是否可以正常访问"""
    try:
        print("🧪 测试前端服务器...")
        response = requests.get('http://localhost:8000', timeout=10)
        if response.status_code == 200:
            print("✅ 前端服务器运行正常！")
            print(f"📄 响应状态码: {response.status_code}")
            print(f"📄 响应内容长度: {len(response.text)} 字符")
            print(f"📄 响应内容预览: {response.text[:200]}...")
            return True
        else:
            print(f"❌ 前端服务器返回错误码: {response.status_code}")
            return False
    except requests.ConnectionError:
        print("❌ 无法连接到前端服务器，请检查服务器是否运行")
        return False
    except Exception as e:
        print(f"❌ 测试前端服务器时出错: {e}")
        return False

def test_backend_server():
    """测试后端服务器是否可以正常访问"""
    try:
        print("\n🧪 测试后端服务器...")
        response = requests.get('http://localhost:5000/api/data', timeout=10)
        if response.status_code == 200:
            print("✅ 后端服务器运行正常！")
            print(f"📄 响应状态码: {response.status_code}")
            data = response.json()
            print(f"📊 当前环境数据: {data}")
            return True
        else:
            print(f"❌ 后端服务器返回错误码: {response.status_code}")
            return False
    except requests.ConnectionError:
        print("❌ 无法连接到后端服务器，请检查服务器是否运行")
        return False
    except Exception as e:
        print(f"❌ 测试后端服务器时出错: {e}")
        return False

if __name__ == "__main__":
    test_frontend_server()
    test_backend_server()