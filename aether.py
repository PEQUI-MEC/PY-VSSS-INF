import threading
from mujoco_py import load_model_from_path, MjSim, MjViewer
import math
import pprint  # pra printar bonitinho

from strategy import Athena
from control import Zeus

"""
Deus do espaço e do paraíso
Faz a conexão entre o simulador e os módulos do programa
"""

# DEFINIÇÕES
field_width = 640
field_height = 480
pp = pprint.PrettyPrinter(indent=4)


# FUNÇÕES
def convertPositionX(coord):
    """
    Traz o valor pra positivo e multiplica pela proporção (largura máxima)/(posição x máxima)
    :param coord: Coordenada da posição no mundo da simulação a ser convertida
    :return: Coordenada da posição na proporção utilizada pela estratégia
    """
    return (coord + 0.8083874182591296) * field_width / 1.6167748365182593


def convertPositionY(coord):
    """
    Traz o valor pra positivo e multiplica pela proporção (altura máxima)/(posição y máxima)
    :param coord: Coordenada da posição no mundo da simulação a ser convertida
    :return: Coordenada da posição na proporção utilizada pela estratégia
    """
    return (coord + 0.8083874182591296) * field_height / 1.6167748365182593


def convertVelocity(vel):
    return vel * 10


def generatePositions(team):
    """
    Cria o vetor de posições no formato esperado pela estratégia
    O 'sim.data.qpos' possui, em cada posição, o seguinte:
        0: pos X
        1: pos Y
        2: pos Z
        3: mat rotation X
        4: mat rotation Y
        5: mat rotation Z
        6: quat rotation X
        7: quat rotation Y
        8: quat rotation Z
    :return: Vetor de posições no formato correto
    """
    r1 = -math.atan2(
        2 * (
                sim.data.qpos[robot_joints[3 * team] + 3] * sim.data.qpos[robot_joints[3 * team] + 6] +
                sim.data.qpos[robot_joints[3 * team] + 4] * sim.data.qpos[robot_joints[3 * team] + 6]
        ),
        1 - 2 * (
                sim.data.qpos[robot_joints[3 * team] + 5] * sim.data.qpos[robot_joints[3 * team] + 5] +
                sim.data.qpos[robot_joints[3 * team] + 6] * sim.data.qpos[robot_joints[3 * team] + 6]
        )
    )
    r2 = -math.atan2(
        2 * (
                sim.data.qpos[robot_joints[1 + 3 * team] + 3] * sim.data.qpos[robot_joints[1 + 3 * team] + 6] +
                sim.data.qpos[robot_joints[1 + 3 * team] + 4] * sim.data.qpos[robot_joints[1 + 3 * team] + 6]
        ),
        1 - 2 * (
                sim.data.qpos[robot_joints[1 + 3 * team] + 5] * sim.data.qpos[robot_joints[1 + 3 * team] + 5] +
                sim.data.qpos[robot_joints[1 + 3 * team] + 6] * sim.data.qpos[robot_joints[1 + 3 * team] + 6]
        )
    )
    r3 = -math.atan2(
        2 * (
                sim.data.qpos[robot_joints[2 + 3 * team] + 3] * sim.data.qpos[robot_joints[2 + 3 * team] + 6] +
                sim.data.qpos[robot_joints[2 + 3 * team] + 4] * sim.data.qpos[robot_joints[2 + 3 * team] + 6]
        ),
        1 - 2 * (
                sim.data.qpos[robot_joints[2 + 3 * team] + 5] * sim.data.qpos[robot_joints[2 + 3 * team] + 5] +
                sim.data.qpos[robot_joints[2 + 3 * team] + 6] * sim.data.qpos[robot_joints[2 + 3 * team] + 6]
        )
    )
    return [
        [  # robôs aliados
            {
                "position": (convertPositionX(sim.data.qpos[robot_joints[3 * team]]),
                             convertPositionY(sim.data.qpos[robot_joints[3 * team] + 1])),
                "orientation": r1
            },
            {
                "position": (convertPositionX(sim.data.qpos[robot_joints[1 + 3 * team]]),
                             convertPositionY(sim.data.qpos[robot_joints[1 + 3 * team] + 1])),
                "orientation": r2
            },
            {
                "position": (convertPositionX(sim.data.qpos[robot_joints[2 + 3 * team]]),
                             convertPositionY(sim.data.qpos[robot_joints[2 + 3 * team] + 1])),
                "orientation": r3
            }
        ],
        [  # robôs adversários
            {
                "position": (convertPositionX(sim.data.qpos[robot_joints[(3 + 3 * team) % 6]]),
                             convertPositionY(sim.data.qpos[robot_joints[(3 + 3 * team) % 6] + 1])),
            },
            {
                "position": (convertPositionX(sim.data.qpos[robot_joints[(4 + 3 * team) % 6]]),
                             convertPositionY(sim.data.qpos[robot_joints[(4 + 3 * team) % 6] + 1])),
            },
            {
                "position": (convertPositionX(sim.data.qpos[robot_joints[(5 + 3 * team) % 6]]),
                             convertPositionY(sim.data.qpos[robot_joints[(5 + 3 * team) % 6] + 1])),
            }
        ],
        {  # bola
            "position": (convertPositionX(sim.data.qpos[ball_joint]),
                         convertPositionY(sim.data.qpos[ball_joint + 1]))
        }
    ]


