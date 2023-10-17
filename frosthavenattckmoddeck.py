# -*- coding: utf-8 -*-
import random
import textwrap


class Card:
    def __init__(self):
        self.Damage = None
        self.Effects = dict()
        self.Generates = []
        self.Specials = []
        self.Roll = False
        self.Critical = False
        self.Miss = False
        self.OneUse = False

    def set_damage(self, damage):
        self.Damage = damage
        return self

    def add_effect(self, effect, num=0):
        if effect in self.Effects:
            self.Effects[effect] += num
        else:
            self.Effects[effect] = num
        return self

    def add_element(self, element):
        self.Generates.append(element)
        return self

    def add_special(self, special):
        self.Specials.append(special)
        return self

    def set_roll(self):
        self.set_roll_critical_miss(roll=True)
        return self

    def set_critical(self):
        self.set_roll_critical_miss(critical=True)
        return self

    def set_miss(self):
        self.set_roll_critical_miss(miss=True)
        return self

    def set_one_use(self):
        self.OneUse = True
        return self

    def set_roll_critical_miss(self, roll=False, critical=False, miss=False):
        self.Roll = roll
        self.Critical = critical
        self.Miss = miss

    def copy(self):
        copy = Card()
        copy.set_damage(self.Damage)
        for effect, num in self.Effects:
            copy.add_effect(effect, num)
        for element in self.Generates:
            copy.add_element(element)
        for special in self.Specials:
            copy.add_special(special)
        if self.Critical:
            copy.set_critical()
        if self.Miss:
            copy.set_miss()

        return copy

    def __str__(self):
        text = ""

        if self.Miss:
            text += "Damage: MISS\n"
        else:
            if self.Critical:
                if self.Damage is not None:
                    text += "Damage: " + str(self.Damage) + " X Critical\n"
                else:
                    text += "Damage: +0 X Critical\n"
            else:
                if self.Damage is not None:
                    text += "Damage: " + str(self.Damage) + "\n"

        if len(self.Effects) > 0:
            text += "Effects: \n-" + '\n-'.join(
                str(effect if self.Effects[effect] == 0 else f"{effect} {self.Effects[effect]}") for effect in
                self.Effects.keys()) + "\n"
        if len(self.Generates) > 0:
            text += "Generates: \n-" + '\n-'.join(self.Generates) + "\n"
        if len(self.Specials) > 0:
            text += "Specials: \n-" + '\n-'.join(self.Specials) + "\n"
        if self.Roll:
            text += "Roll\n"

        return text

    def __add__(self, other):
        if other.Damage is not None:
            if self.Damage is None:
                self.Damage = other.Damage
            else:
                self.Damage += other.Damage

        for element in other.Generates:
            if element not in self.Generates:
                self.add_element(element)

        if len(other.Effects) > 0:
            for effect, num in other.Effects.items():
                self.add_effect(effect, num)

        for special in other.Specials:
            self.add_special(special)

        if other.Miss:
            self.set_miss()

        if other.Critical:
            self.set_critical()

        return self


