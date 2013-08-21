import game_objects
import objects

#Assorted utilitily to automate common game stuff
import game_utils

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
        
        self.make_types()
        self.make_grid()

    def make_types(self):
        config = self.load_config('unit_types')
        for name, stats in config.items():
            type = objects.RobotType(self, **stats)
            type.name = name
            setattr(self, name, type)

    def make_grid(self):
        #Load config stuff
        config = self.load_config('defaults')

        #Make a grid of tiles
        self.grid = game_utils.Grid(self, objects.Tile)
        #And make it width x height.
        self.grid.generate(self.width, self.height)

        #And generate a map:
        #The config/tiles directory has all the different tiles
        #Add/remove/edit those to get what you want from it
        generator = game_utils.TileMapGenerator(self, self.width, self.height)
        #Build a basic map
        generator.generate()

        #Place 1 base on the map for each player
        generator.sprinkle(config['globals']['factories'], 'b')

        #Place 5 mines on the map for each player
        generator.sprinkle(config['globals']['mines'], 'm')

        #And ensure all empty space, bases, and mines are connected
        generator.connect_map(' bm')

        #Then use the data on the generator to populate our map:
        for i in generator:
            tile = self.grid[i.x, i.y]
            if i.value == '#':
                tile.wall = True
            elif i.value == 'b':
                base = objects.Factory(self, x=i.x, y=i.y)
                if i.x < self.width / 2:
                    base.owner = self.players[0]
                else:
                    base.owner = self.players[1]
            elif i.value == 'm':
                objects.Mine(self, x=i.x, y=i.y)

        for i in self.players:
            i.money = config['globals']['starting_money']

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
