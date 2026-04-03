# [The Communication Protocol](https://huggingface.co/learn/mcp-course/unit1/communication-protocol)

MCP defines a standardized communication protocol that enables Clients and Servers to exchange messages in a consistent, predictable way.

## JSON-RPC: The Foundation

At its core, MCP uses [JSON-RPC 2.0](https://www.jsonrpc.org/specification) as the message format for all communication between Clients and Servers. JSON-RPC is a lightweight remote procedure call protocol encoded in JSON.

## 1. Requests

Sent from Client to Server to initiate an operation. A Request message includes:

* A unique identifier (id)
* The method name to invoke (e.g., tools/call)
* Parameters for the method (if any)

Example request:

```jsonrpc
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/call",
  "params": {
    "name": "weather",
    "arguments": {
      "location": "San Francisco"
    }
  }
}
```
