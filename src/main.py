from scheduler.job_scheduler import JobScheduler


def main():
    scheduler = JobScheduler()
    scheduler.run()


if __name__ == "__main__":
    main()