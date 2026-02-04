from flask import Flask, request, jsonify
from flask_cors import CORS
import socket
import threading
import requests
import json
import time

app = Flask(__name__)
CORS(app)  # 添加 CORS 支持

# 全局变量存储最新数据
latest_data = {
    "temp": "未知",
    "humidity": "未知",
    "alarm": "正常",
    "weather_temp": "未知",
    "weather_hum": "未知",
    "weather_text": "未知"
}

# TCP客户端配置
SERVER_HOST = "39.105.100.121"
SERVER_PORT = 8080
tcp_client = None

# 自动模式状态
auto_mode_enabled = False
# AI控制模式状态
ai_mode_enabled = False

def connect_server():
    """连接云服务器"""
    global tcp_client
    try:
        tcp_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcp_client.connect((SERVER_HOST, SERVER_PORT))
        # 发送前端角色
        tcp_client.sendall("role:app\n".encode('utf-8'))
        print("✅ 前端连接服务器成功")
        # 启动接收数据线程
        recv_thread = threading.Thread(target=receive_data)
        recv_thread.daemon = True
        recv_thread.start()
    except Exception as e:
        print(f"❌ 前端连接服务器失败: {e}")
        print("⚠️  云服务器连接失败，但AI功能仍然可用")

def receive_data():
    """接收服务器转发的数据"""
    global latest_data
    while True:
        try:
            if tcp_client:
                data = tcp_client.recv(1024).decode('utf-8').strip()
                if data:
                    print(f"📥 收到服务器数据: {data}")
                    print(f"📥 数据长度: {len(data)}")
                    print(f"📥 数据类型: {type(data)}")
                    
                    # 解析数据
                    # 特殊处理天气数据
                    if "weather:" in data:
                        # 提取天气数据部分
                        weather_part = data.split("weather:")[1]
                        print(f"📥 提取天气部分: {weather_part}")
                        
                        # 直接解析天气数据，不进行复杂的结束位置判断
                        # 按逗号分割所有部分
                        weather_items = weather_part.split(",")
                        print(f"📥 天气数据项列表: {weather_items}")
                        
                        # 遍历所有天气数据项
                        for item in weather_items:
                            print(f"📥 处理天气数据项: {item}")
                            if "=" in item:
                                key, value = item.split("=", 1)
                                print(f"📥 天气数据键值对: {key}={value}")
                                if key == "temp":
                                    latest_data["weather_temp"] = value
                                    print(f"📥 更新天气温度: {value}")
                                elif key == "hum":
                                    latest_data["weather_hum"] = value
                                    print(f"📥 更新天气湿度: {value}")
                                elif key == "text":
                                    latest_data["weather_text"] = value
                                    print(f"📥 更新天气状况: {value}")
                    
                    # 解析其他数据（非天气数据）
                    else:
                        print(f"📥 处理非天气数据: {data}")
                        parts = data.split(",")
                        print(f"📥 分割后的数据项: {parts}")
                        for part in parts:
                            print(f"📥 处理数据项: {part}")
                            # 处理 key:value 格式
                            if ":" in part:
                                key, value = part.split(":", 1)
                                print(f"📥 解析 key:value 格式: {key}={value}")
                                if key == "temp":
                                    latest_data["temp"] = value
                                    print(f"📥 更新本地温度: {value}")
                                elif key == "hum":
                                    latest_data["humidity"] = value
                                    print(f"📥 更新本地湿度: {value}")
                                elif key == "alarm":
                                    latest_data["alarm"] = "高温报警" if value == "high_temp" else "正常"
                                    print(f"📥 更新报警状态: {latest_data['alarm']}")
                            # 处理 key=value 格式
                            elif "=" in part:
                                key, value = part.split("=", 1)
                                print(f"📥 解析 key=value 格式: {key}={value}")
                                if key == "temp":
                                    latest_data["temp"] = value
                                    print(f"📥 更新本地温度: {value}")
                                elif key == "hum":
                                    latest_data["humidity"] = value
                                    print(f"📥 更新本地湿度: {value}")
                                elif key == "alarm":
                                    latest_data["alarm"] = "高温报警" if value == "high_temp" else "正常"
                                    print(f"📥 更新报警状态: {latest_data['alarm']}")
                            else:
                                print(f"📥 无法解析的数据项: {part}")
                        
                        # 打印更新后的数据
                        print(f"📥 更新后的数据: {latest_data}")
        except Exception as e:
            print(f"❌ 接收数据出错: {e}")
            import traceback
            traceback.print_exc()
            # 重连
            connect_server()
            continue

@app.route('/api/data', methods=['GET'])
def get_data():
    """获取最新数据"""
    return jsonify(latest_data)

