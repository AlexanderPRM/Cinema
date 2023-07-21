import datetime

from pydantic import BaseModel, field_validator


class Subscribtion(BaseModel):
    title: str
    duration: int
    cost: int
    description: str
    discount: int = 0
    discount_duration: str | None = None

    @field_validator("discount_duration")
    def discount_duration_validate(cls, value):
        if value is not None:
            try:
                datetime.datetime.strptime(value, "%Y-%m-%d %H:%M:%S")
            except ValueError:
                raise ValueError(
                    "Discount duration not correct. \
                        Correct format: YEAR-MONTH-DAY HOUR:MINUTE:SECONDS"
                )
        return value
