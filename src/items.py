from src.schemas.characterSchema import ItemInfo
from src.exceptions.mainExceptions import ItemNotFoundedError

HELMETS = {
	"leather_helmet": {"name": "Leather helmet", "type": "armor", "slot": "helmet", "defense": 2, "description": "The leather helmet is made from simple animal leather; it’s good for a start, but not very durable.", "max_stack": 1}
}

CHESTPLATES = {
	"leather_chestplate": {"name": "Leather chestplate", "type": "armor", "slot": "chestplate", "defense": 4, "description": "The leather breastplate is made from simple animal leather; it will protect you from cuts, but don’t rely on it too much — it’s not that durable.", "max_stack": 1}
}

LEGGINGS = {
	"leather_legging": {"name": "Leather legging", "type": "armor", "slot": "legging", "defense": 3, "description": "Leather leggings made from simple animal leather will protect you from cuts, but don’t rely on them too much — they’re not very durable, though they are warm.", "max_stack": 1}
}

BOOTS = {
	"leather_boot": {"name": "Leather boots", "type": "armor", "slot": "boot", "defense": 1, "description": "Leather boots, made from simple animal leather, warm.", "max_stack": 1}
}

HANDKINDS = {
	"iron_sword": {"name": "Iron sword", "type": "weapon", "two_hands": False, "damage": 5, "shell_type": None, "description": "The sword is sharp and durable enough to be used by most knights.", "max_stack": 1},

	"wooden_bow": {"name": "Wooden bow", "type": "weapon", "two_hands": True, "damage": 7, "shell_type": "arrow", "description": "For beginner archers, you should be careful, otherwise you might break or tear the string.", "max_stack": 1}
}

CONSUMABLES = {
	"health_potion": {"name": "Health potion", "type": "consumable", "recovery_type": "health", "recovery_value": 20, "damage": 0, "description": "A common potion that restores a small amount of health, a widely used remedy.", "max_stack": 12},
	"mana_potion": {"name": "Mana potion", "type": "consumable", "recovery_type": "mana", "recovery_value": 15, "damage": 0, "description": "A common mana potion, it helps mages for a long time, because it’s not easy to advance as a mage…", "max_stack": 12},
}

GADGETS = {
	"throw_knife": {"name": "Throwable knife", "type": "throw", "damage": 8, "description": "Good sharp knives that can be useful in battle, but they require accuracy.", "max_stack": 16},
}

SHELLS = {
	"wooden_arrow": {"name": "Wooden arrow", "type": "shell", "shell_type": "arrow", "damage": 2, "description": "The simplest arrow; unfortunately, such arrows won’t be able to penetrate iron...", "max_stack": 64}
}

ITEMS = {
	**HELMETS,
	**CHESTPLATES,
	**LEGGINGS,
	**BOOTS,
	**HANDKINDS,
	**CONSUMABLES,
	**GADGETS,
	**SHELLS
}

def get_item(item_id: str) -> ItemInfo:
    data = ITEMS.get(item_id)
    if data is None:
        raise ItemNotFoundedError(f"Item {item_id} not found")
    return ItemInfo(item_id=item_id, **data)