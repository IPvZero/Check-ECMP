from nornir import InitNornir
from nornir.plugins.tasks.networking import netmiko_send_command, netmiko_send_config
from nornir.plugins.functions.text import print_result
import colorama
from colorama import Fore, Style
import threading

LOCK = threading.Lock()

def get_facts(task):
    my_list=[]
    r = task.run(netmiko_send_command, command_string="show ip route", use_genie=True)
    task.host["facts"] = r.result
    hops = task.host["facts"]["vrf"]["default"]["address_family"]["ipv4"]["routes"]["0.0.0.0/0"]["next_hop"]["next_hop_list"]
    LOCK.acquire()
    if len(hops) != 2:
        print("*" * 75)
        print(Fore.RED + Style.BRIGHT +
                f"ALERT: Device {task.host} does not have equal cost multi-paths to all destinations" + Style.RESET_ALL
)
        print("*" * 75 + "\n")
    else:
        print("*" * 75)
        print(Fore.GREEN + Style.BRIGHT +
                f"ECMP is active for Device {task.host}" + Style.RESET_ALL
)
        print("*" * 75 + "\n")
    LOCK.release()

def main() -> None:
    nr = InitNornir(config_file="config.yaml")
    targets = nr.filter(layer="access")
    result = targets.run(task=get_facts)

if __name__ == '__main__':
    main()
