from xml.etree import ElementTree


def count_brick_values(brick, level):
    color_values[brick.attrib['color']] += level
    for below in brick:
        count_brick_values(below, level + 1)


root = ElementTree.fromstring(input())
color_values = {'red': 0, 'green': 0, 'blue': 0}
count_brick_values(root, 1)
print(str(color_values['red']) + ' ' + str(color_values['green']) + ' ' + str(color_values['blue']))
