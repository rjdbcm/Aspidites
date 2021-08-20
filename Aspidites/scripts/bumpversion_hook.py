import os
import sys
from Aspidites import __version__


def main(*arg):  # 'major', 'minor', or 'patch'
    last_version = __version__
    vstring = f'**v{last_version}**'
    # Read in the file
    data = open('CHANGELOG.md', 'r').read()
    open('CHANGELOG.bak', 'w').write(data)

    # Replace the target string
    commit_log = '\n-' + f'\n- '.join(
        [i.strip() for i in
         os.popen(
             f'git log --abbrev-commit --pretty=oneline v{last_version}...HEAD'
         ).readlines()
         ]
    )
    changes = '\n'.join(
        [vstring, commit_log, '\n']
    )

    data = data.replace(vstring, changes)

    # Write the file out again
    open('CHANGELOG.md', 'w').write(data)


if __name__ == '__main__':
    main(sys.argv)