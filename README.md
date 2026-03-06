# SmartGatewayMonitor

智能网关监控系统 - 融合环境监控、智能控制和 AI 决策的智能家居解决方案

## 项目简介

SmartGatewayMonitor 是一套面向智能家居场景的综合监控系统，融合了环境监控、智能控制和 AI 决策等技术，旨在解决用户在日常居家生活中面临的环境调节和设备智能管理问题。

系统通过实时采集环境数据、提供多种控制模式（手动、自动、AI）以及基于本地 LLM 模型的智能决策，为用户打造更加舒适、智能的家居环境。



<img width="348" height="256" alt="image" src="https://github.com/user-attachments/assets/109e5717-98d9-46c0-a0b4-b314644766ae" />

<img width="333" height="249" alt="image" src="https://github.com/user-attachments/assets/a943117a-2b61-4742-9897-c614d9777425" />



## 功能特性

### 🔍 环境数据监控
- 实时采集本地温湿度数据
- 获取室外温度、湿度、天气状况等信息
- 通过前端图表可视化展示历史数据变化趋势
- 每 3 秒自动更新一次数据，确保信息实时性

### 🎮 智能设备控制
- **手动控制**：用户可通过界面直接控制开窗/关窗
- **自动模式**：基于环境数据自动控制设备
- **AI 控制模式**：基于本地 LLM 模型智能决策
- 通过后端 API 发送指令，经云服务器转发至本地设备执行

### 🤖 AI 智能体系统
- 基于本地部署的 deepseek-r1:8b 模型
- 实现智能决策和自然语言交互功能
- 根据环境数据提供智能的开关窗建议
- 与用户进行自然语言对话，回答用户关于环境控制的问题

## 技术栈

### 硬件层
- **环境传感器**：DHT11/DHT22 温湿度传感器
- **执行器**：电机驱动窗户开关机构
- **网络模块**：ESP8266/ESP32 WiFi 模块

### 服务器层
- **本地服务器**：Python 3.8+, Flask 2.0+, Ollama 0.1.20+
- **云服务器**：TCP 通信服务
- **AI 模型**：deepseek-r1:8b（本地部署）

### 前端层
- **开发技术**：HTML5, Tailwind CSS, JavaScript
- **数据可视化**：Chart.js
- **图标库**：Font Awesome

## 系统架构

```
+-------------------+
|    前端层         |
|  Web 界面         |
|  数据可视化       |
|  AI 聊天功能      |
+-------------------+
|       HTTP API    |
+-------------------+
|    服务器层       |
|  Flask 后端服务   |
|  Ollama AI 服务   |
|  TCP 客户端       |
+-------------------+
|       TCP         |
+-------------------+
|    硬件层         |
|  环境传感器       |
|  执行器           |
|  TCP 客户端       |
+-------------------+
```

## 安装步骤

### 1. 硬件准备
- 安装 DHT11/DHT22 温湿度传感器
- 连接窗户控制执行器
- 配置 ESP8266/ESP32 WiFi 模块

### 2. 服务器环境搭建

#### 本地服务器
```bash
# 克隆项目
git clone <repository-url>
cd SmartGatewayMonitor

# 安装依赖
pip install -r requirements.txt

# 安装 Ollama（用于本地部署 AI 模型）
# 参考 https://ollama.com/download

# 下载 AI 模型
ollama pull deepseek-r1:8b

# 启动 Ollama 服务
ollama serve

# 启动后端服务
python app.py
```

#### 云服务器
```bash
# 启动 TCP 通信服务
python tcp_server.py
```

### 3. 前端部署
- 将前端文件部署到 Web 服务器或直接在浏览器中打开
- 配置前端 API 地址指向本地服务器

## 使用说明

### 1. 访问系统
打开浏览器，访问前端界面地址（默认为 http://localhost:5000）

### 2. 控制模式切换
- **手动模式**：点击界面上的开窗/关窗按钮直接控制
- **自动模式**：系统基于环境数据自动控制
- **AI 模式**：系统基于本地 LLM 模型智能决策

### 3. 查看环境数据
- 在主界面查看实时环境数据
- 在数据可视化区域查看历史数据趋势

### 4. 与 AI 交互
- 点击 AI 聊天按钮打开聊天界面
- 向 AI 提问关于环境控制的问题
- 查看 AI 基于当前环境数据的智能建议

