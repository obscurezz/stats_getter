from worker import OsWorker


if __name__ == '__main__':
    replicat_list: str = input('Enter replicat list: ')
    os_worker = OsWorker(replicat_list)

    stats_value: str = input('Enter stats value: ')
    print('Getting stats...')
    os_worker.write_to_json(stats_value)
    print('Stats collected.')
