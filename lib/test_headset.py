from lib.headset import Zen5Headset


def test_create_electrode_matrix():
    headset = Zen5Headset()
    placements = headset.right_frontal_placements
    e_matrix = headset.create_electrode_matrix(placements)
    assert len(e_matrix) == len(placements)