# CALLBACKS
def athena1Ready(strategyInfo):
    pp.pprint(strategyInfo)
    zeusThread = threading.Thread(target=zeus1.getVelocities, args=[strategyInfo])
    zeusThread.start()


def athena2Ready(strategyInfo):
    zeusThread = threading.Thread(target=zeus2.getVelocities, args=[strategyInfo])
    zeusThread.start()


def zeus1Ready(velocities):
    sim.data.ctrl[0] = convertVelocity(velocities[0]["vLeft"])
    sim.data.ctrl[1] = convertVelocity(velocities[0]["vRight"])
    sim.data.ctrl[2] = convertVelocity(velocities[1]["vLeft"])
    sim.data.ctrl[3] = convertVelocity(velocities[1]["vRight"])
    sim.data.ctrl[4] = convertVelocity(velocities[2]["vLeft"])
    sim.data.ctrl[5] = convertVelocity(velocities[2]["vRight"])

    # refaz o ciclo
    athenaThread = threading.Thread(target=athena1.getTargets, args=[generatePositions(0)])
    athenaThread.start()


def zeus2Ready(velocities):
    sim.data.ctrl[6] = convertVelocity(velocities[0]["vLeft"])
    sim.data.ctrl[7] = convertVelocity(velocities[0]["vRight"])
    sim.data.ctrl[8] = convertVelocity(velocities[1]["vLeft"])
    sim.data.ctrl[9] = convertVelocity(velocities[1]["vRight"])
    sim.data.ctrl[10] = convertVelocity(velocities[2]["vLeft"])
    sim.data.ctrl[11] = convertVelocity(velocities[2]["vRight"])

    # refaz o ciclo
    athenaThread = threading.Thread(target=athena2.getTargets, args=[generatePositions(1)])
    athenaThread.start()


# PREPARAÇÃO
model = load_model_from_path("simulator/scene.xml")
sim = MjSim(model)
viewer = MjViewer(sim)
ball_joint = sim.model.get_joint_qpos_addr("Ball")[0]
robot_joints = [
    sim.model.get_joint_qpos_addr("Robot_01")[0],
    sim.model.get_joint_qpos_addr("Robot_02")[0],
    sim.model.get_joint_qpos_addr("Robot_03")[0],
    sim.model.get_joint_qpos_addr("Robot_04")[0],
    sim.model.get_joint_qpos_addr("Robot_05")[0],
    sim.model.get_joint_qpos_addr("Robot_06")[0]
]

# EXECUÇÃO
# prepara os módulos
athena1 = Athena(athena1Ready)
athena2 = Athena(athena2Ready)
zeus1 = Zeus(zeus1Ready)
zeus2 = Zeus(zeus2Ready)
athena1.setup(3, field_width, field_height, 0.8)
athena2.setup(3, field_width, field_height, 0.8)
zeus1.setup(3)
zeus2.setup(3)

# inicializa a cascata
initThread1 = threading.Thread(target=athena1.getTargets, args=[generatePositions(0)])
initThread2 = threading.Thread(target=athena2.getTargets, args=[generatePositions(1)])
initThread1.start()
# initThread2.start() # TODO habilitar quando funcionar

while True:
    sim.step()
    viewer.render()
