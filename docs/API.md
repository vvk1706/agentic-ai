# API Documentation

This document provides comprehensive API documentation for the AI Math Assistant project, including tools, agents, and LLM integrations.

## 📋 Table of Contents

- [Core Concepts](#core-concepts)
- [Tool API](#tool-api)
- [Agent API](#agent-api)
- [LLM Integration](#llm-integration)
- [Built-in Tools](#built-in-tools)
- [Custom Tool Development](#custom-tool-development)
- [Error Handling](#error-handling)
- [Examples](#examples)

## 🎯 Core Concepts

### Tool

A **Tool** is a wrapper around a Python function that makes it compatible with LangChain agents. Tools have three essential components:

1. **Name**: Unique identifier for the tool
2. **Function**: The actual Python function to execute
3. **Description**: Explains what the tool does (used by LLM to decide when to use it)

### Agent

An **Agent** is an orchestrator that:
- Receives user queries
- Decides which tools to use
- Executes tools in the correct order
- Returns formatted results

### LLM (Large Language Model)

The **LLM** is the "brain" that:
- Understands natural language queries
- Plans tool execution strategy
- Interprets tool results
- Generates human-readable responses

## 🔧 Tool API

### Creating a Tool

```python
from langchain.agents import Tool

tool = Tool(
    name="ToolName",
    func=your_function,
    description="Description of what the tool does"
)
```

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `name` | `str` | Yes | Unique identifier for the tool |
| `func` | `Callable` | Yes | Python function to execute |
| `description` | `str` | Yes | Clear description for LLM understanding |
| `return_direct` | `bool` | No | If True, return result directly without LLM processing |
| `args_schema` | `Type[BaseModel]` | No | Pydantic model for input validation |

#### Tool Function Signature

```python
def tool_function(inputs: str) -> dict:
    """
    Tool functions should follow this pattern.
    
    Args:
        inputs (str): String input from the agent
        
    Returns:
        dict: Dictionary with 'result' key containing the output
    """
    # Process inputs
    result = process(inputs)
    return {"result": result}
```

### Tool Methods

#### `invoke(input: str) -> dict`

Execute the tool with given input.

```python
result = tool.invoke("input string")
print(result)  # {'result': output}
```

#### `run(input: str) -> str`

Execute the tool and return result as string.

```python
result = tool.run("input string")
print(result)  # "output"
```

### Mathematical Tools

#### AddTool

Adds a list of numbers from string input.

```python
from langchain.agents import Tool

def add_numbers(inputs: str) -> dict:
    """
    Adds numbers extracted from input string.
    
    Args:
        inputs (str): String containing numbers (e.g., "10 20 30")
        
    Returns:
        dict: {'result': sum_of_numbers}
        
    Example:
        >>> add_numbers("10 20 30")
        {'result': 60}
    """
    numbers = [int(x) for x in inputs.replace(",", "").split() if x.isdigit()]
    result = sum(numbers)
    return {"result": result}

add_tool = Tool(
    name="AddTool",
    func=add_numbers,
    description="Adds a list of numbers and returns the result."
)
```

**Usage:**
```python
# Direct function call
result = add_numbers("5 10 15")
print(result)  # {'result': 30}

# Through tool
result = add_tool.invoke("5 10 15")
print(result)  # {'result': 30}
```

#### MultTool

Multiplies a list of numbers from string input.

```python
def mult_numbers(inputs: str) -> dict:
    """
    Multiplies numbers extracted from input string.
    
    Args:
        inputs (str): String containing numbers (e.g., "2 3 4")
        
    Returns:
        dict: {'result': product_of_numbers}
        
    Example:
        >>> mult_numbers("2 3 4")
        {'result': 24}
    """
    numbers = [int(x) for x in inputs.replace(",", "").split() if x.isdigit()]
    result = 1
    for x in numbers:
        result *= x
    return {"result": result}

mult_tool = Tool(
    name="MultTool",
    func=mult_numbers,
    description="Multiply a list of numbers and returns the result."
)
```

**Usage:**
```python
result = mult_tool.invoke("2 5 10")
print(result)  # {'result': 100}
```

#### SubtractTool

Subtracts numbers sequentially from string input.

```python
def subtract_numbers(inputs: str) -> dict:
    """
    Subtracts numbers sequentially from input string.
    
    Args:
        inputs (str): String containing numbers (e.g., "100 20 10")
        
    Returns:
        dict: {'result': result_of_subtraction}
        
    Example:
        >>> subtract_numbers("100 20 10")
        {'result': 70}  # 100 - 20 - 10
    """
    numbers = [int(x) for x in inputs.replace(",", "").split() if x.isdigit()]
    if not numbers:
        return {"result": 0}
    result = numbers[0]
    for num in numbers[1:]:
        result -= num
    return {"result": result}

subtract_tool = Tool(
    name="SubtractTool",
    func=subtract_numbers,
    description="Subtracts numbers sequentially and returns the result."
)
```

#### PowerTool

Calculates base raised to exponent power.

```python
def power_tool(inputs: str) -> dict:
    """
    Calculates base raised to exponent power.
    
    Args:
        inputs (str): String with base and exponent (e.g., "2 3" for 2^3)
        
    Returns:
        dict: {'result': power_result}
        
    Raises:
        ValueError: If not exactly two numbers provided
        
    Example:
        >>> power_tool("2 8")
        {'result': 256}  # 2^8
    """
    numbers = [int(x) for x in inputs.replace(",", "").split() if x.isdigit()]
    if len(numbers) != 2:
        raise ValueError("Power tool requires exactly two numbers: base and exponent")
    return {"result": numbers[0] ** numbers[1]}

power = Tool(
    name="PowerTool",
    func=power_tool,
    description="Calculates base raised to exponent power. Input format: 'base exponent'"
)
```

## 🤖 Agent API

### Creating an Agent

```python
from langchain.agents import initialize_agent, AgentType

agent = initialize_agent(
    tools=[tool1, tool2, tool3],
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)
```

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `tools` | `List[Tool]` | Yes | List of tools available to the agent |
| `llm` | `BaseLanguageModel` | Yes | Language model to use |
| `agent` | `AgentType` | Yes | Type of agent to create |
| `verbose` | `bool` | No | If True, print reasoning steps |
| `max_iterations` | `int` | No | Maximum number of tool calls |
| `early_stopping_method` | `str` | No | When to stop: "force" or "generate" |
| `handle_parsing_errors` | `bool` | No | How to handle parsing errors |

#### Agent Types

| Type | Description | Use Case |
|------|-------------|----------|
| `ZERO_SHOT_REACT_DESCRIPTION` | Uses tool descriptions to decide | General purpose, most common |
| `CONVERSATIONAL_REACT_DESCRIPTION` | Maintains conversation memory | Chat applications |
| `STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION` | Handles complex inputs | Multi-parameter tools |

### Agent Methods

#### `invoke(input: str) -> dict`

Execute the agent with a query.

```python
result = agent.invoke("What is 25 plus 15 multiplied by 2?")
print(result)
```

#### `run(input: str) -> str`

Execute and return result as string.

```python
result = agent.run("Calculate 10 + 20")
print(result)  # "30"
```

### Agent Configuration Example

```python
from langchain.agents import initialize_agent, AgentType
from langchain_ollama import ChatOllama

# Initialize LLM
llm = ChatOllama(model='llama3', url='http://localhost:11434')

# Create tools
tools = [add_tool, mult_tool, subtract_tool, power]

# Initialize agent
agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
    max_iterations=5,
    handle_parsing_errors=True
)

# Use agent
response = agent.invoke("Add 10 and 20, then multiply by 3")
print(response['output'])
```

## 🔌 LLM Integration

### Ollama Integration

```python
from langchain_ollama import ChatOllama

llm = ChatOllama(
    model='llama3',           # Model name
    url='http://localhost:11434',  # Ollama server URL
    temperature=0.7,          # Randomness (0-1)
    num_predict=256,          # Max tokens to generate
    top_k=40,                 # Top-k sampling
    top_p=0.9                 # Top-p sampling
)
```

#### Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `model` | `str` | Required | Model name (e.g., 'llama3', 'granite-code') |
| `url` | `str` | `http://localhost:11434` | Ollama server URL |
| `temperature` | `float` | `0.8` | Randomness in responses (0-1) |
| `num_predict` | `int` | `128` | Maximum tokens to generate |
| `top_k` | `int` | `40` | Top-k sampling parameter |
| `top_p` | `float` | `0.9` | Top-p (nucleus) sampling |

### OpenAI Integration

```python
from langchain_openai import ChatOpenAI
import os

llm = ChatOpenAI(
    model="gpt-4",
    api_key=os.getenv("OPENAI_API_KEY"),
    temperature=0.7,
    max_tokens=256
)
```

#### Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `model` | `str` | `gpt-3.5-turbo` | Model name |
| `api_key` | `str` | Required | OpenAI API key |
| `temperature` | `float` | `0.7` | Randomness (0-2) |
| `max_tokens` | `int` | `None` | Maximum tokens to generate |
| `top_p` | `float` | `1.0` | Nucleus sampling |

### IBM watsonx Integration

```python
from langchain_ibm import ChatWatsonx
import os

llm = ChatWatsonx(
    model_id="ibm/granite-3-2-8b-instruct",
    url="https://us-south.ml.cloud.ibm.com",
    project_id=os.getenv("WATSONX_PROJECT_ID"),
    api_key=os.getenv("WATSONX_API_KEY"),
    params={
        "temperature": 0.7,
        "max_new_tokens": 256
    }
)
```

## 🛠️ Built-in Tools

LangChain provides several built-in tools:

### Wikipedia Tool

```python
from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper

wikipedia = WikipediaQueryRun(
    api_wrapper=WikipediaAPIWrapper()
)

result = wikipedia.run("Python programming language")
```

### Calculator Tool

```python
from langchain.chains import LLMMathChain
from langchain.agents import Tool

llm_math = LLMMathChain.from_llm(llm=llm)

calculator = Tool(
    name="Calculator",
    func=llm_math.run,
    description="Useful for mathematical calculations"
)
```

## 🎨 Custom Tool Development

### Basic Custom Tool

```python
from langchain.agents import Tool

def custom_function(inputs: str) -> dict:
    """Your custom logic here."""
    # Process inputs
    result = your_processing_logic(inputs)
    return {"result": result}

custom_tool = Tool(
    name="CustomTool",
    func=custom_function,
    description="Clear description of what this tool does"
)
```

### Advanced Custom Tool with Validation

```python
from langchain.tools import BaseTool
from pydantic import BaseModel, Field
from typing import Type

class CustomToolInput(BaseModel):
    """Input schema for custom tool."""
    value: int = Field(description="The input value")
    operation: str = Field(description="Operation to perform")

class CustomTool(BaseTool):
    name = "custom_tool"
    description = "Performs custom operations"
    args_schema: Type[BaseModel] = CustomToolInput
    
    def _run(self, value: int, operation: str) -> str:
        """Execute the tool."""
        if operation == "double":
            return str(value * 2)
        elif operation == "square":
            return str(value ** 2)
        return "Unknown operation"
    
    async def _arun(self, value: int, operation: str) -> str:
        """Async version."""
        return self._run(value, operation)
```

## ⚠️ Error Handling

### Tool-Level Error Handling

```python
def safe_divide(inputs: str) -> dict:
    """Division with error handling."""
    try:
        numbers = [float(x) for x in inputs.split() if x.replace('.','').isdigit()]
        if len(numbers) != 2:
            return {"error": "Exactly two numbers required"}
        if numbers[1] == 0:
            return {"error": "Cannot divide by zero"}
        return {"result": numbers[0] / numbers[1]}
    except Exception as e:
        return {"error": f"Error: {str(e)}"}

divide_tool = Tool(
    name="DivideTool",
    func=safe_divide,
    description="Divides two numbers safely"
)
```

### Agent-Level Error Handling

```python
agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    handle_parsing_errors=True,  # Handle parsing errors
    max_iterations=5,             # Prevent infinite loops
    early_stopping_method="generate"  # Generate response on max iterations
)

try:
    result = agent.invoke("your query")
except Exception as e:
    print(f"Agent error: {e}")
```

## 📚 Examples

### Example 1: Simple Math Query

```python
from langchain_ollama import ChatOllama
from langchain.agents import Tool, initialize_agent, AgentType

# Setup
llm = ChatOllama(model='llama3', url='http://localhost:11434')
tools = [add_tool, mult_tool]
agent = initialize_agent(tools, llm, AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True)

# Query
result = agent.invoke("What is 15 plus 25?")
print(result['output'])  # "40"
```

### Example 2: Complex Multi-Step Query

```python
# Query with multiple operations
result = agent.invoke("Add 10 and 20, then multiply the result by 3")
print(result['output'])  # "90"
```

### Example 3: Custom Tool Integration

```python
# Create custom tool
def factorial(inputs: str) -> dict:
    n = int(inputs.strip())
    result = 1
    for i in range(1, n + 1):
        result *= i
    return {"result": result}

factorial_tool = Tool(
    name="FactorialTool",
    func=factorial,
    description="Calculates factorial of a number"
)

# Add to agent
tools = [add_tool, mult_tool, factorial_tool]
agent = initialize_agent(tools, llm, AgentType.ZERO_SHOT_REACT_DESCRIPTION)

# Use
result = agent.invoke("What is the factorial of 5?")
print(result['output'])  # "120"
```

## 🔗 Related Documentation

- [Setup Guide](SETUP.md)
- [Examples](EXAMPLES.md)
- [Contributing Guide](../CONTRIBUTING.md)
- [LangChain Official Docs](https://python.langchain.com/)

---

For more information or questions, please open an issue on GitHub.