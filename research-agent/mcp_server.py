from mcp.server.fastmcp import FastMCP
import random

mcp = FastMCP("support-agent-utils")


@mcp.tool()
def check_ticket_status(ticket_id: str) -> str:
    """
    Check the status of a customer support ticket.
    
    Use this tool when a user asks about the status of their existing ticket.
    
    Args:
        ticket_id: The ID of the ticket (e.g., "TKT-1234").
    """
    statuses = ["Open", "In Progress", "Waiting on Customer", "Resolved", "Closed"]
    # Mocking a response
    status = random.choice(statuses)
    return f"Ticket {ticket_id} is currently: {status}. Our team is working on it."


@mcp.tool()
def create_ticket(issue_description: str, priority: str = "Medium") -> str:
    """
    Create a new customer support ticket.
    
    Use this tool when a user wants to escalate an issue to a human or explicitly asks to open a ticket.
    
    Args:
        issue_description: A brief summary of the issue.
        priority: "Low", "Medium", "High", or "Critical". Defaults to "Medium".
    """
    # Mock ticket ID generation
    ticket_id = f"TKT-{random.randint(1000, 9999)}"
    return f"Successfully created ticket {ticket_id} with priority {priority}. A human agent will review it shortly."


if __name__ == "__main__":
    mcp.run(transport="stdio")