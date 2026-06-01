"""
nested Pydantic models and data relationships
to pass mypy properly
mypy --python-executable venv/bin/python3 *.py
"""

from datetime import datetime
from enum import Enum
from typing import List
from pydantic import BaseModel, Field, model_validator


class Rank(str, Enum):
    """authorized crew ranks"""
    CADET = "cadet"
    OFFICER = "officer"
    LIEUTENANT = "lieutenant"
    CAPTAIN = "captain"
    COMMANDER = "commander"


class CrewMember(BaseModel):
    """individual crew member model"""
    member_id: str = Field(..., min_length=3, max_length=10)
    name: str = Field(..., min_length=2, max_length=50)
    rank: Rank
    age: int = Field(..., ge=18, le=80)
    specialization: str = Field(..., min_length=3, max_length=30)
    years_experience: int = Field(..., ge=0, le=50)
    is_active: bool = True


class SpaceMission(BaseModel):
    """space mission model"""
    mission_id: str = Field(..., min_length=5, max_length=15)
    mission_name: str = Field(..., min_length=3, max_length=100)
    destination: str = Field(..., min_length=3, max_length=50)
    launch_date: datetime
    duration_days: int = Field(..., ge=1, le=3650)
    crew: List[CrewMember] = Field(..., min_length=1, max_length=12)
    mission_status: str = "planned"
    budget_millions: float = Field(..., ge=1.0, le=10000.0)
 
    @model_validator(mode='after')
    def validate_mission_safety(self) -> 'SpaceMission':
        """validates mission security"""
        if not self.mission_id.startswith('M'):
            raise ValueError("Mission ID must start with 'M'")
        if not all(member.is_active for member in self.crew):
            raise ValueError("All crew members must be active")
        has_leader = any(
                m.rank in (Rank.COMMANDER, Rank.CAPTAIN) for m in self.crew
                )
        if not has_leader:
            raise ValueError(
                    "Mission must have at least one Commander or Captain"
                    )
        if self.duration_days > 365:
            exp_crew = sum(1 for m in self.crew if m.years_experience >= 5)
            if (exp_crew / len(self.crew)) < 0.5:
                raise ValueError(
                        "Long missions (> 365 days) need 50% experience crew "
                        "(5+ years)"
                        )
        return self


def main() -> None:
    """testing valid and invalid configs"""
    print("Space Mission Crew Validation")
    print("====================================")
    leader = CrewMember(
            member_id="CMD01", name="Sarah Connor", rank=Rank.COMMANDER,
            age=40, specialization="Mission Command", years_experience=15
            )
    pilot = CrewMember(
            member_id="LT02", name="John Smith", rank=Rank.LIEUTENANT,
            age=32, specialization="Navigation", years_experience=6
            )
    engineer = CrewMember(
            member_id="OFF03", name="Alice Johnson", rank=Rank.OFFICER,
            age=28, specialization="Engineering", years_experience=4
            )
    try:
        valid_mission = SpaceMission(
                mission_id="M2024_MARS",
                mission_name="Mars Colony Establishment",
                destination="Mars",
                launch_date=datetime(2024, 10, 15, 12, 0),
                duration_days=900,
                crew=[leader, pilot, engineer],
                budget_millions=2500.0
                )
        print("Valid mission created:")
        print(f"Mission: {valid_mission.mission_name}")
        print(f"ID: {valid_mission.mission_id}")
        print(f"Destination: {valid_mission.destination}")
        print(f"Duration: {valid_mission.duration_days} days")
        print(f"Budget: ${valid_mission.budget_millions}M")
        print(f"Crew size: {len(valid_mission.crew)}")
        print("Crew members:")
        for member in valid_mission.crew:
            print(f"- {member.name} ({member.rank.value}) - "
                  f"{member.specialization}")
    except Exception as e:
        print(f"Unexpected error creating valid mission: {e}")
    print("\n=======================================")
    print("Expected validation error:")
    try:
        """creating invalid space mission"""
        SpaceMission(
                mission_id="M2024_FAIL",
                mission_name="Unled Expedition",
                destination="Moon",
                launch_date=datetime(2024, 12, 1),
                duration_days=30,
                crew=[pilot, engineer],
                budget_millions=150.0
                )
    except Exception as e:
        if hasattr(e, 'errors'):
            msg = e.errors()[0]['msg']
            if msg.startswith("Value error, "):
                msg = msg[13:]
            print(msg)
        else:
            print(e)


if __name__ == "__main__":
    main()
