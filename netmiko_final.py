# netmiko_final.py (เวอร์ชันที่ถูกต้อง)
from netmiko import ConnectHandler
from pprint import pprint

device_ip = "10.0.15.61"
username = "admin"
password = "cisco"

device_params = {
    "device_type": "cisco_ios",
    "ip": device_ip,
    "username": username,
    "password": password,
    "conn_timeout": 60,
}

def gigabit_status():
    """
    เวอร์ชันสุดท้ายที่ทำงานโดยการอ่าน Text ดิบ (Manual Parse)
    และให้ผลลัพธ์ตรงตามที่ผู้ใช้ต้องการ
    """
    try:
        with ConnectHandler(**device_params) as ssh:
            up = 0
            down = 0
            admin_down = 0
            interface_details = []

            ssh.disable_paging()
            raw_output = ssh.send_command("show ip interface brief")

            lines = raw_output.strip().split('\n')

            for line in lines:
                if line.startswith("GigabitEthernet"):
                    parts = line.split()
                    interface_name = parts[0]
                    
                    if "administratively" in line:
                        admin_down += 1
                        interface_details.append(f"{interface_name} administratively down")
                    elif len(parts) >= 6 and parts[-2] == "up" and parts[-1] == "up":
                        up += 1
                        interface_details.append(f"{interface_name} up")
                    else:
                        down += 1
                        interface_details.append(f"{interface_name} down")

            if not interface_details:
                return "No GigabitEthernet interfaces found."

            detailed_part = ", ".join(interface_details)
            summary_part = f"{up} up, {down} down, {admin_down} administratively down"
            final_answer = f"{detailed_part} -> {summary_part}"

            pprint(final_answer)
            return final_answer

    except Exception as e:
        error_message = f"Error connecting/executing command: {e}"
        print(error_message)
        return error_message