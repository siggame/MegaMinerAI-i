# -*- python -*-

import utility
import json
import client_json

class GameObject():
    def __init__(self):
        pass


#Mappable
#The base object for all mappable things
class Mappable(GameObject):

    #INIT
    def __init__(self, connection, parent_game, id, x, y):
        self.connection = connection
        self.parent_game = parent_game
        self.id = id
        self.x = x
        self.y = y

    #MODEL FUNCTIONS

    #MODEL DATUM ACCESSORS
    #id
    #Unique Identifier
    def get_id(self):
        return id
    #x
    #The x coordinate
    def get_x(self):
        return x
    #y
    #The y coordinate
    def get_y(self):
        return y



#Player
#Stores information about a player in the game
class Player(GameObject):

    #INIT
    def __init__(self, connection, parent_game, id, name, time, expensivium, money):
        self.connection = connection
        self.parent_game = parent_game
        self.id = id
        self.name = name
        self.time = time
        self.expensivium = expensivium
        self.money = money

    #MODEL FUNCTIONS
    #talk
    #Allows a player to display a message to the screen
    def talk(self, message):
        function_call = client_json.function_call.copy()
        function_call.update({"type": 'talk'})
        function_call.get("args").update({"actor": self.id})

        function_call.get("args").update({'message': repr(message)})

        utility.send_string(self.connection, json.dumps(function_call))

        received_status = False
        status = None
        while not received_status:
            message = utility.receive_string(self.connection)
            message = json.loads(message)

            if message.get("type") == "success":
                received_status = True
                status = True
            elif message.get("type") == "failure":
                received_status = True
                status = False
            if message.get("type") == "changes":
                self.parent_game.update_game(message)

        return status

    #MODEL DATUM ACCESSORS
    #id
    #Unique Identifier
    def get_id(self):
        return id
    #name
    #Player's name
    def get_name(self):
        return name
    #time
    #The amount of time this player has before timing out
    def get_time(self):
        return time
    #expensivium
    #Player's points, one with more at end of game wins
    def get_expensivium(self):
        return expensivium
    #money
    #Player' money, used to build new units
    def get_money(self):
        return money



#RobotType
#This class describes the characteristics for each type of robot
class RobotType(GameObject):

    #INIT
    def __init__(self, connection, parent_game, id, max_health, range, splash, damage, movement, attacks):
        self.connection = connection
        self.parent_game = parent_game
        self.id = id
        self.max_health = max_health
        self.range = range
        self.splash = splash
        self.damage = damage
        self.movement = movement
        self.attacks = attacks

    #MODEL FUNCTIONS

    #MODEL DATUM ACCESSORS
    #id
    #Unique Identifier
    def get_id(self):
        return id
    #max_health
    #The robot's starting and maximum health
    def get_max_health(self):
        return max_health
    #range
    #The robot's attack range
    def get_range(self):
        return range
    #splash
    #How many tiles away from the robot's target its attacks deal damage
    def get_splash(self):
        return splash
    #damage
    #How much damage the robot's attacks do
    def get_damage(self):
        return damage
    #movement
    #How far the robot can move each turn
    def get_movement(self):
        return movement
    #attacks
    #How many times the robot can attack each turn.
    def get_attacks(self):
        return attacks



