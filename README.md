# AI Math Assistant with LangChain Tool Calling

A comprehensive educational project demonstrating how to build AI agents using LangChain's tool calling capabilities. This repository contains a Jupyter notebook tutorial that teaches you how to create custom tools and orchestrate them with language models to solve mathematical problems through natural language interaction.

## 🎯 Overview

This project showcases the power of LangChain's agent framework by building an AI Math Assistant that can:
- Understand natural language mathematical queries
- Break down complex operations into simple steps
- Execute multiple mathematical operations sequentially
- Provide accurate results through tool orchestration

## 📚 What You'll Learn

- **Tool Calling Fundamentals**: Understanding how AI agents use tools to perform specific tasks
- **Custom Tool Creation**: Building specialized tools for mathematical operations
- **Agent Architecture**: How agents coordinate between language models and tools
- **LangChain Integration**: Working with IBM watsonx, OpenAI, and Ollama models
- **Error Handling**: Implementing robust tool functionality
- **Multi-Tool Orchestration**: Combining multiple tools to solve complex problems

## 🚀 Features

- **Mathematical Operations**: Addition, multiplication, subtraction, and power calculations
- **Natural Language Interface**: Interact with the assistant using plain English
- **Multiple LLM Support**: Compatible with IBM watsonx Granite, OpenAI GPT, and Ollama models
- **Extensible Architecture**: Easy to add new tools and capabilities
- **Educational Content**: Step-by-step tutorial with detailed explanations

## 📋 Prerequisites

- Python 3.13+ (tested with Python 3.13.5)
- Jupyter Notebook or JupyterLab
- Basic understanding of Python programming
- Familiarity with AI/ML concepts (helpful but not required)

## 🛠️ Installation

### 1. Clone the Repository

```bash
git clone <repository-url>
cd agentic-ai
```

### 2. Create a Virtual Environment (Recommended)

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Required Dependencies

```bash
pip install langchain
pip install langchain-ollama
pip install langchain-community
pip install wikipedia
pip install openai
pip install langchain-openai
```

Or install all at once:

```bash
pip install langchain langchain-ollama langchain-community wikipedia openai langchain-openai
```

## 📖 Usage

### Running the Jupyter Notebook

1. Start Jupyter:
```bash
jupyter notebook
```

2. Navigate to the notebook:
```
assets/cognitiveclass/notebooks/AI-Math-Assistant Tool Calling.ipynb
```

3. Follow the step-by-step tutorial in the notebook

### Quick Start Example

```python
from langchain_ollama import ChatOllama
from langchain.agents import Tool, AgentType

# Initialize the language model
llm = ChatOllama(model='llama3', url='http://localhost:11434')

# Define a simple addition tool
def add_numbers(inputs: str) -> dict:
    numbers = [int(x) for x in inputs.replace(",", "").split() if x.isdigit()]
    result = sum(numbers)
    return {"result": result}

# Create the tool
add_tool = Tool(
    name="AddTool",
    func=add_numbers,
    description="Adds a list of numbers and returns the result."
)

# Use the tool
result = add_tool.invoke("10 20 30")
print(result)  # Output: {'result': 60}
```

## 🏗️ Project Structure

```
agentic-ai/
├── assets/
│   └── cognitiveclass/
│       └── notebooks/
│           ├── AI-Math-Assistant Tool Calling.ipynb  # Main tutorial notebook
│           ├── .ipynb_checkpoints/                   # Jupyter checkpoints
│           ├── .jupyter/                             # Jupyter configuration
│           ├── .virtual_documents/                   # Virtual documents
│           └── anaconda_projects/                    # Anaconda project files
├── .gitignore                                        # Git ignore rules
└── README.md                                         # This file
```

## 🔧 Configuration

### Using Different LLM Providers

#### IBM watsonx (Granite Models)
```python
from langchain_ibm import ChatWatsonx

llm = ChatWatsonx(
    model_id="ibm/granite-3-2-8b-instruct",
    url="https://us-south.ml.cloud.ibm.com",
    project_id="your-project-id",
    api_key="your-api-key"
)
```

#### OpenAI
```python
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(
    model="gpt-4",
    api_key="your-openai-api-key"
)
```

#### Ollama (Local)
```python
from langchain_ollama import ChatOllama

llm = ChatOllama(
    model='llama3',
    url='http://localhost:11434'
)
```

## 📝 Tutorial Contents

The Jupyter notebook covers:

1. **Setup and Installation**: Getting your environment ready
2. **LLM Selection**: Choosing the right language model
3. **Function Basics**: Understanding tool functions
4. **Tool Creation**: Building custom tools with the Tool class
5. **Agent Initialization**: Setting up agents to use tools
6. **Multi-Tool Orchestration**: Combining multiple tools
7. **Built-in Tools**: Exploring LangChain's pre-built tools
8. **Exercises**: Hands-on practice creating new tools

## 🎓 Learning Objectives

After completing this tutorial, you will be able to:

- ✅ Explain the concept of tools in LangChain
- ✅ Create custom tools for specific tasks
- ✅ Build AI agents that can use multiple tools
- ✅ Debug and improve tool functionality
- ✅ Test tool implementations with various inputs
- ✅ Integrate different LLM providers
- ✅ Design tool architectures for complex workflows

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **IBM Skills Network**: For providing the educational framework
- **LangChain**: For the powerful agent framework
- **IBM watsonx**: For Granite language models
- **OpenAI**: For GPT models
- **Ollama**: For local LLM deployment

## 📞 Support

If you encounter any issues or have questions:

1. Check the [documentation](docs/)
2. Review existing [issues](../../issues)
3. Create a new issue with detailed information

## 🔗 Additional Resources

- [LangChain Documentation](https://python.langchain.com/)
- [IBM watsonx.ai](https://www.ibm.com/watsonx)
- [OpenAI API Documentation](https://platform.openai.com/docs)
- [Ollama Documentation](https://ollama.ai/)

## 🚦 Status

This project is actively maintained and updated with new features and improvements.

---

**Note**: This project is designed for educational purposes. When running locally, you'll need to configure your own API keys for IBM watsonx or OpenAI services. The Skills Network environment provides free access with limitations.