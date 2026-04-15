# Architecture Documentation

This document provides an in-depth look at the architecture of the AI Math Assistant project, explaining how components interact and the design decisions behind the implementation.

## 📋 Table of Contents

- [System Overview](#system-overview)
- [Component Architecture](#component-architecture)
- [Data Flow](#data-flow)
- [Design Patterns](#design-patterns)
- [LLM Integration Layer](#llm-integration-layer)
- [Tool Framework](#tool-framework)
- [Agent Orchestration](#agent-orchestration)
- [Extension Points](#extension-points)

## 🏗️ System Overview

The AI Math Assistant is built on a modular architecture that separates concerns into distinct layers:

```
┌─────────────────────────────────────────────────────────┐
│                    User Interface Layer                  │
│              (Jupyter Notebook / CLI)                    │
└─────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────┐
│                    Agent Layer                           │
│         (Query Understanding & Tool Orchestration)       │
└─────────────────────────────────────────────────────────┘
                            │
                ┌───────────┴───────────┐
                ▼                       ▼
┌──────────────────────────┐  ┌──────────────────────────┐
│      LLM Layer           │  │      Tool Layer          │
│  (Language Models)       │  │  (Mathematical Tools)    │
└──────────────────────────┘  └──────────────────────────┘
                │                       │
                └───────────┬───────────┘
                            ▼
┌─────────────────────────────────────────────────────────┐
│                  Execution Layer                         │
│            (Function Execution & Results)                │
└─────────────────────────────────────────────────────────┘
```

### Key Components

1. **User Interface Layer**: Jupyter notebooks or CLI for user interaction
2. **Agent Layer**: Orchestrates tool selection and execution
3. **LLM Layer**: Provides natural language understanding
4. **Tool Layer**: Contains specialized functions for specific tasks
5. **Execution Layer**: Handles actual computation and result formatting

## 🔧 Component Architecture

### 1. Tool Component

Tools are the fundamental building blocks that encapsulate specific functionality.

```python
┌─────────────────────────────────────────┐
│              Tool                        │
├─────────────────────────────────────────┤
│ - name: str                              │
│ - description: str                       │
│ - func: Callable[[str], dict]           │
├─────────────────────────────────────────┤
│ + invoke(input: str) -> dict            │
│ + run(input: str) -> str                │
└─────────────────────────────────────────┘
```

**Responsibilities:**
- Encapsulate a single, well-defined operation
- Validate input data
- Execute the operation
- Return structured results
- Handle errors gracefully

**Example Implementation:**

```python
from langchain.agents import Tool

def add_numbers(inputs: str) -> dict:
    """
    Core function that performs the operation.
    
    Design principles:
    1. Single responsibility
    2. Clear input/output contract
    3. Error handling
    4. Type safety
    """
    try:
        # Input parsing
        numbers = [int(x) for x in inputs.replace(",", "").split() 
                   if x.isdigit()]
        
        # Validation
        if not numbers:
            return {"error": "No valid numbers found"}
        
        # Execution
        result = sum(numbers)
        
        # Return structured result
        return {"result": result}
        
    except Exception as e:
        return {"error": str(e)}

# Tool wrapper
add_tool = Tool(
    name="AddTool",
    func=add_numbers,
    description="Adds a list of numbers and returns the result."
)
```

### 2. Agent Component

The agent is the orchestration layer that coordinates between the LLM and tools.

```python
┌─────────────────────────────────────────┐
│              Agent                       │
├─────────────────────────────────────────┤
│ - tools: List[Tool]                      │
│ - llm: BaseLanguageModel                 │
│ - agent_type: AgentType                  │
│ - memory: Optional[Memory]               │
├─────────────────────────────────────────┤
│ + invoke(query: str) -> dict            │
│ + plan(query: str) -> List[Action]      │
│ + execute(action: Action) -> Result     │
│ + synthesize(results: List) -> str      │
└─────────────────────────────────────────┘
```

**Responsibilities:**
- Parse user queries
- Plan tool execution sequence
- Execute tools in correct order
- Aggregate results
- Generate natural language responses

**Agent Types:**

1. **ZERO_SHOT_REACT_DESCRIPTION**
   - Uses tool descriptions to decide which tool to use
   - No prior examples needed
   - Best for general-purpose applications

2. **CONVERSATIONAL_REACT_DESCRIPTION**
   - Maintains conversation history
   - Context-aware responses
   - Best for chat applications

3. **STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION**
   - Handles complex, structured inputs
   - Multi-parameter tool support
   - Best for advanced use cases

### 3. LLM Component

The Language Model provides natural language understanding and generation.

```python
┌─────────────────────────────────────────┐
│         Language Model                   │
├─────────────────────────────────────────┤
│ - model_id: str                          │
│ - temperature: float                     │
│ - max_tokens: int                        │
├─────────────────────────────────────────┤
│ + invoke(prompt: str) -> Response       │
│ + stream(prompt: str) -> Iterator       │
│ + batch(prompts: List) -> List          │
└─────────────────────────────────────────┘
```

**Supported Providers:**

1. **Ollama** (Local)
   - Free, runs locally
   - No API key required
   - Good for development and testing

2. **OpenAI** (Cloud)
   - High quality responses
   - Requires API key
   - Pay per use

3. **IBM watsonx** (Enterprise)
   - Enterprise-grade
   - Granite models
   - Requires credentials

## 🔄 Data Flow

### Query Processing Flow

```
User Query
    │
    ▼
┌─────────────────────┐
│  Agent receives     │
│  natural language   │
│  query              │
└─────────────────────┘
    │
    ▼
┌─────────────────────┐
│  LLM analyzes       │
│  query and          │
│  determines intent  │
└─────────────────────┘
    │
    ▼
┌─────────────────────┐
│  Agent selects      │
│  appropriate        │
│  tool(s)            │
└─────────────────────┘
    │
    ▼
┌─────────────────────┐
│  Tool executes      │
│  with parsed        │
│  parameters         │
└─────────────────────┘
    │
    ▼
┌─────────────────────┐
│  Result returned    │
│  to agent           │
└─────────────────────┘
    │
    ▼
┌─────────────────────┐
│  LLM formats        │
│  response in        │
│  natural language   │
└─────────────────────┘
    │
    ▼
User Response
```

### Multi-Step Query Flow

For complex queries requiring multiple tools:

```
Query: "Add 10 and 20, then multiply by 3"
    │
    ▼
┌─────────────────────────────────────┐
│ Step 1: LLM identifies two          │
│ operations needed                    │
└─────────────────────────────────────┘
    │
    ├─────────────────┐
    ▼                 ▼
┌─────────┐     ┌─────────┐
│ AddTool │     │MultTool │
│ 10 + 20 │     │ ? * 3   │
│ = 30    │     │         │
└─────────┘     └─────────┘
    │                 ▲
    └─────────────────┘
                │
                ▼
        ┌─────────────┐
        │  MultTool   │
        │  30 * 3     │
        │  = 90       │
        └─────────────┘
                │
                ▼
        Final Result: 90
```

## 🎨 Design Patterns

### 1. Strategy Pattern (Tool Selection)

The agent uses the Strategy pattern to select and execute different tools based on the query.

```python
class ToolStrategy:
    """Abstract strategy for tool execution."""
    
    def execute(self, inputs: str) -> dict:
        raise NotImplementedError

class AddStrategy(ToolStrategy):
    def execute(self, inputs: str) -> dict:
        return add_numbers(inputs)

class MultiplyStrategy(ToolStrategy):
    def execute(self, inputs: str) -> dict:
        return mult_numbers(inputs)
```

### 2. Factory Pattern (Tool Creation)

Tools can be created using a factory pattern for consistency.

```python
class ToolFactory:
    """Factory for creating tools."""
    
    @staticmethod
    def create_math_tool(
        name: str,
        operation: callable,
        description: str
    ) -> Tool:
        """Create a mathematical tool."""
        
        def tool_function(inputs: str) -> dict:
            try:
                numbers = parse_numbers(inputs)
                result = operation(numbers)
                return {"result": result}
            except Exception as e:
                return {"error": str(e)}
        
        return Tool(
            name=name,
            func=tool_function,
            description=description
        )
```

### 3. Chain of Responsibility (Error Handling)

Error handling follows a chain of responsibility pattern.

```python
class ErrorHandler:
    """Base error handler."""
    
    def __init__(self, next_handler=None):
        self.next_handler = next_handler
    
    def handle(self, error):
        if self.can_handle(error):
            return self.process(error)
        elif self.next_handler:
            return self.next_handler.handle(error)
        return {"error": "Unhandled error"}
    
    def can_handle(self, error):
        raise NotImplementedError
    
    def process(self, error):
        raise NotImplementedError

class ValidationErrorHandler(ErrorHandler):
    def can_handle(self, error):
        return isinstance(error, ValueError)
    
    def process(self, error):
        return {"error": f"Validation error: {str(error)}"}

class DivisionByZeroHandler(ErrorHandler):
    def can_handle(self, error):
        return isinstance(error, ZeroDivisionError)
    
    def process(self, error):
        return {"error": "Cannot divide by zero"}
```

### 4. Decorator Pattern (Tool Enhancement)

Tools can be enhanced with decorators for logging, caching, etc.

```python
def logged_tool(tool_func):
    """Decorator to add logging to tools."""
    
    def wrapper(inputs: str) -> dict:
        print(f"Executing tool with inputs: {inputs}")
        result = tool_func(inputs)
        print(f"Tool result: {result}")
        return result
    
    return wrapper

def cached_tool(tool_func):
    """Decorator to add caching to tools."""
    cache = {}
    
    def wrapper(inputs: str) -> dict:
        if inputs in cache:
            print(f"Cache hit for: {inputs}")
            return cache[inputs]
        
        result = tool_func(inputs)
        cache[inputs] = result
        return result
    
    return wrapper

# Usage
@logged_tool
@cached_tool
def add_numbers(inputs: str) -> dict:
    numbers = [int(x) for x in inputs.split() if x.isdigit()]
    return {"result": sum(numbers)}
```

## 🔌 LLM Integration Layer

### Abstraction Layer

The LLM integration uses an abstraction layer to support multiple providers.

```python
from abc import ABC, abstractmethod

class LLMProvider(ABC):
    """Abstract base class for LLM providers."""
    
    @abstractmethod
    def invoke(self, prompt: str) -> str:
        """Send prompt and get response."""
        pass
    
    @abstractmethod
    def configure(self, **kwargs):
        """Configure provider-specific settings."""
        pass

class OllamaProvider(LLMProvider):
    def __init__(self, model: str, url: str):
        self.llm = ChatOllama(model=model, url=url)
    
    def invoke(self, prompt: str) -> str:
        response = self.llm.invoke(prompt)
        return response.content
    
    def configure(self, **kwargs):
        # Configure Ollama-specific settings
        pass

class OpenAIProvider(LLMProvider):
    def __init__(self, model: str, api_key: str):
        self.llm = ChatOpenAI(model=model, api_key=api_key)
    
    def invoke(self, prompt: str) -> str:
        response = self.llm.invoke(prompt)
        return response.content
    
    def configure(self, **kwargs):
        # Configure OpenAI-specific settings
        pass
```

## 🛠️ Tool Framework

### Tool Interface

All tools implement a common interface:

```python
from typing import Protocol

class ToolProtocol(Protocol):
    """Protocol defining tool interface."""
    
    name: str
    description: str
    
    def invoke(self, inputs: str) -> dict:
        """Execute the tool."""
        ...
    
    def validate(self, inputs: str) -> bool:
        """Validate inputs before execution."""
        ...
```

### Tool Registry

Tools are managed through a registry:

```python
class ToolRegistry:
    """Registry for managing tools."""
    
    def __init__(self):
        self._tools = {}
    
    def register(self, tool: Tool):
        """Register a new tool."""
        self._tools[tool.name] = tool
    
    def get(self, name: str) -> Tool:
        """Get tool by name."""
        return self._tools.get(name)
    
    def list_tools(self) -> list:
        """List all registered tools."""
        return list(self._tools.values())
    
    def unregister(self, name: str):
        """Remove a tool from registry."""
        if name in self._tools:
            del self._tools[name]

# Usage
registry = ToolRegistry()
registry.register(add_tool)
registry.register(mult_tool)

# Get all tools for agent
tools = registry.list_tools()
agent = initialize_agent(tools, llm, AgentType.ZERO_SHOT_REACT_DESCRIPTION)
```

## 🎯 Agent Orchestration

### Agent Execution Pipeline

```python
class AgentPipeline:
    """Pipeline for agent execution."""
    
    def __init__(self, agent):
        self.agent = agent
        self.middleware = []
    
    def add_middleware(self, middleware):
        """Add middleware to pipeline."""
        self.middleware.append(middleware)
    
    def execute(self, query: str) -> dict:
        """Execute query through pipeline."""
        
        # Pre-processing
        for mw in self.middleware:
            query = mw.pre_process(query)
        
        # Agent execution
        result = self.agent.invoke(query)
        
        # Post-processing
        for mw in reversed(self.middleware):
            result = mw.post_process(result)
        
        return result

class LoggingMiddleware:
    """Middleware for logging."""
    
    def pre_process(self, query: str) -> str:
        print(f"Query: {query}")
        return query
    
    def post_process(self, result: dict) -> dict:
        print(f"Result: {result}")
        return result

class ValidationMiddleware:
    """Middleware for validation."""
    
    def pre_process(self, query: str) -> str:
        if not query.strip():
            raise ValueError("Empty query")
        return query
    
    def post_process(self, result: dict) -> dict:
        if "error" in result:
            print(f"Warning: {result['error']}")
        return result
```

## 🔌 Extension Points

### Adding New Tools

1. **Create the function:**
```python
def new_operation(inputs: str) -> dict:
    # Implementation
    return {"result": result}
```

2. **Wrap in Tool:**
```python
new_tool = Tool(
    name="NewTool",
    func=new_operation,
    description="Description"
)
```

3. **Register with agent:**
```python
tools.append(new_tool)
agent = initialize_agent(tools, llm, AgentType.ZERO_SHOT_REACT_DESCRIPTION)
```

### Adding New LLM Providers

1. **Implement provider class:**
```python
class NewProvider(LLMProvider):
    def invoke(self, prompt: str) -> str:
        # Implementation
        pass
```

2. **Configure and use:**
```python
llm = NewProvider(config)
agent = initialize_agent(tools, llm, AgentType.ZERO_SHOT_REACT_DESCRIPTION)
```

## 📊 Performance Considerations

### Caching Strategy

```python
from functools import lru_cache

@lru_cache(maxsize=128)
def cached_operation(inputs: str) -> dict:
    """Cached version of expensive operation."""
    # Expensive computation
    return result
```

### Async Support

```python
import asyncio

async def async_tool(inputs: str) -> dict:
    """Async tool for concurrent execution."""
    result = await async_operation(inputs)
    return {"result": result}
```

## 🔗 Related Documentation

- [API Documentation](API.md)
- [Setup Guide](SETUP.md)
- [Examples](EXAMPLES.md)
- [Contributing Guide](../CONTRIBUTING.md)

---

This architecture is designed to be extensible, maintainable, and scalable. For questions or suggestions, please open an issue on GitHub.