class ModDeck:

    def __init__(self):
        self.Deck = []
        self.Discard = []
        self.NeedShuffle = False

        self.classOptions = []
        self.perksOptions = []
        self.perksSelection = dict()
        self.currentClass = ""

        self.CardMin2 = Card().set_damage(-2)
        self.CardMin1 = Card().set_damage(-1)
        self.CardZero = Card().set_damage(0)
        self.CardPls1 = Card().set_damage(1)
        self.CardPls2 = Card().set_damage(2)
        self.CardCrit = Card().set_critical()
        self.CardMiss = Card().set_miss()

        CardMin2 = self.CardMin2
        CardMin1 = self.CardMin1
        CardZero = self.CardZero
        CardPls1 = self.CardPls1
        CardPls2 = self.CardPls2

        DamageZeroDisarm = CardZero.copy().add_effect("Disarm")
        DamageZeroWound = CardZero.copy().add_effect("Wound")
        DamageZeroTargetPls1 = CardZero.copy().add_effect("Target", 1)

        DamageZeroHazardousTerrain = CardZero.copy().add_special(
            "Damage +0, Create one 1-hex hazardous terrain tile in a featureless hex adjacent to the target")
        DamageZeroHeal2Trap = CardZero.copy().add_special(
            "Damage +0, Create one Heal 2 trap in an empty hex adjacent to the target")
        DamageZeroDamage1Trap = CardZero.copy().add_special(
            "Damage +0, Create one Damage 1 trap in an empty hex adjacent to the target")
        DamageZeroBuffTrap = CardZero.copy().add_special(
            "Damage +0, Add Damage 2 or Heal 2 to a trap within Distance 2")

        DamagePls1GenIceLeaf = CardPls1.copy().add_element("Ice").add_element("Leaf")
        DamagePls1GenFireLeaf = CardPls1.copy().add_element("Fire").add_element("Leaf")
        DamagePls1Disarm = CardPls1.copy().add_effect("Disarm")
        DamagePls1MuddleRoll = CardPls1.copy().add_effect("Muddle").set_roll()
        DamagePls1Wound = CardPls1.copy().add_effect("Wound")
        DamagePls1Immobilize = CardPls1.copy().add_effect("Immobilize")
        DamagePls1ShieldRoll = CardPls1.copy().add_effect("Shield", 1).set_roll()

        DamagePls2Muddle = CardPls2.copy().add_effect("Muddle")
        DamagePls2Immobilize = CardPls2.copy().add_effect("Immobilize")
        DamagePls2RegenerateSelf = CardPls2.copy().add_effect("Regenerate self").set_roll()

        DamagePls3 = Card().set_damage(3)

        Pierce3Roll = Card().add_effect("Pierce", 3).set_roll()
        TidePls1Or2 = CardPls1.copy().add_special("If you performed a Tide action this card is +2 instead of 1")
        Heal1SelfRoll = Card().add_effect("Heal self", 1).set_roll()
        DamagePls2IcyTerrain = CardPls2.copy().add_special(
            "Create one 1-hex Icy terrain tile in a featureless hex adjecent to the target")
        Push2Roll = Card().add_effect("Push", 2).set_roll()
        Push2OrPull2Roll = Card().add_effect("Push or Pull", 2).set_roll()
        DelayedPls2Roll = Card().add_special(
            "Place this card on your active Area. On your next attack discard this card to add Damage +2").set_roll()

        DamageMin1Gain1TimeToken = CardMin1.copy().add_special("Gain 1 Time Token")

        currentClass = 'CT'

        self.Classes = dict()
        self.Classes["CT"] = {
            "name": "Lurker Chrashing Tide",
            "perks": [
                {"text": "Replace one (Damage -1) card with two (Piercing 3, Roll) cards",
                 "add": [Pierce3Roll, Pierce3Roll],
                 "remove": [CardMin1]},
                {"text": "Replace one (Damage -1) card with two (Piercing 3, Roll) cards",
                 "add": [Pierce3Roll, Pierce3Roll],
                 "remove": [CardMin1]},
                {"text": "Replace one (Damage -1) card with one (Damage +0, Target +1) card",
                 "add": [DamageZeroTargetPls1],
                 "remove": [CardMin1]},
                {"text": "Replace one (Damage -1) card with one (Damage +0, Target +1) card",
                 "add": [DamageZeroTargetPls1],
                 "remove": [CardMin1]}
            ]
        }
        self.Classes["TF"] = {
            "name": "Algox Frozen Fist",
            "perks": [
                {"add": [DamageZeroDisarm], "remove": [CardMin1]},
                {"add": [DamageZeroDisarm], "remove": [CardMin1]},
                {"add": [CardPls1], "remove": [CardMin1]},
                {"add": [CardZero], "remove": [CardMin2]},
                {"add": [DamagePls1ShieldRoll], "remove": [CardZero]},
                {"add": [DamagePls1ShieldRoll], "remove": [CardZero]},
                {"add": [DamagePls1GenIceLeaf], "remove": [CardZero]},
                {"add": [DamagePls1GenIceLeaf], "remove": [CardZero]},
                {"add": [DamagePls2IcyTerrain], "remove": [CardZero]},
                {"add": [DamagePls2IcyTerrain], "remove": [CardZero]},
                {"add": [DamagePls3], "remove": []},
                {"add": [Heal1SelfRoll, Heal1SelfRoll], "remove": []},
                {"add": [Heal1SelfRoll, Heal1SelfRoll], "remove": []},
                {"add": [Heal1SelfRoll, Heal1SelfRoll], "remove": []}
            ]
        }
        self.Classes["QB"] = {
            "name": "Quatryl Blinkblade",
            "perks": [
                {"add": [], "remove": [CardMin2]},
                {"add": [CardPls1], "remove": [CardMin1]},
                {"add": [CardPls1], "remove": [CardMin1]},
                {"add": [DamageZeroWound], "remove": [CardMin1]},
                {"add": [DamageZeroWound], "remove": [CardMin1]},
                {"add": [DamagePls1Immobilize], "remove": [CardZero]},
                {"add": [DamagePls1Immobilize], "remove": [CardZero]},
                {"add": [DelayedPls2Roll], "remove": [CardZero]},
                {"add": [DelayedPls2Roll], "remove": [CardZero]},
                {"add": [DelayedPls2Roll], "remove": [CardZero]},
                {"add": [CardPls2, CardPls2], "remove": [CardPls1, CardPls1]},
                {"add": [DamageMin1Gain1TimeToken], "remove": []},
                {"add": [DamageMin1Gain1TimeToken], "remove": []},
                {"add": [DamagePls2RegenerateSelf], "remove": []},
                {"add": [DamagePls2RegenerateSelf], "remove": []}
            ]
        }

        self.Classes["SP"] = {
            "name": "Savvas Pyroclast",
            "perks": [
                {"add": [], "remove": [CardMin1, CardMin1]},
                {"add": [], "remove": [CardMin2]},
                {"add": [DamagePls1Wound], "remove": [CardZero]},
                {"add": [DamagePls1Wound], "remove": [CardZero]},
                {"add": [DamageZeroHazardousTerrain], "remove": [CardMin1]},
                {"add": [DamageZeroHazardousTerrain], "remove": [CardMin1]},
                {"add": [Push2Roll, Push2Roll], "remove": [CardZero, CardZero]},
                {"add": [Push2Roll, Push2Roll], "remove": [CardZero, CardZero]},
                {"add": [CardPls2, CardPls2], "remove": [CardPls1, CardPls1]},
                {"add": [DamagePls1GenFireLeaf, DamagePls1GenFireLeaf], "remove": []},
                {"add": [DamagePls1GenFireLeaf, DamagePls1GenFireLeaf], "remove": []},
                {"add": [DamagePls1MuddleRoll, DamagePls1MuddleRoll], "remove": []},
            ]
        }

        self.Classes["VT"] = {
            "name": "Vermling Trapper",
            "perks": [
                {"add": [], "remove": [CardMin2]},
                {"add": [DamageZeroHeal2Trap], "remove": [CardMin1]},
                {"add": [DamageZeroHeal2Trap], "remove": [CardMin1]},
                {"add": [DamageZeroDamage1Trap], "remove": [CardMin1]},
                {"add": [DamageZeroDamage1Trap], "remove": [CardMin1]},
                {"add": [DamageZeroDamage1Trap], "remove": [CardMin1]},
                {"add": [DamageZeroBuffTrap, DamageZeroBuffTrap], "remove": [CardZero, CardZero]},
                {"add": [DamageZeroBuffTrap, DamageZeroBuffTrap], "remove": [CardZero, CardZero]},
                {"add": [DamageZeroBuffTrap, DamageZeroBuffTrap], "remove": [CardZero, CardZero]},
                {"add": [DamagePls2Immobilize, DamagePls2Immobilize], "remove": [CardPls1, CardPls1]},
                {"add": [DamagePls2Immobilize, DamagePls2Immobilize], "remove": [CardPls1, CardPls1]},
                {"add": [Push2OrPull2Roll, Push2OrPull2Roll], "remove": []},
                {"add": [Push2OrPull2Roll, Push2OrPull2Roll], "remove": []},
                {"add": [Push2OrPull2Roll, Push2OrPull2Roll], "remove": []}
            ]
        }

        #self.InitDeck()

    def GetClasses(self):
        return self.Classes

    # @title
    def PrintDeck(self):
        cards = []
        wrapper = textwrap.TextWrapper(width=80)
        for card in self.Deck:
            cards.append(str(card))

        word_list = wrapper.wrap(text=f"{', '.join(cards)}")

        # Print each line.
        for element in word_list:
            print(element)

    def addCard(self, x, count=1):
        for i in range(count):
            self.Deck.append(x)

    def removeCard(self, x, count=1):
        for i in range(count):
            if x in self.Deck:
                self.Deck.remove(x)

    def drawCard(self):
        combined_card = Card()
        card = random.choice(self.Deck)
        if card == self.CardCrit or card == self.CardMiss:
            self.NeedShuffle = True
        self.Deck.remove(card)
        if not card.OneUse:
            self.Discard.append(card)
        combined_card += card
        while card.Roll:
            card = random.choice(self.Deck)
            self.Deck.remove(card)
            if card == self.CardCrit or card == self.CardMiss:
                self.NeedShuffle = True
            if not card.OneUse:
                self.Discard.append(card)
            combined_card += card

        return combined_card

    # @title
    def InitDeck(self):
        self.Deck.clear()
        self.Discard.clear()
        self.addCard(self.CardCrit)
        self.addCard(self.CardMiss)
        self.addCard(self.CardMin2)
        self.addCard(self.CardMin1, 5)
        self.addCard(self.CardZero, 6)
        self.addCard(self.CardPls1, 5)
        self.addCard(self.CardPls2)

    # @title
    def ShuffleDeck(self):
        for i in range(len(self.Discard)):
            self.Deck.append(self.Discard.pop())

    # @title
    def selectClass(self, x):
        if x == self.currentClass:
            return
        self.InitDeck()
        self.NeedShuffle = False
        self.currentClass = x
        self.perksSelection = dict()
        #for i in range(len(self.Classes[currentClass]["perks"])):
        #    self.perksSelection.append(False)


    def activatePerk(self, id, perk):
        #id = self.perksOptions.index(x['owner'])
        #perk = self.Classes[self.currentClass]["perks"][id]
        if self.perksSelection.get(id) is not None:
            self.perksSelection[id] = not self.perksSelection[id]
        else:
            self.perksSelection[id] = True
        #if x['new']:
        if self.perksSelection[id]:
            for c in perk["add"]:
                self.addCard(c)
            for c in perk["remove"]:
                self.removeCard(c)
        else:
            for c in perk["add"]:
                self.removeCard(c)
            for c in perk["remove"]:
                self.addCard(c)

    def NumToText(self, num):
        if num == 1:
            return "one"
        if num == 2:
            return "two"
        return ""

    def GeneratePerkText(self, perk):
        if len(perk['add']) > 0 and len(perk['remove']) > 0:
            return f"Replace {self.NumToText(len(perk['remove']))} {perk['remove'][0]} with {self.NumToText(len(perk['add']))} {perk['add'][0]}"
        if len(perk['add']) > 0:
            return f"Add {self.NumToText(len(perk['add']))} {perk['add'][0]}"
        if len(perk['remove']) > 0:
            return f"Remove {self.NumToText(len(perk['remove']))} {perk['remove'][0]}"

    def discard_deck_size(self):
        return len(self.Discard)

    def active_deck_size(self):
        return len(self.Deck)

    def blessingAction(self):
        self.addCard(self.CardCrit.copy().set_one_use())

    def curseAction(self):
        self.addCard(self.CardMiss.copy().set_one_use())

    def shuffleAction(self):
        self.ShuffleDeck()
        self.NeedShuffle = False

    def drawCardAction(self):
        text = f"Damage roll:\n"
        text += f"{self.drawCard()}"
        return text

    def draw2CardAction(self):
        text = f"Damage roll 1:\n"
        text += f"{self.drawCard()}"
        text += "\n"
        text += f"Damage roll 2:\n"
        text += f"{self.drawCard()}"
        return text
