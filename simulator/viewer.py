from mujoco_py import MjViewer
from mujoco_py.generated import const
import glfw
from multiprocessing import Process
import imageio
import time


class Viewer(MjViewer):
    def __init__(self, sim, aether):
        super(Viewer, self).__init__(sim)
        self.infos = {}
        self.aether = aether
        glfw.set_key_callback(self.window, self.key_callback)

    def _create_full_overlay(self):
        # TOP LEFT

        if "ball" in self.infos:
            self.add_overlay(const.GRID_TOPLEFT, "Ball Pose", self.infos["ball"])

        if "robots1" in self.infos:
            self.add_overlay(const.GRID_TOPLEFT, "Robot [1]", self.infos["robots1"][0])
            self.add_overlay(const.GRID_TOPLEFT, "Robot [2]", self.infos["robots1"][1])
            self.add_overlay(const.GRID_TOPLEFT, "Robot [3]", self.infos["robots1"][2])

        if "robots2" in self.infos:
            self.add_overlay(const.GRID_TOPLEFT, "Robot [4]", self.infos["robots2"][0])
            self.add_overlay(const.GRID_TOPLEFT, "Robot [5]", self.infos["robots2"][1])
            self.add_overlay(const.GRID_TOPLEFT, "Robot [6]", self.infos["robots2"][2])

        # TOP RIGHT

        if self._paused is not None:
            if not self._paused:
                self.add_overlay(const.GRID_TOPRIGHT, "Stop", "[Space]")
            else:
                self.add_overlay(const.GRID_TOPRIGHT, "Start", "[Space]")
            self.add_overlay(const.GRID_TOPRIGHT,
                             "Advance simulation by one step", "[P]")

        self.add_overlay(const.GRID_TOPRIGHT, "Reset Simulation", "[Backspace]")

        if self._render_every_frame:
            self.add_overlay(const.GRID_TOPRIGHT, "", "")
        else:
            self.add_overlay(const.GRID_TOPRIGHT, "Run speed = %.3f x real time" %
                             self._run_speed, "[S]lower, [F]aster")
        self.add_overlay(
            const.GRID_TOPRIGHT, "Ren[d]er every frame", "Off" if self._render_every_frame else "On")
        self.add_overlay(const.GRID_TOPRIGHT, "Switch camera (#cams = %d)" % (self._ncam + 1),
                                              "[Tab] (camera ID = %d)" % self.cam.fixedcamid)
        self.add_overlay(const.GRID_TOPRIGHT, "[C]ontact forces", "Off" if self.vopt.flags[
                         10] == 1 else "On")
        self.add_overlay(
            const.GRID_TOPRIGHT, "Referenc[e] frames", "Off" if self.vopt.frame == 1 else "On")
        self.add_overlay(const.GRID_TOPRIGHT,
                         "T[r]ansparent", "On" if self._transparent else "Off")

        # BOTTOM LEFT

        if "fps" in self.infos:
            self.add_overlay(const.GRID_BOTTOMLEFT, "Team FPS", self.infos["fps"])

        if self._record_video:
            extra = " (while video is not recorded)"
        else:
            extra = ""
        self.add_overlay(const.GRID_BOTTOMLEFT, "FPS", "%d%s" %
                         (1 / self._time_per_render, extra))
        self.add_overlay(const.GRID_BOTTOMLEFT, "Solver iterations", str(
            self.sim.data.solver_iter + 1))

        # BOTTOM RIGHT

        self.add_overlay(const.GRID_BOTTOMRIGHT, "[H]ide Menu", "")

        self.add_overlay(const.GRID_BOTTOMRIGHT, "Cap[t]ure frame", "")
        if self._image_idx > 0:
            fname = self._image_path % (self._image_idx - 1)
            self.add_overlay(const.GRID_BOTTOMRIGHT, "   saved as %s" % fname, "")

        if self._record_video:
            ndots = int(7 * (time.time() % 1))
            dots = ("." * ndots) + (" " * (6 - ndots))
            self.add_overlay(const.GRID_BOTTOMRIGHT,
                             "Record [V]ideo (On) " + dots, "")
        else:
            self.add_overlay(const.GRID_BOTTOMRIGHT, "Record [V]ideo (Off) ", "")
        if self._video_idx > 0:
            fname = self._video_path % (self._video_idx - 1)
            self.add_overlay(const.GRID_BOTTOMRIGHT, "   saved as %s" % fname, "")

        self.add_overlay(const.GRID_BOTTOMRIGHT, "Move Ball: [U], [D], [R], [L]", "")
        self.add_overlay(const.GRID_BOTTOMRIGHT, "    (Shift keeps velocity)", "")

    def key_callback(self, window, key, scancode, action, mods):
        if action == glfw.REPEAT or action == glfw.PRESS:
            if key == glfw.KEY_UP:
                self.aether.moveBall(0, mods == glfw.MOD_SHIFT)
            elif key == glfw.KEY_DOWN:
                self.aether.moveBall(1, mods == glfw.MOD_SHIFT)
            elif key == glfw.KEY_LEFT:
                self.aether.moveBall(2, mods == glfw.MOD_SHIFT)
            elif key == glfw.KEY_RIGHT:
                self.aether.moveBall(3, mods == glfw.MOD_SHIFT)

        elif action == glfw.RELEASE:
            # toggles robots on or off
            if key == glfw.KEY_1:
                self.aether.toggleRobot(0, mods == glfw.MOD_SHIFT)
            elif key == glfw.KEY_2:
                self.aether.toggleRobot(1, mods == glfw.MOD_SHIFT)
            elif key == glfw.KEY_3:
                self.aether.toggleRobot(2, mods == glfw.MOD_SHIFT)
            elif key == glfw.KEY_4:
                self.aether.toggleRobot(3, mods == glfw.MOD_SHIFT)
            elif key == glfw.KEY_5:
                self.aether.toggleRobot(4, mods == glfw.MOD_SHIFT)
            elif key == glfw.KEY_6:
                self.aether.toggleRobot(5, mods == glfw.MOD_SHIFT)

            # default [modified] calls
            elif key == glfw.KEY_BACKSPACE:
                self.aether.reset()

            elif key == glfw.KEY_TAB:  # Switches cameras.
                self.cam.fixedcamid += 1
                self.cam.type = const.CAMERA_FIXED
                if self.cam.fixedcamid >= self._ncam:
                    self.cam.fixedcamid = -1
                    self.cam.type = const.CAMERA_FREE
            elif key == glfw.KEY_H:  # hides all overlay.
                self._hide_overlay = not self._hide_overlay
            elif key == glfw.KEY_SPACE and self._paused is not None:  # stops simulation.
                self._paused = not self._paused
                self.aether.startStop(self._paused)

            # Advances simulation by one step.
            elif key == glfw.KEY_P and self._paused is not None:
                self._advance_by_one_step = True
                self._paused = True
            elif key == glfw.KEY_V or \
                    (key == glfw.KEY_ESCAPE and self._record_video):  # Records video. Trigers with V or if in progress by ESC.
                self._record_video = not self._record_video
                if not self._record_video and len(self._video_frames) > 0:
                    # This include captures console, if in the top declaration.
                    frames = [f for f in self._video_frames]
                    fps = (1 / self._time_per_render)
                    process = Process(target=save_video,
                                      args=(frames, self._video_path % self._video_idx, fps))
                    process.start()
                    self._video_frames = []
                    self._video_idx += 1
            elif key == glfw.KEY_T:  # capture screenshot
                img = self._read_pixels_as_in_window()
                imageio.imwrite(self._image_path % self._image_idx, img)
                self._image_idx += 1
            elif key == glfw.KEY_S:  # Slows down simulation.
                self._run_speed /= 2.0
            elif key == glfw.KEY_F:  # Speeds up simulation.
                self._run_speed *= 2.0
            elif key == glfw.KEY_C:  # Displays contact forces.
                vopt = self.vopt
                vopt.flags[10] = vopt.flags[11] = not vopt.flags[10]
            elif key == glfw.KEY_D:  # turn off / turn on rendering every frame.
                self._render_every_frame = not self._render_every_frame
            elif key == glfw.KEY_E:
                vopt = self.vopt
                vopt.frame = 1 - vopt.frame
            elif key == glfw.KEY_R:  # makes everything little bit transparent.
                self._transparent = not self._transparent
                if self._transparent:
                    self.sim.model.geom_rgba[:, 3] /= 5.0
                else:
                    self.sim.model.geom_rgba[:, 3] *= 5.0
            elif key == glfw.KEY_M:  # Shows / hides mocap bodies
                self._show_mocap = not self._show_mocap
                for body_idx1, val in enumerate(self.sim.model.body_mocapid):
                    if val != -1:
                        for geom_idx, body_idx2 in enumerate(self.sim.model.geom_bodyid):
                            if body_idx1 == body_idx2:
                                if not self._show_mocap:
                                    # Store transparency for later to show it.
                                    self.sim.extras[
                                        geom_idx] = self.sim.model.geom_rgba[geom_idx, 3]
                                    self.sim.model.geom_rgba[geom_idx, 3] = 0
                                else:
                                    self.sim.model.geom_rgba[
                                        geom_idx, 3] = self.sim.extras[geom_idx]

        # super().key_callback(window, key, scancode, action, mods)


def save_video(frames, filename, fps):
    writer = imageio.get_writer(filename, fps=fps)
    for f in frames:
        writer.append_data(f)
    writer.close()
