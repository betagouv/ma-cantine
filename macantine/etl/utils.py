import logging
from typing import Dict

logger = logging.getLogger(__name__)


def compute_percentage(valueKey, totalKey, ratio=False):
    """
    Compute a percentage (between 0 and 100) or a ratio (between 0 and 1).
    """
    if totalKey and valueKey:
        if totalKey > 0 and valueKey >= 0:
            if ratio:
                return float(valueKey / totalKey)
            return float(100 * valueKey / totalKey)


def format_geo_name(geo_code: int, geo_names: Dict[int, str]):
    """
    Format the name of a region or department from its code
    """
    if isinstance(geo_code, str) and geo_code not in ["978", "987", "975", "988"]:
        geo_name = geo_names[geo_code].split(" - ")[1].lstrip()
        return geo_name


def datetimes_to_str(df):
    date_columns = df.select_dtypes(include=["datetime64[ns, UTC]"]).columns
    for date_column in date_columns:
        df[date_column] = df[date_column].apply(lambda x: x.strftime("%Y-%m-%d %H:%M"))
    return df
