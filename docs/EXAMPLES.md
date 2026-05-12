# Examples and Use Cases

This document provides practical examples and use cases for the AI Math Assistant project, demonstrating various ways to use tools and agents.

## 📋 Table of Contents

- [Basic Examples](#basic-examples)
- [Mathematical Operations](#mathematical-operations)
- [Multi-Step Queries](#multi-step-queries)
- [Custom Tool Examples](#custom-tool-examples)
- [Advanced Use Cases](#advanced-use-cases)
- [Error Handling Examples](#error-handling-examples)
- [Integration Examples](#integration-examples)

## 🎯 Basic Examples

### Example 1: Simple Addition

```python
from langchain.agents import Tool

def add_numbers(inputs: str) -> dict:
    numbers = [int(x) for x in inputs.replace(",", "").split() if x.isdigit()]
    return {"result": sum(numbers)}

add_tool = Tool(
    name="AddTool",
    func=add_numbers,
    description="Adds a list of numbers and returns the result."
)

# Direct usage
result = add_tool.invoke("10 20 30")
print(result)  # Output: {'result': 60}
```

### Example 2: Simple Multiplication

```python
def mult_numbers(inputs: str) -> dict:
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

# Direct usage
result = mult_tool.invoke("2 5 10")
print(result)  # Output: {'result': 100}
```

## 🔢 Mathematical Operations

### Example 3: Subtraction Tool

```python
def subtract_numbers(inputs: str) -> dict:
    """Subtracts numbers sequentially."""
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
    description="Subtracts numbers sequentially from the first number."
)

# Usage
result = subtract_tool.invoke("100 25 15")
print(result)  # Output: {'result': 60} (100 - 25 - 15)
```

### Example 4: Power/Exponent Tool

```python
def power_tool(inputs: str) -> dict:
    """Calculates base raised to exponent."""
    numbers = [int(x) for x in inputs.replace(",", "").split() if x.isdigit()]
    if len(numbers) != 2:
        raise ValueError("Power tool requires exactly two numbers")
    return {"result": numbers[0] ** numbers[1]}

power = Tool(
    name="PowerTool",
    func=power_tool,
    description="Calculates base raised to exponent power. Format: 'base exponent'"
)

# Usage
result = power.invoke("2 8")
print(result)  # Output: {'result': 256} (2^8)
```

### Example 5: Division Tool

```python
def divide_numbers(inputs: str) -> dict:
    """Divides numbers sequentially with error handling."""
    try:
        numbers = [float(x) for x in inputs.replace(",", "").split() 
                   if x.replace('.', '').replace('-', '').isdigit()]
        if len(numbers) < 2:
            return {"error": "At least two numbers required"}
        
        result = numbers[0]
        for num in numbers[1:]:
            if num == 0:
                return {"error": "Cannot divide by zero"}
            result /= num
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

divide_tool = Tool(
    name="DivideTool",
    func=divide_numbers,
    description="Divides numbers sequentially. Handles division by zero."
)

# Usage
result = divide_tool.invoke("100 5 2")
print(result)  # Output: {'result': 10.0} (100 / 5 / 2)
```

## 🔄 Multi-Step Queries

### Example 6: Using Agent for Complex Queries

```python
from langchain_ollama import ChatOllama
from langchain.agents import initialize_agent, AgentType

# Setup
llm = ChatOllama(model='llama3', url='http://localhost:11434')
tools = [add_tool, mult_tool, subtract_tool]

agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)

# Complex query
query = "Add 25 and 15, then multiply the result by 2"
result = agent.invoke(query)
print(result['output'])  # Output: "80"

# The agent will:
# 1. Use AddTool: 25 + 15 = 40
# 2. Use MultTool: 40 * 2 = 80
```

### Example 7: Multi-Operation Chain

```python
# Query with multiple operations
query = "Calculate 10 plus 20, subtract 5, then multiply by 3"
result = agent.invoke(query)
print(result['output'])  # Output: "75"

# Steps:
# 1. AddTool: 10 + 20 = 30
# 2. SubtractTool: 30 - 5 = 25
# 3. MultTool: 25 * 3 = 75
```

### Example 8: Power and Addition

```python
tools = [add_tool, power]
agent = initialize_agent(tools, llm, AgentType.ZERO_SHOT_REACT_DESCRIPTION)

query = "What is 2 to the power of 5, plus 10?"
result = agent.invoke(query)
print(result['output'])  # Output: "42"

# Steps:
# 1. PowerTool: 2^5 = 32
# 2. AddTool: 32 + 10 = 42
```

## 🎨 Custom Tool Examples

### Example 9: Factorial Tool

```python
def factorial(inputs: str) -> dict:
    """Calculates factorial of a number."""
    try:
        n = int(inputs.strip())
        if n < 0:
            return {"error": "Factorial not defined for negative numbers"}
        if n > 20:
            return {"error": "Number too large (max 20)"}
        
        result = 1
        for i in range(1, n + 1):
            result *= i
        return {"result": result}
    except ValueError:
        return {"error": "Invalid input"}

factorial_tool = Tool(
    name="FactorialTool",
    func=factorial,
    description="Calculates factorial of a number (0-20)"
)

# Usage
result = factorial_tool.invoke("5")
print(result)  # Output: {'result': 120}
```

### Example 10: Square Root Tool

```python
import math

def square_root(inputs: str) -> dict:
    """Calculates square root of a number."""
    try:
        number = float(inputs.strip())
        if number < 0:
            return {"error": "Cannot calculate square root of negative number"}
        result = math.sqrt(number)
        return {"result": result}
    except ValueError:
        return {"error": "Invalid input"}

sqrt_tool = Tool(
    name="SquareRootTool",
    func=square_root,
    description="Calculates square root of a number"
)

# Usage
result = sqrt_tool.invoke("16")
print(result)  # Output: {'result': 4.0}
```

### Example 11: Modulo Tool

```python
def modulo(inputs: str) -> dict:
    """Calculates modulo (remainder) of division."""
    try:
        numbers = [int(x) for x in inputs.split() if x.isdigit()]
        if len(numbers) != 2:
            return {"error": "Exactly two numbers required"}
        if numbers[1] == 0:
            return {"error": "Cannot divide by zero"}
        return {"result": numbers[0] % numbers[1]}
    except Exception as e:
        return {"error": str(e)}

modulo_tool = Tool(
    name="ModuloTool",
    func=modulo,
    description="Calculates remainder of division. Format: 'dividend divisor'"
)

# Usage
result = modulo_tool.invoke("17 5")
print(result)  # Output: {'result': 2}
```

### Example 12: Average Tool

```python
def average(inputs: str) -> dict:
    """Calculates average of numbers."""
    numbers = [float(x) for x in inputs.replace(",", "").split() 
               if x.replace('.', '').replace('-', '').isdigit()]
    if not numbers:
        return {"error": "No valid numbers found"}
    result = sum(numbers) / len(numbers)
    return {"result": result}

average_tool = Tool(
    name="AverageTool",
    func=average,
    description="Calculates average (mean) of a list of numbers"
)

# Usage
result = average_tool.invoke("10 20 30 40 50")
print(result)  # Output: {'result': 30.0}
```

## 🚀 Advanced Use Cases

### Example 13: Statistical Toolkit

```python
import statistics

def median(inputs: str) -> dict:
    """Calculates median of numbers."""
    numbers = [float(x) for x in inputs.split() if x.replace('.','').isdigit()]
    if not numbers:
        return {"error": "No valid numbers"}
    return {"result": statistics.median(numbers)}

def std_dev(inputs: str) -> dict:
    """Calculates standard deviation."""
    numbers = [float(x) for x in inputs.split() if x.replace('.','').isdigit()]
    if len(numbers) < 2:
        return {"error": "At least 2 numbers required"}
    return {"result": statistics.stdev(numbers)}

median_tool = Tool(
    name="MedianTool",
    func=median,
    description="Calculates median of numbers"
)

stdev_tool = Tool(
    name="StdDevTool",
    func=std_dev,
    description="Calculates standard deviation of numbers"
)

# Create statistical agent
stat_tools = [average_tool, median_tool, stdev_tool]
stat_agent = initialize_agent(stat_tools, llm, AgentType.ZERO_SHOT_REACT_DESCRIPTION)

# Usage
result = stat_agent.invoke("What is the average and median of 5, 10, 15, 20, 25?")
print(result['output'])
```

### Example 14: Temperature Converter

```python
def celsius_to_fahrenheit(inputs: str) -> dict:
    """Converts Celsius to Fahrenheit."""
    try:
        celsius = float(inputs.strip())
        fahrenheit = (celsius * 9/5) + 32
        return {"result": fahrenheit}
    except ValueError:
        return {"error": "Invalid temperature"}

def fahrenheit_to_celsius(inputs: str) -> dict:
    """Converts Fahrenheit to Celsius."""
    try:
        fahrenheit = float(inputs.strip())
        celsius = (fahrenheit - 32) * 5/9
        return {"result": celsius}
    except ValueError:
        return {"error": "Invalid temperature"}

c_to_f_tool = Tool(
    name="CelsiusToFahrenheit",
    func=celsius_to_fahrenheit,
    description="Converts temperature from Celsius to Fahrenheit"
)

f_to_c_tool = Tool(
    name="FahrenheitToCelsius",
    func=fahrenheit_to_celsius,
    description="Converts temperature from Fahrenheit to Celsius"
)

# Usage
result = c_to_f_tool.invoke("25")
print(result)  # Output: {'result': 77.0}
```

### Example 15: Unit Converter

```python
def meters_to_feet(inputs: str) -> dict:
    """Converts meters to feet."""
    try:
        meters = float(inputs.strip())
        feet = meters * 3.28084
        return {"result": feet}
    except ValueError:
        return {"error": "Invalid input"}

def kilograms_to_pounds(inputs: str) -> dict:
    """Converts kilograms to pounds."""
    try:
        kg = float(inputs.strip())
        pounds = kg * 2.20462
        return {"result": pounds}
    except ValueError:
        return {"error": "Invalid input"}

m_to_ft_tool = Tool(
    name="MetersToFeet",
    func=meters_to_feet,
    description="Converts meters to feet"
)

kg_to_lb_tool = Tool(
    name="KilogramsToPounds",
    func=kilograms_to_pounds,
    description="Converts kilograms to pounds"
)

# Create conversion agent
conversion_tools = [m_to_ft_tool, kg_to_lb_tool, c_to_f_tool, f_to_c_tool]
converter_agent = initialize_agent(
    conversion_tools, 
    llm, 
    AgentType.ZERO_SHOT_REACT_DESCRIPTION
)

# Usage
result = converter_agent.invoke("Convert 100 meters to feet")
print(result['output'])
```

## ⚠️ Error Handling Examples

### Example 16: Robust Division with Error Handling

```python
def safe_divide(inputs: str) -> dict:
    """Division with comprehensive error handling."""
    try:
        # Extract numbers
        parts = inputs.replace(",", "").split()
        numbers = []
        
        for part in parts:
            try:
                numbers.append(float(part))
            except ValueError:
                continue
        
        # Validate input
        if len(numbers) < 2:
            return {
                "error": "At least two numbers required for division",
                "received": len(numbers)
            }
        
        # Perform division
        result = numbers[0]
        for i, num in enumerate(numbers[1:], 1):
            if num == 0:
                return {
                    "error": f"Division by zero at position {i+1}",
                    "partial_result": result
                }
            result /= num
        
        return {"result": round(result, 6)}
        
    except Exception as e:
        return {"error": f"Unexpected error: {str(e)}"}

safe_divide_tool = Tool(
    name="SafeDivideTool",
    func=safe_divide,
    description="Safely divides numbers with error handling"
)

# Test cases
print(safe_divide_tool.invoke("100 5 2"))      # Success
print(safe_divide_tool.invoke("100 0"))        # Division by zero
print(safe_divide_tool.invoke("100"))          # Not enough numbers
print(safe_divide_tool.invoke("abc def"))      # Invalid input
```

### Example 17: Input Validation

```python
def validated_power(inputs: str) -> dict:
    """Power calculation with validation."""
    try:
        numbers = [float(x) for x in inputs.split() if x.replace('.','').replace('-','').isdigit()]
        
        if len(numbers) != 2:
            return {
                "error": "Exactly two numbers required (base and exponent)",
                "received": len(numbers)
            }
        
        base, exponent = numbers
        
        # Validate ranges
        if abs(base) > 1000:
            return {"error": "Base too large (max ±1000)"}
        if abs(exponent) > 100:
            return {"error": "Exponent too large (max ±100)"}
        
        # Calculate
        result = base ** exponent
        
        # Check for overflow
        if abs(result) > 1e308:
            return {"error": "Result too large (overflow)"}
        
        return {"result": result}
        
    except OverflowError:
        return {"error": "Calculation resulted in overflow"}
    except Exception as e:
        return {"error": f"Error: {str(e)}"}

validated_power_tool = Tool(
    name="ValidatedPowerTool",
    func=validated_power,
    description="Calculates power with input validation"
)
```

## 🔗 Integration Examples

### Example 18: Combining with Wikipedia

```python
from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper

# Create Wikipedia tool
wikipedia = WikipediaQueryRun(
    api_wrapper=WikipediaAPIWrapper()
)

# Combine with math tools
all_tools = [add_tool, mult_tool, wikipedia]
combined_agent = initialize_agent(
    all_tools,
    llm,
    AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)

# Use both types of tools
result = combined_agent.invoke(
    "What is the population of Tokyo? Then multiply it by 2."
)
print(result['output'])
```

### Example 19: Complete Math Assistant

```python
# Create comprehensive math toolkit
math_tools = [
    add_tool,
    mult_tool,
    subtract_tool,
    divide_tool,
    power,
    factorial_tool,
    sqrt_tool,
    modulo_tool,
    average_tool
]

# Initialize agent
math_assistant = initialize_agent(
    math_tools,
    llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
    max_iterations=10
)

# Complex queries
queries = [
    "What is the factorial of 6?",
    "Calculate the average of 12, 18, 24, 30",
    "What is 2 to the power of 10, divided by 4?",
    "Find the square root of 144, then add 5"
]

for query in queries:
    print(f"\nQuery: {query}")
    result = math_assistant.invoke(query)
    print(f"Answer: {result['output']}")
```

## 📚 Best Practices

### Example 20: Tool Design Pattern

```python
def create_math_tool(name: str, operation: callable, description: str) -> Tool:
    """Factory function for creating math tools."""
    
    def tool_function(inputs: str) -> dict:
        try:
            numbers = [float(x) for x in inputs.split() 
                      if x.replace('.','').replace('-','').isdigit()]
            if not numbers:
                return {"error": "No valid numbers found"}
            result = operation(numbers)
            return {"result": result}
        except Exception as e:
            return {"error": str(e)}
    
    return Tool(
        name=name,
        func=tool_function,
        description=description
    )

# Create tools using factory
sum_tool = create_math_tool(
    "SumTool",
    lambda nums: sum(nums),
    "Calculates sum of numbers"
)

product_tool = create_math_tool(
    "ProductTool",
    lambda nums: math.prod(nums),
    "Calculates product of numbers"
)

max_tool = create_math_tool(
    "MaxTool",
    lambda nums: max(nums),
    "Finds maximum value"
)

min_tool = create_math_tool(
    "MinTool",
    lambda nums: min(nums),
    "Finds minimum value"
)
```

## 🎓 Learning Path

1. **Start with Basic Examples** (1-5): Learn individual tools
2. **Progress to Multi-Step** (6-8): Understand agent orchestration
3. **Create Custom Tools** (9-12): Build your own functionality
4. **Explore Advanced Use Cases** (13-15): Complex applications
5. **Master Error Handling** (16-17): Robust implementations
6. **Integrate Systems** (18-19): Combine multiple capabilities

## 🔗 Related Documentation

- [API Documentation](API.md)
- [Setup Guide](SETUP.md)
- [Contributing Guide](../CONTRIBUTING.md)

---

For more examples or to contribute your own, please see our [Contributing Guide](../CONTRIBUTING.md).