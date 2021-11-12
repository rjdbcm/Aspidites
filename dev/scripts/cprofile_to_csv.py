import cProfile
import pstats
import io
import csv


def prof_to_csv(prof):
    out_stream = io.StringIO()
    pstats.Stats(prof, stream=out_stream).print_stats()
    result = out_stream.getvalue()
    # chop off header lines
    result = 'ncalls' + result.split('ncalls')[-1]
    lines = [','.join(line.rstrip().split(None, 5)) for line in result.split('\n')]
    return '\n'.join(lines)


if __name__ == '__main__':
    with open('combined.csv', 'w') as out:
        print(prof_to_csv('combined.prof'), file=out)
