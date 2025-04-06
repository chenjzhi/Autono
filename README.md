<div align="center">
    <p>
        <img src="https://github.com/vortezwohl/Autono/releases/download/autono_icon/autono_logo.png" alt="Autono" height="125">
    </p>
    <p style="font-weight: 800; font-size: 24px; color:rgb(143, 88, 195)">
        A <a href="https://arxiv.org/abs/2210.03629">ReAct</a> Based Highly Robust Autonomous Agent Framework.
    </p>
    <p style="font-weight: 600; font-size: 16px">
        <a href="https://github.com/modelcontextprotocol">MCP</a> is currently supported. <a href="#integration-with-mcp">How to use McpAgent</a>.
    </p>
</div>

<h4 align="center">
    <p>
        <b>English</b> |
        <a href="https://github.com/vortezwohl/Autono/blob/main/i18n/README_zh-hant.md">繁體中文</a> |
        <a href="https://github.com/vortezwohl/Autono/blob/main/i18n/README_zh-hans.md">简体中文</a> |
        <a href="https://github.com/vortezwohl/Autono/blob/main/i18n/README_ja-jp.md">日本語</a>
    </p>
</h4>

<h5></br></h5>

## Abstract

This paper (project) proposes a highly robust autonomous agent framework based on the ReAct paradigm, designed to solve complex tasks through adaptive decision making and multi-agent collaboration. Unlike traditional frameworks that rely on fixed workflows generated by LLM-based planners, this framework dynamically generates next actions during agent execution based on prior trajectories, thereby enhancing its robustness. To address potential termination issues caused by adaptive execution paths, I propose a timely abandonment strategy incorporating a probabilistic penalty mechanism. For multi-agent collaboration, I introduce a memory transfer mechanism that enables shared and dynamically updated memory among agents. The framework's innovative timely abandonment strategy dynamically adjusts the probability of task abandonment via probabilistic penalties, allowing developers to balance conservative and exploratory tendencies in agent execution strategies by tuning hyperparameters. This significantly improves adaptability and task execution efficiency in complex environments. Additionally, agents can be extended through external tool integration, supported by modular design and MCP protocol compatibility, which enables flexible action space expansion. Through explicit division of labor, the multi-agent collaboration mechanism enables agents to focus on specific task components, thereby significantly improving execution efficiency and quality.

## Experiment

The experimental results demonstrate that the `autono` framework significantly outperforms `autogen` and `langchain` in handling tasks of varying complexity, especially in multi-step tasks with possible failures.

| Framework   | Version | Model                                      | one-step-task | multi-step-task | multi-step-task-with-possible-failure |
| ------ | --- |----------------------------------------- | ------------- | --------------- | ---------------------------------------- |
| `autono` | `1.0.0` |gpt-4o-mini<br>qwen-plus<br>deepseek-v3 | 96.7%</br>100%</br>100% | 100%</br>96.7%</br>100% | 76.7%</br>93.3%</br>93.3% |
| `autogen` | `0.4.9.2` |gpt-4o-mini<br>qwen-plus<br>deepseek-v3 |90%</br>90%</br>N/A | 53.3%</br>0%</br>N/A | 3.3%</br>3.3%</br>N/A |
| `langchain` | `0.3.21` |gpt-4o-mini<br>qwen-plus<br>deepseek-v3 | 73.3%</br>73.3%</br>76.7% | 13.3%</br>13.3%</br>13.3% | 10%</br>13.3%</br>6.7% |

- `one-step-task`: Tasks that can be completed with a single tool call.
- `multi-step-task`: Tasks that require multiple tool calls to complete, with no possibility of tool failure.
- `multi-step-task-with-possible-failure`: Tasks that require multiple tool calls to complete, where tools may fail, requiring the agent to retry and correct errors.

> The deepseek-v3 model is not supported by `autogen-agentchat==0.4.9.2`.

