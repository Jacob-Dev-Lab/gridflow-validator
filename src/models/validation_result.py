from dataclasses import dataclass


@dataclass
class ValidationResult:
    hour_label: str
    csv_value: int
    xml_value: int
    direction: str
    is_valid: bool

    def __str__(self):
        status = "MATCH ✅" if self.is_valid else "MISMATCH ❌"
        return (
            f"{status}\n"
            f"Hour: {self.hour_label}\n"
            f"CSV Value: {self.csv_value}\n"
            f"XML Value: {self.xml_value}\n"
            f"Direction: {self.direction}"
        )