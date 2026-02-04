融合视觉识别与语音交互的老年人智能看护系统设计与实现
一、基本信息
项目	内容
论文题目	融合视觉识别与语音交互的老年人智能看护系统设计与实现
学生信息	张楠（天津科技大学人工智能学院物联网工程 2021 级，学号 21104122）
指导教师	史艳翠
研究方向	物联网应用技术
完成时间	2025 年 5 月
核心定位	面向独居 / 高龄老年人，融合计算机视觉、语音交互、智能控制技术，解决安全、孤独、生活不便问题
二、系统核心功能
（一）人物摔倒检测系统
核心技术：YOLOv8n-Pose 姿态估计模型 + 自定义摔倒判定算法，Roboflow 数据集训练，AutoDL 云算力平台训练后转为 TensorRT 模型
硬件配置：Web Camera 语音视频摄像头（200 万像素，640*480@25FPS）、笔记本电脑（NVIDIA GeForce GTX 1650，CUDA 11.8）
功能实现：本地低延迟检测，触发后通过蜂鸣器报警 + 邮件推送告警（含摔倒图像），视频流通过 SRS 流媒体服务器实时推送到 APP
判定条件：肩膀与脚踝 / 膝盖相对位置、关键点宽高比、膝盖与髋部角度、肩 - 髋 - 膝夹角等 5 项指标
（二）AI 智能体交互系统
核心技术：SileroVAD 语音检测 + DoubaoASR 语音识别 + ChatGLM LLM 语义理解 + EdgeTTS 文字转语音
硬件配置：ESP32-S3-N16R8 主控、INMP441 数字麦克风、MAX98357 音频放大模块、3W8R 扬声器、0.91 寸 OLED 屏
功能实现：音频采集→WiFi 上传云端→语音转文字→LLM 生成回复→文字转语音→本地播放，支持休眠唤醒机制
（三）智能家居控制系统
核心技术：STM32 主控 + ESP8266-01S 通信模块，MQTT 协议，本地自动控制 + APP 远程控制
硬件配置：STM32F103C8T6、DHT11 温湿度传感器、光敏电阻、LED 灯（模拟电灯）、直流电机（模拟风扇）、蜂鸣器
功能实现：
自动控制：光照不足时开灯，温度＞30℃或湿度＞70% 时启动风扇
远程控制：APP 发送指令，通过 TCP 服务器转发至 ESP8266，再通过串口控制 STM32
三、系统架构设计
（一）分层架构
硬件层：摔倒检测设备、AI 交互设备、智能家居控制设备
服务器层：阿里云 ECS（2 核 2G，Ubuntu22.04）、MySQL 数据库、SRS 流媒体服务器、TCP 通信服务器、API 服务
前端层：Flutter 开发的 APP（登录注册、远程监控、设备控制、用户信息）
（二）技术栈
硬件开发：C 语言（单片机驱动）
后端开发：Python（Flask 框架、模型推理）、MySQL（数据存储）、Docker（服务部署）、WebSocket/TCP（通信）
前端开发：Dart（Flutter 框架）
工程管理：Gitee（代码托管）、Maven（依赖管理）、Git（版本控制）
（三）数据库设计
数据库	表名	核心字段	用途
iot_system	device_control	设备编号、操作时间、设备类型、状态	存储设备控制日志
iot_system	sensor_data	数据编号、时间戳、温度、湿度	存储温湿度传感器数据
user_management	user_info	用户编号、用户名、密码哈希值、邮箱	存储用户账户信息
user_management	verification_code	编号、邮箱、验证码、创建时间、过期时间	存储注册 / 找回密码验证码
（四）服务器配置
端口开放：TCP（3456/5000/6000 等）、UDP（8000）、HTTP（8080/8083/8088）、RTMP（1935）
核心服务：SRS 流媒体服务器（支持 RTMP/WebRTC）、TCP 通信服务器（设备 - 云端桥梁）、AI 智能体后端（6652 端口）
四、APP 功能设计
（一）核心页面
登录注册页：支持邮箱验证码注册、密码重置，用户名 / 邮箱唯一校验
远程监控页：视频地址订阅、WebRTC 协议实时播放、摔倒检测开关
智能家居页：温湿度数据可视化（折线图）、设备手动 / 自动控制切换
用户信息页：个人信息展示、头像修改、退出登录
（二）核心交互
视频流传输：WebRTC 协议（低延迟），支持后台切换不中断播放
指令通信：APP→Device-API→TCP 服务器→ESP8266→STM32
数据同步：传感器数据每秒上传云端，APP 轮询获取最新数据
五、系统测试结果
测试模块	测试内容	结论
APP 功能	注册登录、验证码校验、会话持久化、视频播放	全部通过，功能正常
摔倒检测	摔倒识别、误判率、告警邮件、多场景适配	识别准确率 0.99+，无明显误判
AI 交互	唤醒响应、语音识别、语义理解、语音播放	交互流畅，断网提示异常
智能家居	设备控制、传感器数据上传、自动控制逻辑	响应及时，控制精准
六、总结与展望
（一）核心成果
实现三大核心功能的一体化集成，满足老年人安全看护、情感陪伴、生活便捷需求
模型轻量化部署，本地推理低延迟，适配边缘计算场景
支持远程监控与控制，操作简单适配老年人群体
（二）现存不足
摔倒检测仅支持单摄像头，复杂光照 / 遮挡场景准确率下降
AI 交互依赖网络，无离线唤醒与对话功能
智能家居挂载设备有限，APP 界面功能需优化
（三）未来展望
扩展多摄像头接入，优化摔倒检测算法鲁棒性
开发离线交互功能，降低网络依赖
增加更多家居设备适配，优化 APP 交互体验
推进实际场景应用落地，完善智慧养老解决方案
21104122_张楠_论文定稿.pdf
我需要提取所有内容
融合视觉识别与语音交互的老年人智能看护系统设计与实现
一、基础信息
项目	详情
论文标题	融合视觉识别与语音交互的老年人智能看护系统设计与实现（An Intelligent Monitoring System for the Elderly Combining Vision-based Recognition and Speech Interaction）
学生信息	姓名：张楠；学号：21104122；年级：2021 级；学科专业：物联网工程；学院：人工智能学院
指导教师	史艳翠
研究方向	物联网应用技术
完成时间	2025 年 5 月
学校信息	天津科技大学（学校代码：10057）；密级：公开
申请学位	工学学士
二、学位声明与授权
（一）原创性声明
本人郑重声明：所呈交的学位论文，是本人在导师的指导下，独立进行研究工作所取得的成果。除文中已经注明引用的内容外，本论文不包含任何其他个人或集体已经发表或撰写过的作品成果。对本文的研究做出重要贡献的个人和集体，均已在文中以明确方式标明。本人完全知晓本声明的法律后果由本人承担。
声明人签名：张楠；日期：2025 年 5 月 25 日
（二）使用授权书
本人同意学校保留并向国家有关部门或机构送交论文的复印件和电子版，允许论文被查阅和借阅。本学位论文属于公开论文。
作者签名：张楠；日期：2025 年 5 月 25 日
指导教师签名：史艳翠；日期：2025 年 5 月 25 日
三、毕业设计（论文）任务书
（一）基本信息
学院：人工智能学院；专业：物联网工程；学生学号：21104122；学生姓名：张楠；指导教师：史艳翠
完成期限：2024 年 11 月 20 日至 2025 年 6 月 10 日
（二）设计内容
本智能看护系统是融合计算机视觉、语音交互和智能控制等技术，构建的一套面向独居或者高龄老年人群体的综合系统，聚焦解决老年人在日常居家生活中面临的身体安全问题、心理孤独问题和生活不便问题。
（三）主要功能
人物摔倒检测：使用 YOLOv8-Pose 姿态估计的深度学习模型，配合 Roboflow 上人物摔倒的数据集，在 AutoDL 云算力平台上进行模型训练，最后转为 TensorRT 模型部署到边缘计算平台上。能够实时处理摄像头画面，在设备本地实现低延迟且准确的人物摔倒检测。当人物摔倒时生成告警信息并通过邮件推送至用户邮箱。
AI 智能体交互：通过工作流集成 SilroVAD 语音检测模型、DoubaoASR 豆包语音识别模型、ChatGLM LLM 智谱清言语音处理模型、EdgeTTS 文字转语音模型形成 AI 智能体，配合硬件进行语音输入和输出，能够实现流畅的自然语言对话，为老年人提供全天候的精神慰藉和情感支持。
智能家居控制：使用 STM32 作为控制芯片，Esp8266-01S 作为通信模块，LED 灯模拟电灯，电机佩戴螺旋浆模拟风扇，蜂鸣器模拟报警设备，同时部署温湿度传感器与光照传感器，通过 APP 远程发送指令来控制设备状态，也可以设定特定的温湿度或光照阈值，跟随环境变化自动调整家居设备的工作状态。
（四）论文撰写要求
独立完成，严禁抄袭。
外文翻译与题目相关，中文不少于 5000 字。
论文应严格按照毕业手册要求撰写，方案合理、条理清晰、图表齐全，设计符合规范，不少于 25 篇参考文献，其中至少 5 篇英文文献，近五年参考文献不少于 10 篇，并在正文中引用注释，文字不少于 20000 字。
（五）参考文献（部分）
[1] 杨涵墨。中国人口老龄化新趋势及老年人口新特征 [J]. 人口与经济，2022 (05):17-28.
[2] 宁吉喆。第七次全国人口普查主要数据情况 [R]. 2021.
[3] 国家卫生健康委员会. 2023 年国家老龄工作报告 [Z]. 2023.
[4] Raza M, Yousaf M H, Velastin S A. Integrating Attention Mechanisms in YOLOv8 for Improved Fall Detection Performance[J]. IEEE Access, 2024, 12:45678-45690.
[5] Kaplan F, Ramirez R. The role of conversational AI agents in providing support and social care for the elderly[J]. Expert Systems with Applications, 2023, 214:119035.
指导教师签字：史艳翠；填写日期：2025 年 1 月 10 日
四、摘要与关键词
（一）中文摘要
中国人口老龄化程度正在不断加深，独居及高龄老人的居家安全与精神陪伴问题也日益突出，传统的养老方式难以胜任现阶段的养老需求，本系统可实现智能看护，能有效满足当前多样化、智能化的看护需求。
本系统主要由三个子系统组成：人物摔倒检测系统，基于 YOLOv8n-Pose 模型与自定义摔倒判定算法，结合邮件告警与蜂鸣器报警机制，可在被监护对象发生摔倒行为时实现快速响应，有效降低独居老年人错过救助时机的风险；AI 智能体交互系统，可以实时监听对话并提供准确有效的回复，从而缓解老年人因缺少沟通交流而导致的焦虑和空虚；智能家居控制系统，可以让居家生活更加方便快捷，通过 APP 就可实现对各类家具设备的远程控制，让老年人的居家生活更加舒适。
本智能看护系统立足于当前智慧养老市场不断扩展的前提下，将前沿科技落实到日常生活中，不仅满足现代老年人更高的养老条件要求，还具备一定的社会应用价值，尤其适用于面向老年人的智能照护场景，具有良好的推广前景。
（二）关键词
物联网；智能看护系统；摔倒检测；语音交互；智能家居
（三）英文摘要（ABSTRACT）
The aging degree of China's population is deepening, and the problem of home safety and spiritual companionship of the elderly living alone and the elderly is also increasingly prominent. The traditional way of pension is difficult to meet the needs of pension at this stage. This system can realize intelligent nursing, which can effectively meet the current diversified and intelligent nursing needs.
The system mainly consists of three subsystems: the fall detection system, which is based on YOLOv8n-Pose model and custom fall judgment algorithm, combined with email alarm and buzzer alarm mechanism, can achieve rapid response when the monitored object falls, and effectively reduce the risk of missing the rescue opportunity for the elderly living alone. The AI agent interaction system can monitor the dialogue in real time and provide accurate and effective responses, so as to alleviate the anxiety and emptiness caused by the lack of communication among the elderly. Smart home control system can make home life more convenient and fast. Remote control of all kinds of furniture and equipment can be realized through APP, so that the home life of the elderly is more comfortable.
Based on the premise of the continuous expansion of the current smart pension market, this intelligent care system implements cutting-edge technology into daily life. It not only meets the higher requirements of modern elderly pension conditions, but also has certain social application value, especially for intelligent care scenarios for the elderly, which has good promotion prospects.
（四）英文关键词（Key Words）
Internet of Things; intelligent care system; fall detection; voice interaction; smart home
五、目录
第 1 章 绪论 .............................................................. 1
1.1 课题研究背景 ........................................................ 1
1.2 研究发展现状 ........................................................ 2
1.3 论文工作安排 ........................................................ 4
第 2 章 系统分析 .............................................................. 5
2.1 系统总体功能 ........................................................ 5
2.2 系统架构设计 ........................................................ 5
2.3 可行性分析 .......................................................... 6
第 3 章 智能看护系统的硬件设计 .................................................. 7
3.1 人物摔倒检测系统设计 ................................................ 7
3.2 AI 智能体交互系统设计 ............................................... 11
3.3 智能家居控制系统设计 ............................................... 16
第 4 章 智能看护系统的云服务器设计 ............................................. 22
4.1 云服务器环境搭建 ................................................... 22
4.2 MySQL 数据库设计 ................................................... 23
4.3 部署 SRS 流媒体服务 .................................................. 25
4.4 TCP 通信服务设计 ................................................... 25
4.5 AI 智能体后端设计 ................................................... 26
4.6 用户管理 User-API 设计 ............................................... 27
4.7 硬件控制 Device-API 设计 ............................................. 29
第 5 章 智能看护系统的 APP 设计 .................................................. 31
5.1 APP 开发工具 ........................................................ 31
5.2 用户登录注册页面设计 ............................................... 31
5.3 远程监控页面设计 ................................................... 35
5.4 智能家居页面设计 ................................................... 37
5.5 用户信息页面设计 ................................................... 39
第 6 章 系统测试与结果分析 ..................................................... 41
第 7 章 总结与展望 ............................................................. 45
参考文献 ..................................................................... 46
致谢 ......................................................................... 48
六、正文内容
第 1 章 绪论
1.1 课题研究背景
人口老龄化是指老年人口在总人口所占比例逐渐上升的现象。如今，中国不得不面对人口老龄化逐渐加重这一现实挑战。根据第七次全国人口普查的数据显示，截至 2020 年，60 岁及以上人口已达到 2.64 亿，占全国总人口的 18.7%，其中 65 岁及以上人口就有 1.91 亿，占比高达 13.5%，比 2010 年分别上升了 5.44% 和 4.63%。全球每 4 个老年人中就有 1 个是中国人，未来 30 多年中国还将进入老龄化快速深化期，高龄老人（80 岁及以上）占比将超过 10%。
老年人口分布呈现出城乡倒置、东高西低的特点，城市的工作机会吸引大量的年轻人，农村老龄化的问题更加严峻。2020 年农村 60 岁及以上人口占比达到了 23.81%，远高于城市和镇区，在一些偏远的乡村里面，十室九空，青壮年劳动力严重失衡，只剩下大量驻村的老年人守护着这片生养他们的土地。同时，农村由于经济、地理等多种因素，政府和家庭能够提供的养老保障也十分有限，农村高龄、失能老人的居家照护面临的困难已经远远超出家庭能承受的范畴。更关键的是中国在经济尚未完全富裕的情况下，老龄化问题却愈演愈劣，经济基础尚不牢靠，社会保障还在完善中，面对庞大的老年群体，国家和家庭都感受到沉甸甸的压力。中国政府已将其作为国家战略，积极应对这一挑战，推动养老事业和产业的发展。
人口老龄化是一种社会挑战，但它也推动了医疗和养老等相关产业的发展，“银发经济” 迅速崛起。围绕老年人生活、健康、情感等相关主题的服务需求，吸引着越来越多的投资，智慧养老正逐步从概念走向现实。刘旭指出，数字化赋能是破解养老难题的重要抓手，通过引入大数据、人工智能、云计算等技术，不仅可以让服务更加高效，也能让老人的生活多一份温度与陪伴，这种以科技手段为支撑、以人性化关怀为核心的服务模式，是值得借鉴参考的。
智慧养老发展的道路并不是一帆风顺的，现实情况是，不少智能设备安装完后却难以得到有效使用，不少平台建起来未能充分发挥服务功能，大量的投入却见效甚微。吕子阳分析指出，这背后既有技术设计不贴合现实需求，也有政府、企业和用户之间的协调机制不健全，导致智慧养老 “叫好不叫座” 的现象发生。很多地方表面上喊出了智慧养老的口号，但在产品供给、服务内容、人才支持等实际操作方面，却有明显短板，比如在某些农村地区，连基本的网络覆盖都难以保证，更别提远程监控或语音交互设备的安装落地。即便如此，深圳、杭州、成都等互联网发达城市正积极布局智慧养老试点，用技术为老年人筑起第二道保护网。记者康琼艳也指出，未来的养老服务不仅要解决 “有没有” 这个问题，还需要解决 “好不好用” 这一真实体验需求。只有当养老不再仅仅意味着看护和照料，而是关心、陪伴和理解时，智慧养老才不再是一个虚假的口号，而是切实为老年人带来温暖的阳光。
1.2 研究发展现状
1.2.1 人物摔倒检测技术
因为身体逐渐衰老、反应力不如从前、平衡力减弱等多种原因，老年人群体在日常生活中容易发生摔倒。当跌倒后如果没有被人及时发现，不仅会对他们身体上造成严重的损害，也可能会影响到他们的心理健康。为此不断有人在研究人物摔倒检测的相关技术，现有的技术大致可分为三类，分别是可穿戴传感器方法、传统视觉方法和深度学习方法。
用传感器和陀螺仪制作穿戴设备是最早期的方法，原理是通过识别老年人姿态变化来判断是否发生跌倒。吉师毅等人设计了一种集成 MPU6050 陀螺仪与 MAX30102 心率血氧传感器的跌倒检测系统，若检测到穿戴设备的对象跌倒，就会通过 SIM800C 模块发送报警短信。此类方法有一定的局限性，老年人可能因穿戴不舒适而放弃穿戴或忘记穿戴等多种原因影响检测结果的稳定。
除了智能穿戴设备检测人物摔倒这一思路，还有一个办法就是使用视觉方法来判断。传统视觉方法多以几何轮廓分析为核心，邓志锋等人提出一种结合人体椭圆轮廓与时间序列特征的 CNN 方法，融合长短轴比、方向角与质心速度用于动作识别，提升了对摔倒与相似行为的区分能力。近年来，基于 YOLO 等深度学习模型的目标检测方法成为研究主流，相比传统视觉的方法，这类模型更加轻便小巧，尤其适用于边缘计算平台，市场应用更广。秦梓竣等人采用 YOLOv5 构建人物摔倒检测模型，能够有效识别仰摔、侧摔等多种摔倒姿态，并在实际部署中表现出良好的响应能力。还有研究者把注意力机制引入 YOLOv8 中，优化了模型在重点区域的识别能力，在多个数据集上获得了优异的识别结果，使得这项技术实用性大幅提升。除了单纯优化 YOLO 模型的方法外，还可以通过引入 MobileNetV2 模型配合使用，YOLO 模型识别高效，MobileNetV2 模型识别准确，彼此优点互补，相互配合，解决了实时性与准确性的平衡问题。
1.2.2 AI 智能体交互技术
除了需要注意老年人的身体监控外，不容忽视的还有他们心理健康方面的问题。智能语音交互系统这一技术在近几年随着 AI 的快速发展受到越来越多的关注，基于语音识别技术、自然语言处理技术以及大语言模型技术的对话式人工智能系统，在智慧养老这一领域正在不断被开发应用。
国内目前已经有了对话式 AI 技术的初步应用案例，只不过并不是关于日常聊天的，更加偏向固定的服务场景。杨雪提出的对话式人工智能在财务共享中心已经实现了自然语言交互、自动报告生成、智能问答等功能，这一研究如果迁移到智慧养老方面，就可以为老年人提供日常咨询需求、用药提醒和心理慰藉。虽然有了一些应用案例，但真的要实现机器对人类语言的准确识别并非易事。刘子寒等人结合复杂声学环境与多说话人识别场景，提出基于支持向量机的语音识别方法。在语者性别不明、多声道干扰条件下依然具备较高的语义识别准确率，这项研究成果为多人共同居住环境下老年家庭智能语音系统的设计提供了重要参考依据。Alotaibi 等人发现，对话式 AI 系统能通过人机对话机制为老年人群体提供情绪陪伴功能、健康提醒功能以及社交激励功能，此类系统在孤独感缓解方面成效显著，同时能提供个性化定制服务。值得关注的是用户信任度指标和接受度指标均维持在较高水平，这一表现说明这一技术有很好的发展需求。
1.2.3 智能家居控制技术
智能家居控制技术可以改善老年人的居家生活质量，帮助他们轻松完成日常家居生活操作，减少对子女的依赖，让他们可以更加有尊严、独立地享受自己的晚年生活，同时还能为他们的安全保驾护航。
智能家具技术发展的初衷，就是为了让居家生活更加方便舒适，郭丽研发的以移动端 APP 为操作核心的智能家居平台，可以使用 APP 遥控家中各类智能设备，简化了传统设备操作步骤，可以让老年人生活更加便捷。
除了让生活更加便捷之外，智能家居技术还可以保障老年人安全。最常见的关于安全方面的智能家居技术，是以单片机为核心，传感器为辅助，提前预设场景条件，当达到条件之后自动触发相应的操作来实现自动化控制。张晟祺等人设计了一套融合跌倒检测与家居控制功能的多用途系统，该系统检测到老年人可能发生跌倒事件时，会联动家居设备发出告警，为老年人提供不错的安全保护。还有一种则更加高级，通过引入视觉识别技术，实时检测家庭中的人员生活习惯和环境参数，能推理出更加合理的空间布局优化方案，这让智能家居控制技术向个性化方向发展迈了一步。
技术在落实的过程中，还需要考虑到经济成本，只有较低的成本才能使技术的落实推广更加迅速，才能改善更多老年人的生活体验。Chen 等人构建了一种基于 ATMEGA2560 与 ESP32 组合芯片的智能控制系统，集成了环境感知、图像采集、语音控制和定位功能，依托 MQTT 协议完成与云端的通信任务，使用较低成本就实现了高度集成的家居物联网应用。这一重大改变展现出广阔的产品推广前景，值得借鉴。
1.3 论文工作安排
第一章是绪论，主要讲解中国人口老龄化不断加重，智能养老的市场也在不断的扩大，除此之外，本文还调研了国内外关于人物摔倒检测、AI 智能体交互和智能家居控制相关的技术发展现状。
第二章是系统分析，主要介绍是本系统总体的功能、架构，和对上述的技术和架构进行的可行性分析，为后续的开发提供理论依据。
第三章是智能看护系统的硬件设计，这章主要介绍本系统核心的三个子系统：人物摔倒检测系统、AI 智能体交互系统和智能家居控制系统的硬件和核心的代码。
第四章是智能看护系统的云服务器设计，主要介绍云服务器开发环境的搭建过程和部署到云服务器上的各类后端服务器、API 的核心代码。
第五章是智能看护系统的 APP 设计，主要介绍 APP 的开发工具，还有各个页面的布局设计以及核心代码的展示。
第六章是系统测试与结果分析，主要是为本文前四章的设想、架构和实现的功能进行验证，判断系统的设计是否合理，功能是否可靠。
第七章是总结与展望，本章是对全文进行总结归纳，自查不足，展望未来。
第 2 章 系统分析
2.1 系统总体功能
本研究采用模块化的设计理念，把系统进行解耦为独立且可复用的功能模块，基于功能独立性原则，将系统拆解为人物摔倒检测系统、AI 智能体交互系统、智能家居控制系统，同时使用 Gitee 云平台进行代码托管，提高系统的灵活性、可维护性和开发效率。
2.2 系统架构设计
本系统采用分层架构，硬件层包含人物摔倒检测设备、AI 智能体交互设备和智能家居控制设备；服务器层包含 Mysql 数据库和所有云服务后端；前端层包含用户登录注册、查看远程监控、查看用户信息和控制智能家居。工程管理方面，使用 Git 工具配合 Gitee 将代码云托管，Maven 和 XML 管理依赖和资源，Docker 部署项目。编程语言则选用 Dart 和 Java 语言编写前端，Python 编写后端，C 语言编写单片机驱动。
2.3 可行性分析
2.3.1 技术可行性
在搭建系统的框架和技术选型时，本系统选择的是物联网和人工智能领域中较为成熟且应用广泛的技术，拥有着活跃的开源社区和长期持久的维护。比如，YOLOV8n-Pose 模型是一种在目标检测和姿势识别领域具有优异性能的轻量化模型；选用的 VAD、ASR、LLM、TTS 模型都是大公司旗下长期开发和维护的模型；STM32 单片机和 ESP8266 配合使用的技术方案也广泛被运用在各个应用中，值得信赖。
2.3.2 经济可行性
从经济可行性角度上看，主要是关注硬件成本的控制以及开发的效率上。选用的核心硬件如 STM32 和 ESP32-S3，均是市场上较为常见而且性价比高的组件，价格适中，购买的渠道广泛。使用的传感器设备也都是标准型号，能够低价批量采购。因为技术层面选用了开源工具和开发框架，开发周期和软件成本大大降低，同时开源方案也十分稳定可靠，具备较强的经济可行性。
2.3.3 社会可行性
本系统设计充分考虑中国老年化社会的现状和智慧养老的需求，目的是解决社会问题，同时将前沿的技术应用到开发智慧养老系统，符合国家对于智慧养老和智能家居领域的政策支持，有广泛的社会需求和发展潜力。本系统依托于社会，为社会服务，并非空中楼阁，符合当前的社会发展趋势，有希望在未来为老年人提供更加安全便捷的生活环境，推动养老行业的发展。
第 3 章 智能看护系统的硬件设计
3.1 人物摔倒检测系统设计
摔倒对上了一定年纪的老年人危害极大，尤其是在生活中，多数情况是老年人摔倒后无法被及时发现，从而导致产生了更严重的身体损伤。本系统通过 WebCamera 语音视频摄像头采集图像数据，在本地计算机上运行 YOLOV8n-Pose 姿态识别模型与自定义运动轨迹分析算法，分析并判断出现在视频图像中的人物是否出现摔倒行为。一旦检测到视频图像中出现了人物摔倒的情况，那么就会触发告警机制，从而最大程度降低意外风险，这一部分功能主要为老年人的安全健康保驾护航。
3.1.1 硬件设备
采集视频图像和音频数据的是 Web Camera 语音视频摄像头，该摄像头的清晰度为 200 万像素，视频格式为 24 位 RGB，信噪比为 48db，动态范围为 72db，功能特点是内置图像压缩，自动白平衡，主管色彩补偿，手动调焦。本系统在实际传输音视频过程中，考虑到传输的低延迟和算法推理的运行速度，最后选择的是 640*480@25FPS 的视频传输帧率。
充当大脑并主管视频流推送到服务器和运行算法推理的硬件设备，采用的是笔记本电脑，显卡为 NVIDIA GeForve GTX 1650，环境配置 CUDA 版本为 11.8，TensorRT 版本为 10.10.0.31，PyTorch 版本为 2.7.0+cu118。显卡在模型运行前后状态的对比情况如下表所示：
参数	运行前	运行后	说明
GPU 温度	46°C	48°C	温升仅 + 2°C，功耗较低
功耗	11W	19W	增加 8W
显存占用	33MiB	156MiB	仅使用 156MiB
GPU 利用率	0%	40%	利用率为中等偏低水平
主要进程	无模型进程	Python.exe	运行 Anaconda 中的模型
下面是一些当前市面上具备轻量 GPU 或神经加速模块的适合迁移部署的常见边缘平台：
设备名称	GPU/NPU/ 加速单元	备注
（未命名）	128CUDA 核心	-
（未命名）	384 核心 + 48Tensor 核心	-
Orange Pi 5 +NPU	6Tops NPU	支持 ONNX/NNIE 推理
RK3588 开发板	-	-
3.1.2 框架设计和实现流程
在搭建人物摔倒检测系统之前，需要训练好所需要的 YOLOV8n-Pose 模型，先从公开的 Roboflow 数据集网站上下载适合训练的人物摔倒图集，还有 Ultralytics 官网的 YOLOV8n-Pose 预训练模型，接着在 AutoDL 云算力平台上租借服务器对模型进行反复的训练，导出识别准确率最高的权重文件。模型训练的流程为：Robofow 上获取人物摔倒数据集→获取 YOLO 官方预训练模型→租借 AutoDL 算力云服务器→导入模型和数据集→反复训练和优化模型→得到最佳训练的权重文件。
本系统使用的模型相关训练数据中，训练完的模型识别准确率主要看 metrics/mAP50-95 (B)，此图是展示模型的识别准确率的折线图，数据越高则代表识别越准确，本系统使用的模型在反复训练后数值稳定在 0.99+，是比较高质量的检测模型。
模型训练之后，使用 OpenCV 技术从本地摄像头捕获视频和音频数据。当摔倒检测功能被激活，人物摔倒检测算法将对视频数据逐帧分析，识别是否有人物摔倒事件。一旦检测到摔倒，系统将向用户邮箱发送带有人物摔倒图像的告警邮件。不管人物摔倒检测功能是否启动，视频流都会被发送到云服务器上的 SRS 流媒体服务器，视频流会被 WebRTC 协议实时传输到 APP 端，APP 端使用 Flutter-RTC 技术接收并向用户展示视频流内容。
3.1.3 核心功能代码
视频流经过模型进行推理之后，会获得人体的各个关键点的信息，通过分析肩部、髋部、膝盖和脚踝的相对位置及角度，从而判断人物有是否摔倒行为，这套算法对不同的摔倒姿势都有一定的适应性。
python
运行
# 判断是否发生摔倒
# 判断条件1:肩膀是否低于脚踝
if min(pt5[1], pt6[1]) >= center_ankle[1]:
    print("满足条件1:肩膀低于脚踝")
    return True