@app.route('/api/send_cmd', methods=['POST'])
def send_cmd():
    """发送控制指令"""
    cmd = request.json.get('cmd')
    if not cmd or not tcp_client:
        return jsonify({"status": "fail", "msg": "指令为空或未连接服务器"})
    try:
        if cmd == 'auto_mode':
            global auto_mode_enabled
            auto_mode_enabled = not auto_mode_enabled
            if auto_mode_enabled:
                # 启动自动模式处理线程
                auto_thread = threading.Thread(target=auto_mode_handler)
                auto_thread.daemon = True
                auto_thread.start()
                return jsonify({"status": "success", "msg": "自动模式已开启"})
            else:
                return jsonify({"status": "success", "msg": "自动模式已关闭"})
        elif cmd == 'ai_mode':
            global ai_mode_enabled
            ai_mode_enabled = not ai_mode_enabled
            if ai_mode_enabled:
                # 启动AI模式处理线程
                ai_thread = threading.Thread(target=ai_mode_handler)
                ai_thread.daemon = True
                ai_thread.start()
                return jsonify({"status": "success", "msg": "AI控制模式已开启"})
            else:
                return jsonify({"status": "success", "msg": "AI控制模式已关闭"})
        else:
            tcp_client.sendall((f"cmd:{cmd}\n").encode('utf-8'))
            return jsonify({"status": "success", "msg": f"指令{cmd}发送成功"})
    except Exception as e:
        return jsonify({"status": "fail", "msg": str(e)})

def auto_mode_handler():
    """自动模式处理函数"""
    global auto_mode_enabled
    while auto_mode_enabled:
        try:
            # 获取当前环境数据
            temp = latest_data.get('temp', '未知')
            humidity = latest_data.get('humidity', '未知')
            weather_temp = latest_data.get('weather_temp', '未知')
            weather_hum = latest_data.get('weather_hum', '未知')
            weather_text = latest_data.get('weather_text', '未知')
            alarm = latest_data.get('alarm', '正常')
            
            # 尝试转换温度和湿度为数字
            try:
                temp = float(temp)
                humidity = float(humidity)
                weather_temp = float(weather_temp)
                weather_hum = float(weather_hum)
            except (ValueError, TypeError):
                print("⚠️ 环境数据格式错误，跳过自动判断")
                time.sleep(10)
                continue
            
            # 自动开关逻辑判断
            if should_open_window(temp, humidity, weather_temp, weather_hum, weather_text, alarm):
                tcp_client.sendall("cmd:open_window\n".encode('utf-8'))
                print("🚪 自动执行：开窗")
            elif should_close_window(temp, humidity, weather_temp, weather_hum, weather_text, alarm):
                tcp_client.sendall("cmd:close_window\n".encode('utf-8'))
                print("🚪 自动执行：关窗")
            
            # 每10秒检查一次
            time.sleep(10)
        except Exception as e:
            print(f"❌ 自动模式处理出错: {e}")
            time.sleep(10)
            continue

def should_open_window(temp, humidity, weather_temp, weather_hum, weather_text, alarm):
    """判断是否应该开窗"""
    # 本地温度过高
    if temp > 28:
        return True
    # 本地湿度适宜且室外天气良好
    if 40 <= humidity <= 60 and weather_text in ['晴', '多云'] and 18 <= weather_temp <= 26:
        return True
    # 本地有高温报警
    if alarm == '高温报警':
        return True
    return False

def should_close_window(temp, humidity, weather_temp, weather_hum, weather_text, alarm):
    """判断是否应该关窗"""
    # 本地温度过低
    if temp < 15:
        return True
    # 本地湿度不适宜
    if humidity > 70:
        return True
    # 室外天气恶劣
    if weather_text in ['雨', '雪', '雾', '霾', '沙尘暴']:
        return True
    # 室外温度过高或过低
    if weather_temp > 30 or weather_temp < 5:
        return True
    return False

