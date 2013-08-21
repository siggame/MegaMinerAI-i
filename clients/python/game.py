import time
import client_json
from ai import AI
import json
import sys
import game_objects
import operator
import utility
import socket


class GameOverException(Exception):
    def __init__(self, winner, reason):
        Exception.__init__(self)
        self.winner = winner
        self.reason = reason

class Game:

    def __init__(self, conn, addr, port, name):
        self.serv_conn = conn
        self.serv_addr = addr
        self.serv_port = port
        self.game_name = name
        self.ai = AI()
        self.ai.connection = self.serv_conn

    #Attempt to connect to the server
    def connect(self):
        while True:
            try:
                #Attempting to connect
                self.serv_conn.connect((self.serv_addr, self.serv_port))
            except socket.error:
                #Failed to connect
                time.sleep(1)
            else:
                #Client connected
                return True

    def receive(self):
        data = utility.receive_string(self.serv_conn)
        message = json.loads(data)

        if message['type'] == 'changes':
            self.update_game(message)
        elif message['type'] == 'player_id':
            self.ai.my_player_id = message['args']['id']
        elif message['type'] == 'game_over':
            raise GameOverException(message["args"]["winner"], message["args"]["reason"])
        return message

    def wait_for(self, *types):
        while True:
            message = self.receive()
            if message['type'] in types:
                return message

    #Attempt to login to the server
    def login(self):
        login_json = client_json.login.copy()
        login_json['args']['username'] = self.ai.username
        login_json['args']['password'] = self.ai.password

        utility.send_string(self.serv_conn, json.dumps(login_json))

        message = self.wait_for('success', 'failure')
        if message['type'] == 'success':
            #Login success
            return True
        else:
            #Login failed
            return False

    #Attempt to create a game on the server
    def create_game(self):
        create_game_json = client_json.create_game.copy()
        if self.game_name is not None:
            create_game_json['args']['game_name'] = self.game_name

        utility.send_string(self.serv_conn, json.dumps(create_game_json))

        message = self.wait_for('success', 'failure')
        if message['type'] == "success":
            self.game_name = message['args']['name']
            print("Game created: {}".format(self.game_name))
            return True
        else:
            #Game creation failed
            return False

    #Receive Player ID from server
    def recv_player_id(self):
        self.wait_for('player_id')
        return True

    #Runs before main_loop has began.
    def init_main(self):
        self.wait_for('start_game')

        self.ai.init()
        return True

    #Runs after main_loop has finished.
    def end_main(self):
        self.ai.end()
        return True

    #Main connection loop until end of game.
    def main_loop(self):
        while True:
            message = self.wait_for('start_turn', 'game_over')
            if message['type'] == 'game_over':
                return True

            if self.ai.my_player_id == self.ai.player_id:
                utility.v_print("Turn Number: {}".format(self.ai.turn_number))
                self.ai.run()
                utility.send_string(self.serv_conn, json.dumps(client_json.end_turn))

     
    def get_log(self):
        log_json = client_json.get_log.copy()
        utility.send_string(self.serv_conn, json.dumps(log_json))

        message = self.wait_for('success', 'failure')
        if message['type'] == "success":
            file = open(self.game_name + '.glog', 'wb')
            file.write(message['args']['log'].encode('utf-8'))
            file.close()

    #Update game from message
    def update_game(self, message):
        if message.get("type") != "changes":
            return False

        for change in message.get("args").get("changes"):
            if change.get("action") == "add":
                self.change_add(change)

            elif change.get("action") == "remove":
                self.change_remove(change)

            elif change.get("action") == "update":
                self.change_update(change)

            elif change.get("action") == "global_update":
                self.change_global_update(change)

        return True

    #Parse the add action
    def change_add(self, change):
        values = change.get("values")
        if change.get("type") == "Player":
            temp = game_objects.Player(connection=self.serv_conn, parent_game=self, id=values.get("id"), name=values.get("name"), time=values.get("time"), expensivium=values.get("expensivium"), money=values.get("money"))
            self.ai.players.append(temp)
        if change.get("type") == "RobotType":
            temp = game_objects.RobotType(connection=self.serv_conn, parent_game=self, id=values.get("id"), max_health=values.get("max_health"), range=values.get("range"), splash=values.get("splash"), damage=values.get("damage"), movement=values.get("movement"), attacks=values.get("attacks"))
            self.ai.robotTypes.append(temp)
        if change.get("type") == "Robot":
            temp = game_objects.Robot(connection=self.serv_conn, parent_game=self, id=values.get("id"), x=values.get("x"), y=values.get("y"), owner=values.get("owner"), type=values.get("type"), health=values.get("health"), moves_left=values.get("moves_left"), attack_left=values.get("attack_left"), max_health=values.get("max_health"), range=values.get("range"), splash=values.get("splash"), damage=values.get("damage"), movement=values.get("movement"), attacks=values.get("attacks"))
            self.ai.robots.append(temp)
        if change.get("type") == "Factory":
            temp = game_objects.Factory(connection=self.serv_conn, parent_game=self, id=values.get("id"), x=values.get("x"), y=values.get("y"), owner=values.get("owner"))
            self.ai.factorys.append(temp)
        if change.get("type") == "Mine":
            temp = game_objects.Mine(connection=self.serv_conn, parent_game=self, id=values.get("id"), x=values.get("x"), y=values.get("y"), owner=values.get("owner"))
            self.ai.mines.append(temp)
        if change.get("type") == "Tile":
            temp = game_objects.Tile(connection=self.serv_conn, parent_game=self, id=values.get("id"), x=values.get("x"), y=values.get("y"), wall=values.get("wall"))
            self.ai.tiles.append(temp)
        return True

    #Parse the remove action.
    def change_remove(self, change):
        remove_id = change.get("id")
        try:
            index = self.ai.players.find(remove_id, key=operator.attrgetter('id'))
        except:
            pass
        else:
            self.ai.players.remove(index)
            return True
        try:
            index = self.ai.robotTypes.find(remove_id, key=operator.attrgetter('id'))
        except:
            pass
        else:
            self.ai.robotTypes.remove(index)
            return True
        try:
            index = self.ai.robots.find(remove_id, key=operator.attrgetter('id'))
        except:
            pass
        else:
            self.ai.robots.remove(index)
            return True
        try:
            index = self.ai.factorys.find(remove_id, key=operator.attrgetter('id'))
        except:
            pass
        else:
            self.ai.factorys.remove(index)
            return True
        try:
            index = self.ai.mines.find(remove_id, key=operator.attrgetter('id'))
        except:
            pass
        else:
            self.ai.mines.remove(index)
            return True
        try:
            index = self.ai.tiles.find(remove_id, key=operator.attrgetter('id'))
        except:
            pass
        else:
            self.ai.tiles.remove(index)
            return True
        return False

    #Parse the update action.
    def change_update(self, change):
        change_id = change.get("id")
        values = change.get("values")
        try:
            index = self.ai.players.find(change_id, key=operator.attrgetter('id'))
        except:
            pass
        else:
            self.ai.players[index].__dict__.update(values)
            return True
        try:
            index = self.ai.robotTypes.find(change_id, key=operator.attrgetter('id'))
        except:
            pass
        else:
            self.ai.robotTypes[index].__dict__.update(values)
            return True
        try:
            index = self.ai.robots.find(change_id, key=operator.attrgetter('id'))
        except:
            pass
        else:
            self.ai.robots[index].__dict__.update(values)
            return True
        try:
            index = self.ai.factorys.find(change_id, key=operator.attrgetter('id'))
        except:
            pass
        else:
            self.ai.factorys[index].__dict__.update(values)
            return True
        try:
            index = self.ai.mines.find(change_id, key=operator.attrgetter('id'))
        except:
            pass
        else:
            self.ai.mines[index].__dict__.update(values)
            return True
        try:
            index = self.ai.tiles.find(change_id, key=operator.attrgetter('id'))
        except:
            pass
        else:
            self.ai.tiles[index].__dict__.update(values)
            return True
        return False

    #Parse the global_update action
    def change_global_update(self, change):
        values = change.get("values")
        self.ai.__dict__.update(values)
        return True

    def run(self):
        if not self.connect(): return False
        if not self.login(): return False
        if not self.create_game(): return False
        if not self.recv_player_id(): return False

        if not self.init_main(): return False
        try:
            self.main_loop()
        except GameOverException as e:
            if e.winner == self.ai.my_player_id:
                game_over_message = "You Win! - {reason}".format(reason=e.reason)
            else:
                game_over_message = "You Lose! - {reason}".format(reason=e.reason)
        else:
            game_over_message = "Game over was never reached."

        if not self.end_main(): return False
        print(game_over_message)

        if not self.get_log(): return False
        
