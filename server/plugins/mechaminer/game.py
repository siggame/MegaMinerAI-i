import game_objects
import objects

class Game(game_objects.Game):
    _name = 'mechaminer'
    _game_version = 1
    _server_version = 1
    _globals = ['turn_number', 'game_name', 'width', 'height', 'player_id', 'fighter_id', 'healer_id', 'sniper_id', 'bomber_id']
    _relations = {'bomber': 'RobotType', 'player': 'Player', 'sniper': 'RobotType', 'fighter': 'RobotType', 'healer': 'RobotType'}
    _remotes = {}

    def before_start(self):
        #TODO: Initialize the game

        #Create any objects that should exist at the start (Tiles, for example)
        #Initialize any global values
        #At this point Player objects exist
        #(But any game-specific values will be uninitialized)
        config = self.load_config('defaults')
        self.game_length = config['globals']['game_length']
        self.width = config['globals']['width']
        self.height = config['globals']['height']

    def before_turn(self):
        #TODO: Initialize the turn
        #turn_number and current_player will be valued for the coming turn

        #Common operations include:
        #Setting current player's units to ready to move/attack
        #Start of turn income
        #Creating units whose construction began previously
        pass

    def after_turn(self):
        #TODO: Clean up any values at the end of a turn
        #turn_number and current_player will be valued for the past turn
        #This is called before check_winner, so this is a good place for any
        #Score calculation

        #Common operations include:
        #Setting all units to no moves_left/attacks_left
        #Any end of turn costs/damage
        pass

    def check_winner(self):
        #TODO: Calculate if anyone has won and return the winner and reason
        if self.turn_number >= self.game_length:
            return self.players[0], 'won due to tie'
        else:
            return None, 'the battle continues'
