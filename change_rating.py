import json

def load():
    rating = open("rating.txt", "r")
    table  = json.loads(rating.read())
    rating.close()
    return table

def load_cmd():
    cmdf = open("cmd.txt", "r")
    cmdlist = json.loads(cmdf.read())
    cmdf.close()
    return cmdlist

def save(table):
    rating = open("rating.txt", "w")
    rating.write(json.dumps(table))
    rating.close()
#    print(json.dumps(table, sort_keys=True, indent=4))
    print("Rating updated!")

def add_player(name, games=0, tournaments=0, rating=1200):
    table = load()
    table[name] = [name, games, tournaments, rating]
    save(table)

def e_game(r_a, r_b):
    return 1 / (1 + 10**((r_b - r_a) / 400))

def k_player(r):
    if r >= 2400:
        return 10
    elif r < 2400:
        return 20

def add_result(w_name, b_name, w_points):
    table = load()
    table[w_name][1] += 1
    table[b_name][1] += 1
    r_w, r_b = table[w_name][3], table[b_name][3]
    if table[w_name][1] < 30:
        k_w = 30
    else:
        k_w = k_player(r_w)
    if table[b_name][1] < 30:
        k_b = 30
    else:
        k_b = k_player(r_b)

    e_w = e_game(r_w, r_b)
    e_b = e_game(r_b, r_w)

    r_wn = r_w + k_w * (w_points - e_w)
    r_bn = r_b + k_b * (1 - w_points - e_b)

    table[w_name][3] = int(r_wn)
    table[b_name][3] = int(r_bn)
    save(table)
    print("Results added!")

def add_tournament(name):
    table = load()
    table[name][2] += 1
    save(table)
    print("Tournament added!")

def show_table(table):
    print("{} | {} | {} | {}".format("Фамилия И.".ljust(15, " "), "Игры".rjust(5, " "), "Турн.".rjust(5, " "), "ELO".rjust(4, " ")))
    print("-" * 38)
    for i in sorted(table.items()):
        print("{} | {} | {} | {}".format(i[1][0].ljust(15, " "), str(i[1][1]).rjust(5, " "), str(i[1][2]).rjust(5, " "), str(i[1][3]).rjust(4, " ")))
        print("=" * 38)

cmd_list = load_cmd()

while True:
    table = load()
    cmd = input("> ")
    if cmd == "help":
        print(*sorted(cmd_list.items()), sep="\n")
    elif cmd == "reg":
        name = input("Фамилия И.> ")
        if name not in table:
            add_player(name)
        add_tournament(name)
    elif cmd == "game":
        wname, bname = input("Игрок белыми> "), input("Игрок черными> ")
        wscore = float(input("Очки белых (1, 0.5, 0)> "))
        add_result(wname, bname, wscore)
    elif cmd == "exit":
        save(table)
        break
    elif cmd == "table":
        show_table(table)
    else:
        print("Type 'help' for command list.")