#Robot
#Your primary Unit
class Robot(Mappable):

    #INIT
    def __init__(self, connection, parent_game, id, x, y, owner, type, health, moves_left, attack_left, max_health, range, splash, damage, movement, attacks):
        self.connection = connection
        self.parent_game = parent_game
        self.id = id
        self.x = x
        self.y = y
        self.owner = owner
        self.type = type
        self.health = health
        self.moves_left = moves_left
        self.attack_left = attack_left
        self.max_health = max_health
        self.range = range
        self.splash = splash
        self.damage = damage
        self.movement = movement
        self.attacks = attacks

    #MODEL FUNCTIONS
    #move
    #
    def move(self, destination):
        function_call = client_json.function_call.copy()
        function_call.update({"type": 'move'})
        function_call.get("args").update({"actor": self.id})

        function_call.get("args").update({'destination': repr(destination)})

        utility.send_string(self.connection, json.dumps(function_call))

        received_status = False
        status = None
        while not received_status:
            message = utility.receive_string(self.connection)
            message = json.loads(message)

            if message.get("type") == "success":
                received_status = True
                status = True
            elif message.get("type") == "failure":
                received_status = True
                status = False
            if message.get("type") == "changes":
                self.parent_game.update_game(message)

        return status
    #attack
    #
    def attack(self, target):
        function_call = client_json.function_call.copy()
        function_call.update({"type": 'attack'})
        function_call.get("args").update({"actor": self.id})

        function_call.get("args").update({'target': repr(target)})

        utility.send_string(self.connection, json.dumps(function_call))

        received_status = False
        status = None
        while not received_status:
            message = utility.receive_string(self.connection)
            message = json.loads(message)

            if message.get("type") == "success":
                received_status = True
                status = True
            elif message.get("type") == "failure":
                received_status = True
                status = False
            if message.get("type") == "changes":
                self.parent_game.update_game(message)

        return status

    #MODEL DATUM ACCESSORS
    #id
    #Unique Identifier
    def get_id(self):
        return id
    #x
    #The x coordinate
    def get_x(self):
        return x
    #y
    #The y coordinate
    def get_y(self):
        return y
    #owner
    #The owner of this Robot
    def get_owner(self):
        return owner
    #type
    #The model of the robot
    def get_type(self):
        return type
    #health
    #The Robot's level
    def get_health(self):
        return health
    #moves_left
    #The number of times this robot can still move this turn
    def get_moves_left(self):
        return moves_left
    #attack_left
    #The number of times this robot can still attack this turn
    def get_attack_left(self):
        return attack_left
    #max_health
    #
    def get_max_health(self):
        return max_health
    #range
    #
    def get_range(self):
        return range
    #splash
    #
    def get_splash(self):
        return splash
    #damage
    #
    def get_damage(self):
        return damage
    #movement
    #
    def get_movement(self):
        return movement
    #attacks
    #
    def get_attacks(self):
        return attacks



#Factory
#A base that can produce robots
class Factory(Mappable):

    #INIT
    def __init__(self, connection, parent_game, id, x, y, owner):
        self.connection = connection
        self.parent_game = parent_game
        self.id = id
        self.x = x
        self.y = y
        self.owner = owner

    #MODEL FUNCTIONS
    #spawn
    #Creates a Robot on the base of the given type.
    def spawn(self, type):
        function_call = client_json.function_call.copy()
        function_call.update({"type": 'spawn'})
        function_call.get("args").update({"actor": self.id})

        function_call.get("args").update({'type': repr(type)})

        utility.send_string(self.connection, json.dumps(function_call))

        received_status = False
        status = None
        while not received_status:
            message = utility.receive_string(self.connection)
            message = json.loads(message)

            if message.get("type") == "success":
                received_status = True
                status = True
            elif message.get("type") == "failure":
                received_status = True
                status = False
            if message.get("type") == "changes":
                self.parent_game.update_game(message)

        return status

    #MODEL DATUM ACCESSORS
    #id
    #Unique Identifier
    def get_id(self):
        return id
    #x
    #The x coordinate
    def get_x(self):
        return x
    #y
    #The y coordinate
    def get_y(self):
        return y
    #owner
    #The owner of this base
    def get_owner(self):
        return owner



#Mine
#A mine that produces expensivium every turn. Obtained by moving a robot onto its tile.
class Mine(Mappable):

    #INIT
    def __init__(self, connection, parent_game, id, x, y, owner):
        self.connection = connection
        self.parent_game = parent_game
        self.id = id
        self.x = x
        self.y = y
        self.owner = owner

    #MODEL FUNCTIONS

    #MODEL DATUM ACCESSORS
    #id
    #Unique Identifier
    def get_id(self):
        return id
    #x
    #The x coordinate
    def get_x(self):
        return x
    #y
    #The y coordinate
    def get_y(self):
        return y
    #owner
    #The owner of this mine
    def get_owner(self):
        return owner



#Tile
#
class Tile(Mappable):

    #INIT
    def __init__(self, connection, parent_game, id, x, y, wall):
        self.connection = connection
        self.parent_game = parent_game
        self.id = id
        self.x = x
        self.y = y
        self.wall = wall

    #MODEL FUNCTIONS

    #MODEL DATUM ACCESSORS
    #id
    #Unique Identifier
    def get_id(self):
        return id
    #x
    #The x coordinate
    def get_x(self):
        return x
    #y
    #The y coordinate
    def get_y(self):
        return y
    #wall
    #
    def get_wall(self):
        return wall


