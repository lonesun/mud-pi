"""Micro utility to convert text file lines into MUD send_message commands."""


def to_mud(mud, to, file_path):
    # latin1 matches the encoding MudServer uses when sending, so every byte round-trips
    with open(file_path, "r", encoding="latin1") as f:
        for line in f:
            mud.send_message(to, line.rstrip("\r\n"))
