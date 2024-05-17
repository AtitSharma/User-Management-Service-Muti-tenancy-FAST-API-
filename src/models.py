from datetime import datetime

import pytz
from sqlalchemy import Column, DateTime, event


class TimeStampMixin:
    """Timestamping mixin"""

    nepal_timezone = pytz.timezone("Asia/Kathmandu")
    created_at = Column(DateTime, default=datetime.now(nepal_timezone))
    created_at._creation_order = 9998
    updated_at = Column(DateTime, default=datetime.now(nepal_timezone))
    updated_at._creation_order = 9998

    @staticmethod
    def _updated_at(mapper, connection, target):
        target.updated_at = default = datetime.now(  # noqa
            TimeStampMixin.nepal_timezone
        )  # noqa F841

    @classmethod
    def __declare_last__(cls):
        event.listen(cls, "before_update", cls._updated_at)
