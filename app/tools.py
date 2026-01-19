"""Agent tools for external operations"""

from datetime import datetime
from langchain.tools import tool


@tool
def calculate_metric(metric_name: str, values: str) -> str:
    """
    Calculate a business metric.
    
    Args:
        metric_name: Name of metric (aov, conversion_rate, clv, etc.)
        values: Comma-separated values needed for calculation
    """
    try:
        nums = [float(x.strip()) for x in values.split(",")]
        
        if metric_name.lower() == "aov":
            # Average Order Value = total revenue / number of orders
            if len(nums) >= 2:
                result = nums[0] / nums[1]
                return f"AOV: ${result:.2f}"
                
        elif metric_name.lower() == "conversion_rate":
            # Conversion Rate = (conversions / visitors) * 100
            if len(nums) >= 2:
                result = (nums[0] / nums[1]) * 100
                return f"Conversion Rate: {result:.2f}%"
                
        elif metric_name.lower() == "churn_rate":
            # Churn Rate = (customers lost / total customers) * 100
            if len(nums) >= 2:
                result = (nums[0] / nums[1]) * 100
                return f"Churn Rate: {result:.2f}%"
                
        return f"Calculated {metric_name} with values {values}"
        
    except Exception as e:
        return f"Error calculating metric: {str(e)}"


@tool
def get_current_time() -> str:
    """Get the current date and time"""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
