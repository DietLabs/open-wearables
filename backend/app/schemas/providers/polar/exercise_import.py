from pydantic import BaseModel, Field, field_validator


class HeartRateJSON(BaseModel):
    average: int | None = None
    maximum: int | None = None


class HRSamplesJSON(BaseModel):
    recording_rate: int = Field(alias="recording-rate")
    sample_type: str = Field(alias="sample-type")
    data: str


class HRZoneJSON(BaseModel):
    index: int
    lower_limit: int = Field(alias="lower-limit")
    upper_limit: int = Field(alias="upper-limit")
    in_zone: str = Field(alias="in-zone")


class RoutePointJSON(BaseModel):
    latitude: float | None = None
    longitude: float | None = None
    time: str | None = None
    satellites: int | None = None
    fix: int | None = None


class TrainingLoadProJSON(BaseModel):
    date: str | None = None
    cardio_load: int | None = Field(None, alias="cardio-load")
    muscle_load: int | None = Field(None, alias="muscle-load")
    perceived_load: int | None = Field(None, alias="perceived-load")
    cardio_load_interpretation: str | None = Field(None, alias="cardio-load-interpretation")
    muscle_load_interpretation: str | None = Field(None, alias="muscle-load-interpretation")
    perceived_load_interpretation: str | None = Field(None, alias="perceived-load-interpretation")
    user_rpe: str | None = Field(None, alias="user-rpe")

    @field_validator("cardio_load", "muscle_load", "perceived_load", mode="before")
    @classmethod
    def _round_float_to_int(cls, value: object) -> object:
        # Polar returns fractional load scores (e.g. cardio-load 6.26022),
        # but we only store whole numbers — round instead of failing validation.
        if isinstance(value, float):
            return round(value)
        return value


class ExerciseJSON(BaseModel):
    id: str
    upload_time: str | None = None
    polar_user: str | None = None
    device: str
    device_id: str | None = None

    sport: str
    detailed_sport_info: str | None = None

    start_time: str
    start_time_utc_offset: int
    duration: str

    calories: int | None = None
    distance: int | None = None
    heart_rate: HeartRateJSON | None = None
    heart_rate_zones: list[HRZoneJSON] | None = None

    training_load: float | None = None
    training_load_pro: TrainingLoadProJSON | None = None
    has_route: bool | None = None

    fat_percentage: int | None = None
    carbohydrate_percentage: int | None = None
    protein_percentage: int | None = None
    running_index: int | None = Field(None, alias="running-index")

    club_id: int | None = None
    club_name: str | None = None

    samples: list[HRSamplesJSON] | None = None
    route: list[RoutePointJSON] | None = None

    @field_validator(
        "calories",
        "distance",
        "fat_percentage",
        "carbohydrate_percentage",
        "protein_percentage",
        "running_index",
        mode="before",
    )
    @classmethod
    def _round_float_to_int(cls, value: object) -> object:
        # Polar returns fractional values for these fields (e.g. fat_percentage 19.6816),
        # but we only store whole numbers — round instead of failing validation.
        if isinstance(value, float):
            return round(value)
        return value
