from mcp.server.fastmcp import FastMCP
from typing import List


employee_leaves = {
    "E001": {"balance": 18, "history": ["2024-12-25", "2025-01-01"]},
    "E002": {"balance": 20, "history": []}
}

mcp = FastMCP("LeaveManager")

@mcp.tool()
def get_employee_leave_balance(employee_id: str) -> str:
    """
    Get the leave balance for a specific employee.
    
    Args:
        employee_id (str): The ID of the employee.
    
    Returns:
        int: The leave balance of the employee.
    """
    if employee_id in employee_leaves:
        return f'{employee_id} has {employee_leaves[employee_id]["balance"]} leave days remaining.'
    else:
        return "Employee ID not found."

# Abhi: Tool to apply leave
@mcp.tool()
def apply_leave(employee_id: str, leave_dates: List[str]) -> str:
    """
    Apply leave for specific dates (e.g., ["2025-04-17", "2025-05-01"])
    """
    if employee_id not in employee_leaves:
        return "Employee ID not found."

    requested_days = len(leave_dates)
    available_balance = employee_leaves[employee_id]["balance"]

    if available_balance < requested_days:
        return f"Insufficient leave balance. You requested {requested_days} day(s) but have only {available_balance}."

    # Deduct balance and add to history
    employee_leaves[employee_id]["balance"] -= requested_days
    employee_leaves[employee_id]["history"].extend(leave_dates)

    return f"Leave applied for {requested_days} day(s). Remaining balance: {employee_leaves[employee_id]['balance']}."

# Resource: Leave history
@mcp.tool()
def get_leave_history(employee_id: str) -> str:
    """Get leave history for the employee"""
    data = employee_leaves.get(employee_id)
    if data:
        history = ', '.join(data['history']) if data['history'] else "No leaves taken."
        return f"Leave history for {employee_id}: {history}"
    return "Employee ID not found."


if __name__ == "__main__":
    mcp.run()