import marshal, os
import logging

import uncompyle2


GAME_ENTITES_PATH = r"D:\MyGames\Revelation\res\entities_2024_09_02"
PROJECT_PATH = os.path.abspath(os.path.curdir)

logging.basicConfig(level=logging.INFO, filename="py_log.log",filemode="w",
                    format="%(asctime)s %(levelname)s %(message)s")

def add_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def get_file_paths(directory):
    file_paths = []
    for root, dirs, files in os.walk(directory):
        for name in files:
            file_paths.append(root + "\\" + name)

    return file_paths

def decompile(co, dest_path, src_path):
    dest_path = dest_path.replace(".o", ".py")

    src_dest_dir = os.path.abspath(os.path.curdir) + dest_path.split("entities")[1].split("/")[0]
    add_dir(src_dest_dir)

    src_dest_file = os.path.join(src_dest_dir, dest_path.split("/")[-1])

    with open(src_dest_file, "wb") as f:
        try:
            logging.info("Decompiling {} to {}.".format(src_path, src_dest_file))
            uncompyle2.uncompyle("2.7", co, out=f)
        except:
            logging.warning("Particially decompiled {}!".format(src_dest_file))

add_dir("decompiled_src")
os.chdir("decompiled_src")

file_paths = get_file_paths(GAME_ENTITES_PATH)
import sys
for i, file_path in enumerate(file_paths):
    print "[{}/{}] file - {}".format(i + 1, len(file_paths), file_path)

    with open(file_path, "rb") as f:
        file_bytes = f.read()
        if file_bytes.startswith("\x63\x00\x00\x00"):
            co = marshal.loads(file_bytes)
            decompile(co, co.co_filename, file_path)
