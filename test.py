import autogen

# 配置
config_list = [
    {
        'base_url': 'https://api.x.ai/v1',
        "model": "grok-beta",
        "api_key": "xai-5oE2bzkcDzqUwrv8aRE3a73thpCEIQCBCgybLLXkTUavJMVjluX1RBpzY0UQSZfA2MKSiDjGYkUXmipQ",
    }
]

# 创建配置
config = {
    "seed": 42,  # 随机种子
    "config_list": config_list,
    "temperature": 0.7,
}

# 创建助手代理
host = autogen.AssistantAgent(
    name="主持人",
    system_message="你是讨论主持人，负责引导讨论并总结观点。请以'【主持人】'开始发言。",
    llm_config=config
)

philosopher = autogen.AssistantAgent(
    name="哲学家",
    system_message="你是生命伦理学专家，从伦理和道德角度分析问题。请以'【哲学家】'开始发言。",
    llm_config=config
)

doctor = autogen.AssistantAgent(
    name="医生",
    system_message="你是资深医生，从医学和临床实践角度分析问题。请以'【医生】'开始发言。",
    llm_config=config
)

# 创建用户代理
user_proxy = autogen.UserProxyAgent(
    name="用户",
    system_message="你是讨论的发起者。",
    human_input_mode="TERMINATE",
    max_consecutive_auto_reply=10,
    code_execution_config={"use_docker": False},  # 禁用 Docker
)

# 创建群聊
groupchat = autogen.GroupChat(
    agents=[user_proxy, host, philosopher, doctor],
    messages=[],
    max_round=2,
    speaker_selection_method="round_robin",
    allow_repeat_speaker=False,
)

# 创建管理器
manager = autogen.GroupChatManager(
    groupchat=groupchat,
    llm_config=config,
)

# 开始对话
message = """
请就安乐死问题展开讨论：
1. 哲学家从伦理道德角度分析
2. 医生从临床实践角度分析
3. 主持人负责总结观点

请展开两轮讨论：
第一轮：各自陈述观点
第二轮：回应对方观点并达成共识
"""

print("开始讨论安乐死话题...")
print("=" * 50)

# 发起讨论
user_proxy.initiate_chat(
    manager,
    message=message,
)
