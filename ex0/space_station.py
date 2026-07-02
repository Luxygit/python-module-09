"""explicit data validation with Pydantic layout"""

from datetime import datetime
from pydantic import BaseModel, Field, ValidationError  # type: ignore


class SpaceStation(BaseModel):
    """pydantic model verificator for space station logs"""
    station_id: str = Field(..., min_length=3, max_length=10)
    name: str = Field(..., min_length=1, max_length=50)
    crew_size: int = Field(..., ge=1, le=20)
    power_level: float = Field(..., ge=0.0, le=100.0)
    oxygen_level: float = Field(..., ge=0.0, le=100.0)
    last_maintenance: datetime
    is_operational: bool = True
    notes: str | None = Field(default=None, max_length=200)


def main() -> None:
    """executing invalid and valid states"""
    print("Space Station Data Validation")
    print("=====================================")
    try:
        valid_station = SpaceStation(
                station_id="ISS001",
                name="International Space Station",
                crew_size=6,
                power_level=85.5,
                oxygen_level=92.3,
                last_maintenance="2024-06-23T12:00:00",
                notes="All observations OK."
                )
        status = "Operation" if valid_station.is_operational\
            else "Offline"
        print("Valid station created:")
        print(f"ID: {valid_station.station_id}")
        print(f"Name: {valid_station.name}")
        print(f"Crew: {valid_station.crew_size} people")
        print(f"Power: {valid_station.power_level}%")
        print(f"Oxygen: {valid_station.oxygen_level}%")
        print(f"Status: {status}")
        if valid_station.notes:
            print(f"Notes: {valid_station.notes}")
    except Exception as e:
        print(f"Unexpected initialization error: {e}")
    print("\n=========================================")
    print("Expected validation error:")
    try:
        SpaceStation(
                station_id="ISS002",
                name="Overcrowded Station",
                crew_size=25,
                power_level=50.0,
                oxygen_level=50.0,
                last_maintenance=datetime.now()
                )
    except ValidationError as e:
        for err in e.errors():
            print(err['msg'])


if __name__ == "__main__":
    main()
