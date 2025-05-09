import re
import json

with open('processing/new_magic_item_definitions.json', "r", encoding='utf-8') as file:
    item_definitions = json.load(file)

with open('processing/ddb_config.json', "r", encoding='utf-8') as file:
    config = json.load(file)

banned_types = ["Antimatter Rifle", 'Laser Rifle', 'Rifle, Automatic', 'Rifle, Hunting', 'Semiautomatic Pistol',
                "pistol", "Pistol", 'Musket', 'Revolver', 'Shotgun', 'Laser Pistol', 'Pistol, Automatic']
dmg_items = [
    item
    for item in item_definitions["data"]
    if any([source["sourceId"] == 146 for source in item["sources"]]) and
       item["magic"] and
       not item["isLegacy"] and
       item["type"] not in banned_types and
       "Firearm" not in item["name"] and
       item["rarity"] != "Varies"
]

remove_keys = ["isLegacy", "isCustomItem", "isContainer", "canBeAddedToInventory", "tags", "isPack", "cost",
               "stackable", "sourcePageNumber", "sourceId", "version", "isHomebrew", "capacityWeight", "snippet",
               "magic", "definitionKey", "weight", "weightMultiplier", "capacity", "bundleSize", "avatarUrl",
               "largeAvatarUrl", "grantedModifiers", "weaponBehaviors", "canEquip", "subType", "baseItemId",
               "strengthRequirement", "armorClass", "stealthCheck", "damage", "damageType", "fixedDamage",
               "attackType", "levelInfusionGranted", "armorTypeId", "gearTypeId", "properties", "groupedId",
               "baseTypeId", "entityTypeId", "categoryId"]
for item in dmg_items:
    for key in remove_keys:
        item.pop(key, None)

remaining_keys = {}
for item in dmg_items:
    for key in item.keys():
        if key not in remaining_keys.keys():
            remaining_keys.update({key: set([])})
        if type(item[key]) in [dict, list]:
            continue
        remaining_keys[key].add(item[key])

base_url = "https://www.dndbeyond.com/magic-items"
for item in dmg_items:
    item_name = item['name']
    item_name = re.sub(r'[^a-zA-Z ]', '', item_name)
    item_name = item_name.replace(' ', '-')
    sub_url = f"{base_url}/{item['id']}-{item_name}"
    item.update({"url": sub_url})
    for source in item["sources"]:
        source_name = next((
            config_source["description"]
            for config_source in config["sources"]
            if config_source["id"] == source["sourceId"]
        ), None
        )
        if not source_name:
            continue
        source.update({"sourceName": source_name})

with open("dmg-magic-item-definitions.json", "w", encoding="utf-8") as file:
    json.dump(dmg_items, file, ensure_ascii=False, indent=4)

print()

