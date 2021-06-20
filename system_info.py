import datetime
import subprocess
import argparse

TIME = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))


class SystemInfo:
    def __init__(self, cli_arguments: argparse.Namespace):
        self.show_all_processes: bool = cli_arguments.show_all_processes
        self.system_users: bool = cli_arguments.system_users
        self.processes_started: bool = cli_arguments.processes_started
        self.processes_by_user: str = cli_arguments.processes_by_user
        self.total_use_memory: bool = cli_arguments.total_use_memory
        self.total_use_cpu: bool = cli_arguments.total_use_cpu
        self.most_mem_load: bool = cli_arguments.most_mem_load
        self.most_cpu_load: bool = cli_arguments.most_cpu_load

        self.res_show_all_processes: str = ""
        self.res_system_users: str = ""
        self.res_processes_started: str = ""
        self.res_processes_by_user: str = ""
        self.res_total_use_memory: str = ""
        self.res_total_use_cpu: str = ""
        self.res_most_mem_load: str = ""
        self.res_most_cpu_load: str = ""

    def __del__(self):
        self.res_all_processes = ""
        self.res_system_users: str = ""
        self.res_processes_started: str = ""
        self.res_processes_by_user: str = ""
        self.res_total_use_memory: str = ""
        self.res_total_use_cpu: str = ""
        self.res_most_cpu_load: str = ""
        self.res_most_mem_load: str = ""

    @staticmethod
    def run_command_in_shell(command_args: list) -> str:
        """
        Run Linux command in shell and return its output
        """
        command = " ".join([*command_args])
        shell_process = subprocess.run(
            args=command,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            shell=True,
            encoding="utf-8",
            text=True
        )
        output = shell_process.stdout.rstrip()
        return output

    def print_all_processes(self):
        """
        Print all running processes' information from console
        """
        self.show_all_processes = self.run_command_in_shell(command_args=[
            "ps", "aux"
        ])
        header = "\r\nAll processes:\r\n"
        self.create_report(header, self.show_all_processes)
        exit()

    def print_system_users(self):
        self.res_system_users = self.run_command_in_shell(command_args=[
            "ps", "axo", "user"
        ])
        header = "\r\nAll system users:\r\n"
        self.create_report(header, self.res_system_users)
        exit()

    def print_processes_started(self):
        self.res_processes_started = self.run_command_in_shell(command_args=[
            "ps", "-e", "|", "wc", "-l"
        ])
        header = "\r\nNumber of running processes:\r\n"
        self.create_report(header, self.res_processes_started)
        exit()

    def print_processes_by_user(self):
        self.res_processes_by_user = self.run_command_in_shell(command_args=[
            "ps", "-U", f"{self.processes_by_user}", "|", "wc", "-l"
        ])
        header = f"\r\nProcesses by user: {self.processes_by_user}\r\n"
        self.create_report(header, self.res_processes_by_user)
        exit()

    def print_total_use_memory(self):
        self.res_total_use_memory = self.run_command_in_shell(command_args=[
            "ps", "u", "|", "awk", "'{sum=sum+$6}; END {print sum/1024}'"
        ])
        header = "\r\nTotal use memory:\r\n"
        self.create_report(header, self.res_total_use_memory)
        exit()

    def print_total_use_cpu(self):
        self.res_total_use_cpu = self.run_command_in_shell(command_args=[
            "ps", "aux", "|", "awk", "'{usage+=($3)} END {print usage ""\"%""\" }'"
        ])
        header = "\r\nTotal use cpu:\r\n"
        self.create_report(header, self.res_total_use_cpu)
        exit()

    def print_most_mem_load(self):
        self.res_most_mem_load = self.run_command_in_shell(command_args=[
            "ps", "-eo", "cmd", "--no-headers", "--width", "20", "--sort", "-pmem", "|", "head -1"
        ])
        header = "\r\nMost process memory load:\r\n"
        self.create_report(header, self.res_most_mem_load)
        exit()

    def print_most_cpu_load(self):
        self.res_most_mem_load = self.run_command_in_shell(command_args=[
            "ps", "-eo", "cmd", "--no-headers", "--width", "20", "--sort", "-pcpu", "|", "head -1"
        ])
        header = "\r\nMost process cpu load:\r\n"
        self.create_report(header, self.res_most_mem_load)
        exit()

    @staticmethod
    def create_report(*args):
        with open('report.txt', 'w') as f:
            f.writelines("Date report: ")
            f.writelines(TIME)
            f.writelines("\n__________________")
            f.writelines(args)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--show_all_processes",
        action="store_true",
        help="List all running processes"
    )
    parser.add_argument(
        "--system_users",
        action="store_true",
        help="List system users"
    )

    parser.add_argument(
        "--processes_started",
        action="store_true",
        help="Number of running processes"
    )

    parser.add_argument(
        "--processes_by_user",
        action="store",
        help="Enter name user"
    )

    parser.add_argument(
        "--total_use_memory",
        action="store_true",
        help="Total use memory MB"
    )

    parser.add_argument(
        "--total_use_cpu",
        action="store_true",
        help="Total use CPU"
    )

    parser.add_argument(
        "--most_mem_load",
        action="store_true",
        help="Most process memory load"
    )

    parser.add_argument(
        "--most_cpu_load",
        action="store_true",
        help="Most process cpu load"
    )

    args = parser.parse_args()
    fs = SystemInfo(cli_arguments=args)
    if fs.show_all_processes:
        fs.print_all_processes()
    if fs.system_users:
        fs.print_system_users()
    if fs.processes_started:
        fs.print_processes_started()
    if fs.processes_by_user:
        fs.print_processes_by_user()
    if fs.total_use_memory:
        fs.print_total_use_memory()
    if fs.total_use_cpu:
        fs.print_total_use_cpu()
    if fs.most_mem_load:
        fs.print_most_mem_load()
    if fs.most_cpu_load:
        fs.print_most_cpu_load()
