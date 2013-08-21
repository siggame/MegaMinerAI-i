# -*- python -*-
import socket

#  @brief Class to store competitor-accessible data and functions


class BaseAI():

    def __init__(self):
        pass

    connection = None
    game_name = "mechaminer"

    #  @breif The player_id of the competitor.
    my_player_id = 0

    #  @brief How many turns it has been since the beginning of the game
    turn_number = None

    #  @brief The player whose turn it currently is
    player = None

    #  @brief What number game this is for the server
    game_name = None

    #  @brief The width of the map (max X value)
    width = None

    #  @brief The height of the map (max Y value)
    height = None

    fighter = None

    healer = None

    sniper = None

    bomber = None


    #  @brief List containing all Players.
    players = []

    #  @brief List containing all RobotTypes.
    robotTypes = []

    #  @brief List containing all Robots.
    robots = []

    #  @brief List containing all Factorys.
    factorys = []

    #  @brief List containing all Mines.
    mines = []

    #  @brief List containing all Tiles.
    tiles = []


    #  @breif Accessor function for turn_number
    def get_turn_number(self):
        return self.turn_number

    #  @breif Accessor function for player
    def get_player(self):
        return self.player

    #  @breif Accessor function for game_name
    def get_game_name(self):
        return self.game_name

    #  @breif Accessor function for width
    def get_width(self):
        return self.width

    #  @breif Accessor function for height
    def get_height(self):
        return self.height

    #  @breif Accessor function for fighter
    def get_fighter(self):
        return self.fighter

    #  @breif Accessor function for healer
    def get_healer(self):
        return self.healer

    #  @breif Accessor function for sniper
    def get_sniper(self):
        return self.sniper

    #  @breif Accessor function for bomber
    def get_bomber(self):
        return self.bomber


