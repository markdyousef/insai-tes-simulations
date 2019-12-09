from simnibs import sim_struct
import numpy as np


class Headset:
    dimensions = [1.2, 1.2]
    shape = "rect"
    thickness = 1.00 + 1.50

    def __init__(self, right_frontal_placements, left_frontal_placements):
        self.right_frontal_placements = right_frontal_placements
        self.left_frontal_placements = left_frontal_placements

    def get_electrodes(self, e_montage):
        electrodes = np.array([self.get_electrode(electrode)
                               for electrode in e_montage])
        return electrodes.flatten()

    def get_electrode(self, electrode):
        if 'LF' in electrode:
            return self.create_electrode_matrix(
                self.left_frontal_placements)
        if 'RF' in electrode:
            return self.create_electrode_matrix(
                self.right_frontal_placements)

    def create_electrode_matrix(self, placements):
        electrode_list = []
        for placement in placements:
            electrode = sim_struct.ELECTRODE()
            electrode.shape = self.shape
            electrode.dimensions = self.dimensions
            electrode.centre = placement
            electrode.thickness = self.thickness
            electrode_list.append(electrode)

        return electrode_list

    def select_onoff(self, electrode, current):
        size = len(self.get_electrode(electrode))
        matrix = []
        if "0" in electrode:
            on = [current] * size
            matrix = matrix + on
        elif "1" in electrode:
            on = [current] * (size // 2)
            off = [0] * (size // 2)
            matrix = on + off
        elif "2" in electrode:
            on = [current] * (size // 2)
            off = [0] * (size // 2)
            matrix = off + on

        return matrix

    def get_cs_matrix(self, electrode, current):
        size = len(self.get_electrode(electrode))
        CS_MATRIX = [-1, -1, -1, -1, 1, -1, -1, -1, -1, 1]

        matrix = []
        if "0" in electrode:
            n_anode = 2
            total_current = current * n_anode
            cathode_current = round(-total_current /
                                    (len(CS_MATRIX) - n_anode), 3)
            matrix = [current if c >
                      0 else cathode_current for c in CS_MATRIX]

        elif "1" in electrode:
            n_anode = 1
            total_current = current * n_anode
            cs_matrix = CS_MATRIX[0:5]
            off = [0] * (size // 2)
            cathode_current = round(-total_current /
                                    (len(cs_matrix) - n_anode), 3)

            matrix = [current if c >
                      0 else cathode_current for c in cs_matrix] + off

        elif "2" in electrode:
            n_anode = 1
            total_current = current * n_anode
            cs_matrix = CS_MATRIX[0:5]
            off = [0] * (size // 2)
            cathode_current = round(-total_current /
                                    (len(cs_matrix) - n_anode), 3)

            matrix = off + [current if c >
                            0 else cathode_current for c in cs_matrix]

        return matrix

    def get_anode_matrix(self, electrode, current=2):
        return self.select_onoff(electrode, current)

    def get_cathode_matrix(self, electrode, current=2):
        return self.select_onoff(electrode, -current)

    def get_currents(self, e_montage, e_current):
        currents = []
        # configs: "A-*", "C-*", "CS-*", * is left / right / both
        # center-surround electrode configuration
        # TODO: filter substring CS-* and improve
        for electrode in e_montage:
            current = []
            if "CS" in electrode:
                current = self.get_cs_matrix(electrode, e_current)
            elif "C" in electrode:
                current = self.get_cathode_matrix(electrode, e_current)
            elif "A" in electrode:
                current = self.get_anode_matrix(electrode, e_current)

            currents = currents + current

        return currents


class Zen4Headset(Headset):
    right_frontal_placements = [[10.75, 84.05, 63.73],
                                [10.58, 90.04, 39.65],
                                [41.99, 73.99, 55.49],
                                [42.52, 78.55, 36.19],
                                [28.1, 84.39, 50.92],  # center
                                [62.02, 50.16, 49.96],
                                [63.92, 54.51, 29.24],
                                [53.36, 66.67, 44.47]]  # center

    left_frontal_placements = [[-10.31, 83.3, 63.43],
                               [-11.89, 88.62, 41.37],
                               [-40.05, 73.9, 54.85],
                               [-42.19, 79.27, 37.08],
                               [-26.38, 83.11, 50.06],  # center
                               [-63.22, 45.13, 51.9],
                               [-64.65, 52.09, 30.67],
                               [-54.72, 66.67, 44.47]]  # center

    def __init__(self):
        Headset.__init__(
            self, self.right_frontal_placements, self.left_frontal_placements)


class Zen5Headset(Headset):
    # 4x1 electrode
    right_frontal_placements = [[10.75, 84.05, 63.73],
                                [10.58, 90.04, 39.65],
                                [41.99, 73.99, 55.49],
                                [42.81, 79.89, 30.71],
                                [25.29, 85.72, 49.71],  # center
                                [51.51, 66.68, 49.78],
                                [53.78, 71.06, 26.09],
                                [69.18, 39.72, 41.25],
                                [69.91, 43.95, 19.4],
                                [63.41, 54.45, 34.95]]  # center

    left_frontal_placements = [[-10.75, 84.05, 63.73],
                               [-10.58, 90.04, 39.65],
                               [-41.99, 73.99, 55.49],
                               [-42.81, 79.89, 30.71],
                               [-25.29, 85.72, 49.71],  # center
                               [-51.51, 66.68, 49.78],
                               [-53.78, 71.06, 26.09],
                               [-69.18, 39.72, 41.25],
                               [-69.91, 43.95, 19.4],
                               [-63.41, 54.45, 34.95]]  # center

    def __init__(self):
        Headset.__init__(
            self, self.right_frontal_placements, self.left_frontal_placements)
