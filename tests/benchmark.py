import resource
from model.distribution import Distribution

if __name__ == '__main__':
    NUM_CONDITIONS = 10 ** 7

    mem_init = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    v = [Distribution()] * NUM_CONDITIONS
    mem_final = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss

    print(mem_init)
    print(mem_final)

    print(mem_final - mem_init)
