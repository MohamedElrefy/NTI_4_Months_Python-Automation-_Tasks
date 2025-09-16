import re
import argparse
from datetime import datetime
parser = argparse.ArgumentParser()
parser.add_argument("-i","--input",type=str,required=True)
parser.add_argument("-f",action="store_true")
args =parser.parse_args()


  
def interfaces_info(input):
    interface_config=[]
    interfaces_regex=r"interface\sGigabitEthernet0\/(\d)\n\snameif\s(inside|outside)\n.*\n\s+ip\saddress\s(\d+\.\d+\.\d+\.\d+)\s(\d+\.\d+\.\d+\.\d+)"
    interfaces_result = re.findall(interfaces_regex,input)
    for interface in interfaces_result:
        if interface[1].strip()=="inside":
          zone="trust"
        elif interface[1].strip()=="outside":
          zone="untrust"
        else:
          print("undefined zone")  
        configs=f"set interfaces ge-0/0/{interface[0]} unit 0 family inet address {interface[2]}\nset security zones security-zone {zone} interfaces ge-0/0/{interface[0]}"
        interface_config.append(configs)
        
    return f"{"\n".join(interface_config)}\n"
    
def network_object(input):
    network_config=[]
    network_regex= r"object\snetwork\s+(.*)\n\shost\s+(.*)"
    network_result=re.findall(network_regex,input)
    for net in network_result:
        net_config=f"set security address-book global address {net[0]} {net[1]}/32"
        network_config.append(net_config)
    return f"{"\n".join(network_config)}\n" 

def network_group(input):
    group_config=[]
    group_name_regex= r"object-group\snetwork\s+(.*)"
    group_name=re.findall(group_name_regex,input)
    ip_regex=r"network-object\s+host\s+(\d+\.\d+\.\d+\.\d+)"
    ips=re.findall(ip_regex,input)
    if group_name:
      for net in group_name:
        for ip in ips:
           configs=f"set security address-book global address-set {net} address {ip}/32"
           group_config.append(configs)
    return f"{"\n".join(group_config)}\n"

def acess_list(input):
   list_configs=[]
   list_regex=r"access-list\s+(.*)\sextended.*host\s(\d+\.\d+\.\d+\.\d+)\s(?:eq\s+(\d+))?"
   lists=re.findall(list_regex,input)     
   for list in lists:
       if list[2].strip()== "80":
         list_conf=f"set security policies from-zone untrust to-zone trust policy {list[0]} match source-address any destination-address {list[1]} application junos-http"
       elif list[2].strip()== "443":
         list_conf=f"set security policies from-zone untrust to-zone trust policy {list[0]} match source-address any destination-address {list[1]} application junos-https"
       elif list[2].strip()== "22":
         list_conf=f"set security policies from-zone untrust to-zone trust policy {list[0]} match source-address any destination-address {list[1]} application junos-ssh"
       elif list[2].strip()== "25":
         list_conf=f"set security policies from-zone untrust to-zone trust policy {list[0]} match source-address any destination-address {list[1]} application junos-smtp"
       elif list[2].strip()== "587":
         list_conf=f"set applications application smtp-submission protocol tcp destination-port 587\nset security policies from-zone untrust to-zone trust policy {list[0]} match source-address any destination-address {list[1]} application smtp-submission" 
       elif list[2].strip()== "53":
         list_conf=f"set security policies from-zone untrust to-zone trust policy {list[0]} match source-address any destination-address {list[1]} application junos-dns-udp"
       elif list[2].strip()== "123":
         list_conf=f"set security policies from-zone untrust to-zone trust policy {list[0]} match source-address any destination-address {list[1]} application junos-ntp" 
       elif list[2].strip()== "":
         list_conf=f"set security policies from-zone untrust to-zone trust policy {list[0]} match source-address any destination-address {list[1]} application junos-icmp"
       else:
         print("This is undefined port yet")
       list_configs.append(list_conf)
   return f"{"\n".join(list_configs)}\n"

def route(input):
   route_configs=[]
   route_regex=r"route\s+(?:inside|outside)\s+(\d+\.\d+\.\d+\.\d+)\s+(\d+\.\d+\.\d+\.\d+)\s+(\d+\.\d+\.\d+\.\d+)"
   routes=re.findall(route_regex,input)
   for route in routes:
      prefix=0
      for digit in route[1].split("."):
        element=bin(int(digit))
        prefix+=element.count("1")
      route_config=f"set routing-options static route {route[0]}/{prefix} next-hop {route[2]}"
      route_configs.append(route_config) 
   return f"{"\n".join(route_configs)}\n"

def Translate_Func(input_file):
   with open(input_file,"r") as file:
     config_content=file.read()
     if args.f:
        with open(f"output_{datetime.now().strftime("%Y%m%d_%H%M%S")}.txt","w") as output:
          output.write(interfaces_info(config_content)+network_object(config_content)+network_group(config_content)+acess_list(config_content)+route(config_content))
     else:
       print(interfaces_info(config_content)+network_object(config_content)+network_group(config_content)+acess_list(config_content)+route(config_content))
      
        
   
if __name__ == "__main__":
    Translate_Func(args.input)


  


        
   
           










    