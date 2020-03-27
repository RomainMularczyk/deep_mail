import pickle

with open("filters/update", "wb") as update_file:
    dump_update = pickle.Pickler(update_file)
    dump_update.dump("Sun, 01 Mar 2020 00:01:00 +0000")

with open("filters/update", "rb") as update_file:
    read_update = pickle.Unpickler(update_file, encoding="utf-8").load()
    print(read_update)