## 核心功能代码示例

### AI 模型调用

```python
# AI模型调用代码
import requests
import json

def get_ai_decision(environment_data):
    """
    获取AI基于环境数据的决策
    """
    prompt = f"""
    作为智能家居环境控制专家，基于以下环境数据，提供智能的窗户控制建议：
    本地温度：{environment_data['local_temp']}°C
    本地湿度：{environment_data['local_humi']}%
    室外温度：{environment_data['outdoor_temp']}°C
    室外湿度：{environment_data['outdoor_humi']}%
    天气状况：{environment_data['weather']}
    
    请给出明确的建议：开窗、关窗或保持现状，并说明理由。
    """
    
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "deepseek-r1:8b",
            "prompt": prompt,
            "stream": False
        }
    )
    
    if response.status_code == 200:
        result = response.json()
        return result.get('response', '无法获取AI建议')
    return 'AI服务不可用'
```

### 数据更新

```javascript
// 数据更新函数
async function updateData() {
    try {
        const response = await fetch('/api/environment');
        if (response.ok) {
            const data = await response.json();
            // 更新数据卡片
            document.getElementById('local-temp').textContent = data.local_temp + '°C';
            document.getElementById('local-humi').textContent = data.local_humi + '%';
            document.getElementById('outdoor-temp').textContent = data.outdoor_temp + '°C';
            document.getElementById('weather').textContent = data.weather;
            
            // 更新图表
            updateCharts(data);
            
            // 更新AI建议
            updateAIAdvice(data);
            
            // 更新状态
            document.getElementById('status').textContent = '数据更新成功';
            document.getElementById('last-update').textContent = new Date().toLocaleTimeString();
        }
    } catch (error) {
        console.error('Error updating data:', error);
        document.getElementById('status').textContent = '数据更新失败';
    }
}
```

## 系统测试

### 测试环境
- **硬件环境**：本地温湿度传感器、窗户控制执行器、WiFi 模块
- **服务器环境**：本地服务器（8GB 内存，4 核心 CPU）、云服务器（2GB 内存，2 核心 CPU）
- **网络环境**：家庭宽带网络（下行 100Mbps，上行 20Mbps）
- **浏览器环境**：Chrome、Firefox、Safari 等主流浏览器

### 测试结果

#### 功能测试
- ✅ 环境数据监控：数据采集准确，更新及时，图表展示清晰
- ✅ 设备控制：手动控制响应迅速，自动模式逻辑正确，AI 控制决策合理
- ✅ AI 智能决策：基于环境数据的决策建议符合实际需求
- ✅ AI 自然语言交互：能够理解用户问题，提供准确的环境控制建议
- ✅ 系统稳定性：长时间运行无异常，网络波动时能够自动重连

#### 性能测试
- ⚡ 数据更新延迟：前端数据更新延迟小于 1 秒
- ⚡ 控制指令响应：控制指令从发送到执行的延迟小于 2 秒
- ⚡ AI 模型推理：AI 模型生成回复的时间约为 3-5 秒
- ⚡ 系统资源占用：本地服务器 CPU 使用率约为 30%，内存使用率约为 40%

## 未来展望

### 功能扩展
- **设备支持**：扩展支持灯光、空调、窗帘等更多智能家居设备
- **环境参数**：增加 PM2.5、CO2 浓度、噪声、光照等环境参数的采集和分析
- **移动应用**：开发 iOS 和 Android 移动应用，实现更便捷的远程控制

### 技术优化
- **AI 模型**：考虑模型量化、边缘计算等技术，提高 AI 推理速度，降低硬件要求
- **离线能力**：增强离线运行能力，减少对网络的依赖
- **个性化**：根据用户的生活习惯和偏好，对 AI 模型进行微调，提供更个性化的服务

### 安全性
- **数据加密**：加强数据传输和存储的加密措施
- **访问控制**：实现用户认证和权限管理
- **安全审计**：增加系统操作日志和安全审计功能

## 致谢

本项目在开发过程中，得到了指导教师的悉心指导和帮助，以及同学们的支持和协助。在此，向所有关心和帮助过项目开发的老师和同学表示衷心的感谢！

## 许可证

MIT License

## 联系方式

如有问题或建议，欢迎联系项目维护者：
- 邮箱：<maintainer-email>
- GitHub：<repository-url>