# 判断条件2:肩膀是否高于膝盖
if max(pt5[1], pt6[1]) > min(pt13[1], pt14[1]):
    print("满足条件2:肩膀高于膝盖")
    return True
# 判断条件3:关键点的宽高比
x_coords = keypoints[:, 0]
y_coords = keypoints[:, 1]
xmin, xmax = x_coords.min(), x_coords.max()
ymin, ymax = y_coords.min(), y_coords.max()
aspect_ratio = (xmax - xmin) / (ymax - ymin)
if aspect_ratio > 0.9:  # 宽高比阈值
    print("满足条件3:宽高比过大")
    return True
# 判断条件4:膝盖与髋部的角度
theta2 = np.degrees(np.arctan2(pt14[1] - center_hip[1], pt14[0] - center_hip[0]))
theta1 = np.degrees(np.arctan2(pt13[1] - center_hip[1], pt13[0] - center_hip[0]))
if min(abs(theta1), abs(theta2)) < 30 and max(abs(theta1), abs(theta2)) < 70:
    print("满足条件4:膝盖与髋部的角度异常")
    return True
# 判断条件5:肩膀、髋部、膝盖的夹角
v1 = np.array([center_shoulder[0] - center_hip[0], center_shoulder[1] - center_hip[1]])
v2 = np.array([center_knee[0] - center_hip[0], center_knee[1] - center_hip[1]])
dot_product = np.dot(v1, v2)
magnitude = np.linalg.norm(v1) * np.linalg.norm(v2)
theta3 = np.degrees(np.arccos(dot_product / magnitude))
if theta3 < 70:  # 夹角阈值
    print("满足条件5:肩膀、髋部、膝盖的夹角异常")
    return True
