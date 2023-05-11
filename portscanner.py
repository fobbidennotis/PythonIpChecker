import requests
import nmap

# Returns a an array of tuples containing open ports and their services
def scan_ports(target, port_range="1-1024"):
    nm = nmap.PortScanner()
    nm.scan(target, port_range)

    open_ports_and_services = [
        (port, f'{service["name"]} {service["version"]} {service["extrainfo"]}')
        for host in nm.all_hosts()
        for proto in nm[host].all_protocols()
        for port, service in nm[host][proto].items()
        if service["state"] == "open"
    ]
    return open_ports_and_services

# Returns a tuple of (ip, country, city, timezone) and (lat, lon)
def get_ip_info(ip):
    try:
        response = requests.get(url=f'http://ip-api.com/json/{ip}').json()
        print(response)
        data = (
            response['query'],
            response['country'],
            response['city'],
            response['timezone']
        )
        lat_lot = response.get('lat'), response.get('lon') 
        return data, lat_lot
    except requests.ConnectionError:
        print('[!] Error! Request Connection Error!')
        exit(1)

def main():
    ip = input('Ip : ')
    get_ip_info(ip=ip)

if __name__ == '__main__':
    main()
