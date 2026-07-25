# Webull SDK Development Specification

## New API Interface Development Process

When adding a new API interface, the following steps must be completed:

### 1. Request Class (Request)
- File path: `webull/data/request/` or `webull/trade/request/`
- Inherit from `ApiRequest`
- Define the API path, version, and HTTP method in `__init__`
- **Must specify the `version='v2'` parameter**
- Provide `set_xxx()` methods to set parameters
- Use `add_query_param()` for GET requests
- Use `add_body_params()` for POST requests

#### Request Class Example
```python
class GetExampleRequest(ApiRequest):
    def __init__(self):
        ApiRequest.__init__(self, "/openapi/xxx/example", version="v2", method="GET", query_params={})
```

### 2. Business Implementation Class
- File path: `webull/data/quotes/` or `webull/trade/trade/`
- Accept `api_client` as a constructor parameter
- Each method corresponds to one API interface
- Create the corresponding Request object, set its parameters, and call `self.client.get_response(request)`
- Write detailed docstring documentation

### 3. Client Registration
- Register the new business class in `DataClient` or `TradeClient`
- Add the corresponding import statement

### 4. Sample Code (Required)
- File path: the corresponding module folder under `samples/`
- Include a complete usage example
- Include necessary comments and explanations

### 5. Commit Code (Required)
- After completing all the steps above, the code must be committed as a git commit
- The commit message must be written in English

## Code Style

- Use the Apache 2.0 license header
- `# coding=utf-8` encoding declaration
- Detailed docstring documentation
- Perform parameter validation in the set methods
- **Code comments must be in English; Chinese comments are not allowed**

## Module Organization Principles

- Related interfaces should be placed in the same business class
- Different types of interfaces (e.g., news, quotes, trading) should be managed separately
- When creating a new module, also create the corresponding sample code directory
