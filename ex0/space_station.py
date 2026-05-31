"""explicit data validation with Pydantic layout"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, ValidationError


class SpaceStation(BaseModel):
    """pydantic model verificator for space station logs"""
    station_id: str = Field(..., min_length=3, max_length=10)
    name: str = Field(..., ming_length=1, max_length=50)
    crew_size: int = Field(..., ge=1, le=20)
    power_level: float = Field(..., ge=0.0, le=100.0)
    oxygen_level: float = Field(..., ge=0.0, le=100.0)
    last_maintenance: datetime
    is_operational: bool = True
    notes: Optional[str] = Field(None, max_length=200)


def main() -> None:
    """executing invalid and valid states"""
    print("Space Station Data Validation")
    print("=====================================")
    # valid space station log
    try:
        valid_station = SpaceStation(
                station_id="ISO01",
                name="International Space Station",
                crew_size=6,
                power_level=85.5,
                oxygen_level=92.3,
                last_maintenance="2026-05-30T12:00:00",
                is_operationnal=True,
                notes="All observation arrays running normally."
                )
        print("Valid station created:")
        print(f"ID: {valid_station.station_id}")
        print(f"Name: {valid_station.name}")
        print(f"Crew: {valid_station.crew_size} people")
        print(f"Power: {valid_station.power_level}%")
        print(f"Oxygen: {valid_station.oxygen_level}%")
        status_str = "Operational" if valid_station.is_operational\
            else "Offline"
        print(f"Status: {status_str}")
    except ValidationError as e:
        print(f"Unexpected initialization error: {e}")
    print("=========================================")
    print("Expected validation error:")
    try:
        SpaceStation(
                station_id="FAIL42",
                name="Overcrowded Hub",
                crew_size=25,
                power_level=42.0,
                oxygen_level=80.0,
                last_maintenance=datetime.now(),
                )
    except ValidationError as ve:
        # extracting localized error array block fields
        for error in ve.errors():
            print(error["msg"])


if __name__ == "__main__":
    main()
