# Setup and Installation Guide

This guide provides detailed instructions for setting up the AI Math Assistant project on your local machine.

## 📋 Table of Contents

- [System Requirements](#system-requirements)
- [Installation Methods](#installation-methods)
- [Environment Setup](#environment-setup)
- [LLM Provider Configuration](#llm-provider-configuration)
- [Verification](#verification)
- [Troubleshooting](#troubleshooting)

## 💻 System Requirements

### Minimum Requirements

- **Operating System**: Linux, macOS, or Windows 10+
- **Python**: 3.13 or higher
- **RAM**: 4GB minimum (8GB recommended)
- **Disk Space**: 2GB free space
- **Internet**: Required for package installation and API access

### Recommended Requirements

- **Python**: 3.13.5 or latest stable version
- **RAM**: 16GB (for running local LLMs with Ollama)
- **GPU**: NVIDIA GPU with CUDA support (optional, for Ollama)

## 🚀 Installation Methods

### Method 1: Standard Installation (Recommended)

#### Step 1: Clone the Repository

```bash
# Using HTTPS
git clone https://github.com/your-username/agentic-ai.git
cd agentic-ai

# Or using SSH
git clone git@github.com:your-username/agentic-ai.git
cd agentic-ai
```

#### Step 2: Create Virtual Environment

**Using venv (Python built-in):**

```bash
# Create virtual environment
python -m venv venv

# Activate on Linux/macOS
source venv/bin/activate

# Activate on Windows
venv\Scripts\activate
```

**Using conda:**

```bash
# Create conda environment
conda create -n agentic-ai python=3.13

# Activate environment
conda activate agentic-ai
```

#### Step 3: Install Dependencies

```bash
# Install all required packages
pip install langchain langchain-ollama langchain-community wikipedia openai langchain-openai

# Or install from requirements file (if available)
pip install -r requirements.txt
```

#### Step 4: Install Jupyter

```bash
# Install Jupyter Notebook
pip install jupyter

# Or install JupyterLab (recommended)
pip install jupyterlab
```

### Method 2: Development Installation

For contributors who want to modify the code:

```bash
# Clone the repository
git clone https://github.com/your-username/agentic-ai.git
cd agentic-ai

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in editable mode with development dependencies
pip install -e .
pip install pytest black flake8 mypy jupyter
```

### Method 3: Docker Installation (Coming Soon)

Docker support is planned for future releases.

## 🔧 Environment Setup

### Creating a Requirements File

If you need to create a `requirements.txt` file:

```bash
# After installing all packages
pip freeze > requirements.txt
```

Example `requirements.txt`:

```
langchain==0.3.23
langchain-ollama==0.3.0
langchain-community==0.3.16
langchain-openai==0.3.16
wikipedia==1.4.0
openai==1.77.0
jupyter==1.0.0
```

### Environment Variables

Create a `.env` file in the project root for API keys:

```bash
# .env file
OPENAI_API_KEY=your_openai_api_key_here
WATSONX_API_KEY=your_watsonx_api_key_here
WATSONX_PROJECT_ID=your_project_id_here
OLLAMA_URL=http://localhost:11434
```

**Important**: Add `.env` to your `.gitignore` to avoid committing sensitive information.

## 🤖 LLM Provider Configuration

### Option 1: Ollama (Local, Free)

Ollama allows you to run LLMs locally without API keys.

#### Install Ollama

**Linux:**
```bash
curl -fsSL https://ollama.com/install.sh | sh
```

**macOS:**
```bash
brew install ollama
```

**Windows:**
Download from [ollama.com](https://ollama.com/download)

#### Pull Models

```bash
# Pull Llama 3 model
ollama pull llama3

# Pull Granite Code model
ollama pull granite-code

# List available models
ollama list
```

#### Start Ollama Server

```bash
# Start Ollama service
ollama serve

# The server will run on http://localhost:11434
```

#### Configure in Python

```python
from langchain_ollama import ChatOllama

llm = ChatOllama(
    model='llama3',
    url='http://localhost:11434'
)
```

### Option 2: OpenAI (Cloud, Paid)

#### Get API Key

1. Sign up at [platform.openai.com](https://platform.openai.com)
2. Navigate to API Keys section
3. Create a new API key
4. Copy and save the key securely

#### Configure in Python

```python
from langchain_openai import ChatOpenAI
import os

llm = ChatOpenAI(
    model="gpt-4",
    api_key=os.getenv("OPENAI_API_KEY")  # Or directly: "your-api-key"
)
```

#### Set Environment Variable

**Linux/macOS:**
```bash
export OPENAI_API_KEY='your-api-key-here'
```

**Windows (PowerShell):**
```powershell
$env:OPENAI_API_KEY='your-api-key-here'
```

**Windows (Command Prompt):**
```cmd
set OPENAI_API_KEY=your-api-key-here
```

### Option 3: IBM watsonx (Cloud, Enterprise)

#### Get API Credentials

1. Sign up at [IBM Cloud](https://cloud.ibm.com)
2. Create a watsonx.ai instance
3. Get your API key and project ID

#### Configure in Python

```python
from langchain_ibm import ChatWatsonx
import os

llm = ChatWatsonx(
    model_id="ibm/granite-3-2-8b-instruct",
    url="https://us-south.ml.cloud.ibm.com",
    project_id=os.getenv("WATSONX_PROJECT_ID"),
    api_key=os.getenv("WATSONX_API_KEY")
)
```

## ✅ Verification

### Verify Python Installation

```bash
python --version
# Should output: Python 3.13.x or higher
```

### Verify Package Installation

```python
# Run in Python interpreter or Jupyter
import sys
print(f"Python version: {sys.version}")

import langchain
print(f"LangChain version: {langchain.__version__}")

from langchain_ollama import ChatOllama
print("LangChain Ollama imported successfully")

from langchain_openai import ChatOpenAI
print("LangChain OpenAI imported successfully")
```

### Test LLM Connection

**Test Ollama:**

```python
from langchain_ollama import ChatOllama

llm = ChatOllama(model='llama3', url='http://localhost:11434')
response = llm.invoke("Hello, how are you?")
print(response.content)
```

**Test OpenAI:**

```python
from langchain_openai import ChatOpenAI
import os

llm = ChatOpenAI(
    model="gpt-3.5-turbo",
    api_key=os.getenv("OPENAI_API_KEY")
)
response = llm.invoke("Hello, how are you?")
print(response.content)
```

### Launch Jupyter Notebook

```bash
# Start Jupyter Notebook
jupyter notebook

# Or start JupyterLab
jupyter lab

# Navigate to: assets/cognitiveclass/notebooks/AI-Math-Assistant Tool Calling.ipynb
```

## 🔍 Troubleshooting

### Common Issues

#### Issue 1: Python Version Mismatch

**Problem**: `python --version` shows Python 2.x or older version

**Solution**:
```bash
# Try python3 instead
python3 --version

# Use python3 for all commands
python3 -m venv venv
```

#### Issue 2: pip Not Found

**Problem**: `pip: command not found`

**Solution**:
```bash
# Use python -m pip instead
python -m pip install --upgrade pip

# Or install pip
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python get-pip.py
```

#### Issue 3: Permission Denied

**Problem**: Permission errors during installation

**Solution**:
```bash
# Use --user flag
pip install --user langchain

# Or use sudo (not recommended)
sudo pip install langchain
```

#### Issue 4: Ollama Connection Failed

**Problem**: Cannot connect to Ollama server

**Solution**:
```bash
# Check if Ollama is running
curl http://localhost:11434/api/tags

# Start Ollama service
ollama serve

# Check firewall settings
# Ensure port 11434 is not blocked
```

#### Issue 5: OpenAI API Key Invalid

**Problem**: Authentication error with OpenAI

**Solution**:
1. Verify API key is correct
2. Check if key has expired
3. Ensure billing is set up on OpenAI account
4. Verify environment variable is set correctly:
   ```bash
   echo $OPENAI_API_KEY  # Linux/macOS
   echo %OPENAI_API_KEY%  # Windows
   ```

#### Issue 6: Import Errors

**Problem**: `ModuleNotFoundError: No module named 'langchain'`

**Solution**:
```bash
# Ensure virtual environment is activated
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows

# Reinstall packages
pip install langchain langchain-ollama langchain-community
```

#### Issue 7: Jupyter Kernel Issues

**Problem**: Jupyter can't find Python kernel

**Solution**:
```bash
# Install ipykernel
pip install ipykernel

# Add kernel to Jupyter
python -m ipykernel install --user --name=agentic-ai

# Select the kernel in Jupyter: Kernel > Change Kernel > agentic-ai
```

### Getting Help

If you encounter issues not covered here:

1. Check the [main README](../README.md)
2. Review [existing issues](https://github.com/your-username/agentic-ai/issues)
3. Search [LangChain documentation](https://python.langchain.com/)
4. Create a new issue with:
   - Your OS and Python version
   - Complete error message
   - Steps to reproduce
   - What you've already tried

## 📚 Next Steps

After successful setup:

1. Open the Jupyter notebook: `assets/cognitiveclass/notebooks/AI-Math-Assistant Tool Calling.ipynb`
2. Follow the tutorial step-by-step
3. Experiment with creating your own tools
4. Check out the [API Documentation](API.md)
5. Review [examples](EXAMPLES.md)

## 🔄 Updating

To update the project and dependencies:

```bash
# Pull latest changes
git pull origin main

# Update dependencies
pip install --upgrade langchain langchain-ollama langchain-community

# Update Ollama models
ollama pull llama3
```

## 🗑️ Uninstallation

To remove the project:

```bash
# Deactivate virtual environment
deactivate

# Remove project directory
cd ..
rm -rf agentic-ai

# Remove conda environment (if used)
conda env remove -n agentic-ai
```

---

**Need more help?** Check out our [Contributing Guide](../CONTRIBUTING.md) or open an issue on GitHub.