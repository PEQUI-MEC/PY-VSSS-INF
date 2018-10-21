from strategy import Athena
from control import Zeus
from mujoco_py import load_model_from_path, MjSim, MjViewer

"""
Deus do espaço e do paraíso
Faz a conexão entre o simulador e os módulos do programa
"""

# DEFINIÇÕES
field_width = 640
field_height = 480


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


def generatePositions():
    return [
        [  # robôs aliados
            {
                "position": (convertPositionX(sim.data.qpos[robot_joints[0]]),
                             convertPositionY(sim.data.qpos[robot_joints[0] + 1])),
                "orientation": sim.data.qpos[robot_joints[0] + 3]  # TODO colocar a orientação no formato correto
            },
            {
                "position": (convertPositionX(sim.data.qpos[robot_joints[1]]),
                             convertPositionY(sim.data.qpos[robot_joints[1] + 1])),
                "orientation": sim.data.qpos[robot_joints[1] + 3]
            },
            {
                "position": (convertPositionX(sim.data.qpos[robot_joints[2]]),
                             convertPositionY(sim.data.qpos[robot_joints[2] + 1])),
                "orientation": sim.data.qpos[robot_joints[2] + 3]
            }
        ],
        [  # robôs adversários
            {
                "position": (convertPositionX(sim.data.qpos[robot_joints[3]]),
                             convertPositionY(sim.data.qpos[robot_joints[3] + 1])),
            },
            {
                "position": (convertPositionX(sim.data.qpos[robot_joints[4]]),
                             convertPositionY(sim.data.qpos[robot_joints[4] + 1])),
            },
            {
                "position": (convertPositionX(sim.data.qpos[robot_joints[5]]),
                             convertPositionY(sim.data.qpos[robot_joints[5] + 1])),
            }
        ],
        {  # bola
            "position": (convertPositionX(sim.data.qpos[ball_joint]),
                         convertPositionY(sim.data.qpos[ball_joint + 1]))
        }
    ]


# CALLBACKS
def athenaReady(strategyInfo):
    zeus.getVelocities(strategyInfo)


def zeusReady(velocities):
    sim.data.ctrl[0] = velocities[0]["vLeft"]
    sim.data.ctrl[1] = velocities[0]["vRight"]
    sim.data.ctrl[2] = velocities[1]["vLeft"]
    sim.data.ctrl[3] = velocities[1]["vRight"]
    sim.data.ctrl[4] = velocities[2]["vLeft"]
    sim.data.ctrl[5] = velocities[2]["vRight"]

    sim.step()
    viewer.render()

    # refaz o ciclo
    athena.getTargets(generatePositions())


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
athena = Athena(athenaReady)
zeus = Zeus(zeusReady)
athena.setup(3, field_width, field_height, 1.0)
zeus.setup(3)

# inicializa a cascata
athena.getTargets(generatePositions())