摄像头采集视频流在本地完成模型推理之后，识别结果会直接叠加至原始画面中，视频流将被重新编码然后同步传输，从而在不依赖后端服务器的情况下，完成本地智能处理与实时推流，比传统的云端识别更加迅速，也更加安全。
python
运行
# 获取检测框的坐标
if hasattr(result, "boxes") and result.boxes is not None:
    for box in result.boxes.xyxy.cpu().numpy():
        x1, y1, x2, y2 = map(int, box)
        label = "Fall Detected!" if is_fall else "No Fall"
        color = (0, 0, 255) if is_fall else (0, 255, 0)
        # 在检测框顶部绘制摔倒状态
        cv2.putText(
            img,
            label,
            (x1, y1 - 20),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            color,
            2,
            cv2.LINE_AA,
        )
当在连续检测到摔倒行为后，通过附带摔倒事件图像的邮件通知用户，让用户及时掌握信息，避免发送误判断，下面的代码实现了事件图像的自动保存、打包与发送功能。
python
运行
# 保存当前帧为图片文件
image_path = "fall_detected.jpg"
cv2.imwrite(image_path, img)
# 构建邮件内容
message = MIMEMultipart()
message["From"] = sender_email
message["To"] = receiver_email
message["Subject"] = "摔倒告警"
# 添加邮件正文
body = (
    f"检测到摔倒事件!\n\n"
    f"连续检测次数: {fall_detection_threshold}\n\n"
    f"检测时间: {formatted_time}\n"
    f"请查看附件中的图片以确认摔倒情况。\n\n"
    f"此邮件由系统自动发送,请勿回复。"
)
3.2 AI 智能体交互系统设计
对于老年人群体，除了需要注意他们的身体安全外，还需要关注心理健康。在当前社会生活中，老年群体在社会中所占的比例日益上升，青年人口数量却相对减少，人口年龄结构正在发生变化。伴随着经济的快速发展，很多年轻人都会选择远离家乡，独自前往大城市发展，快节奏的异地生活迫使年轻一代和老年一代的交流沟通以及相互陪伴的时间被逐渐压缩。很多老年人长期无法感受到亲情的关爱，出现了心理上的焦虑、抑郁等心理疾病。许多情况只需满足日常交流就可以解决，而不需要专业的治疗，针对这种情况，AI 智能体交互系统在一定程度上可以填补老年人在情感陪伴方面的空白。随着 AI 从概念走向实际应用，AI 智能体为缓解老年人孤独感、提升心理幸福感提供了新的解决思路与技术路径。
3.2.1 硬件设计
为了实现 AI 智能体交互系统，引入了下面一系列的硬件设备，充当类似于人体的耳朵和嘴两个器官，具备 “听” 和 “说” 两个功能，具体的信息介绍如下：
乐鑫官方出品的 SP32-S3-N16R8，是一款性能强劲的双核 Wi-Fi + 蓝牙 SoC 控制器，非常适用于本系统中的语音识别和数据上传任务，自带的外设资源同时也利于与其他语音与音频模块配合使用。
INMP441 是一款基于 I2S 接口输出的数字麦克风，该模块体积小，安装方便，输出为数字音频数据，省去了传统模拟信号放大与转换的过程，能够直接对接主控设备进行音频采样。
MAX98357 是一款支持 I2S 输入的数字音频放大模块，模块小巧、无需额外 DAC 转换，配合 ESP32 可直接用于音频回放。
扬声器用于音频输出，配合 MAX98357 模块使用，体积虽小，但音量充足，适合家居环境中语音播报使用。
0.91 寸 OLED 屏幕，功耗低，显示清晰，是语音模块运行状态反馈的理想组件。
上面的所有硬件设备通过面包板和跳线进行连接，组成 AI 智能体交互系统的硬件系统。
3.2.2 框架设计和实现流程
交互功能从 ESP32-S3 设备捕获音频开始，音频数据通过 WiFi 传输至云服务器上的 AI 智能体后端。在后端处理数据时，会先调用火山引擎下的 DoubaoASR 语音识别技术将音频信号转换为文本格式。转换得到的文本随后会被输入智谱清言的 ChatGLM 大语言模型，该模型负责进行自然语言处理和理解，从而生成接近于人的自然语音的回复文本。生成的回复文本会通过微软 Azure Cognitive Services 的 EdgeTTS 文字转语音技术转换成音频格式，最后通过 WiFi 回传至 ESP32-S3-N16R8 设备，在设备本地由扬声器进行语音播放。如果设备长时间未读取到有音频数据的输入，那么系统会默认进入休眠状态，等待下一次的唤醒。
3.2.3 核心功能代码
音频的采集和处理是 AI 智能体交互最重要的功能，获取到原始音频数据后会先进行检查，如果采样率不是 16KHz，将会进行重新采样，避免杂音的干扰。如果启用了唤醒词检测那么会对音频数据进行检查，如果启用了音频处理器，那么会对音频流处理。如果唤醒词检测和音频处理器都没有启用，那么在监听的状态下会将音频进行 Opus 编码直接通过协议层发送。
cpp
运行
// 音频采集和处理
void Application::InputAudio() {
    auto codec = Board::GetInstance().GetAudioCodec();
    std::vector<int16_t> data;
    if (!codec->InputData(data)) {  // 获取原始音频数据
        return;
    }
    if (codec->input_sample_rate() != 16000) {  // 采样率转换逻辑(单/双通道)
        // ...
    }
#if CONFIG_USE_WAKE_WORD_DETECT
    if (wake_word_detect_.IsDetectionRunning()) {
        wake_word_detect_.Feed(data);  // 喂给唤醒词检测模块
    }
#endif
#if CONFIG_USE_AUDIO_PROCESSOR
    if (audio_processor_.IsRunning()) {
        audio_processor_.Input(data);  // 音频处理器处理
    }
#else
    if (device_state_ == kDeviceStateListening) {
        background_task_->Schedule([this, data = std::move(data)]() mutable {
            opus_encoder_->Encode(std::move(data), [this](std::vector<uint8_t>&& opus) {
                Schedule([this, opus = std::move(opus)]() {
                    protocol_->SendAudio(opus);  // 发送到服务器
                });
            });
        });
    }
#endif
}
用户输入的音频经过采集上传服务器后，服务器会传回用于回复的音频，此音频会在本地设备上进行播放，播放的流程如下：先检查有没有需要播放的音频数据，当处于监听状态时，长时间没有音频则会先清空音频队列避免干扰语音识别，如果有则取出音频进行异步解码，解码后再次匹配采样率，如果不符合则重新采样，最后进行播放。
cpp
运行
// 音频输出逻辑
void Application::OutputAudio() {
    auto now = std::chrono::steady_clock::now();
    auto codec = Board::GetInstance().GetAudioCodec();
    std::unique_lock<std::mutex> lock(mutex_);
    if (audio_decode_queue_.empty()) {  // 如果空闲且长时间无音频播放,关闭音频输出
        if (device_state_ == kDeviceStateIdle) {
            auto duration = std::chrono::duration_cast<std::chrono::seconds>(now - last_output_time_).count();
            if (duration > max_silence_seconds) {
                codec->EnableOutput(false);
            }
        }
        return;
    }
    if (device_state_ == kDeviceStateListening) {
        audio_decode_queue_.clear();  // 监听状态下丢弃音频
        return;
    }
    // 取出音频数据
    auto pcm = std::move(audio_decode_queue_.front());
    audio_decode_queue_.pop();
    lock.unlock();
    // 如果采样率不一致,进行重采样
    if (opus_decode_sample_rate_ != codec->output_sample_rate()) {
        int target_size = output_resampler_.GetOutputSamples(pcm.size());
        std::vector<int16_t> resampled(target_size);
        output_resampler_.Process(pcm.data(), pcm.size(), resampled.data());
        pcm = std::move(resampled);
    }
    codec->OutputData(pcm);  // 播放音频
    last_output_time_ = now;
}
3.3 智能家居控制系统设计
老年人群体因为身体逐渐衰老，行动能力逐渐减弱，许多日常生活中的操作已经变得不再轻松。本系统通过温湿度传感器、光照传感器采集居住环境数据，结合移动端 App 的远程控制指令，实现对家庭设备的联动管理，如调节灯光、风扇、蜂鸣器等设备的运行状态，还可以根据提前预设的条件开启自动化控制，如在光线昏暗时自动开启照明、室内温度或湿度过高时自动开启风扇等。整体功能贴切生活实际，可以让老年人群体享受科技带来的便捷，为他们打造一个更加舒适的生活环境。
3.3.1 硬件设计
为了实现智能家居控制系统，引入了下面一系列的硬件设备，充当类似于人体的手和皮肤两个器官，具有 “操作” 和 “感受” 的功能，具体的信息介绍如下：
STM32F103C8T6，该系统板支持多种外设接口，便于与传感器和执行器连接，适合作为智能家居的核心控制板。
0.96 寸 OLED 屏幕使用 I2C 接口进行通信，用户在本地查看实时信息，相比传统的 LCD 屏幕，OLED 屏具有低功耗、高对比度的优势。
直插两脚 LED 灯是基本的视觉反馈元件，在系统中主要用于模拟家中的电灯，简单直观，反应迅速。
直流电机是一种将电能转换为机械能的装置，在本系统中可用于模拟家中的风扇，通过控制电压实现启停与方向调节。
ESP8266-01S 支持 Wi-Fi 网络连接，作为网络通信桥梁，负责将传感器采集的数据上传至云端服务器，并接收来自服务器的指令。
DHT11 是一款基础型温湿度传感器，可用于测量环境中的温度与相对湿度，优点在于价格低廉、使用简单，非常适合入门级智能家居系统。
蜂鸣器是一种声音反馈装置，用于系统告警，当有人摔倒时，蜂鸣器可以发出声音提示用户注意。
光敏电阻可用于检测环境光照强度，其阻值随光照强度的变化而变化，单片机可读取其电压变化，判断当前环境明暗程度。
将上面的所有硬件设备通过面包板和跳线进行连接，组成智能家居控制系统的硬件系统。
3.3.2 框架设计和实现流程
智能家居控制主要分为两部分，上传环境数据并在 APP 端展示和在 APP 端下达指令控制智能家居设备。
上传数据的流程是：STM32 采集传感器数据→单片机通过 ESP8266 传输数据到云服务器→云服务器接受数据并存储到数据库→APP 调用 “传感器 API” 获取温湿度数据并展示。
下达指令时的流程是：APP 调用硬件控制 API 向 TCP 服务器发送指令→TCP 服务器转发指令给 ESP8266→ESP8266 通过串口发送指令给 STM32 单片机→单片机根据指令控制设备状态。
3.3.3 核心功能代码
核心控制逻辑运行于主循环中，程序通过串口监听接收到的控制命令，并结合自动控制逻辑完成 LED 灯、电机等外设的状态切换，同时，借助定时中断机制实现每秒周期性任务的调度，完成数据采集、状态刷新与上传。
c
运行
while (1)
{
    if (Received_Flag)
    {
        switch (Received_Char)
        {
            case 'A':
                Buzzer_ON();//蜂鸣器响
                break;
            case 'B':
                Buzzer_OFF();//蜂鸣器灭
                break;
            case 'C':
                LED_Auto_Mode=0;//手动模式
                GPIO_SetBits(GPIOC, GPIO_Pin_13);//LED 灯亮
                break;
            case 'D':
                LED_Auto_Mode=0;//手动模式
                GPIO_ResetBits(GPIOC, GPIO_Pin_13);//LED 灯灭
                break;
            case 'E':
                Motor_Auto_Mode =0;//手动模式
                Motor_SetSpeed(100);//电机转
                break;
            case 'F':
                Motor_Auto_Mode =0;//手动模式
                Motor_SetSpeed(0);// 电机停
                break;
            case 'G':
                LED_Auto_Mode = 1;
                break;
            case 'H':
                Motor_Auto_Mode = 1;
                break;
            default:
                printf("Unknown Command: %c\r\n", Received_Char);
                break;
        }
        Received_Flag = 0;
    }

    if(Flag_1s)
    {
        Flag_1s = 0;
        // 采集温湿度数据
        DHT11_Read_Data(&Temp, &Humi);
        // 采集光照数据
        Light = LightSensor_Get();
        
        if(LED_Auto_Mode)//LED自动模式(根据光敏电阻)
        {
            if(Light < 300)//光照不足
            {
                GPIO_SetBits(GPIOC, GPIO_Pin_13);//LED亮
            }
            else
            {
                GPIO_ResetBits(GPIOC, GPIO_Pin_13);//LED 灭
            }
        }
        
        if(Motor_Auto_Mode)//电机自动模式(根据温湿度)
        {
            if (Temp > 30 || Humi > 70)
            {
                Motor_SetSpeed(100);//自动启动电机
            }
            else
            {
                Motor_SetSpeed(0);//停止电机
            }
        }
        
        // 上传数据到云服务器
        Upload_Data(Temp, Humi, Light);
    }
}
第 4 章 智能看护系统的云服务器设计
4.1 云服务器环境搭建
在本系统的设计与实现过程中，云服务器承担着数据存储、任务调度与设备通信的关键职责。为了确保后端服务的稳定运行和网络连接的流畅响应，系统选用阿里云提供的弹性计算服务（Elastic Compute Service, ECS）作为基础部署平台。
本项目所使用的服务器配置如下：处理器为双核，内存为 2GB，操作系统为 Ubuntu22.04（64 位），镜像 ID 为 ubuntu_22_04_x64_20G_alibase_20250324.vhd，采用 80GB SSD 作为存储介质，公网带宽峰值为 100Mbps，部署区域为阿里云北京节点。该配置在性能与成本之间达成了良好平衡，能够满足后端服务模块的稳定运行，并具备一定的并发处理能力。
为保证服务端通信的正常建立，云服务器需对外开放若干关键端口，TCP 通信模块监听 3456 端口；Flask 框架部署的 API 服务监听 5000 和 6000 端口；HTTP 协议的服务监听 8080、8083 和 8088 端口；RTMP 推流服务监听 1935 端口；WebRTC 通信监听 8000 端口；AI 智能体后端服务监听 6652 端口。所有上述端口已在阿里云的安全组中显式定义，以确保网络可达性与服务稳定性。
4.2 MySQL 数据库设计
4.2.1 数据库介绍
MySQL 是一个关系型数据库管理系统，由瑞典 MySQL AB 公司开发，属于 Oracle 旗下产品，是最流行的关系型数据库管理系统之一。
4.2.2 数据库结构
为了实现智能看护系统中设备状态的远程管理、环境数据的本地存储以及用户账户的注册登录功能，系统设计并部署了两个数据库：物联网系统库（iot_system）和用户管理库（user_management）。物联网系统库包含设备控制（device_control）表和传感器数据（sensor_data）表。用户管理库包含用户信息（user_info）表和验证码（verification_code）表。
设备控制表用于存储风扇、蜂鸣器、LED 灯被用户控制的操作日志，每当用户通过 APP 或系统自动逻辑控制设备时，后端会自动向设备控制表写入记录。device_control 结构如下表所示：
备注	字段名	字段类型	可否为空	关键字	默认值
设备编号	id	int	否	主键、自增	auto_increment
操作时间	timestamp	timestamp	是	否	CURRENT_TIMESTAMP
设备类型	device_type	varchar(20)	否	否	无
设备状态	status	varchar(10)	否	否	无
传感器数据表用于存储从单片机传上来的温湿度数据，每一行温湿度数据都有对应的存储时间，APP 端每次会从此表获取最新的 10 条信息，并通过折线图的形式实时展示。sensor_data 结构如下表所示：
备注	字段名	字段类型	可否为空	关键字	默认值
数据编号	id	int	否	主键、自增	auto_increment
数据时间	timestamp	timestamp	是	否	CURRENT_TIMESTAMP
温度	temperature	float	否	否	无
湿度	humidity	float	否	否	无
用户信息表用于存储注册用户的基本资料，其中用户名和邮箱均设置唯一性约束，防止重复注册。密码字段为哈希存储形式，保障账户安全。user_info 结构如下表所示：
备注	字段名	字段类型	可否为空	关键字	默认值
用户编号	id	int	否	主键、自增	auto_increment
用户名	username	varchar(50)	否	唯一	无
密码哈希值	password_hash	varchar(255)	否	否	无
邮箱地址	email	varchar(100)	否	唯一	无
注册时间	created_at	timestamp	是	否	CURRENT_TIMESTAMP
上次登录时间	last_login	timestamp	是	否	null
验证码记录表用于存储用户注册、找回密码等操作时生成的邮箱验证码，系统在发送验证码的同时，将其内容、发送时间、过期时间等写入 verification_codes 表，并标记是否已使用。verification_codes 结构如下表所示：
备注	字段名	字段类型	可否为空	关键字	默认值
验证码编号	id	int	否	主键、自增	auto_increment
绑定邮箱	email	varchar(255)	否	否	无
验证码内容	code	varchar(10)	否	否	无
创建时间	created_at	datetime	否	否	无
过期时间	expires_at	datetime	否	否	无
是否已使用	is_used	tinyint(1)	否	否	0
4.3 部署 SRS 流媒体服务器
为实现视频流传输与接入服务，本系统在云服务器中使用 Docker 容器部署了 SRS（Simple Realtime Server）流媒体服务器，SRS 是一款高性能、支持 RTMP/HTTP-FLV/WebRTC 等协议的视频服务器，适合嵌入式设备和物联网场景下的实时视频接入。容器 ID 为 b453lacffe9b，启动命令为./objs/srs -c conf/srs.conf，容器名称为 mysrs。容器部署之后，端口的映射关系如下表所示：
端口	协议	用途
1935	TCP	RTMP 推流 / 拉流
1985	TCP	HTTP API 接口
1990	TCP	HTTPS-API 接口
8088	TCP	HTTP 播放页面及管理面板
8000	UDP	WebRTC 通信
4.4 TCP 通信服务器设计
TCP 通信服务器主要充当连接桥梁，在云服务器中，STM32 通过 ESP8266 与 TCP 服务器建立连接后，会发送温湿度数据给服务器。TCP 服务器将数据会存储到数据库中，方便 APP 访问。APP 调用设备控制 API 发送指令时，指令会通过 TCP 服务器转发给单片机。
TCP 服务器同时需要承接 APP 和单片机发送来的信息，那么它需要能够辨别对应数据来源是哪一处。在系统内部设计中，单片机发送来的数据与 APP 发送来的指令的格式是不一样的，因此用数据格式判断指令的来源，如果是上传的信息则存储，如果是指令则转发。
python
运行
# 如果是控制命令
if data in ["A", "B", "C", "D", "E", "F", "G", "H"]:
    print(f"Received command: {data}")
    broadcast_command(data)  # 向所有客户端广播命令
    continue
