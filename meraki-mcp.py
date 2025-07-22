# meraki_server_requests.py

import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from fastmcp import FastMCP
import requests
import urllib3
import json

# --- Print a version identifier to the logs ---
print("--- Running Script Version: USER_REQUESTS_BASED ---", file=sys.stderr)

# --- Find and Load the .env File ---
script_location = Path(__file__).resolve().parent
env_file_path = script_location / '.env'
load_dotenv(dotenv_path=env_file_path)

# --- Load Credentials ---
MERAKI_API_KEY = os.getenv("MERAKI_API_KEY")
MERAKI_ORG_ID = os.getenv("MERAKI_ORG_ID")

# --- Disable SSL Warnings ---
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# --- Your MerakiMCPConnector Class ---
class MerakiMCPConnector:
    def __init__(self, api_key: str, org_id: str = None):
        self.api_key = api_key
        self.org_id = org_id
        self.base_url = "https://api.meraki.com/api/v1"
        self.workflows_base_url = "https://us.workflows.meraki.com/api/v1"
        self.headers = {
            "X-Cisco-Meraki-API-Key": api_key,
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        self.session = requests.Session()
        self.session.headers.update(self.headers)
        self.session.verify = False

    def get_organizations(self) -> list:
        """Gets a list of organizations."""
        url = f"{self.base_url}/organizations"
        response = self.session.get(url)
        response.raise_for_status()
        return response.json()

    def get_organization_networks(self) -> list:
        """Gets networks for the configured organization."""
        if not self.org_id:
            raise ValueError("MERAKI_ORG_ID is required for this operation.")
        url = f"{self.base_url}/organizations/{self.org_id}/networks"
        response = self.session.get(url)
        response.raise_for_status()
        return response.json()

    def list_workflows(self) -> list:
        """Lists available workflows, trying different auth methods."""
        if not self.org_id:
            raise ValueError("MERAKI_ORG_ID is required for this operation.")
        
        url = f"{self.workflows_base_url}/organizations/{self.org_id}/workflows"
        
        # Try Bearer token auth first
        try:
            headers = {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}
            response = self.session.get(url, headers=headers)
            if response.status_code != 401:
                response.raise_for_status()
                return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Bearer auth failed, trying API key. Error: {e}", file=sys.stderr)

        # Fallback to API Key auth
        response = self.session.get(url)
        response.raise_for_status()
        return response.json()

# --- Create the MCP Server ---
mcp = FastMCP(
    name="Meraki Direct API MCP",
    instructions="A robust MCP server for Meraki using direct requests."
)

# --- Helper Function to Initialize the Connector ---
def get_connector():
    if not MERAKI_API_KEY:
        raise ValueError("Missing MERAKI_API_KEY in .env file.")
    return MerakiMCPConnector(MERAKI_API_KEY, MERAKI_ORG_ID)

# --- Define the Tools ---
@mcp.tool()
def get_organizations() -> list:
    """Retrieves a list of all organizations accessible by the API key."""
    try:
        connector = get_connector()
        return connector.get_organizations()
    except Exception as e:
        print(f"Error in get_organizations tool: {e}", file=sys.stderr)
        return [{"error": str(e)}]

@mcp.tool()
def get_organization_networks() -> list:
    """Retrieves a list of all networks within the configured organization."""
    try:
        connector = get_connector()
        return connector.get_organization_networks()
    except Exception as e:
        print(f"Error in get_organization_networks tool: {e}", file=sys.stderr)
        return [{"error": str(e)}]

@mcp.tool()
def list_workflows() -> list:
    """Retrieves a list of available Meraki Workflows."""
    try:
        connector = get_connector()
        return connector.list_workflows()
    except Exception as e:
        print(f"Error in list_workflows tool: {e}", file=sys.stderr)
        return [{"error": str(e)}]

# --- Main Execution Block ---
if __name__ == "__main__":
    mcp.run()
