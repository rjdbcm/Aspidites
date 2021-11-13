from pathlib import Path
from Aspidites.woma.fileutils import atomic_save, mkdir_p


def test_atomic_save_rename():
    fname = Path("./tmp/final.txt")
    fstr = str(fname)
    mkdir_p(str(fname.parent))
    with atomic_save(fstr) as f:
        f.write(b"rofl")
        f.write(b"\n")
    with open(fstr, "r") as f:
        line1 = f.readlines()
    assert line1[0] == "rofl\n"
    # assert line2 == "\n"
    fname.unlink()
    fname.parent.rmdir()
