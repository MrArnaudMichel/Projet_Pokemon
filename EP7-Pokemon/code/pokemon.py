import json
import math
import random

from move import Move


class Pokemon:
    def __init__(self, data, level: int):
        self.klass = data['klass']
        self.id = data['id']
        self.dbSymbol = data['dbSymbol']
        self.forms = data['forms']
        self.evolutions = self.forms[0]['evolutions']
        self.type = self.get_types()
        self.baseHp = self.forms[0]['baseHp']
        self.baseAtk = self.forms[0]['baseAtk']
        self.baseDfe = self.forms[0]['baseDfe']
        self.baseSpd = self.forms[0]['baseSpd']
        self.baseAts = self.forms[0]['baseAts']
        self.baseDfs = self.forms[0]['baseDfs']
        self.evHp = self.forms[0]['evHp']
        self.evAtk = self.forms[0]['evAtk']
        self.evDfe = self.forms[0]['evDfe']
        self.evSpd = self.forms[0]['evSpd']
        self.evAts = self.forms[0]['evAts']
        self.evDfs = self.forms[0]['evDfs']
        self.experienceType = self.forms[0]['experienceType']
        self.baseExperience = self.forms[0]['baseExperience']
        self.baseLoyalty = self.forms[0]['baseLoyalty']
        self.catchRate = self.forms[0]['catchRate']
        self.femaleRate = self.forms[0]['femaleRate']
        self.breedGroups = self.forms[0]['breedGroups']
        self.hatchSteps = self.forms[0]['hatchSteps']
        self.babyDbSymbol = self.forms[0]['babyDbSymbol']
        self.babyForm = self.forms[0]['babyForm']
        self.itemHeld = self.forms[0]['itemHeld']
        self.abilities = self.forms[0]['abilities']
        self.frontOffsetY = self.forms[0]['frontOffsetY']
        self.resources = self.forms[0]['resources']
        self.moveSet = self.forms[0]['moveSet']

        self.level = level
        self.gender = "female" if random.randint(1, 100) <= self.femaleRate else "male"
        if self.femaleRate == -1:
            self.gender = "genderless"
        self.ivs = {key: random.randint(1, 31) for key in self.get_base_stats().keys()}
        self.base_stats = self.get_base_stats()

        self.maxhp = self.update_stats("hp")
        self.hp = self.update_stats("hp")
        self.atk = self.update_stats("atk")
        self.dfe = self.update_stats("dfe")
        self.ats = self.update_stats("ats")
        self.dfs = self.update_stats("dfs")
        self.spd = self.update_stats("spd")

        self.shiny = "shiny" if random.randint(1, 10) == 1 else ""
        self.xp = 0
        self.points_ev = 0

        self.moves: list[Move] = self.setmoves()
        self.status = ""

        self.xp_to_next_level = self.xp_to_next_level()

        self.evolution = None

    def get_types(self):
        type1 = self.forms[0]['type1']
        type2 = self.forms[0]['type2']
        if type2 == "__undef__":
            return [type1]
        return [type1, type2]

    def get_base_stats(self):
        return {
            "hp": self.forms[0]['baseHp'],
            "atk": self.forms[0]['baseAtk'],
            "dfe": self.forms[0]['baseDfe'],
            "spd": self.forms[0]['baseSpd'],
            "ats": self.forms[0]['baseAts'],
            "dfs": self.forms[0]['baseDfs'],
        }

    def update_stats(self, stat):
        base_stat = self.get_base_stats()[stat]
        iv = self.ivs[stat]
        ev = self.get_ev()[stat]
        level = self.level
        nature = 1.0
        if stat == "hp":
            return math.floor(((2 * base_stat + iv + math.floor(ev / 4)) * level / 100) + level / 10)
        return math.floor((((2 * base_stat + iv + math.floor(ev / 4)) * level / 100) + 5) * nature)

    def xp_to_next_level(self):
        if self.level == 100:
            return 0
        if self.experienceType == 1:
            return math.floor((4 * (self.level ** 3)) / 5)
        elif self.experienceType == 3:
            return math.floor(((6 / 5) * (self.level ** 3)) - (15 * (self.level ** 2)) + (100 * self.level) - 140)
        elif self.experienceType == 0:
            return self.level ** 3
        elif self.experienceType == 2:
            return 5 * (self.level ** 3) / 4
        elif self.experienceType == 4:
            if self.level <= 50:
                return math.floor((self.level ** 3) * (100 - self.level) / 50)
            elif self.level <= 68:
                return math.floor((self.level ** 3) * (150 - self.level) / 100)
            elif self.level <= 98:
                return math.floor((self.level ** 3) * math.floor((1911 - 10 * self.level) / 3) / 500)
            elif self.level <= 100:
                return math.floor((self.level ** 3) * (160 - self.level) / 100)

    def setmoves(self):
        list_move: list[dict] = []
        list_attack: list[Move] = []
        for move in self.moveSet:
            try:
                if move['level'] <= self.level:
                    list_move.append(move)
            except:
                pass
        min = 2
        if len(list_move) < min:
            min = len(list_move)
        max = 4
        if len(list_move) < 4:
            max = len(list_move)
        for i in range(random.randint(min, max)):
            chosed = random.choice(list_move)
            list_move.remove(chosed)
            list_attack.append(Move.createMove(chosed['move']))
        return list_attack

    def get_ev(self):
        return {
            "hp": self.forms[0]["evHp"],
            "atk": self.forms[0]["evAtk"],
            "dfe": self.forms[0]["evDfe"],
            "ats": self.forms[0]["evAts"],
            "dfs": self.forms[0]["evDfs"],
            "spd": self.forms[0]["evSpd"]
        }

    @staticmethod
    def createPokemon(name: str, level: int) -> "Pokemon":
        return Pokemon(json.load(open(f"../../assets/json/pokemon/{name.lower()}.json")), level)
