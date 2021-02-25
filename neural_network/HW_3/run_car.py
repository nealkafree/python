# from HW_3.cars import *
from neural_network.HW_3.cars.world import SimpleCarWorld
from neural_network.HW_3.cars.agent import SimpleCarAgent
from neural_network.HW_3.cars.physics import SimplePhysics
from neural_network.HW_3.cars.track import generate_map
import numpy as np
import random

import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-s", "--steps", type=int)
parser.add_argument("-f", "--filename", type=str)
parser.add_argument("-e", "--evaluate", type=bool)
parser.add_argument("--seed", type=int)
args = parser.parse_args()

print(args.steps, args.seed, args.filename, args.evaluate)


seed = args.seed if args.seed else 3
np.random.seed(seed)
random.seed(seed)
m = generate_map(8, 5, 3, 3)

# steps = args.steps
steps = 500
# filename = args.filename
filename = 'network_config_agent_0_layers_17_35_35_11_1.txt'
evaluate = args.evaluate
# evaluate = True

if filename:
    agent = SimpleCarAgent.from_file(filename)
    w = SimpleCarWorld(1, m, SimplePhysics, SimpleCarAgent, timedelta=0.2)
    if evaluate:
        print(w.evaluate_agent(agent))
    else:
        w.set_agents([agent])
        w.run(steps)
else:
    SimpleCarWorld(1, m, SimplePhysics, SimpleCarAgent, timedelta=0.2).run(steps)
