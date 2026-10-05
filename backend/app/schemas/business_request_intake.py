"""Owner WP23 revision-2 contract: empty input and task-id-only output."""

from uuid import UUID

from pydantic import BaseModel, ConfigDict


class BusinessRequestInput(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)


class BusinessRequestOutput(BaseModel):
    task_id: UUID
