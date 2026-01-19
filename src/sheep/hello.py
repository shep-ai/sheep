```python
"""
A simple module to demonstrate adding a new file to the sheep package.
"""

def say_hello(name: str = "Sheep") -> str:
    """
    Returns a greeting message.
    """
    return f"Hello, {name}!"

if __name__ == "__main__":
    print(say_hello())
    print(say_hello("World"))
```