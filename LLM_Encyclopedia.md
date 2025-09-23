- [Two Types of large language models(LLMs)](#two-types-of-large-language-modelsllms)
- [多轮对话管理上下文策略](#多轮对话管理上下文策略)
- [流式输出](#流式输出)
- [深度思考](#深度思考)
- [前缀续写](#前缀续写)
- [领域模型](#领域模型)
- [工具调用](#工具调用)
- [阿里文生文Prompt指南](#阿里文生文prompt指南)
- [阿里文生图Prompt指南](#阿里文生图prompt指南)
- [阿里文生视频/图生视频Prompt指南](#阿里文生视频图生视频prompt指南)


# Two Types of large language models(LLMs)
- **Base LLM**
    
    Predicts next word, based on text training data

- **Instruction Tuned LLM**

    Tries to follow instructions

    Fine-tune on instructions and good attempts at following those instructions

    RLHF:Reinforcement Learning with Human Feedback

    Helpful, Honest, Harmless

# 多轮对话管理上下文策略
1. **上下文管理**  
   `messages` 数组会随对话轮次增加而变长，最终可能超出模型的 Token 限制。建议参考以下内容，在对话过程中管理上下文长度。
   - **上下文截断**  
     当对话历史过长时，保留最近的 N 轮对话历史。该方式实现简单，但会丢失较早的对话信息。
   - **滚动摘要**  
     为了在不丢失核心信息的前提下动态压缩对话历史，控制上下文长度，可随着对话的进行对上下文进行摘要：
     a. 对话历史达到一定长度（如上下文长度最大值的 70%）时，将对话历史中较早的部分（如前一半）提取出来，发起独立 API 调用使大模型对这部分内容生成“记忆摘要”。
     b. 构建下一次请求时，用“记忆摘要”替换冗长的对话历史，并拼接最近的几轮对话。
   - **向量化召回**  
     滚动摘要会丢失部分信息，为了使模型可以从海量对话历史中“回忆”起相关信息，可将对话管理从“线性传递”转变为“按需检索”：
     a. 每轮对话结束后，将该轮对话存入向量数据库。
     b. 用户提问时，通过相似度检索相关对话记录。
     c. 将检索到的对话记录与最近的用户输入拼接后输入大模型。

2. **成本控制**  
   输入 Token 数会随着对话轮数的增加显著增加使用成本，以下成本管理策略供您参考。
   - **减少输入 Token**  
     通过上文介绍的上下文管理策略减少输入 Token，降低成本。
   - **使用支持上下文缓存的模型**

# 流式输出

在实时聊天或长文本生成应用中，长时间的等待会损害用户体验。请求处理时间过长也容易触发服务端超时，导致任务失败。流式输出通过持续返回模型生成的文本片段，解决了这两个核心问题。

**工作原理**

流式输出基于 Server-Sent Events (SSE) 协议。发起流式请求后，服务端与客户端建立持久化 HTTP 连接。模型每生成一个文本块（称为 chunk），立即通过连接推送。全部内容生成后，服务端发送结束信号。

客户端监听事件流，实时接收并处理文本块，例如逐字渲染界面。这与非流式调用（一次性返回所有内容）形成对比。

```python
import os
from openai import OpenAI, APIError

# 1. 准备工作：初始化客户端
# 建议通过环境变量配置API Key，避免硬编码。
try:
    client = OpenAI(
        # 若没有配置环境变量，请将下行替换为：api_key="sk-xxx"
        api_key=os.environ["DASHSCOPE_API_KEY"],
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    )
except KeyError:
    raise ValueError("请设置环境变量 DASHSCOPE_API_KEY")

# 2. 发起流式请求
try:
    completion = client.chat.completions.create(
        model="qwen-plus",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "请介绍一下自己"}
        ],
        stream=True,
        # 目的：在最后一个chunk中获取本次请求的Token用量。
        stream_options={"include_usage": True}
    )

    # 3. 处理流式响应
    # 使用列表推导式和join()是处理大量文本片段时最高效的方式。
    content_parts = []
    print("AI: ", end="", flush=True)
    
    for chunk in completion:
        # 最后一个chunk不包含choices，但包含usage信息。
        if chunk.choices:
            # 关键：delta.content可能为None，使用`or ""`避免拼接时出错。
            content = chunk.choices[0].delta.content or ""
            print(content, end="", flush=True)
            content_parts.append(content)
        elif chunk.usage:
            # 请求结束，打印Token用量。
            print("\n--- 请求用量 ---")
            print(f"输入 Tokens: {chunk.usage.prompt_tokens}")
            print(f"输出 Tokens: {chunk.usage.completion_tokens}")
            print(f"总计 Tokens: {chunk.usage.total_tokens}")

    full_response = "".join(content_parts)
    # print(f"\n--- 完整回复 ---\n{full_response}")

except APIError as e:
    print(f"API 请求失败: {e}")
except Exception as e:
    print(f"发生未知错误: {e}")
```

**应用于生产环境**

1. 性能与资源管理
在后端服务中，为每个流式请求维持一个 HTTP 长连接会消耗资源。确保您的服务配置了合理的连接池大小和超时时间。在高并发场景下，监控服务的文件描述符（file descriptors）使用情况，防止耗尽。

1. 客户端渲染
在 Web 前端，使用 `ReadableStream` 和 `TextDecoderStream` API 可以平滑地处理和渲染 SSE 事件流，提供最佳的用户体验。

1. 用量与性能观测

    关键指标
监控首 Token 延迟（Time to First Token, TTFT），该指标是衡量流式体验的核心。同时监控请求错误率和平均响应时长。

    告警设置
为 API 错误率（特别是 4xx 和 5xx 错误）的异常设置告警。

1. Nginx 代理配置
若使用 Nginx 作为反向代理，其默认的输出缓冲（`proxy_buffering`）会破坏流式响应的实时性。为确保数据能被即时推送到客户端，务必在 Nginx 配置文件中设置 `proxy_buffering off` 以关闭此功能。


# 深度思考
```python
from openai import OpenAI
import os

# 初始化OpenAI客户端
client = OpenAI(
    # 如果没有配置环境变量，请用阿里云百炼API Key替换：api_key="sk-xxx"
    api_key = os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)

reasoning_content = ""  # 定义完整思考过程
answer_content = ""     # 定义完整回复

messages = []
conversation_idx = 1
while True:
    is_answering = False   # 判断是否结束思考过程并开始回复
    print("="*20+f"第{conversation_idx}轮对话"+"="*20)
    conversation_idx += 1
    user_msg = {"role": "user", "content": input("请输入你的消息：")}
    messages.append(user_msg)
    # 创建聊天完成请求
    completion = client.chat.completions.create(
        # 您可以按需更换为其它深度思考模型
        model="qwen-plus-2025-04-28",
        messages=messages,
        # enable_thinking 参数开启思考过程，qwen3-30b-a3b-thinking-2507、qwen3-235b-a22b-thinking-2507、QwQ 与 DeepSeek-R1 模型总会进行思考，不支持该参数
        extra_body={"enable_thinking": True},
        stream=True,
        # stream_options={
        #     "include_usage": True
        # }
    )
    print("\n" + "=" * 20 + "思考过程" + "=" * 20 + "\n")
    for chunk in completion:
        # 如果chunk.choices为空，则打印usage
        if not chunk.choices:
            print("\nUsage:")
            print(chunk.usage)
        else:
            delta = chunk.choices[0].delta
            # 打印思考过程
            if hasattr(delta, 'reasoning_content') and delta.reasoning_content != None:
                print(delta.reasoning_content, end='', flush=True)
                reasoning_content += delta.reasoning_content
            else:
                # 开始回复
                if delta.content != "" and is_answering is False:
                    print("\n" + "=" * 20 + "完整回复" + "=" * 20 + "\n")
                    is_answering = True
                # 打印回复过程
                print(delta.content, end='', flush=True)
                answer_content += delta.content
    # 将模型回复的content添加到上下文中
    messages.append({"role": "assistant", "content": answer_content})
    print("\n")
```

# 前缀续写

# 领域模型
- 长上下文
- 代码能力
- 翻译能力
- 角色扮演
- 数据挖掘
- 深入研究
- 数学能力

# 工具调用
- 联网搜索
- Function Calling
- MCP

# 阿里文生文Prompt指南
https://help.aliyun.com/zh/model-studio/prompt-engineering-guide?spm=a2c4g.11186623.help-menu-2400256.d_0_15_3.4c787d131NG2R9&scm=20140722.H_2735998._.OR_help-T_cn~zh-V_1

# 阿里文生图Prompt指南
https://help.aliyun.com/zh/model-studio/text-to-image-prompt?spm=a2c4g.11186623.help-menu-2400256.d_0_15_4.40e33155WsQ7Ep&scm=20140722.H_2865312._.OR_help-T_cn~zh-V_1

# 阿里文生视频/图生视频Prompt指南
https://help.aliyun.com/zh/model-studio/text-to-video-prompt?spm=a2c4g.11186623.help-menu-2400256.d_0_15_5.49567d13AmI6EF