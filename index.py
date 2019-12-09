from simnibs import sim_struct, run_simnibs
from lib.headset import Zen5Headset
import os
import threading
import logging


def get_tdcslist(e_montage, e_current):
    headset = Zen5Headset()
    tdcslist = sim_struct.TDCSLIST()
    # Simulation parameters
    currents = headset.get_currents(e_montage, e_current)
    print(e_montage)
    print(currents)
    assert sum(currents) == 0
    tdcslist.currents = currents

    electrodes = headset.get_electrodes(e_montage)
    # add channel number to electrodes
    for i, e in enumerate(electrodes):
        e.channelnr = i + 1

    [tdcslist.add_electrode(e) for e in electrodes]

    return tdcslist


def run_cs_session():
    logging.info("Starting Center-Surround simulation")
    s = sim_struct.SESSION()
    s.fnamehead = os.path.join('models', 'ernie', 'ernie.msh')
    s.pathfem = os.path.join('results', 'simulation-zen5-cs')
    s.open_in_gmsh = False

    montages = [["RF-CS"], ["LF-CS"], ["LF-CS", "RF-CS"]]
    electrode_montages = generate_selections(montages)
    logging.info(f"{len(electrode_montages)} simulations")
    electrode_current = [2] * len(electrode_montages)

    run_simulations(s, electrode_montages, electrode_current)


def run_bimodal_session():
    logging.info("Starting Biomodal simulation")
    s = sim_struct.SESSION()
    s.fnamehead = os.path.join('models', 'ernie', 'ernie.msh')
    s.pathfem = os.path.join('results', 'simulation-zen5-bimodal')
    s.open_in_gmsh = False

    montages = [["LF-A", "RF-C"], ["LF-C", "RF-A"]]
    electrode_montages = generate_selections(montages)
    logging.info(f"{len(electrode_montages)} simulations")
    electrode_current = [2] * len(electrode_montages)
    run_simulations(s, electrode_montages, electrode_current)


def generate_selections(montages):
    # every electrode can be 0 (full on), 1 (left on), 2 (right on)
    electrode_montages = []
    n_selections = 3
    for montage in montages:
        e_montages = [montage] * n_selections
        for i, e_montage in enumerate(e_montages):
            _montage = [f"{e}{i}" for e in e_montage]
            electrode_montages.append(_montage)

    return electrode_montages


def run_simulations(session, electrode_montages, electrode_current):
    for e_montage, e_current in zip(electrode_montages,
                                    electrode_current):

        tdcslist = get_tdcslist(e_montage, e_current)
        session.add_poslist(tdcslist)

    run_simnibs(session, cpus=3)


def main():
    x = threading.Thread(target=run_bimodal_session)
    x.start()
    y = threading.Thread(target=run_cs_session)
    y.start()


main()
