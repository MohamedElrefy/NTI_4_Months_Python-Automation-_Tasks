# Cisco ASA to Juniper SRX Translation Assignment

## Objective
In this assignment, you will write a Python script to translate Cisco ASA firewall configurations into Juniper SRX configurations.

You are provided with:
- `asa_config1.txt` : Example ASA configuration (with interfaces, objects, ACLs, static routes)
- `asa_config2.txt` : Another ASA configuration

## Tasks
1. Parse the ASA configuration files and extract:
   - Interfaces
   - Objects (network, host)
   - Access-lists
   - Static routes

2. Translate them into Juniper SRX 'set' commands:
   - Map ASA interfaces (`outside`, `inside`) to SRX interfaces (`ge-0/0/0`, `ge-0/0/1`)
   - Convert ASA access-lists to SRX security policies
   - Convert ASA static routes to SRX static routes

3. Insert your generated configuration lines into the appropriate sections of `srx_template.txt`.

## Translation Methodology
When translating from Cisco ASA to Juniper SRX, follow these principles:

- **Interfaces & Zones**:  
  - ASA `interface ...` contains an `ip address` and a `nameif`.  
  - The `nameif` corresponds to a Juniper **security zone name**.  
  - The interface itself (`GigabitEthernet0/0`) is mapped to an SRX interface (e.g., `ge-0/0/0`).  
    set interfaces <interface name> unit 0 family inet address <ip address>

    set security zones security-zone <zone name> interfaces <interface name>

- **Objects**:  
  - ASA `object network <NAME>` with a `host <IP>` becomes a Juniper address-book entry:  
    ```
    set security address-book global address <NAME> <IP>/32
    ```

- **Access-lists**:  
  - ASA `access-list` rules define traffic permissions.  
  - These become SRX security policies, placed between zones:  
    ```
    set security policies from-zone <src-zone> to-zone <dst-zone> policy <POLICY-NAME> ...
    ```

- **Static Routes**:  
  - ASA `route <interface> <destination> <mask> <next-hop>`  
  - Becomes SRX static route:  
    ```
    set routing-options static route <destination>/<prefix> next-hop <next-hop>
    ```

- **Applications**:  
  - Standard ports map to built-in JunOS applications (`junos-http`, `junos-https`, `junos-ssh`, etc.).  
  - Non-standard ports require custom applications.  


## Notes
- For simplicity, assume:
  - ASA `outside` → SRX `ge-0/0/0` in `untrust` zone
  - ASA `inside` → SRX `ge-0/0/1` in `trust` zone
- JunOS has built-in applications like `junos-http`, `junos-https`, `junos-ssh`, `junos-icmp`, `junos-smtp`, `junos-dns-udp`, `junos-ntp` to represent the port number.

## Deliverables
- Python script called asa_srx_translator.py that can have 2 arguments:
"-f": if the user passes the arg "-f" then the user gets the output in a file named "output" appended with the date and time now in txt format and if the -f arg was not passed then the output should be printed in the screen 
"-i" , "--input": this arg represents the input configuration file name i.e. the ASA config file name 