# 如果是温湿度数据
if "Temp" in data and "Humi" in data:
    parts = data.split(" ")
    temp = float(parts[0].split(":")[1])
    humi = float(parts[1].split(":")[1])
    # 将数据保存到MySQL并自动清理表
    save_sensor_data(temp, humi)
else:
    print("Unknown data format received.")
由于温湿度数据是一直在上传并刷新，MySQL 数据库虽然庞大但最终存储也有限，所以服务器会定期的查询是否存储过多，当数据大于 1000 行的时候就会重新清理数据再存储，避免功能出现异常。
python
运行
# 检查表中行数
query = "INSERT INTO sensor_data (temperature, humidity) VALUES (%s, %s)"
cursor.execute(query, (temp, humi))
cursor.execute("SELECT COUNT(*) FROM sensor_data")
row_count = cursor.fetchone()[0]
# 如果行数超过1000,删除最旧的1000行
if row_count > 1000:
    cursor.execute("DELETE FROM sensor_data ORDER BY id ASC LIMIT 1000")
conn.commit()
4.5 AI 智能体后端设计
在前面的 AI 智能体固件核心代码处已经说明，固件主要用于采集音频数据发到服务器，然后将服务器返回的音频进行播放，AI 智能体后端主要负责建立连接，将发送来的音频进行解析然后进行处理，最后发送回复的音频。
后端代码最主要的是先启动 WebSocket 服务器，等待固件的连接，为之后的音频数据的接受和回传搭建好桥梁。
python
运行
# 启动WebSocket服务器
ws_server = WebSocketServer(config)
ws_task = asyncio.create_task(ws_server.start())
try:
    await wait_for_exit()  # 监听退出信号
