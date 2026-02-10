"""Agent tools for external operations"""

from datetime import datetime
from langchain.tools import tool
from config import logger_app


@tool
def calculate_metric(metric_name: str, values: str) -> str:
    """
    Compute an official business metric using the centralized metrics logic.

    This tool represents the company's authoritative metrics service.
    Product and strategy documents intentionally omit calculation formulas
    and defer all computations to this tool to ensure consistency.

    IMPORTANT:
    - The input values are assumed to be pre-aggregated outputs from data pipelines
      (e.g., totals, counts, retained revenue).
    - This tool should be used whenever a document explicitly references
      the "metrics service" or "official calculation".

    Args:
        metric_name: Name of the metric to compute.
            Supported values:
            - "nrr": Net Revenue Retention
            - "stam": Successful Transactions per Active Merchant
            - "payment_success_rate": Adjusted Payment Success Rate

        values: Comma-separated numeric values required for the metric.
            The expected inputs depend on the metric:
            - nrr: retained_revenue, starting_revenue
            - stam: successful_transactions, active_merchants
            - payment_success_rate: successful_payments, valid_payment_attempts

    Returns:
        A human-readable string containing the official computed metric.
    """
    logger_app.info(f"Tool 'calculate_metric' invoked: metric={metric_name}, values={values}")
    
    try:
        nums = [float(x.strip()) for x in values.split(",")]
        logger_app.debug(f"Parsed values: {nums}")

        metric = metric_name.lower()
        result = None

        if metric == "nrr":
            # Net Revenue Retention = retained revenue / starting revenue
            if len(nums) >= 2 and nums[1] != 0:
                result = (nums[0] / nums[1]) * 100
                output = f"Net Revenue Retention (NRR): {result:.2f}%"
                logger_app.info(f"Calculated NRR: {result:.2f}%")
                return output

        elif metric == "stam":
            # Successful Transactions per Active Merchant
            if len(nums) >= 2 and nums[1] != 0:
                result = nums[0] / nums[1]
                output = f"STAM: {result:.2f} successful transactions per merchant"
                logger_app.info(f"Calculated STAM: {result:.2f}")
                return output

        elif metric == "payment_success_rate":
            # Adjusted Payment Success Rate
            if len(nums) >= 2 and nums[1] != 0:
                result = (nums[0] / nums[1]) * 100
                output = f"Payment Success Rate (Adjusted): {result:.2f}%"
                logger_app.info(f"Calculated Payment Success Rate: {result:.2f}%")
                return output

        warning_msg = (
            f"Metric '{metric_name}' could not be computed. "
            "Please verify the metric name and input values."
        )
        logger_app.warning(f"Failed to compute metric '{metric_name}' with values {nums}")
        return warning_msg

    except Exception as e:
        error_msg = f"Error computing metric '{metric_name}': {str(e)}"
        logger_app.error(error_msg)
        return error_msg

@tool
def get_current_time() -> str:
    """Get the current date and time"""
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger_app.debug(f"Tool 'get_current_time' invoked: {current_time}")
    return current_time
