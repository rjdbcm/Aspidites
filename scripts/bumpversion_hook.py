import os

from Aspidites import __version__


def main():
    vstring = f'**v{__version__}**'
    # Read in the file
    data = open('CHANGELOG.md', 'r').read()
    open('CHANGELOG.bak', 'w').write(data)

    # Replace the target string
    commit_log = '\n- '.join(
        os.popen(f'git log --abbrev-commit --pretty=oneline v{__version__}...HEAD').readlines()
    )
    changes = '\n'.join(
        [vstring, commit_log, '\n']
    )

    data = data.replace(vstring, changes)

    # Write the file out again
    open('CHANGELOG.md', 'w').write(data)


if __name__ == '__main__':
    main()
