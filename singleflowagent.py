import asyncio
import traceback

from pydantic import ValidationError

from beeai_framework.agents.types import AgentExecutionConfig
from beeai_framework.backend.chat import ChatModel
from beeai_framework.backend.message import UserMessage
from beeai_framework.memory import UnconstrainedMemory

from typing import Any
from beeai_framework.emitter.types import EmitterOptions
from beeai_framework.emitter.emitter import Emitter, EventMeta


# Import agent components
from beeai_framework.workflows.agent import AgentWorkflow
from beeai_framework.workflows.workflow import WorkflowError

# MCP Tool
from beeai_framework.tools.mcp import MCPTool
from mcp.client.stdio import stdio_client
from mcp import ClientSession, StdioServerParameters

# Create connection to Tool Server
server_params = StdioServerParameters(
    command="uv",
    args=[
        "--directory",
        "/Users/alicheraghian/Documents/Github/MCP-server/employee/",
        "run",
        "server.py",
    ],
    env=None,
)


async def tools_from_client() -> list[MCPTool]:
    async with (
        stdio_client(server_params) as (read, write),
        ClientSession(read, write) as session,
    ):
        await session.initialize()
        return await MCPTool.from_client(session)


mcp_tools = asyncio.run(tools_from_client())


async def process_agent_events(
    event_data: Any, event_meta: EventMeta
) -> None:
    """Process agent events and log appropriately"""

    if event_meta.name == "error":
        print("Agent 🤖 : ", str(event_data))
    elif event_meta.name == "retry":
        print("Agent 🤖 : ", "retrying the action...")
    elif event_meta.name == "update":
        if isinstance(event_data, dict) and "update" in event_data:
            print(
                f"Agent({event_data['update']['key']}) 🤖 : ",
                event_data["update"]["parsedValue"],
            )
    elif event_meta.name == "newToken":
        if hasattr(event_data, "value") and hasattr(event_data.value, "get_text_content"):
            print(event_data.value.get_text_content(), end="")


async def observer(emitter: Emitter) -> None:
    emitter.on("*.*", process_agent_events, EmitterOptions(match_nested=True))


async def main() -> None:
    print("🚀 Starting main function...")
    llm = ChatModel.from_name("ollama:granite3.1-dense:8b")
    print("✅ LLM created successfully")
    
    try:
        print("🔧 Creating workflow...")
        workflow = AgentWorkflow(name="Smart assistant")
        print("🔧 Adding agent...")
        workflow.add_agent(
            name="EmployeeChurn",
            instructions="You are a churn prediction specialist capable of predicting whether an employee will churn. Respond only if you can provide a useful answer.",
            tools=mcp_tools,
            llm=llm,
            execution=AgentExecutionConfig(max_iterations=3),
        )
        print("✅ Agent added successfully")

        employee_sample = {
            "YearsAtCompany": 10,
            "EmployeeSatisfaction": 0.90,
            "Position": "Non-Manager",
            "Salary": 2.0,
        }
        prompt = f"Will this employee churn {employee_sample}?"
        print(f"📝 Prompt: {prompt}")
        
        memory = UnconstrainedMemory()
        await memory.add(UserMessage(content=prompt))
        print("✅ Message added to memory")
        
        print("🏃 Starting workflow execution...")
        result = await workflow.run(inputs=memory.messages).observe(observer)
        print("✅ Workflow completed!")
        print(f"📊 Result: {result}")

    except WorkflowError:
        traceback.print_exc()
    except ValidationError:
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())