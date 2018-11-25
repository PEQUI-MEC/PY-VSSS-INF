import unittest
from strategy import Athena
from strategy import Warrior
from helpers.endless import Endless


class TestAthena(unittest.TestCase):
    # TODO testar casos de falha

    numRobots = 3
    fieldWidth = 640
    fieldHeight = 480
    defaultVel = 0.8

    def testSetup(self):
        """
        Testa a interface do setup da athena
        """

        athena = Athena()

        self.assertTrue(athena.setup(TestAthena.numRobots,
                                     TestAthena.fieldWidth,
                                     TestAthena.fieldHeight,
                                     TestAthena.defaultVel))

    def testReset(self):
        """
        Testa o reset do estado da athena sem resetar sua configuração
        """

        athena = Athena()
        athena.setup(TestAthena.numRobots,
                     TestAthena.fieldWidth,
                     TestAthena.fieldHeight,
                     TestAthena.defaultVel)

        self.assertEqual(athena.reset(), 0)

    def testGetTargets(self):
        """
        Testa o formato da resposta do getTargets
        """

        athena = Athena()
        athena.setup(TestAthena.numRobots,
                     TestAthena.fieldWidth,
                     TestAthena.fieldHeight,
                     TestAthena.defaultVel)

        positions = [
            [
                {
                    "position": (Endless.goalieLine, Endless.midField[1]),
                    "orientation": 0.5,
                    "robotLetter": "A"
                },
                {
                    "position": (Endless.areaLine, Endless.midField[1]),
                    "orientation": 0.5,
                    "robotLetter": "B"
                },
                {
                    "position": (Endless.midField[0] - Endless.robotSize, Endless.midField[1]),
                    "orientation": 0.5,
                    "robotLetter": "C"
                }
            ],
            [
                {
                    "position": (Endless.width - Endless.goalieLine, Endless.midField[1])
                },
                {
                    "position": (Endless.width - Endless.areaLine, Endless.midField[1])
                },
                {
                    "position": (Endless.midField[0] + Endless.robotSize, Endless.midField[1])
                }
            ],
            {
                "position": Endless.midField
            }
        ]

        commands = athena.getTargets(positions, True)

        self.assertEqual(type(commands), type([]))

        for warrior in commands:
            self.assertEqual(type(warrior), type({}))
            self.assertIn("robotLetter", warrior)
            self.assertIn("command", warrior)

            if warrior["command"] is not "stop":
                self.assertIn("data", warrior)

                if warrior["command"] == "goTo":
                    self.assertIn("pose", warrior["data"])
                    self.assertIn("target", warrior["data"])
                    self.assertIn("velocity", warrior["data"])

                elif warrior["command"] == "lookAt":
                    self.assertIn("pose", warrior["data"])
                    self.assertIn("target", warrior["data"])
                    self.assertIn("velocity", warrior["data"])

                elif warrior["command"] == "spin":
                    self.assertIn("velocity", warrior["data"])
                    self.assertIn("direction", warrior["data"])

    def testMath(self):
        """
        Testa funções matemáticas embutidas
        """

        athena = Athena()
        athena.setup(TestAthena.numRobots,
                     TestAthena.fieldWidth,
                     TestAthena.fieldHeight,
                     TestAthena.defaultVel)

        positions = [
            [
                {
                    "position": (Endless.goalieLine, Endless.midField[1]),
                    "orientation": 0.5,
                    "robotLetter": "A"
                },
                {
                    "position": (Endless.areaLine, Endless.midField[1]),
                    "orientation": 0.5,
                    "robotLetter": "B"
                },
                {
                    "position": (Endless.midField[0] - Endless.robotSize, Endless.midField[1]),
                    "orientation": 0.5,
                    "robotLetter": "C"
                }
            ],
            [
                {
                    "position": (Endless.width - Endless.goalieLine, Endless.midField[1])
                },
                {
                    "position": (Endless.width - Endless.areaLine, Endless.midField[1])
                },
                {
                    "position": (Endless.midField[0] + Endless.robotSize, Endless.midField[1])
                }
            ],
            {
                "position": Endless.midField
            }
        ]

        # chama uma vez para inicializar o estado
        athena.getTargets(positions, True)

        testWarrior = Warrior()
        testWarrior.position = (0, Endless.midField[1])

        self.assertAlmostEqual(athena.distanceToBall(testWarrior), Endless.midField[0])
        self.assertAlmostEqual(athena.distanceToGoal(testWarrior), Endless.ourGoal[0])
        self.assertAlmostEqual(athena.timeToArrive((0, 0), (0, 100), 1), 100 / Endless.pixelMeterRatio)
        # TODO testar ballInterceptLocation (não está pronto) e valores diferentes para funções básicas

    def testSetters(self):
        """
        Testa interface de configuração
        """

        # prepara a athena
        athena = Athena()
        athena.setup(TestAthena.numRobots,
                     TestAthena.fieldWidth,
                     TestAthena.fieldHeight,
                     TestAthena.defaultVel)

        # testes mais profundos
        positions = [
            [
                {
                    "position": (Endless.goalieLine, Endless.midField[1]),
                    "orientation": 0.5,
                    "robotLetter": "A"
                },
                {
                    "position": (Endless.areaLine, Endless.midField[1]),
                    "orientation": 0.5,
                    "robotLetter": "B"
                },
                {
                    "position": (Endless.midField[0] - Endless.robotSize, Endless.midField[1]),
                    "orientation": 0.5,
                    "robotLetter": "C"
                }
            ],
            [
                {
                    "position": (Endless.width - Endless.goalieLine, Endless.midField[1])
                },
                {
                    "position": (Endless.width - Endless.areaLine, Endless.midField[1])
                },
                {
                    "position": (Endless.midField[0] + Endless.robotSize, Endless.midField[1])
                }
            ],
            {
                "position": Endless.midField
            }
        ]

        # set papeis
        roles = ["Attack", "Goalkeeper", "Defense"]
        self.assertEqual(athena.setRoles(roles), roles)

        # set transições ou posições fixas
        # testa se papeis realmente não mudam (pela ordem e pelas posições passadas, devia mudar
        self.assertFalse(athena.setTransitionsState(False))
        athena.getTargets(positions, True)  # atualiza estado
        self.assertEqual(athena.analyzeAndSetRoles(), roles)
        # agora testa se muda
        self.assertTrue(athena.setTransitionsState(True))
        athena.getTargets(positions, True)  # atualiza estado
        self.assertNotEqual(athena.analyzeAndSetRoles(), roles)

        # set velocidades
        velocities = [0.6, 0.5, 0.4]
        self.assertEqual(athena.setVelocities(velocities), velocities)
        # pra velocidades basta testar o defaultVel de cada robô de acordo com o papel
        athena.getTargets(positions, True)  # atualiza estado
        for warrior in athena.warriors:
            if warrior.role == "Attack":
                self.assertEqual(warrior.defaultVel, velocities[0])
            elif warrior.role == "Defense":
                self.assertEqual(warrior.defaultVel, velocities[1])
            elif warrior.role == "Goalkeeper":
                self.assertEqual(warrior.defaultVel, velocities[2])

        # força os robôs mudarem de ordem e testa se as velocidades se mantêm (transições estavam ligadas)
        athena.setTransitionsState(False)
        athena.getTargets(positions, True)  # atualiza estado
        for warrior in athena.warriors:
            if warrior.role == "Attack":
                self.assertEqual(warrior.defaultVel, velocities[0])
            elif warrior.role == "Defense":
                self.assertEqual(warrior.defaultVel, velocities[1])
            elif warrior.role == "Goalkeeper":
                self.assertEqual(warrior.defaultVel, velocities[2])


if __name__ == '__main__':
    unittest.main()
