import os


def have_py(list_files):
    for file in list_files:
        if file.find('.py') != -1:
            return True
    return False


gen = os.walk('main')
list_dir = [d for d, _, list_files in gen if have_py(list_files)]
list_dir.sort()
with open("output", "w", encoding="UTF-8") as file:
    file.write("\n".join(list_dir))
