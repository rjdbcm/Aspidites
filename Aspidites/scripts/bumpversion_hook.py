import os
import sys
from Aspidites import __version__
from Aspidites._vendor.semantic_version import Version


def main(*arg, last_version=''):  # 'major', 'minor', or 'patch'
    if arg[0][1] == 'major':
        last_version = str(Version(__version__).prev_major())
    elif arg[0][1] == 'minor':
        last_version = str(Version(__version__).prev_minor())
    elif arg[0][1] == 'patch':
        last_version = Version(__version__).prev_patch
    else:
        exit(1)
    vstring = f'**v{last_version}**'
    # Read in the file
    data = open('CHANGELOG.md', 'r').read()
    open('CHANGELOG.bak', 'w').write(data)

    # Replace the target string
    commit_log = f'\n- '.join(
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