> You can reproduce my experiments [here](https://github.com/vortezwohl/experiment-03-22-2025).

## Citation

If you are incorporating the `autono` framework into your research, please remember to properly **cite** it to acknowledge its contribution to your work.

Если вы интегрируете фреймворк `autono` в своё исследование, пожалуйста, не забудьте правильно сослаться на него, указывая его вклад в вашу работу.

もしあなたが研究に `autono` フレームワークを組み入れているなら、その貢献を認めるために適切に引用することを忘れないでください.

如果您正在將 `autono` 框架整合到您的研究中，請務必正確引用它，以聲明它對您工作的貢獻.

```latex
@software{Wu_Autono_2025,
author = {Wu, Zihao},
license = {GPL-3.0},
month = apr,
title = {{Autono}},
url = {https://github.com/vortezwohl/Autono},
version = {1.0.0},
year = {2025}
}
```

## Installation

- From [PYPI](https://pypi.org/project/autono/)

    ```shell
    pip install -U autono
    ```

- From [Github](https://github.com/vortezwohl/Autono/releases)

    Get access to unreleased features.

    ```shell
    pip install git+https://github.com/vortezwohl/Autono.git
    ```

## Quick Start

To start building your own agent, follow the steps listed.

1. set environmental variable `OPENAI_API_KEY`

    ```
    # .env
    OPENAI_API_KEY=sk-...
    ```

2. import required dependencies

    - `Agent` lets you instantiate an agent.

    - `Personality` is an enumeration class used for customizing personalities of agents.

        - `Personality.PRUDENT` makes the agent's behavior more cautious.

        - `Personality.INQUISITIVE` encourages the agent to be more proactive in trying and exploring.

    - `get_openai_model` gives you a `BaseChatModel` as thought engine.

    - `@ability(brain: BaseChatModel, cache: bool = True, cache_dir: str = '')` is a decorator which lets you declare a function as an `Ability`.

    - `@agentic(agent: Agent)` is a decorator which lets you declare a function as an `AgenticAbility`.

    ```python
    from autono import (
        Agent,
        Personality,
        get_openai_model,
        ability,
        agentic
    )
    ```

3. declare functions as basic abilities

    ```python
    @ability
    def calculator(expr: str) -> float:
        # this function only accepts a single math expression
        return simplify(expr)

    @ability
    def write_file(filename: str, content: str) -> str:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
        return f'{content} written to {filename}.'
    ```

4. instantiate an agent

    You can grant abilities to agents while instantiating them.

    ```python
    model = get_openai_model()
    agent = Agent(abilities=[calculator, write_file], brain=model, name='Autono', personality=Personality.INQUISITIVE)
    ```

    - You can also grant more abilities to agents later:

        ```python
        agent.grant_ability(calculator)
        ```

        or

        ```python
        agent.grant_abilities([calculator])
        ```

    - To deprive abilities:

        ```python
        agent.deprive_ability(calculator)
        ```

        or

        ```python
        agent.deprive_abilities([calculator])
        ```
    
    You can change an agent's personality using method `change_personality(personality: Personality)`

    ```python
    agent.change_personality(Personality.PRUDENT)
    ```

5. assign a request to your agent

    ```python
    agent.assign("Here is a sphere with radius of 9.5 cm and pi here is 3.14159, find the area and volume respectively then write the results into a file called 'result.txt'.")
    ```

6. leave the rest to your agent

    ```python
    response = agent.just_do_it()
    print(response)
    ```

> `autono` also supports multi-agent collaboration scenario, declare a function as agent calling ability with `@agentic(agent: Agent)`, then grant it to an agent. [See example](https://github.com/vortezwohl/Autono/blob/autono/demo/multi_agent.py).

## Integration with [MCP](https://github.com/modelcontextprotocol)

I provide `McpAgent` to support tool calls based on the MCP protocol. Below is a brief guide to integrating `McpAgent` with `mcp.stdio_client`:

1. import required dependencies

    - `McpAgent` allows you to instantiate an agent capable of accessing MCP tools.

    - `StdioMcpConfig` is an alias for `mcp.client.stdio.StdioServerParameters` and serves as the MCP server connection configuration.

    - `@mcp_session(mcp_config: StdioMcpConfig)` allows you to declare a function as an MCP session.

    - `sync_call` allows you to synchronizedly call a coroutine function.

    ```python
    from autono import (
        McpAgent,
        get_openai_model,
        StdioMcpConfig,
        mcp_session,
        sync_call
    )
    ```

2. create an MCP session

    - To connect with a stdio based MCP server, use `StdioMcpConfig`.

        ```python
        mcp_config = StdioMcpConfig(
            command='python',
            args=['./my_stdio_mcp_server.py'],
            env=dict(),
            cwd='./mcp_servers'
        )
        ```

        > A function decorated with `@mcp_session` will receive an MCP session instance as its first parameter. A function can be decorated with multiple `@mcp_session` decorators to access sessions for different MCP servers.

        ```python
        @sync_call
        @mcp_session(mcp_config)
        async def run(session, request: str) -> str:
            ...
        ```

    - To connect via HTTP with a SSE based MCP server, just provide the URL.

        ```python
        @sync_call
        @mcp_session('http://localhost:8000/sse')
        async def run(session, request: str) -> str:
            ...
        ```
    
    - To connect via websocket with a WS based MCP server, provide the URL.

        ```python
        @sync_call
        @mcp_session('ws://localhost:8000/message')
        async def run(session, request: str) -> str:
            ...
        ```


3. create an `McpAgent` instance within the MCP session

    After creating `McpAgent`, you need to call the `fetch_abilities()` method to retrieve tool configurations from the MCP server.

    ```python
    @sync_call
    @mcp_session(mcp_config)
    async def run(session, request: str) -> str:
        mcp_agent = await McpAgent(session=session, brain=get_openai_model()).fetch_abilities()
        ...
    ```

4. assign tasks to the `McpAgent` instance and await execution result

    ```python
    @sync_call
    @mcp_session(mcp_config)
    async def run(session, request: str) -> str:
        mcp_agent = await McpAgent(session=session, brain=get_openai_model()).fetch_abilities()
        result = await mcp_agent.assign(request).just_do_it()
        return result.conclusion
    ```

5. call the function

    ```python
    if __name__ == '__main__':
        ret = run(request='What can you do?')
        print(ret)
    ```

> I also provide the complete MCP agent test script. [See example](https://github.com/vortezwohl/Autono/blob/autono/demo/mcp_agent.py).

## Observability

To make the working process of agents observable, I provide two hooks, namely `BeforeActionTaken` and `AfterActionTaken`. 
They allow you to observe and intervene in the decision-making and execution results of each step of the agent's actions. 
You can obtain and modify the agent's decision results for the next action through the `BeforeActionTaken` hook, 
while `AfterActionTaken` allows you to obtain and modify the execution results of the actions (the tampered execution results will be part of the agent's memory).

To start using hooks, follow the steps listed.

1. bring in hooks and messages from `autono`

    ```python
    from autono.brain.hook import BeforeActionTaken, AfterActionTaken
    from autono.message import BeforeActionTakenMessage, AfterActionTakenMessage
    ```

2. declare functions and encapsulate them as hooks

    ```python
    def before_action_taken(agent: Agent, message: BeforeActionTakenMessage):
        print(f'Agent: {agent.name}, Next move: {message}')
        return message

    def after_action_taken(agent: Agent, message: AfterActionTakenMessage):
        print(f'Agent: {agent.name}, Action taken: {message}')
        return message

    before_action_taken_hook = BeforeActionTaken(before_action_taken)
    after_action_taken_hook = AfterActionTaken(after_action_taken)
    ```

    > In these two hook functions, you intercepted the message and printed the information in the message. 
    Afterwards, you returned the message unaltered to the agent. 
    Of course, you also have the option to **modify** the information in the message, 
    thereby achieving intervention in the agent's working process.

3. use hooks during the agent's working process

    ```python
    agent.assign(...).just_do_it(before_action_taken_hook, after_action_taken_hook)
    ```
   