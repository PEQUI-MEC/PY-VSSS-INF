from strategy import Athena
from control import Zeus
from mujoco_py import load_model_from_path, MjSim, MjViewer

"""
Deus do espaço e do paraíso
Faz a conexão entre o simulador e os módulos do programa
"""

# prepara a simulação
model = load_model_from_path("simulator/scene.xml")
sim = MjSim(model)
viewer = MjViewer(sim)


# define os métodos circulares
def athenaReady(strategyInfo):
    zeus.getVelocities(strategyInfo)


def zeusReady(velocities):
    # TODO conectar o atuador
    # sim.data.ctrl[0] = velocities
    # sim.data.ctrl[1] = velocities
    sim.step()
    viewer.render()

    # refaz o ciclo
    # athena.getTargets(sim.positions)


# prepara os módulos
athena = Athena(athenaReady)
zeus = Zeus(zeusReady)

# inicializa a cascata
# TODO pegar variáveis e posições do mujoco
# athena.getTargets(sim.positions)