except asyncio.CancelledError:
    print("任务被取消,清理资源中...")
finally:
    ws_task.cancel()
    try:
        await ws_task
    except asyncio.CancelledError:
        pass
    print("服务器已关闭,程序退出。")
建立完连接之后，数据依次将经过 VAD 语音检测是否有音频输入，ASR 语音识别音频内容，LLM 大语言模型生成对应回复，TTS 文本转语音模型把文本转为音频，最后再通过服务器发送到 ESP32 这个设备进行播报。
python
运行
# 创建对应模型的实例
self.asr = asr.create_instance(
    self.config["selected_module"]["ASR"] if not "type" in self.config["ASR"][self.config["selected_module"]["ASR"]] else self.config["ASR"][self.config["selected_module"]["ASR"]]["type"],
    self.config["delete_audio"],
    self.config["ASR"][self.config["selected_module"]["ASR"]],
)
self.llm = llm.create_instance(
    self.config["selected_module"]["LLM"] if not "type" in self.config["LLM"][self.config["selected_module"]["LLM"]] else self.config["LLM"][self.config["selected_module"]["LLM"]]["type"],
    self.config["LLM"][self.config["selected_module"]["LLM"]],
)
self.tts = tts.create_instance(
    self.config["selected_module"]["TTS"] if not "type" in self.config["TTS"][self.config["selected_module"]["TTS"]] else self.config["TTS"][self.config["selected_module"]["TTS"]]["type"],
    self.config["TTS"][self.config["selected_module"]["TTS"]],
    self.config["delete_audio"],
)
4.6 用户管理 User-API 设计
用户管理 API 和用户信息相关，当用户进行注册、登录、重置密码、修改用户名与邮箱时都会调用此 API 进行逻辑判断和数据库操作。参考市场上绝大部分 APP 的操作，本系统通过合理的设计让用户有一个良好的体验。
无论在注册情况还是重置密码的时候，都会使用到邮箱验证码，在发送前需要判断应用场景。同时，在提供服务时，邮箱验证码需要注意发送的间隙和验证码持续的时间，才能有效保证系统的功能正常和用户账户的安全。
python
运行
# 如果是注册场景,检查邮箱是否已注册
if purpose == 'register':
    check_email_query = "SELECT * FROM user_info WHERE email = %s"
    cursor.execute(check_email_query, (email,))
    existing_user_by_email = cursor.fetchone()
    if existing_user_by_email:
        return jsonify({'error': '该邮箱已注册,请直接登录或使用其他邮箱'}), 400
    # 检查是否在1分钟内已发送验证码
    query = """
    SELECT * FROM verification_codes
    WHERE email = %s AND expires_at > NOW() AND TIMESTAMPDIFF(SECOND, created_at, NOW()) < 60
    """
    cursor.execute(query, (email,))
    existing_code = cursor.fetchone()
    if existing_code:
        return jsonify({'error': '请稍后再试,每分钟只能发送一次验证码'}), 429
