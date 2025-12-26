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
    level_r: float = 1.0
    level_g: float = 1.0
    level_b: float = 1.0
    level_change_r: float = 0
    level_change_g: float = 0
    level_change_b: float = 0
    flat_r: int = 0
    flat_g: int = 0
    flat_b: int = 0
    x_factor_r: float = 1
    x_factor_g: float = 1
    x_factor_b: float = 1
    y_factor_r: float = 1
    y_factor_g: float = 1
    y_factor_b: float = 1
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
