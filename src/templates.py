from dataclasses import dataclass


@dataclass
class Template:
    width: int
    height: int
    initial_r: int
    initial_g: int
    initial_b: int
    velocity_r: float
    velocity_g: float
    velocity_b: float
    weight_r: float = 1.0
    weight_g: float = 1.0
    weight_b: float = 1.0
    turn_back_r: bool = False
    turn_back_g: bool = False
    turn_back_b: bool = False


template1 = Template(
    width=500,
    height=500,
    initial_r=255,
    initial_g=1,
    initial_b=100,
    velocity_r=-0.2,
    velocity_g=1,
    velocity_b=-1,
)