# 生成验证码
code = generate_verification_code()
created_at = datetime.now()
expires_at = created_at + timedelta(minutes=5)
# 插入验证码记录
insert_query = """
INSERT INTO verification_codes (email, code, created_at, expires_at, is_used)
VALUES (%s, %s, %s, %s, 0)
"""
cursor.execute(insert_query, (email, code, created_at, expires_at))
conn.commit()
# 发送验证码邮件
send_verification_email(email, code)
return jsonify({'message': '验证码已发送,请查收'}), 201
用户进行注册账号操作时，服务端会校验当前输入的用户名与邮箱在数据库中是否存在，若不存在则提醒用户更改。之后则会判断提交的验证码是否正确，是否还在有效期。通过所有的判断之后，将对密码字段进行加密处理，然后用户信息才会写入数据库。
python
运行
# 检查用户名是否已注册
check_username_query = "SELECT * FROM user_info WHERE username = %s"
cursor.execute(check_username_query, (username,))
existing_user_by_username = cursor.fetchone()
if existing_user_by_username:
    return jsonify({'error': '该用户名已注册,请使用其他用户名'}), 400
# 验证验证码
query = """
SELECT * FROM verification_codes
WHERE email = %s AND code = %s AND expires_at > NOW() AND is_used = FALSE
"""
cursor.execute(query, (email, verification_code))
code_record = cursor.fetchone()
if not code_record:
    return jsonify({'error': '验证码无效或已过期'}), 400
