def read_file(path):
    with open(path, encoding="UTF-8") as file:
        return file.read().splitlines()


def write_file(path, data):
    with open(path, "w", encoding="UTF-8") as file:
        file.write(data)


text = read_file("dataset_24465_4.txt")
text.reverse()
write_file("output", "\n".join(text))
