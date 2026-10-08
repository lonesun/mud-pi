from threading import local
import time

from mudserver import MudServer
from world.areas import get_recipients

"""A simple Multi-User Dungeon (MUD) game."""

players = {}

mud = MudServer()

from world import area_array as rooms

# control_switch(eingangspunkt)
on_switch = local()
on_switch.is_pressed = True
while on_switch.is_pressed:

    cpu_cycle = time.sleep(0.2)
    cpu_cycle # cycle the game loop without consuming 100% CPU

    mud.update() # tick/update the state of the MUD server

    for id in mud.get_new_players():

        players[id] = {
            "name": None,
            "echo": None,
            "room": None,
            "area": None,
        }


        week_count = time.strftime("%U")
        dotw = time.strftime("%A")
        mud.motd(week=week_count, day=dotw)

        # upcoming adventure art
        mud.ascii_art(week=week_count + 1, day=dotw)

        mud.send_message(id, "Greetings! What, tell me now, is /your/ name?")
        mud.send_message(id, "Please enter your name:")

    for id in mud.get_disconnected_players():

        # if for any reason the player isn't in the player map, skip them and move on to the next one
        if id not in players:
            continue

        # go through all the players in the game
        for pid, pl in players.items():
            # send each player a message to tell them about the diconnected player
            mud.send_message(pid, "[GAME] {} left the game.".format(
                                                        players[id]["name"]))

        # remove the player's entry in the player dictionary
        del(players[id])

    # go through any new commands sent from players
    for id, command, params in mud.get_commands():

        # if for any reason the player isn't in the player map, skip them and move on to the next one
        if id not in players:
            continue

        # if the player hasn't given their name yet, use this first command as their name and move them to the starting room.
        if players[id]["name"] is None:

            players[id]["name"] = command
            players[id]["echo_content"] = "An exceptional actor"
            players[id]["echo"] = players[id]["echo_content"]
            players[id]["room"] = "Tavern"
            players[id]["area"] = rooms[players[id]["room"]]["area"]

            # go through all the players in the game
            for pid, pl in players.items():
                # send each player a message to tell them about the new player
                mud.send_message(pid, "{} entered the game".format(
                                                        players[id]["name"]))

            # send the new player a welcome message
            mud.send_message(id, "Welcome to the game, {}. ".format(
                                                           players[id]["name"])
                             + "Type 'help' for a list of commands. Have fun!")

            # send the new player the description of their current room
            mud.send_message(id, rooms[players[id]["room"]]["description"])

        # each of the possible commands is handled below:

        # 'help' command
        elif command == "help":

            # send the player back the list of possible commands
            mud.send_message(id, "Commands:")
            mud.send_message(id, "  say <message>  - Says something out loud, "
                                 + "e.g. 'say Hello'")
            mud.send_message(id, "  look           - Examines the "
                                 + "surroundings, e.g. 'look'")
            mud.send_message(id, "  go <exit>      - Moves through the exit "
                                 + "specified, e.g. 'go outside'")

        # 'say' command
        elif command == "say":

            # go through every player in the game
            for pid, pl in players.items():
                # if they're in the same room as the player
                if players[pid]["room"] == players[id]["room"]:
                    # send them a message telling them what the player said
                    mud.send_message(pid, "{} says, \"{}\"".format(
                                                players[id]["name"], params))

        # 'look' command
        elif command == "look":

            # store the player's current room
            rm = rooms[players[id]["room"]]

            # send the player back the description of their current room
            mud.send_message(id, rm["description"])

            playershere = []
            # go through every player in the game
            for pid, pl in players.items():
                # if they're in the same room as the player
                if players[pid]["room"] == players[id]["room"]:
                    # ... and they have a name to be shown
                    if players[pid]["name"] is not None:
                        # add their name to the list
                        playershere.append(players[pid]["name"])
                        playershere.append(players[pid]["echo"])
                        playershere.sort()


            # send player a message containing the list of players in the room
            mud.send_message(id, "-" * 77)
            mud.send_message(id, "Players/actors here:\n{},    \n    {}".format(
                                                    " ".join(playershere[::2]), ", ".join(playershere[1::2])))
            mud.send_message(id, "-" * 77)

            # send player a message containing the list of exits from this room
            mud.send_message(id, "Exits are: {}".format(
                                                    ", ".join(rm["exits"])))

        # 'go' command
        elif command == "goto":

            # store the exit name, just the first word of the parameters
            ex = params.lower().split()[0]
            # store the rest of the parameters as the (optional) emote text
            emote_text = " ".join(params.lower().split()[1:])

            # store the player's current room
            rm = rooms[players[id]["room"]]

            # if the specified exit is found in the room's exits list
            if ex in rm["exits"]:

                # go through all the players in the game
                for pid, pl in players.items():

                    if players[pid]["room"] == players[id]["room"] \
                            and pid != id \
                            and emote_text:

                        mud.send_message(pid, "{} => {}: {} {}".format(
                                                      players[id]["name"], ex, players[id]["name"], emote_text))

                    elif players[pid]["room"] == players[id]["room"] \
                            and pid != id:

                        mud.send_message(pid, "{} left towards '{}'.".format(
                                                      players[id]["name"], ex))

                # update the player's current room to the one the exit leads to
                players[id]["room"] = rm["exits"][ex]
                rm = rooms[players[id]["room"]]
                players[id]["area"] = rm["area"]

                # go through all the players in the game
                for pid, pl in players.items():
                    # if player is in the same (new) room and isn't the player
                    # sending the command
                    if players[pid]["room"] == players[id]["room"] \
                            and pid != id:
                        # send them a message telling them that the player
                        # entered the room
                        mud.send_message(pid,
                                         "{} arrived via exit '{}'".format(
                                                      players[id]["name"], ex))

                # send the player a message telling them where they are now
                mud.send_message(id, "You arrive at '{}'".format(
                                                          players[id]["room"]))

            # the specified exit wasn't found in the current room
            else:
                # send back an 'unknown exit' message
                mud.send_message(id, "Unknown exit '{}'".format(ex))

        # !!!NEW!!!
        elif command == "emote" or command == "pose":
            emote_text = params
            emote_listener = EmoteListener()
            emote_listener.notify(emote_text)

            for pid, pl in players.items():
                if players[pid]["room"] == players[id]["room"]:
                    mud.send_message(pid, "{} {}".format(
                                                players[id]["name"], params))

        # !!!NEW!!!
        elif command == "gush":
            gush_text = params
            emote_listener = EmoteListener()
            emote_listener.notify(gush_text)

            same_area = [pid for pid in players
                         if players[pid]["area"] == players[id]["area"]]
            for pid in get_recipients(command, id, same_area):
                mud.send_message(pid, "Somewhere nearby...\n...{} {}".format(
                                            players[id]["name"], params))

        # some other, unrecognised command
        else:
            # send back an 'unknown command' message
            mud.send_message(id, "Unknown command '{}'".format(command))
