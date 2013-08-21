import game_objects
from .game import Game
from  util import command
from game_utils import takes, success, failure

class Mappable(Game.Object):
    _game_state_attributes = ['id', 'x', 'y']
    _relations = {}
    _remotes = {}

    def before_turn(self):
        #TODO: Fill in start of turn values
        #Common example would be giving units moves before their turn
        pass

    def after_turn(self):
        #TODO: Set post-turn values
        #Common example would be zeroing unit moves after the turn
        pass


class Player(Game.Object):
    _game_state_attributes = ['id', 'name', 'time', 'expensivium', 'money']
    _relations = {}
    _remotes = {}

    def before_turn(self):
        #TODO: Fill in start of turn values
        #Common example would be giving units moves before their turn
        pass

    def after_turn(self):
        #TODO: Set post-turn values
        #Common example would be zeroing unit moves after the turn
        pass

    @command
    @takes(message = unicode)
    def talk(self, message = None):
        pass


class RobotType(Game.Object):
    _game_state_attributes = ['id', 'max_health', 'range', 'splash', 'damage', 'movement', 'attacks']
    _relations = {}
    _remotes = {}

    def before_turn(self):
        #TODO: Fill in start of turn values
        #Common example would be giving units moves before their turn
        pass

    def after_turn(self):
        #TODO: Set post-turn values
        #Common example would be zeroing unit moves after the turn
        pass


class Robot(Game.Object):
    _game_state_attributes = ['id', 'x', 'y', 'health', 'moves_left', 'attack_left', 'owner_id', 'type_id']
    _relations = {'owner': 'Player', 'type': 'RobotType'}
    _remotes = {'attacks': 'type', 'damage': 'type', 'range': 'type', 'splash': 'type', 'max_health': 'type', 'movement': 'type'}

    def before_turn(self):
        #TODO: Fill in start of turn values
        #Common example would be giving units moves before their turn
        pass

    def after_turn(self):
        #TODO: Set post-turn values
        #Common example would be zeroing unit moves after the turn
        pass

    @command
    @takes(destination = 'Mappable')
    def move(self, destination = None):
        pass

    @command
    @takes(target = 'Mappable')
    def attack(self, target = None):
        pass


class Factory(Game.Object):
    _game_state_attributes = ['id', 'x', 'y', 'owner_id']
    _relations = {'owner': 'Player'}
    _remotes = {}

    def before_turn(self):
        #TODO: Fill in start of turn values
        #Common example would be giving units moves before their turn
        pass

    def after_turn(self):
        #TODO: Set post-turn values
        #Common example would be zeroing unit moves after the turn
        pass

    @command
    @takes(type = 'RobotType')
    def spawn(self, type = None):
        pass


class Mine(Game.Object):
    _game_state_attributes = ['id', 'x', 'y', 'owner_id']
    _relations = {'owner': 'Player'}
    _remotes = {}

    def before_turn(self):
        #TODO: Fill in start of turn values
        #Common example would be giving units moves before their turn
        pass

    def after_turn(self):
        #Our owner gets points after their turn
        if self.game.player == self.owner:
            self.game.player.expensivium += 1
        else:
            #Or gets money from not having to pay wages
            self.game.player.money += 1


class Tile(Game.Object):
    _game_state_attributes = ['id', 'x', 'y', 'wall']
    _relations = {}
    _remotes = {}

    def before_turn(self):
        #TODO: Fill in start of turn values
        #Common example would be giving units moves before their turn
        pass

    def after_turn(self):
        #TODO: Set post-turn values
        #Common example would be zeroing unit moves after the turn
        pass


