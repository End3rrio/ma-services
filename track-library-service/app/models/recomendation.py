from uuid import UUID
from pydantic import BaseModel, ConfigDict


class Recomendation(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    user_id: UUID
    recommended_track_id: UUID

    def json(self):
        return {
            "user_id": str(self.user_id),
            "recommended_track_id": str(self.recommended_track_id),
        }


class CreateRecommendationRequest(BaseModel):
    user_id: UUID
    recommended_track_id: UUID
