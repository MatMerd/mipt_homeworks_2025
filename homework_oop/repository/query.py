from dataclasses import dataclass
from typing import Dict, Any, Optional


@dataclass
class Query:
    sort_by: Optional[str] = None
    group_by: Optional[str] = None
    filters: Optional[Dict[str, Any]] = None
