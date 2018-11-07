import threading
from mujoco_py import load_model_from_path, MjSim
import math
import time
import numpy as np

from strategy import Athena
from control import Zeus
from simulator.viewer import Viewer


class Aether:
    """
    Deus do espaço e do paraíso
    Faz a conexão entre o simulador e os módulos do programa
    """

    def __init__(self):
        # DEFINIÇÕES
        self.field_width = 640
        self.field_height = 480
        self.cascadeTime = 0
        self.cascadeLoops = 1
        self.cascadeLastTime = 0

        # PREPARAÇÃO
        model = load_model_from_path("simulator/scene.xml")
        self.sim = MjSim(model)
        self.viewer = Viewer(self.sim, self)
        self.ball_joint = self.sim.model.get_joint_qpos_addr("Ball")[0]
        self.robot_joints = [
            self.sim.model.get_joint_qpos_addr("Robot_01")[0],
            self.sim.model.get_joint_qpos_addr("Robot_02")[0],
            self.sim.model.get_joint_qpos_addr("Robot_03")[0],
            self.sim.model.get_joint_qpos_addr("Robot_04")[0],
            self.sim.model.get_joint_qpos_addr("Robot_05")[0],
            self.sim.model.get_joint_qpos_addr("Robot_06")[0]
        ]

        # EXECUÇÃO
        # prepara os módulos
        self.enabled = [False] * 6  # [False, False, False, True, True, True]
        self.athena = [
            Athena(),
            Athena()
        ]
        self.zeus = [
            Zeus(),
            Zeus()
        ]
        self.athena[0].setup(3, self.field_width, self.field_height, 0.8)
        self.athena[1].setup(3, self.field_width, self.field_height, 0.8)
        self.zeus[0].setup(3)
        self.zeus[1].setup(3)

        # inicializa o loop dos dados
        self.pause = False
        self.loopThread1 = threading.Thread(target=self.loopTeam, args=[0])
        self.loopThread2 = threading.Thread(target=self.loopTeam, args=[1])
        self.loopThread1.daemon = True
        self.loopThread2.daemon = True
        self.loopThread1.start()
        self.loopThread2.start()

        self.showInfos(0)
        self.showInfos(1)

    def run(self):
        while True:
            self.sim.step()
            self.viewer.render()

    def loopTeam(self, team):
        while True:
            time.sleep(0.001)

            if self.pause or \
                    (not self.enabled[3 * team] and not self.enabled[3 * team + 1] and not self.enabled[3 * team + 2]):
                continue
            # executa nossos módulos
            positions = self.generatePositions(team)
            commands = self.athena[team].getTargets(positions)
            velocities = self.zeus[team].getVelocities(commands)
            # aplica resultados na simulação
            if self.enabled[0 + 3 * team]:
                self.sim.data.ctrl[0 + 6 * team] = self.convertVelocity(velocities[0]["vLeft"])
                self.sim.data.ctrl[1 + 6 * team] = self.convertVelocity(velocities[0]["vRight"])
            if self.enabled[1 + 3 * team]:
                self.sim.data.ctrl[2 + 6 * team] = self.convertVelocity(velocities[1]["vLeft"])
                self.sim.data.ctrl[3 + 6 * team] = self.convertVelocity(velocities[1]["vRight"])
            if self.enabled[2 + 3 * team]:
                self.sim.data.ctrl[4 + 6 * team] = self.convertVelocity(velocities[2]["vLeft"])
                self.sim.data.ctrl[5 + 6 * team] = self.convertVelocity(velocities[2]["vRight"])

            # mostra resultados
            self.showInfos(team, positions, commands)
            # indicadores 3D
            for i in range(3):
                position = positions[0][i]["position"]
                self.setObjectPose("indicator_" + str(i + 3 * team + 1), position, team, 0.2, velocities[i]["vector"])
                # self.setObjectPose("virtual_robot_1", velocities["virtualPos"], team=0)

    # HELPERS
    def showInfos(self, team, positions=None, commands=None):
        infos = []

        for i in range(3):
            if self.enabled[i + 3 * team] and positions and commands:
                # informações que todos os robôs tem
                robot = "X: " + "{:.1f}".format(positions[0][i]["position"][0])
                robot += ", Y: " + "{:.1f}".format(positions[0][i]["position"][1])
                robot += ", O: " + "{:.1f}".format(positions[0][i]["orientation"])
                robot += ", T: " + commands[i]["tactics"]
                robot += ", C: " + commands[i]["command"]

                if commands[i]["command"] == "lookAt":
                    if type(commands[i]["data"]["target"]) is tuple:
                        robot += "(" + "{:.1f}".format(commands[i]["data"]["target"][0]) + ", "
                        robot += "{:.1f}".format(commands[i]["data"]["target"][1]) + ")"
                    else:
                        robot += "(" + "{:.1f}".format(commands[i]["data"]["target"]) + ")"

                elif commands[i]["command"] == "goTo":
                    robot += "(" + "{:.1f}".format(commands[i]["data"]["target"]["position"][0]) + ", "
                    robot += "{:.1f}".format(commands[i]["data"]["target"]["position"][1]) + ", "

                    if type(commands[i]["data"]["target"]["orientation"]) is tuple:
                        robot += "(" + "{:.1f}".format(commands[i]["data"]["target"]["orientation"][0]) + ", "
                        robot += "{:.1f}".format(commands[i]["data"]["target"]["orientation"][1]) + ") )"
                    else:
                        robot += "{:.1f}".format(commands[i]["data"]["target"]["orientation"]) + ")"

                elif commands[i]["command"] == "spin":
                    robot += "(" + commands[i]["data"]["direction"] + ")"

            else:
                robot = "[OFF]"

            infos.append(robot)

        self.viewer.infos["robots" + str(team + 1)] = infos

        if team == 0:
            if positions:
                self.viewer.infos["ball"] = "X: " + "{:.2f}".format(positions[2]["position"][0]) + ", Y: " + \
                                            "{:.2f}".format(positions[2]["position"][1])
                fps = self.getFPS()
                if fps:
                    self.viewer.infos["fps"] = fps

            if commands:
                # indicadores 3D
                # print(commands[0]["futureBall"])
                self.setObjectPose("virtual_ball", commands[0]["futureBall"], 0, 0.022)
                for i in range(3):
                    if commands[i]["command"] == "goTo":
                        target = commands[i]["data"]["target"]["position"]
                        targetOrientation = commands[i]["data"]["target"]["orientation"]
                        if type(targetOrientation) is tuple:
                            position = positions[0][i]["position"]
                            targetOrientation = math.atan2(position[1] - targetOrientation[1],
                                                           -(position[0] - targetOrientation[0]))

                        self.setObjectPose("target_" + str(i + 1), target, 0, 0.01, targetOrientation)

    def getFPS(self):
        # calcula o fps e manda pra interface
        self.cascadeTime += time.time() - self.cascadeLastTime
        self.cascadeLoops += 1
        self.cascadeLastTime = time.time()
        if self.cascadeTime > 1:
            fps = self.cascadeLoops / self.cascadeTime
            self.cascadeTime = self.cascadeLoops = 0
            return "{:.2f}".format(fps)
        return None

    # FUNÇÕES
    def reset(self):
        for i in range(6):
            self.enabled[i] = False

        self.showInfos(0)
        self.showInfos(1)
        self.sim.reset()

    def startStop(self, pause):
        self.pause = pause

    def moveBall(self, direction, keepVel=False):
        if not keepVel:
            for i in range(6):
                self.sim.data.qvel[self.ball_joint + i] = 0

        if direction == 0:  # UP
            self.sim.data.qpos[self.ball_joint + 1] += 0.01
        elif direction == 1:  # DOWN
            self.sim.data.qpos[self.ball_joint + 1] -= 0.01
        elif direction == 2:  # LEFT
            self.sim.data.qpos[self.ball_joint] -= 0.01
        elif direction == 3:  # RIGHT
            self.sim.data.qpos[self.ball_joint] += 0.01

    def toggleRobot(self, robotId, moveOut=False):
        if self.sim.data.qpos[self.robot_joints[robotId] + 1] >= 1:
            self.enabled[robotId] = False
            if moveOut:
                self.sim.data.qpos[self.robot_joints[robotId] + 1] = 0
        elif moveOut:
            self.enabled[robotId] = False
            self.sim.data.qpos[self.robot_joints[robotId]] = -0.62 + 0.25 * robotId
            self.sim.data.qpos[self.robot_joints[robotId] + 1] = 1.5
            self.sim.data.qpos[self.robot_joints[robotId] + 2] = 0.04
            self.sim.data.ctrl[robotId] = self.sim.data.ctrl[robotId + 1] = 0
        elif self.enabled[robotId]:
            self.enabled[robotId] = False
            self.sim.data.ctrl[robotId] = self.sim.data.ctrl[robotId + 1] = 0
        else:
            self.enabled[robotId] = True

        self.showInfos(0 if robotId < 3 else 1)

    def convertPositionX(self, coord, team):
        """Traz o valor pra positivo e multiplica pela proporção (largura máxima)/(posição x máxima)

        Args:
             coord: Coordenada da posição no mundo da simulação a ser convertida
             team: Time que está pedindo a conversão (0 ou 1)
        Returns:
            Coordenada da posição na proporção utilizada pela estratégia
        """
        if team == 0:
            return (coord + 0.8083874182591296) * self.field_width / 1.6167748365182593
        else:
            return -(coord - 0.8083874182591296) * self.field_width / 1.6167748365182593

    def convertPositionY(self, coord, team):
        """Traz o valor pra positivo e multiplica pela proporção (altura máxima)/(posição y máxima)

        Args:
            coord: Coordenada da posição no mundo da simulação a ser convertida
            team: Time que está pedindo a conversão (0 ou 1)

        Returns:
            Coordenada da posição na proporção utilizada pela estratégia
        """
        if team == 0:
            return (coord + 0.58339083) * self.field_height / 1.16678166
        else:
            return -(coord - 0.58339083) * self.field_height / 1.16678166

    @staticmethod
    def convertVelocity(vel):
        return vel * 30

    def setObjectPose(self, objectName, newPos, team=0, height=0.04, newOrientation=0):
        """Seta a posição e orientação de um objeto no simulador
        Args:
            objectName: Nome do objeto a ter a pose alterada. Esse nome deve ser de um mocap configurado na cena.
                        Se o objeto for virtual_robot_i, o robô é amarelo se i <= 3, azul caso contrário
            newPos: (x, y), 'x' e 'y' valores em pixels
            team: índice do time (valor em pixels inverte de acordo com o time)
            height: altura do objeto no universo
            newOrientation: orientação Z em radianos do objeto
        """
        if team == 0:
            x = (newPos[0] / self.field_width) * 1.6167748365182593 - 0.8083874182591296
            y = (newPos[1] / self.field_height) * 1.16678166 - 0.58339083
        else:
            x = -(newPos[0] / self.field_width) * 1.6167748365182593 + 0.8083874182591296
            y = -(newPos[1] / self.field_height) * 1.16678166 + 0.58339083

        # conversão de eulerAngles para quaternions (wikipedia)
        newQuat = [math.sin(newOrientation / 2), 0, 0, math.cos(newOrientation / 2)]

        self.sim.data.set_mocap_quat(objectName, newQuat)
        self.sim.data.set_mocap_pos(objectName, np.array([x, y, height]))

    def generatePositions(self, team):
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
        r1 = math.pi * team - math.atan2(
            2 * (
                    self.sim.data.qpos[self.robot_joints[3 * team] + 3] * self.sim.data.qpos[self.robot_joints[3 * team] + 6] +
                    self.sim.data.qpos[self.robot_joints[3 * team] + 4] * self.sim.data.qpos[self.robot_joints[3 * team] + 6]
            ),
            1 - 2 * (
                    self.sim.data.qpos[self.robot_joints[3 * team] + 5] * self.sim.data.qpos[self.robot_joints[3 * team] + 5] +
                    self.sim.data.qpos[self.robot_joints[3 * team] + 6] * self.sim.data.qpos[self.robot_joints[3 * team] + 6]
            )
        )
        r2 = math.pi * team - math.atan2(
            2 * (
                    self.sim.data.qpos[self.robot_joints[1 + 3 * team] + 3] * self.sim.data.qpos[self.robot_joints[1 + 3 * team] + 6] +
                    self.sim.data.qpos[self.robot_joints[1 + 3 * team] + 4] * self.sim.data.qpos[self.robot_joints[1 + 3 * team] + 6]
            ),
            1 - 2 * (
                    self.sim.data.qpos[self.robot_joints[1 + 3 * team] + 5] * self.sim.data.qpos[self.robot_joints[1 + 3 * team] + 5] +
                    self.sim.data.qpos[self.robot_joints[1 + 3 * team] + 6] * self.sim.data.qpos[self.robot_joints[1 + 3 * team] + 6]
            )
        )
        r3 = math.pi * team - math.atan2(
            2 * (
                    self.sim.data.qpos[self.robot_joints[2 + 3 * team] + 3] * self.sim.data.qpos[self.robot_joints[2 + 3 * team] + 6] +
                    self.sim.data.qpos[self.robot_joints[2 + 3 * team] + 4] * self.sim.data.qpos[self.robot_joints[2 + 3 * team] + 6]
            ),
            1 - 2 * (
                    self.sim.data.qpos[self.robot_joints[2 + 3 * team] + 5] * self.sim.data.qpos[self.robot_joints[2 + 3 * team] + 5] +
                    self.sim.data.qpos[self.robot_joints[2 + 3 * team] + 6] * self.sim.data.qpos[self.robot_joints[2 + 3 * team] + 6]
            )
        )
        return [
            [  # robôs aliados
                {
                    "position": (self.convertPositionX(self.sim.data.qpos[self.robot_joints[3 * team]], team),
                                 self.convertPositionY(self.sim.data.qpos[self.robot_joints[3 * team] + 1], team)),
                    "orientation": r1,
                    "robotLetter": "A"
                },
                {
                    "position": (self.convertPositionX(self.sim.data.qpos[self.robot_joints[1 + 3 * team]], team),
                                 self.convertPositionY(self.sim.data.qpos[self.robot_joints[1 + 3 * team] + 1], team)),
                    "orientation": r2,
                    "robotLetter": "B"
                },
                {
                    "position": (self.convertPositionX(self.sim.data.qpos[self.robot_joints[2 + 3 * team]], team),
                                 self.convertPositionY(self.sim.data.qpos[self.robot_joints[2 + 3 * team] + 1], team)),
                    "orientation": r3,
                    "robotLetter": "C"
                }
            ],
            [  # robôs adversários
                {
                    "position": (self.convertPositionX(self.sim.data.qpos[self.robot_joints[(3 + 3 * team) % 6]], team),
                                 self.convertPositionY(self.sim.data.qpos[self.robot_joints[(3 + 3 * team) % 6] + 1], team)),
                },
                {
                    "position": (self.convertPositionX(self.sim.data.qpos[self.robot_joints[(4 + 3 * team) % 6]], team),
                                 self.convertPositionY(self.sim.data.qpos[self.robot_joints[(4 + 3 * team) % 6] + 1], team)),
                },
                {
                    "position": (self.convertPositionX(self.sim.data.qpos[self.robot_joints[(5 + 3 * team) % 6]], team),
                                 self.convertPositionY(self.sim.data.qpos[self.robot_joints[(5 + 3 * team) % 6] + 1], team)),
                }
            ],
            {  # bola
                "position": (self.convertPositionX(self.sim.data.qpos[self.ball_joint], team),
                             self.convertPositionY(self.sim.data.qpos[self.ball_joint + 1], team))
            }
        ]


if __name__ == "__main__":
    aether = Aether()
    aether.run()
