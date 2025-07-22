# Meraki MCP Server

Meraki MCP is a Python-based MCP (Model Context Protocol) server for Cisco's Meraki Cloud Platform. This server provides comprehensive tools for querying the Meraki Dashboard API to discover, monitor, and manage your cloud-managed network infrastructure including wireless, switching, security, and SD-WAN.

## Features

* **Organization Management** - Discover and manage all organizations accessible by your API key
* **Network Discovery** - Retrieve and manage all networks within your organization
* **Device Management** - Monitor and configure Meraki devices across all product lines
* **Workflow Automation** - Access and execute available Meraki Workflows for common tasks
* **Multi-product Support** - Unified access to wireless, switching, security appliance, and camera products
* **Cloud-native Management** - Leverage Meraki's cloud-first architecture for simplified operations
* **Simple and extensible MCP server implementation**

## Installation

1. Clone the repository:

```bash
git clone https://github.com/your-repo/meraki-mcp.git
cd meraki-mcp
```

2. Create a virtual environment and activate it:

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

## Configuration

1. Copy the example environment file:

```bash
cp .env-example .env
```

2. Update the `.env` file with your Meraki API credentials:

```env
MERAKI_API_KEY="your-meraki-api-key-here"
MERAKI_ORG_ID="your-organization-id"  # Optional: will auto-discover if not specified
```

## Usage With Claude Desktop Client

1. Configure Claude Desktop to use this MCP server:
   * Open Claude Desktop
   * Go to Settings > Developer > Edit Config
   * Add the following configuration to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "Meraki_MCP": {
      "command": "/path/to/your/meraki-mcp/.venv/bin/fastmcp",
      "args": [
        "run",
        "/path/to/your/meraki-mcp/meraki-mcp.py"
      ]
    }
  }
}
```

   * Replace the paths above to reflect your local environment

2. Restart Claude Desktop

3. Interact with Claude Desktop - you can now ask questions about your Meraki deployment such as:
   * "What organizations do I have access to?"
   * "Show me all networks in my organization"
   * "What Meraki workflows are available?"
   * "List all devices across my networks"
   * "What's the status of my wireless access points?"

## Available Functions

The MCP server provides the following functions:

### Organization Management
- `get_organizations` - Retrieve a list of all organizations accessible by the API key

### Network Management
- `get_organization_networks` - Retrieve a list of all networks within the configured organization

### Workflow Management
- `list_workflows` - Retrieve a list of available Meraki Workflows

## Meraki Product Support

This MCP server supports all Meraki product lines:

### Wireless (MR Series)
- Access points and wireless infrastructure
- Client connectivity and performance monitoring
- RF optimization and analytics

### Switching (MS Series)
- Layer 2/3 switches
- Port configuration and monitoring
- VLAN and network segmentation

### Security Appliances (MX Series)
- Next-generation firewalls
- SD-WAN and VPN connectivity
- Security policy management

### Cameras (MV Series)
- Cloud-managed security cameras
- Video analytics and monitoring
- Smart camera features

### Sensors (MT Series)
- Environmental monitoring
- IoT device management
- Sensor data analytics

## API Key Setup

To use the Meraki MCP server, you'll need to generate an API key:

1. Log into your Meraki Dashboard
2. Navigate to Organization > Settings > Dashboard API access
3. Enable API access for your organization
4. Generate a new API key
5. Copy the API key to your `.env` file

**Important**: API keys inherit the permissions of the user who created them.

## Organization Discovery

The MCP server can automatically discover your organization:
- If `MERAKI_ORG_ID` is not specified, it will use the first organization returned by the API
- For multi-organization setups, specify the exact Organization ID
- You can find Organization IDs in the Meraki Dashboard URL or via the `get_organizations` function

## Meraki Workflows

Meraki Workflows provide pre-built automation for common network management tasks:
- Device provisioning and configuration
- Network monitoring and alerting
- Compliance and security auditing
- Performance optimization

Use the `list_workflows` function to see available workflows in your organization.

## Rate Limiting

Meraki API has rate limits that vary by endpoint:
- Most endpoints: 5 requests per second per organization
- Some endpoints have higher or lower limits
- The MCP server automatically handles rate limiting and retries

## Security Considerations

* Store your Meraki API key securely in the `.env` file
* Never commit API keys to version control
* API keys provide full access to your Meraki organization
* Use dedicated service accounts when possible
* Regularly audit API key usage in the Meraki Dashboard
* Rotate API keys periodically for enhanced security
* Monitor API activity through Dashboard audit logs

## Troubleshooting

If you encounter issues:

1. **Authentication Errors**:
   - Verify your API key is correct and active
   - Check if API access is enabled for your organization
   - Ensure the user account associated with the API key is active

2. **Permission Errors**:
   - Verify the user has appropriate admin permissions
   - Check if the API key has access to the requested organization
   - Ensure network-level permissions are configured correctly

3. **Rate Limiting**:
   - Monitor your API usage in the Meraki Dashboard
   - The server handles rate limiting automatically
   - Consider spreading requests over time for large operations

4. **Network/Organization Access**:
   - Verify the Organization ID is correct
   - Check if you have access to the specified networks
   - Ensure your account hasn't been restricted

## Meraki Dashboard Integration

The MCP server complements the Meraki Dashboard:
- Use for programmatic access to configuration and monitoring data
- Integrate with external systems and workflows
- Automate routine network management tasks
- Generate custom reports and analytics

## Multi-Organization Support

For MSPs and enterprises with multiple organizations:
- Each API key is associated with specific organizations
- Use separate configurations for different organizations
- Consider using organization-specific API keys for security