# 标记验证码为已使用
update_query = "UPDATE verification_codes SET is_used = TRUE WHERE id = %s"
cursor.execute(update_query, (code_record['id'],))
# 加密密码
hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
# 插入用户信息到数据库
insert_query = "INSERT INTO user_info (username, password_hash, email) VALUES (%s, %s, %s)"
cursor.execute(insert_query, (username, hashed_password.decode('utf-8'), email))
conn.commit()
return jsonify({'message': '注册成功,请登录'}), 201
用户登录时，系统会先判断邮箱是否在云端数据库存在，若存在，会将密码使用 bcrypt 加密，然后比对密码的哈希值。在比对成功之后，会更新登录时间，并返回用户的基本信息，在本地持久的保存。主要是为了避免 APP 放置后台后丢失信息，用户需要反复繁琐登录的情况出现。
python
运行
# 登录账号
query = "SELECT * FROM user_info WHERE email = %s"
cursor.execute(query, (email,))
user = cursor.fetchone()
# 账号密码正确
if user and bcrypt.checkpw(password.encode('utf-8'), user['password_hash'].encode('utf-8')):
    # 更新最后登录时间
    update_query = "UPDATE user_info SET last_login = %s WHERE id = %s"
    cursor.execute(update_query, (datetime.now(), user['id']))
    conn.commit()
    # 重新查询用户信息,确保返回最新的last_login
    cursor.execute(query, (email,))
    updated_user = cursor.fetchone()
    cursor.close()
    conn.close()
    return jsonify({
        'message': '登录成功',
        'user': {
            'id': updated_user['id'],
            'username': updated_user['username'],
            'email': updated_user['email'],
            'last_login': updated_user['last_login'].strftime('%Y-%m-%d %H:%M:%S') if updated_user['last_login'] else None
        }
    }), 200
else:
    cursor.close()
    conn.close()
    return jsonify({'error': '邮箱或密码错误'}), 401
4.7 硬件控制 Device-API 设计
硬件控制 Device-API 接口主要负责设备控制相关，APP 调用此 API 时会发送的控制命令到 TCP 服务器，也可以返回数据库查询到最新的温湿度数据。
APP 客户端可通过 POST 方式提交控制指令，系统接收到请求后，会将该指令发送到 TCP 服务器，TCP 服务器在和单片机建立联系之后可以直接转发这一命令，从而达到远程控制的效果。
python
运行
# HTTP API:发送控制命令到 TCP服务器
@app.route('/api/control', methods=['POST'])
def control_device():
    data = request.json
    command = data.get('command')
    if not command or command not in ["A", "B", "C", "D", "E", "F", "G", "H"]:
        return jsonify({"error": "无效的控制命令"}), 400
    # 发送控制命令到TCP服务器
    send_command_to_tcp_server(command)
    return jsonify({"message": f"命令{command}已发送到 TCP 服务器"}), 200
