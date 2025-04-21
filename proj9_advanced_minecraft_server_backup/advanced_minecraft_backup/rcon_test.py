from my_mcrcon import MCRcon, RconPacket

def main():
    rcon_connection = MCRcon("192.168.4.28", "Dragon2002#")
    rcon_connection.connect()
    packet = rcon_connection.send_command("say Testing custom rcon implementation...")
    print(packet)
    packet = rcon_connection.send_command("stop")
    print(packet)
    rcon_connection.close_connection()

main()