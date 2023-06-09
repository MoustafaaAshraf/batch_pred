from pathlib import Path
from typing import Optional

from kfp.v2.dsl import component

from src.components.dependencies import LOGURU, PYTHON


@component(
    base_image=PYTHON,
    packages_to_install=[LOGURU],
    output_component_file=str(Path(__file__).with_suffix(".yaml")),
)
def get_current_time(
    timestamp: Optional[str] = None,
    format_str: Optional[str] = None,
    subtract_days: int = 0,
) -> str:
    """Create timestamp for filtering the data in the pipelines.

    If `timestamp` is empty, return the current time (UTC+0) in ISO 6801 format.
    Otherwise, return the formatted `timestamp`. If `timestamp` is provided, it
    must follow ISO 6801 format (e.g. 2023-05-21T19:00:00). The date part is
    mandatory while any missing part in the time part will be regarded as zero.

    Args:
        timestamp (Optional[str], optional): Timestamp in ISO 6801 format.
            Defaults to None.
        format_str (Optional[str], optional): Formatting string for the output,
            must be compatible with datetime. Defaults to None.
        subtract_days (int, optional): Number of days to subtract from the
            current timestamp. Only used if `timestamp` is None. Defaults to 0.

    Returns:
        str: Formatted input timestamp is ISO 6801 format
    """
    from datetime import datetime, timedelta, timezone

    from loguru import logger

    if not timestamp:
        dt = datetime.now(timezone.utc) - timedelta(days=subtract_days)

        if not format_str:
            return dt.isoformat()
        else:
            return dt.strftime(format=format_str)

    else:
        try:
            dt = datetime.fromisoformat(timestamp)
            logger.info(f"Timestamp in ISO 8601 format: {dt}.")
            if not format_str:
                return dt.isoformat()
            else:
                return dt.strftime(format=format_str)
        except ValueError:
            err = "Timestamp is not in the correct ISO 6801 format "
            logger.error(err)
            raise ValueError(err)
