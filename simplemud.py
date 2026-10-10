from threading import local
import time
import keyboard

from mudserver import MudServer
from world.areas import get_recipients
from players import save as save_players, load as load_players, forget as forget_players

from src.figlet import set_buffer, render_text

from src import attempt_load, save_user_data, seed_database

"""A simple Multi-User Dungeon (MUD) game."""

players = {}

mud = MudServer()

def save_player_position(player):
    """Persists a named player's room to the roster so they can resume where they left off."""
    if player["name"] is None:
        return
    save_user_data(player["name"], player["room"], expected_field="current_room")

from world import area_array as rooms

# control_switch(eingangspunkt)
on_switch = local()
game_start = local()
on_switch.is_looping = True
while on_switch.is_looping:

    def shutdown_game():
        game_start.is_looping = False
        input("Press Enter to confirm shutdown...")
        on_switch.is_looping = False
        mud.shutdown() # gracefully shut down the MUD server

    def pause_game():
        game_start.is_looping = False

    def resume_game():
        game_start.is_looping = True

    def show_game_info():
        print("Displaying information about the game loop.")
        print("Current players:", list(players.keys()))

    def reset_game():

        game_start.is_looping = False
        save_players(players, "players_backup.json")
        print("Players backed up to 'players_backup.json'.")

        players.clear()

        mud.shutdown()

        mud.bootup()

        players = load_players("players_backup.json")

        forget_players("players_backup.json")
        print("Players restored from 'players_backup.json'.")

        print("Game cache cleared and restarted.")
        return

    # game_start = local()
    game_start.time = time.time()
    game_start.is_looping = True

    while game_start.is_looping:

        """
        if keyboard.is_pressed("q"):
            print("Shutting down the game loop.")
            shutdown_game()

        if keyboard.is_pressed("p") and not game_start.is_looping:
            print("Resuming the game loop.")
            resume_game()

        if keyboard.is_pressed("p"):
            print("Pausing the game loop.")
            pause_game()

        if keyboard.is_pressed("i"):
            show_game_info()

        if keyboard.is_pressed("r"):
            print("Resetting the game loop.")
            reset_game()
        """

        # mud.send_message(id, "[TURN_CYCLE]")
        cpu_cycle = time.sleep(0.2)
        cpu_cycle # cycle the game loop without consuming 100% CPU

        mud.update() # tick/update the state of the MUD server

        for id in mud.get_new_players():

            players[id] = {
                "name": None,
                "echo": None,
                "room": None,
                "area": None,
                "uppercase_name": format(["name"][0].upper()) + format(["name"][1:])
            }

            print()
            print("New player connected with ID:", id)
            print("---")
            print("Sending MOTD to new player with ID:", id)
            print()

            week_count = time.strftime("%U")
            dotw = time.strftime("%A")

            # upcoming adventure art
            mud.ascii_art(week=week_count, day=dotw)

            mud.title("Grey Forest")
            mud.motd(week=week_count, day=dotw)

            mud.send_message(id, "Please enter your name:")
            mud.send_message(id, "")

        for id in mud.get_disconnected_players():

            # if for any reason the player isn't in the player map, skip them and move on to the next one
            if id not in players:
                continue

            # go through all the players in the game
            for pid, pl in players.items():
                log_box_top    = "----------" + len(players[id]["uppercase_name"]) * "-" + (64 - len(players[id]["uppercase_name"])) * "-" + "--->-X"
                log_box_middle = "  [GAME]  " +     players[id]["uppercase_name"]        + " has disconnected from the server."
                log_box_bottom = "----------" + len(players[id]["uppercase_name"]) * "-" + (64 - len(players[id]["uppercase_name"])) * "-" + "--->-X"

                # send each player a message to tell them about the diconnected player
                mud.send_message(pid, log_box_top)
                mud.send_message(pid, log_box_middle)
                mud.send_message(pid, log_box_bottom)

            save_player_position(players[id])

            # remove the player's entry in the player dictionary
            del(players[id])

            print()
            print("Player disconnected with ID:", id)
            print("---")

        # go through any new commands sent from players
        for id, command, params in mud.get_commands():

            # if for any reason the player isn't in the player map, skip them and move on to the next one
            if id not in players:
                continue

            # if the player hasn't given their name yet, use this first command as their name and move them to the starting room.
            if players[id]["name"] is None:
                current_room = attempt_load(command, expected_field="current_room")
                description = attempt_load(command, expected_field="description")

                players[id]["name"] = command
                players[id]["uppercase_name"] = players[id]["name"][0].upper() + players[id]["name"][1:]
                players[id]["description"] = description
                players[id]["echo_content"] = "An exceptional actor"
                players[id]["echo"] = players[id]["echo_content"]
                players[id]["room"] = current_room or "Tavern"
                players[id]["area"] = rooms[players[id]["room"]]["area"]

                # go through all the players in the game
                for pid, pl in players.items():
                    # send each player a message to tell them about the new player
                    mud.send_message(pid, "{} entered the game".format(players[id]["uppercase_name"]))

                # send the new player a welcome message
                mud.send_message(id, "Welcome to the game, {}. ".format(players[id]["uppercase_name"])
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
                mud.send_message(id, "  look (l)       - Examines the "
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
                                                    players[id]["uppercase_name"], params))

            # 'look' command
            elif command == "look" or command == "l":

                # store the player's current room
                rm = rooms[players[id]["room"]]

                # send the player back the description of their current room
                mud.look(id, rm, focus="high")

                # (name, echo) pairs, sorted by name, so each echo stays with its name
                playershere = sorted(
                    (pl["name"], pl["echo"])
                    for pl in players.values()
                    if pl["room"] == players[id]["room"] and pl["name"] is not None
                )
                names = [name for name, _ in playershere]
                echoes = [echo for _, echo in playershere]

                # send player a message containing the list of players in the room
                mud.send_message(id, "-" * 80)
                mud.send_message(id, "Players/actors here:")
                for pl in playershere:
                    mud.send_message(id, "{}, {}".format(pl[1], pl[0]))
                mud.send_message(id, "-" * 80)

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
                                                        players[id]["uppercase_name"], ex,
                                                        players[id]["uppercase_name"], emote_text))

                        elif players[pid]["room"] == players[id]["room"] \
                                and pid != id:

                            mud.send_message(pid, "{} left towards '{}'.".format(
                                                        players[id]["uppercase_name"], ex))

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
                                            "{} {}".format(
                                                        players[id]["uppercase_name"], "entered the room."))

                    # send the player a message telling them where they are now
                    mud.send_message(id, "{}".format(
                                                            rooms[players[id]["room"]]["into_event"]))

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
                                                    players[id]["uppercase_name"], params))

            # !!!NEW!!!
            elif command == "gush":
                gush_text = params
                emote_listener = EmoteListener()
                emote_listener.notify(gush_text)

                same_area = [pid for pid in players
                            if players[pid]["area"] == players[id]["area"]]
                for pid in get_recipients(command, id, same_area):
                    mud.send_message(pid, "Somewhere nearby...\n...{} {}".format(
                                                players[id]["uppercase_name"], params))

            elif command == "quit" or command == "q" or command == "QUIT":
                mud.send_message(id, "Goodbye!")
                # Perform any necessary cleanup for the player here
                save_player(players[id])
                for pid in players:
                    if pid != id:
                        mud.send_message(pid, "[GAME] {} left the game.".format(
                                                            players[id]["uppercase_name"]))
                del players[id]
                mud.disconnect_client(id)

            # some other, unrecognised command
            else:
                # send back an 'unknown command' message
                mud.send_message(id, "Unknown command '{}'".format(command))