def ai_mode_handler():
    """AI控制模式处理函数"""
    global ai_mode_enabled
    while ai_mode_enabled:
        try:
            # 获取当前环境数据
            temp = latest_data.get('temp', '18')  # 默认值 18℃
            humidity = latest_data.get('humidity', '19')  # 默认值 19%
            weather_temp = latest_data.get('weather_temp', '2')  # 默认值 2℃
            weather_hum = latest_data.get('weather_hum', '29')  # 默认值 29%
            weather_text = latest_data.get('weather_text', '多云')  # 默认值 多云
            alarm = latest_data.get('alarm', '正常')  # 默认值 正常
            
            # 构建更精确的提示词，请求AI给出开关窗建议
            prompt = f"""你是一个智能环境控制助手，基于本地部署的 deepseek-r1:8b 模型。你的任务是根据当前的环境数据，判断是否应该开关窗。

当前环境数据：
- 本地温度：{temp}℃
- 本地湿度：{humidity}%
- 室外温度：{weather_temp}℃
- 室外湿度：{weather_hum}%
- 天气状况：{weather_text}
- 报警状态：{alarm}

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
            
            print("🤖 AI模式：调用本地Ollama模型...")
            # 调用本地 ollama API
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
                print(f"🤖 AI 建议: {ai_response}")
                
                # 根据AI建议执行相应操作
                if ai_response == 'open':
                    if tcp_client:
                        tcp_client.sendall("cmd:open_window\n".encode('utf-8'))
                        print("🚪 AI执行：开窗")
                    else:
                        print("⚠️  未连接到云服务器，无法执行开窗操作")
                elif ai_response == 'close':
                    if tcp_client:
                        tcp_client.sendall("cmd:close_window\n".encode('utf-8'))
                        print("🚪 AI执行：关窗")
                    else:
                        print("⚠️  未连接到云服务器，无法执行关窗操作")
                else:
                    print("🚪 AI建议：保持当前状态")
            else:
                print(f"❌ AI服务调用失败，错误码：{response.status_code}")
            
            # 每30秒检查一次
            time.sleep(30)
        except requests.ConnectionError:
            print("❌ 无法连接到Ollama服务，请检查服务是否运行")
            time.sleep(30)
            continue
        except requests.Timeout:
            print("❌ Ollama服务调用超时，请检查服务状态")
            time.sleep(30)
            continue
        except Exception as e:
            print(f"❌ AI模式处理出错: {e}")
            import traceback
            traceback.print_exc()
            time.sleep(30)
            continue

@app.route('/api/ai_chat', methods=['POST'])
def ai_chat():
    """AI 聊天接口"""
    try:
        message = request.json.get('message')
        environment = request.json.get('environment', {})
        
        print(f"🤖 收到AI聊天请求: {message}")
        print(f"📊 环境数据: {environment}")
        
        # 构建更简洁的提示词
        prompt = f"""你是一个智能环境控制助手，基于本地部署的 deepseek-r1:8b 模型。你的任务是根据当前的环境数据，为用户提供简洁、清晰的开关窗建议。

当前环境数据：
- 本地温度：{environment.get('temp', '未知')}℃
- 本地湿度：{environment.get('humidity', '未知')}%
- 室外温度：{environment.get('weather_temp', '未知')}℃
- 室外湿度：{environment.get('weather_hum', '未知')}%
- 天气状况：{environment.get('weather_text', '未知')}
- 报警状态：{environment.get('alarm', '未知')}

用户问题：{message}

请根据以上信息，为用户提供简洁、清晰的开关窗建议。

输出格式要求（请严格遵循）：
1. 首先给出明确的建议（开窗/关窗/保持现状）
2. 然后简要说明理由（基于环境数据的分析）
3. 使用简洁的语言，避免冗长的解释
4. 格式清晰，使用换行和缩进，易于阅读

示例输出：
建议: 关窗
- 室外温度较低（2℃），不适合开窗
- 天气状况为多云，需要保暖
"""
        
        # 调用本地 ollama API
        print("🤖 调用Ollama模型...")
        response = requests.post(
            'http://localhost:11434/api/generate',
            json={
                "model": "deepseek-r1:8b",
                "prompt": prompt,
                "stream": False
            },
            timeout=15  # 减少超时时间
        )
        
        if response.status_code == 200:
            result = response.json()
            ai_response = result.get('response', '').strip()
            print(f"✅ AI响应成功: {ai_response[:100]}...")
            return jsonify({"response": ai_response})
        else:
            print(f"❌ AI服务返回错误: {response.status_code}")
            return jsonify({"response": f"抱歉，AI 服务暂时不可用。错误码：{response.status_code}"})
            
    except requests.ConnectionError:
        print("❌ 无法连接到Ollama服务")
        return jsonify({"response": "抱歉，无法连接到本地AI服务，请检查Ollama是否运行。"})
    except requests.Timeout:
        print("❌ Ollama服务调用超时")
        return jsonify({"response": "抱歉，AI服务响应超时，请稍后再试。"})
    except Exception as e:
        print(f"❌ AI 聊天出错: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({"response": f"抱歉，处理你的请求时出错：{str(e)}"})

if __name__ == "__main__":
    # 启动时连接服务器
    connect_server()
    # 运行后端服务（使用非调试模式）
    app.run(host='0.0.0.0', port=5000, debug=False)