import serial
import time
import socket
import json
import threading

class Gateway:
    """智能网关类，连接串口和云服务器"""
    
    def __init__(self):
        # 串口配置
        self.serial_port = 'COM1'  # 添加这一行定义串口端口
        self.baud_rate = 38400
        
        # 云服务器配置
        self.server_host = '39.105.100.121'  # 公网云服务器
        self.server_port = 8080
        
        # 串口对象
        self.ser = None
        
        # TCP客户端对象
        self.tcp_client = None
        
        # 运行状态
        self.running = False
        
        # 线程对象
        self.read_thread = None
        self.tcp_thread = None
    
    def connect_serial(self):
        """连接串口"""
        try:
            self.ser = serial.Serial(self.serial_port, self.baud_rate, timeout=1)
            print(f"✅ 成功连接串口: {self.serial_port} ({self.baud_rate} bps)")
            return True
        except Exception as e:
            print(f"❌ 串口连接失败: {e}")
            return False
    
    def connect_server(self):
        """连接云服务器"""
        try:
            # 关闭现有连接
            if self.tcp_client:
                try:
                    self.tcp_client.close()
                except:
                    pass
            
            # 创建新的socket连接
            self.tcp_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # 设置连接超时
            self.tcp_client.settimeout(10)  # 10秒超时
            # 连接到服务器
            self.tcp_client.connect((self.server_host, self.server_port))
            # 重置超时，用于后续通信
            self.tcp_client.settimeout(None)
            print(f"✅ 成功连接云服务器: {self.server_host}:{self.server_port}")
            
            # 发送角色信息，服务器要求首先发送role:gateway
            try:
                role_message = "role:gateway"
                self.tcp_client.sendall((role_message + "\n").encode('utf-8'))
                print("✅ 已发送角色信息: role:gateway")
            except Exception as e:
                print(f"❌ 发送角色信息失败: {e}")
            
            return True
        except socket.timeout:
            print(f"⏰ 连接服务器超时: {self.server_host}:{self.server_port}")
            print("💡 请检查网络连接和服务器状态")
            return False
        except socket.gaierror:
            print(f"❌ 服务器地址解析失败: {self.server_host}")
            print("💡 请检查服务器地址是否正确")
            return False
        except ConnectionRefusedError:
            print(f"❌ 服务器拒绝连接: {self.server_host}:{self.server_port}")
            print("💡 请检查服务器是否运行，端口是否开放")
            return False
        except Exception as e:
            print(f"❌ 服务器连接失败: {e}")
            print("💡 请检查网络连接和服务器配置")
            return False
    
    def parse_serial_data(self, data):
        """解析串口数据"""
        try:
            # 实际数据格式: "{A0=18,A1=19}"
            temp = None
            humid = None
            
            # 清理数据格式，移除多余的花括号
            data = data.strip('{}')
            
            # 处理可能的重复数据，如 "{A0=18,A1=19}{A0=18,A1=19}"
            if '}{' in data:
                # 只取第一部分
                data = data.split('}{')[0]
            
            # 解析键值对
            parts = data.split(',')
            for part in parts:
                if '=' in part:
                    key, value = part.split('=')
                    if key == 'A0':  # A0 是温度
                        temp = float(value)
                    elif key == 'A1':  # A1 是湿度
                        humid = float(value)
            
            if temp is not None and humid is not None:
                return {
                    'temperature': temp,
                    'humidity': humid,
                    'timestamp': time.time()
                }
            return None
        except Exception as e:
            print(f"❌ 数据解析失败: {e}")
            return None
    
    def read_serial(self):
        """读取串口数据"""
        serial_reconnect_interval = 10  # 串口重连间隔（秒）
        last_serial_reconnect_attempt = 0
        
        while self.running:
            try:
                # 检查串口连接状态
                current_time = time.time()
                if not self.ser:
                    if current_time - last_serial_reconnect_attempt > serial_reconnect_interval:
                        print("⚠️  尝试重新连接串口...")
                        if self.connect_serial():
                            print("✅ 串口重新连接成功")
                        last_serial_reconnect_attempt = current_time
                
                # 读取串口数据
                if self.ser and self.ser.in_waiting > 0:
                    data = self.ser.readline().decode('utf-8').strip()
                    if data:
                        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
                        print(f"[{timestamp}] 📥 串口接收: '{data}'")
                        
                        # 解析数据
                        parsed_data = self.parse_serial_data(data)
                        if parsed_data:
                            print(f"[{timestamp}] 📤 解析结果: {parsed_data}")
                            
                            # 发送到服务器
                            if self.tcp_client:
                                try:
                                    # 服务器期望的格式：temp:25.5,hum:60
                                    temp = parsed_data['temperature']
                                    humid = parsed_data['humidity']
                                    # 构建服务器期望的格式
                                    message = f"temp:{temp},hum:{humid}"
                                    # 发送数据，添加换行符
                                    self.tcp_client.sendall((message + "\n").encode('utf-8'))
                                    print(f"[{timestamp}] ✅ 数据已发送到服务器: {message}")
                                except Exception as e:
                                    print(f"[{timestamp}] ❌ 发送失败: {e}")
                                    # 发送失败，可能连接已断开，重置tcp_client
                                    try:
                                        self.tcp_client.close()
                                    except:
                                        pass
                                    self.tcp_client = None
            except Exception as e:
                print(f"❌ 读取串口时出错: {e}")
                # 出错后重置串口连接
                if self.ser:
                    try:
                        self.ser.close()
                    except:
                        pass
                    self.ser = None
            
            # 防止CPU占用过高
            time.sleep(0.05)
    
    def receive_server_commands(self):
        """接收服务器命令"""
        while self.running:
            try:
                if self.tcp_client:
                    try:
                        # 设置接收超时，避免阻塞
                        self.tcp_client.settimeout(1)
                        # 接收服务器命令
                        data = self.tcp_client.recv(1024)
                        if data:
                            # 处理可能的多行数据
                            commands = data.decode('utf-8').strip().split('\n')
                            for command in commands:
                                command = command.strip()
                                if command:
                                    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
                                    print(f"[{timestamp}] 📥 服务器命令: '{command}'")
                                    
                                    # 处理命令并写入串口
                                    if self.ser:
                                        try:
                                            # 服务器发送的命令格式是cmd:xxx，我们直接写入串口
                                            self.ser.write((command + '\n').encode('utf-8'))
                                            print(f"[{timestamp}] ✅ 命令已写入串口")
                                        except Exception as e:
                                            print(f"[{timestamp}] ❌ 写入串口失败: {e}")
                        else:
                            # 连接已关闭
                            print("⚠️  服务器连接已关闭")
                            try:
                                self.tcp_client.close()
                            except:
                                pass
                            self.tcp_client = None
                    except socket.timeout:
                        # 正常超时，继续循环
                        pass
                    except Exception as e:
                        # 连接错误，重置连接
                        print(f"❌ 接收服务器命令时出错: {e}")
                        try:
                            self.tcp_client.close()
                        except:
                            pass
                        self.tcp_client = None
            except Exception as e:
                # 其他错误
                print(f"❌ 服务器命令处理出错: {e}")
            
            # 防止CPU占用过高
            time.sleep(0.1)
    def start(self):
        """启动网关"""
        print("=" * 100)
        print("智能网关启动中...")
        print("=" * 100)
        
        # 连接串口
        serial_connected = self.connect_serial()
        if not serial_connected:
            print("⚠️  串口连接失败，将在运行中继续尝试连接...")
        else:
            print("✅ 串口连接成功")
        
        # 连接服务器
        server_connected = self.connect_server()
        if not server_connected:
            print("⚠️  服务器连接失败，将尝试重连...")
        else:
            print("✅ 服务器连接成功")
        
        # 设置运行状态（即使串口连接失败也继续启动）
        self.running = True
        
        # 启动读取串口线程
        self.read_thread = threading.Thread(target=self.read_serial)
        self.read_thread.daemon = True
        self.read_thread.start()
        print("✅ 串口读取线程已启动")
        
        # 启动接收服务器命令线程
        self.tcp_thread = threading.Thread(target=self.receive_server_commands)
        self.tcp_thread.daemon = True
        self.tcp_thread.start()
        print("✅ 服务器命令接收线程已启动")
        
        print("=" * 100)
        print("智能网关启动成功！")
        print("正在等待数据...")
        print("=" * 100)
        
        # 主线程保持运行
        try:
            reconnect_interval = 5  # 初始重连间隔（秒）
            max_reconnect_interval = 60  # 最大重连间隔（秒）
            reconnect_count = 0  # 重连计数器
            
            while self.running:
                # 检查服务器连接状态
                if not self.tcp_client:
                    reconnect_count += 1
                    print(f"⚠️  第 {reconnect_count} 次尝试重新连接服务器...")
                    print(f"   连接目标: {self.server_host}:{self.server_port}")
                    
                    if self.connect_server():
                        print("✅ 服务器重新连接成功")
                        reconnect_count = 0
                        reconnect_interval = 5  # 重置重连间隔
                    else:
                        # 指数退避重连策略
                        print(f"⏰ {reconnect_interval}秒后再次尝试...")
                        time.sleep(reconnect_interval)
                        # 重连间隔翻倍，最多60秒
                        reconnect_interval = min(reconnect_interval * 2, max_reconnect_interval)
                else:
                    # 连接正常，重置重连状态
                    reconnect_count = 0
                    reconnect_interval = 5
                    # 定期检查连接状态
                    time.sleep(5)
                    
        except KeyboardInterrupt:
            print("\n⏹️  正在停止网关...")
            self.stop()
    
    def stop(self):
        """停止网关"""
        self.running = False
        
        # 关闭串口
        if self.ser and self.ser.is_open:
            self.ser.close()
            print("✅ 串口已关闭")
        
        # 关闭TCP连接
        if self.tcp_client:
            self.tcp_client.close()
            print("✅ 服务器连接已关闭")
        
        print("✅ 智能网关已停止")

if __name__ == "__main__":
    gateway = Gateway()
    gateway.start()