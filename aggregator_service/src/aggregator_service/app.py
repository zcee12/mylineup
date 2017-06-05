import os

from time import sleep


INTERVAL = 10


def get_pending_jobs(pending_jobs_dir):
    jobs = os.listdir(pending_jobs_dir)
    return jobs


def invoke():
    print "running"


def main():
    while(1):
        invoke()
        sleep(10)


if __name__ == "__main__":
    main()
