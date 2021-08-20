import os
import sys

from Aspidites import __version__
from Aspidites._vendor.semantic_version import Version


def main(*arg):  # 'major', 'minor', or 'patch'
    hook = "prev_" + str(arg[0][1])
    last_version = str(getattr(Version(__version__), hook)())
    vstring = f'**v{last_version}**'
    # Read in the file
    data = open('CHANGELOG.md', 'r').read()
    open('CHANGELOG.bak', 'w').write(data)

    # Replace the target string
    commit_log = '\n- '.join(
        os.popen(f'git log --abbrev-commit --pretty=oneline v{last_version}...HEAD').readlines()
    )
    changes = '\n'.join(
        [vstring, commit_log, '\n']
    )

    data = data.replace(vstring, changes)

    # Write the file out again
    open('CHANGELOG.md', 'w').write(data)


if __name__ == '__main__':
    main(sys.argv)
