BASE_MAX_EXP = 300
EXP_POWER = 1.5

BASE_MAX_HEALTH = 100
HEALTH_PER_LEVEL = 15

BASE_MAX_STAMINA = 100
STAMINA_PER_LEVEL = 8

BASE_MAX_MANA = 100
MANA_PER_LEVEL = 10

MAX_LEVEL = 100


def calc_max_exp(level: int) -> int:
    return int(BASE_MAX_EXP * level ** EXP_POWER)


def calc_max_health(level: int) -> int:
    return BASE_MAX_HEALTH + HEALTH_PER_LEVEL * (level - 1)


def calc_max_stamina(level: int) -> int:
    return BASE_MAX_STAMINA + STAMINA_PER_LEVEL * (level - 1)


def calc_max_mana(level: int) -> int:
    return BASE_MAX_MANA + MANA_PER_LEVEL * (level - 1)