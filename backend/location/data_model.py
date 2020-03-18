from dataclasses import dataclass


@dataclass(frozen=True)
class Location:
    latitude: int
    longitude: int
