import json


class Move:
    def __init__(self, move_data):
        self.id = move_data.get('id')
        self.dbSymbol = move_data.get('dbSymbol')
        self.klass = move_data.get('klass')
        self.mapUse = move_data.get('mapUse')
        self.type = move_data.get('type')
        self.power = move_data.get('power')
        self.accuracy = move_data.get('accuracy')
        self.maxpp = move_data.get('pp')
        self.category = move_data.get('category')
        self.movecriticalRate = move_data.get('movecriticalRate')
        self.battleEngineMethod = move_data.get('battleEngineMethod')
        self.priority = move_data.get('priority')
        self.isDirect = move_data.get('isDirect')
        self.isCharge = move_data.get('isCharge')
        self.isRecharge = move_data.get('isRecharge')
        self.isBlocable = move_data.get('isBlocable')
        self.isSnatchable = move_data.get('isSnatchable')
        self.isMirrorMove = move_data.get('isMirrorMove')
        self.isPunch = move_data.get('isPunch')
        self.isGravity = move_data.get('isGravity')
        self.isMagicCoatAffected = move_data.get('isMagicCoatAffected')
        self.isUnfreeze = move_data.get('isUnfreeze')
        self.isSoundAttack = move_data.get('isSoundAttack')
        self.isDistance = move_data.get('isDistance')
        self.isHeal = move_data.get('isHeal')
        self.isAuthentic = move_data.get('isAuthentic')
        self.isBite = move_data.get('isBite')
        self.isPulse = move_data.get('isPulse')
        self.isBallistics = move_data.get('isBallistics')
        self.isMental = move_data.get('isMental')
        self.isNonSkyBattle = move_data.get('isNonSkyBattle')
        self.isDance = move_data.get('isDance')
        self.isKingRockUtility = move_data.get('isKingRockUtility')
        self.isPowder = move_data.get('isPowder')
        self.effectChance = move_data.get('effectChance')
        self.battleEngineAimedTarget = move_data.get('battleEngineAimedTarget')
        self.battleStageMod: list[dict] = move_data.get('battleStageMod')
        self.moveStatus = move_data.get('moveStatus')

        self.pp = self.maxpp

    @staticmethod
    def createMove(name: str) -> "Move":
        return Move(json.load(open(f"../../assets/json/moves/{name.lower()}.json")))
