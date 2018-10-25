import threading
from mujoco_py import load_model_from_path, MjSim, MjViewer
import math
import time
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
    """Traz o valor pra positivo e multiplica pela proporção (largura máxima)/(posição x máxima)

    Args:
         coord: Coordenada da posição no mundo da simulação a ser convertida

    Returns:
        Coordenada da posição na proporção utilizada pela estratégia
    """
    return (coord + 0.8083874182591296) * field_width / 1.6167748365182593


def convertPositionY(coord):
    """Traz o valor pra positivo e multiplica pela proporção (altura máxima)/(posição y máxima)

    Args:
        coord: Coordenada da posição no mundo da simulação a ser convertida

    Returns:
        Coordenada da posição na proporção utilizada pela estratégia
    """
    return (coord + 0.58339083) * field_height / 1.16678166


def convertVelocity(vel):
    return vel * 10


def generatePositions(team):
    """Cria o vetor de posições no formato esperado pela estratégia
    O 'sim.data.qpos' possui, em cada posição, o seguinte:
        0: pos X
        1: pos Y
        2: pos Z
        3: quat component w
        4: quat component x
        5: quat component y
        6: quat component z

    Returns:
        Vetor de posições no formato correto
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


# LOOP PRINCIPAL
def loop():
    while True:
        commands1 = athena1.getTargets(generatePositions(0))
        commands2 = athena2.getTargets(generatePositions(1))
        velocities1 = zeus1.getVelocities(commands1)
        velocities2 = zeus2.getVelocities(commands2)

        sim.data.ctrl[0] = convertVelocity(velocities1[0]["vLeft"])
        sim.data.ctrl[1] = convertVelocity(velocities1[0]["vRight"])
        sim.data.ctrl[2] = convertVelocity(velocities1[1]["vLeft"])
        sim.data.ctrl[3] = convertVelocity(velocities1[1]["vRight"])
        sim.data.ctrl[4] = convertVelocity(velocities1[2]["vLeft"])
        sim.data.ctrl[5] = convertVelocity(velocities1[2]["vRight"])
        sim.data.ctrl[6] = convertVelocity(velocities2[0]["vLeft"])
        sim.data.ctrl[7] = convertVelocity(velocities2[0]["vRight"])
        sim.data.ctrl[8] = convertVelocity(velocities2[1]["vLeft"])
        sim.data.ctrl[9] = convertVelocity(velocities2[1]["vRight"])
        sim.data.ctrl[10] = convertVelocity(velocities2[2]["vLeft"])
        sim.data.ctrl[11] = convertVelocity(velocities2[2]["vRight"])
        time.sleep(0.0001)


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
athena1 = Athena()
athena2 = Athena()
zeus1 = Zeus()
zeus2 = Zeus()
athena1.setup(3, field_width, field_height, 0.8)
athena2.setup(3, field_width, field_height, 0.8)
zeus1.setup(3)
zeus2.setup(3)

# inicializa o loop dos dados
loopThread = threading.Thread(target=loop)
loopThread.start()

while True:
    sim.step()
    viewer.render()