采用按 ID 降序查询以获取最新记录，从服务器数据库中提取最新的一条传感器数据记录，并返回给客户端，同时为确保查询操作的线程安全与资源回收，系统每次请求都会建立一次独立数据库连接，并在操作结束后显式关闭连接与游标，从而避免资源泄漏和数据不一致问题。
python
运行
# HTTP API:获取最新的传感器数据(基于ID最大值)
@app.route('/api/sensor_data', methods=['GET'])
def get_sensor_data():
    # 动态建立新的数据库连接,保证每次请求数据都是最新的
    db = get_db_connection()
    cursor = db.cursor(pymysql.cursors.DictCursor)
    try:
        # 查询最新的传感器数据(ID最大的一条)
        query = "SELECT * FROM sensor_data ORDER BY id DESC LIMIT 1"
        cursor.execute(query)
        result = cursor.fetchone()  # 获取最新的数据
        if not result:
            return jsonify({"error": "暂无传感器数据"}), 404
        return jsonify(result), 200
    finally:
        cursor.close()
        db.close()  # 确保关闭数据库连接
第 5 章 智能看护系统的 APP 设计
5.1 APP 开发工具
本系统 APP 主要使用基于 Dart 的 Flutter 框架开发，编译工具为 Visual Studio Code 和 Android Studio。首先下载 Android Studio 软件，接着在 Visual Studio Code 里面下载 Flutter 的框架，当配置好开发环境之后，可以使用命令行指令 flutter doctor 检测目前的开发环境。当运行 flutter doctor 后显示所有配置项均正常时，证明开发环境已经配置好了。当环境配置好之后，使用 flutter run 可以运行构建 APP 到手机，这之后就可以进行实机开发。
5.2 用户登录注册页面设计
5.2.1 页面设计
用户登录注册页面设计了注册、登录、忘记密码三个独立功能页面，仿造现阶段绝大部分主流软件所使用的布局设计和功能，通俗易懂，简单易上手。
点击看护助手 APP，默认进入的页面是登录页面，此页面实现用户登录，同时也可以跳转注册和忘记密码的页面。当用户第一次登录没有账户时，可以点击 “注册” 进入注册页面进行账号注册；若用户注册过但忘记密码，可以点击 “忘记密码” 进入重置密码的页面。
5.2.2 核心功能代码
登录页面主要负责实现用户登录以及其他页面的跳转。当用户输入账号和密码并点击 “登录” 按钮时，会调用后端负责登录的 API 接口。接口会判断用户的账号信息是否存在，密码是否正确，并返回相应的响应，页面则根据对应的信息进行跳转或提示。
dart
Future<void> _login() async {
  final response = await http.post(
    Uri.parse('http://39.105.140.201:5000/login'),
    headers: {"Content-Type": "application/json"},
    body: json.encode({
      'username': _usernameController.text,
      'password': _passwordController.text,
    }),
  );
  if (response.statusCode == 200) {
    final data = json.decode(response.body);
    // 保存用户信息到本地
    await _saveUserInfo(data['user']);
    // 跳转到首页
    Navigator.pushReplacementNamed(context, '/home');
  } else {
    final error = json.decode(response.body)['error'];
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(content: Text('登录失败: $error')),
    );
  }
}
在注册页面核心的是关于验证码的判断。输入用户名、密码、邮箱且点击 “发送验证码” 按钮之后，服务器会先检查数据库内是否有相同账号或相同邮箱的账户，如果有就会阻止并提示用户更新信息；如果没有，就会通过邮箱发送验证码，验证码五分钟内有效且只能使用一次。
dart
// 调用发送验证码的接口
Future<void> _sendVerificationCode() async {
  final response = await http.post(
    Uri.parse('http://39.105.140.201:5000/send_verification_code'),
    headers: {'Content-Type': 'application/json'},
    body: json.encode({
      'email': _emailController.text,
      'purpose': 'register', // 注册场景
    }),
  );
  if (response.statusCode == 201) {
    ScaffoldMessenger.of(context).showSnackBar(
      const SnackBar(content: Text('验证码已发送,请查收')),
    );
    // 开始倒计时
    _startCountdown();
  } else {
    final error = json.decode(response.body)['error'];
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(content: Text('发送失败: $error')),
    );
  }
}

// 判断验证码是否正确并注册
Future<void> _register() async {
  if (!_formKey.currentState!.validate()) {
    // 如果表单验证失败,直接返回
    return;
  }
  final response = await http.post(
    Uri.parse('http://39.105.140.201:5000/register'),
    headers: {'Content-Type': 'application/json'},
    body: json.encode({
      'username': _usernameController.text,
      'password': _passwordController.text,
      'email': _emailController.text,
      'verification_code': _verificationCodeController.text,
    }),
  );
  if (response.statusCode == 201) {
    ScaffoldMessenger.of(context).showSnackBar(
      const SnackBar(content: Text('注册成功,请登录')),
    );
    Navigator.pop(context); // 返回登录页面
  } else {
    final error = json.decode(response.body)['error'];
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(content: Text('注册失败: $error')),
    );
  }
}
忘记密码的页面中，核心也是验证码的判断。只有邮箱、验证码正确，才能正常的更改密码，完成找回密码的操作。但不同的地方在于，验证完验证码并输入新密码之后，后端调用的是更改密码的接口，而非注册的接口。
dart
// 重置密码函数
Future<void> _resetPassword() async {
  if (!_formKey.currentState!.validate()) {
    return;
  }
  final response = await http.post(
    Uri.parse('http://39.105.140.201:5000/reset-password'),
    headers: {'Content-Type': 'application/json'},
    body: json.encode({
      'email': _emailController.text,
      'verification_code': _verificationCodeController.text,
      'new_password': _newPasswordController.text,
    }),
  );
  if (response.statusCode == 200) {
    ScaffoldMessenger.of(context).showSnackBar(
      const SnackBar(content: Text('密码重置成功,请登录')),
    );
    Navigator.pop(context); // 返回登录页面
  } else {
    final error = json.decode(response.body)['error'];
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(content: Text('重置失败: $error')),
    );
  }
}
5.3 远程监控页面设计
5.3.1 页面设计
当用户成功登录后，默认进入的页面就是 “监控” 页面。监控页面由视频订阅地址栏、“订阅” 按钮、媒体播放器、“播放” 按钮、“暂停” 按钮和 “开启检测” 按钮组成。在输入对应的视频地址之后，先点击 “订阅”，再点击 “播放” 按钮，APP 会从服务器的 SRS 流媒体服务器上拉取视频的资源；当点击 “开启检测” 之后，远程设备会开启人物摔倒检测功能，推理结果将绘制在视频上，发送至媒体播放器。
5.3.2 核心功能代码
在远程监控页面，输入订阅的地址之后，点击 “播放” 按钮，APP 会向服务器发送请求并拉取视频流，使用 WebRTC 协议建立长久的链接。
dart
Future<void> startWebRTC({required String streamUrl}) async {
  _streamUrl = streamUrl; // 设置为传入的流地址
  _serverUrl = "https://39.105.140.201:1990/rtc/v1/play/";
  if (_peerConnection == null) {
    _peerConnection = await createPeerConnection({
      'iceServers': [
        {'urls': 'stun:stun.l.google.com:19302'},
      ]
    });
    _peerConnection?.onTrack = (event) {
      if (event.track.kind == 'video') {
        _remoteRenderer.srcObject = event.streams[0];
      }
    };
  }
  RTCSessionDescription offer = await _peerConnection!.createOffer();
  await _peerConnection!.setLocalDescription(offer);
  String? remoteSdp = await _fetchRemoteSdp(offer.sdp);
  if (remoteSdp != null) {
    await _peerConnection!.setRemoteDescription(
      RTCSessionDescription(remoteSdp, 'answer'),
    );
  }
}

// 从服务器获取远程SDP
Future<String?> _fetchRemoteSdp(String localSdp) async {
  final response = await http.post(
    Uri.parse('$_serverUrl${Uri.encodeComponent(_streamUrl)}'),
    headers: {'Content-Type': 'application/json'},
    body: json.encode({
      'sdp': localSdp,
      'type': 'offer',
    }