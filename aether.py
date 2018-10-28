import threading
from mujoco_py import load_model_from_path, MjSim
import math
import time

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
        self.enabled = [True, True, True]
        self.athena1 = Athena()
        self.athena2 = Athena()
        self.zeus1 = Zeus()
        self.zeus2 = Zeus()
        self.athena1.setup(3, self.field_width, self.field_height, 0.8)
        self.athena2.setup(3, self.field_width, self.field_height, 0.8)
        self.zeus1.setup(3)
        self.zeus2.setup(3)

        # inicializa o loop dos dados
        loopThread1 = threading.Thread(target=self.loopTeam1)
        loopThread2 = threading.Thread(target=self.loopTeam2)
        loopThread1.daemon = True
        loopThread2.daemon = True
        loopThread1.start()
        # loopThread2.start()

    def run(self):
        while True:
            self.sim.step()
            self.viewer.render()

    def loopTeam1(self):
        while True:
            positions = self.generatePositions(0)
            commands1 = self.athena1.getTargets(positions)
            self.viewer.infos["robots"] = [
                "X: " + "{:.2f}".format(positions[2]["position"][0]) + ", Y: " + "{:.2f}".format(
                    positions[2]["position"][1]),

                "[OFF] " if not self.enabled[0] else "X: " + "{:.2f}".format(positions[0][0]["position"][0]) + ", Y: " +
                                                     "{:.2f}".format(positions[0][0]["position"][1]) + ", O: " +
                                                     "{:.2f}".format(positions[0][0]["orientation"]) +
                                                     " C: " + commands1[0]["command"],

                "[OFF] " if not self.enabled[1] else "X: " + "{:.2f}".format(positions[0][1]["position"][0]) + ", Y: " +
                                                     "{:.2f}".format(positions[0][1]["position"][1]) + ", O: " +
                                                     "{:.2f}".format(positions[0][1]["orientation"]) +
                                                     " C: " + commands1[1]["command"],

                "[OFF] " if not self.enabled[2] else "X: " + "{:.2f}".format(positions[0][2]["position"][0]) + ", Y: " +
                                                     "{:.2f}".format(positions[0][2]["position"][1]) + ", O: " +
                                                     "{:.2f}".format(positions[0][2]["orientation"]) +
                                                     " C: " + commands1[2]["command"],
            ]
            velocities1 = self.zeus1.getVelocities(commands1)

            if self.enabled[0]:
                self.sim.data.ctrl[0] = self.convertVelocity(velocities1[0]["vLeft"])
                self.sim.data.ctrl[1] = self.convertVelocity(velocities1[0]["vRight"])
            if self.enabled[1]:
                self.sim.data.ctrl[2] = self.convertVelocity(velocities1[1]["vLeft"])
                self.sim.data.ctrl[3] = self.convertVelocity(velocities1[1]["vRight"])
            if self.enabled[2]:
                self.sim.data.ctrl[4] = self.convertVelocity(velocities1[2]["vLeft"])
                self.sim.data.ctrl[5] = self.convertVelocity(velocities1[2]["vRight"])

            fps = self.getFPS()
            if fps is not None:
                self.viewer.infos["fps"] = fps

            time.sleep(0.026)  # fixa o fps em 30

    def loopTeam2(self):
        commands2 = self.athena2.getTargets(self.generatePositions(1))
        velocities2 = self.zeus2.getVelocities(commands2)
        self.sim.data.ctrl[6] = self.convertVelocity(velocities2[0]["vLeft"])
        self.sim.data.ctrl[7] = self.convertVelocity(velocities2[0]["vRight"])
        self.sim.data.ctrl[8] = self.convertVelocity(velocities2[1]["vLeft"])
        self.sim.data.ctrl[9] = self.convertVelocity(velocities2[1]["vRight"])
        self.sim.data.ctrl[10] = self.convertVelocity(velocities2[2]["vLeft"])
        self.sim.data.ctrl[11] = self.convertVelocity(velocities2[2]["vRight"])
        time.sleep(0.0001)

    # HELPERS
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
    def moveBall(self, direction):
        if direction == 0:  # UP
            self.sim.data.qpos[self.ball_joint + 1] += 0.01
        elif direction == 1:  # DOWN
            self.sim.data.qpos[self.ball_joint + 1] -= 0.01
        elif direction == 2:  # LEFT
            self.sim.data.qpos[self.ball_joint] -= 0.01
        elif direction == 3:  # RIGHT
            self.sim.data.qpos[self.ball_joint] += 0.01

    def convertPositionX(self, coord):
        """Traz o valor pra positivo e multiplica pela proporção (largura máxima)/(posição x máxima)

        Args:
             coord: Coordenada da posição no mundo da simulação a ser convertida

        Returns:
            Coordenada da posição na proporção utilizada pela estratégia
        """
        return (coord + 0.8083874182591296) * self.field_width / 1.6167748365182593

    def convertPositionY(self, coord):
        """Traz o valor pra positivo e multiplica pela proporção (altura máxima)/(posição y máxima)

        Args:
            coord: Coordenada da posição no mundo da simulação a ser convertida

        Returns:
            Coordenada da posição na proporção utilizada pela estratégia
        """
        return (coord + 0.58339083) * self.field_height / 1.16678166

    @staticmethod
    def convertVelocity(vel):
        return vel * 15

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
        r1 = -math.atan2(
            2 * (
                    self.sim.data.qpos[self.robot_joints[3 * team] + 3] * self.sim.data.qpos[self.robot_joints[3 * team] + 6] +
                    self.sim.data.qpos[self.robot_joints[3 * team] + 4] * self.sim.data.qpos[self.robot_joints[3 * team] + 6]
            ),
            1 - 2 * (
                    self.sim.data.qpos[self.robot_joints[3 * team] + 5] * self.sim.data.qpos[self.robot_joints[3 * team] + 5] +
                    self.sim.data.qpos[self.robot_joints[3 * team] + 6] * self.sim.data.qpos[self.robot_joints[3 * team] + 6]
            )
        )
        r2 = -math.atan2(
            2 * (
                    self.sim.data.qpos[self.robot_joints[1 + 3 * team] + 3] * self.sim.data.qpos[self.robot_joints[1 + 3 * team] + 6] +
                    self.sim.data.qpos[self.robot_joints[1 + 3 * team] + 4] * self.sim.data.qpos[self.robot_joints[1 + 3 * team] + 6]
            ),
            1 - 2 * (
                    self.sim.data.qpos[self.robot_joints[1 + 3 * team] + 5] * self.sim.data.qpos[self.robot_joints[1 + 3 * team] + 5] +
                    self.sim.data.qpos[self.robot_joints[1 + 3 * team] + 6] * self.sim.data.qpos[self.robot_joints[1 + 3 * team] + 6]
            )
        )
        r3 = -math.atan2(
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
                    "position": (self.convertPositionX(self.sim.data.qpos[self.robot_joints[3 * team]]),
                                 self.convertPositionY(self.sim.data.qpos[self.robot_joints[3 * team] + 1])),
                    "orientation": r1,
                    "robotLetter": "A"
                },
                {
                    "position": (self.convertPositionX(self.sim.data.qpos[self.robot_joints[1 + 3 * team]]),
                                 self.convertPositionY(self.sim.data.qpos[self.robot_joints[1 + 3 * team] + 1])),
                    "orientation": r2,
                    "robotLetter": "B"
                },
                {
                    "position": (self.convertPositionX(self.sim.data.qpos[self.robot_joints[2 + 3 * team]]),
                                 self.convertPositionY(self.sim.data.qpos[self.robot_joints[2 + 3 * team] + 1])),
                    "orientation": r3,
                    "robotLetter": "C"
                }
            ],
            [  # robôs adversários
                {
                    "position": (self.convertPositionX(self.sim.data.qpos[self.robot_joints[(3 + 3 * team) % 6]]),
                                 self.convertPositionY(self.sim.data.qpos[self.robot_joints[(3 + 3 * team) % 6] + 1])),
                },
                {
                    "position": (self.convertPositionX(self.sim.data.qpos[self.robot_joints[(4 + 3 * team) % 6]]),
                                 self.convertPositionY(self.sim.data.qpos[self.robot_joints[(4 + 3 * team) % 6] + 1])),
                },
                {
                    "position": (self.convertPositionX(self.sim.data.qpos[self.robot_joints[(5 + 3 * team) % 6]]),
                                 self.convertPositionY(self.sim.data.qpos[self.robot_joints[(5 + 3 * team) % 6] + 1])),
                }
            ],
            {  # bola
                "position": (self.convertPositionX(self.sim.data.qpos[self.ball_joint]),
                             self.convertPositionY(self.sim.data.qpos[self.ball_joint + 1]))
            }
        ]


if __name__ == "__main__":
    aether = Aether()
    aether.run()

