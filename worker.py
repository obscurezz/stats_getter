import json
import subprocess
import time


class OsWorker:
    def __init__(self, replicat_list: str):
        self.replicat_list = replicat_list

    def _get_parameters(self) -> list:
        replicat_configs: list = []

        with open(self.replicat_list, 'r', encoding='utf-8') as filename:
            for string in filename:
                repl_rdy = subprocess.check_output(f"ps -ef |grep replicat |grep {string}", shell=True)
                repl_name: str = repl_rdy.split()[-1].decode('utf-8')
                repl_prm: str = repl_rdy.split()[9].decode('utf-8')

                replicat_configs.append((repl_name, repl_prm))

        return replicat_configs

    def _get_mapping_dict(self) -> dict:
        commands = dict()

        for replicat in self._get_parameters():
            with open(replicat[1], 'r', encoding='utf-8') as config:
                tables = []
                for string in config:
                    if string == '\n':
                        continue
                    elif string.split()[0] in ('MAP', 'TABLE'):
                        tables.append(string.split()[1].replace(',', ''))
                    else:
                        continue
                commands[replicat[0]] = tables

        return commands

    def _get_statistics(self, stats_value: str) -> dict:
        statistics_dict = {'Statistics period': stats_value.lower()}

        for replicat in self._get_mapping_dict().keys():
            statistics_dict[replicat] = dict()
            for table in self._get_mapping_dict()[replicat]:
                try:
                    t = subprocess.check_output(
                        f"echo 'stats {replicat} table {table} {stats_value}'|./ggsci |grep Total |grep -v statistics",
                        shell=True)
                except subprocess.CalledProcessError:
                    t = b"operations 0"
                t_rdy = list(filter(('Total').__ne__, t.decode('utf-8').strip().split()))
                statistics_dict[replicat][table] = [{t_rdy[i]: t_rdy[i + 1]} for i in range(0, len(t_rdy), 2)]

        return statistics_dict

    def write_to_json(self, stats_value: str) -> str:
        filename = f'stats_{time.strftime("%Y%m%d_%H%M%S")}.json'

        with open(filename, 'w') as jsonfile:
            json.dump(self._get_statistics(stats_value), jsonfile, indent=4)

        return f'{filename} created.'
