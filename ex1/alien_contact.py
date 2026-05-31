"""enum to control allowed interaction modes and structural custom data"""

from datetime import datetime
from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field, ValidationError, model_validator


class ContactType(str, Enum):
    """enumeration of authorized tracking modes."""
    RADIO = "radio"
    VISUAL = "visual"
    PHYSICAL = "physical"
    TELEPATHIC = "telepathic"


class AlienContact(BaseModel):
    """Pydantic model verifying structural logs"""
    contact_id: str = Field(..., min_length=5, max_length=15)
    timestamp: datetime
    location: str = Field(..., min_length=3, max_length=100)
    contact_type: ContactType
    signal_strength: float = Field(..., ge=0.0, le=10.0)
    duration_minutes: int = Field(..., ge=1, le=1440)
    witness_count: int = Field(..., ge=1, le=100)
    message_received: Optional[str] = Field(None, max_length=500)
    is_verified: bool = False

    @model_validator(mode="after")
    def validate_business_rules(self) -> "AlienContact":
        """custom validation"""
        if not self.contact_id.startswith("AC"):
            raise ValueError("Contact ID must start with 'AC'")
        if self.contact_type == ContactType.PHYSICAL and not self.is_verified:
            raise ValueError("Physical contact reports must be verified")
        if self.contact_type == ContactType.TELEPATHIC\
                and self.witness_count < 3:
            raise ValueError(
                "Telephatic contact requires at least 3 wtinesses"
            )
        if self.signal_strength > 7.0 and not self.message_received:
            raise ValueError(
                "Strong signals (> 7.0) should include received messages"
            )
        return self


def main() -> None:
    print("Alien Contact Log Validation")
    print("====================================")
    try:
        valid_report = AlienContact(
                contact_id="AC_2024_001",
                timestamp="2024-05-30T22:15:00",
                location="Area 51, Nevada",
                contact_type=ContactType.RADIO,
                signal_strength=8.5,
                duration_minutes=45,
                witness_count=5,
                message_received="Greetings from Zeta Reticuli",
                is_verified=False,
                )
        print("Valid contact report:")
        print(f"ID: {valid_report.contact_id}")
        print(f"Type: {valid_report.contact_type.value}")
        print(f"Location: {valid_report.location}")
        print(f"Signal: {valid_report.signal_strength}/10")
        print(f"Duration: {valid_report.duration_minutes} minutes")
        print(f"Witnesses: {valid_report.witness_count}")
        print(f"Message: '{valid_report.message_received}'")
    except ValidationError as e:
        print(f"Unexpected validation failure: {e}")
    print("\n======================================")
    print("Expected validation error:")
    try:
        AlienContact(
                contact_id="AC_TELE_FAIL",
                timestamp=datetime.now(),
                location="Pluto Station Alpha",
                contact_type=ContactType.TELEPATHIC,
                signal_strength=4.2,
                duration_minutes=10,
                witness_count=2,
                is_verified=True,
                )
    except ValidationError as ve:
        for error in ve.errors():
            print(error["msg"])


if __name__ == "__main__":
    main()
