import telnetlib
import time
import logging

def originate_ami_call(phone_number, ami_user, ami_pass, pbx_ip, caller_id='809'):
    try:
        tn = telnetlib.Telnet(pbx_ip, 7777, timeout=5)
        tn.read_until(b"Asterisk Call Manager")

        tn.write(f"""Action: Login
Username: {ami_user}
Secret: {ami_pass}
Events: off

""".encode())

        time.sleep(0.5)

        tn.write(f"""Action: Originate
Channel: PJSIP/809
Context: from-internal
Exten: {phone_number}
Priority: 1
CallerID: {caller_id} <{caller_id}>
Async: true

""".encode())

        time.sleep(2)

        result = tn.read_very_eager()
        tn.close()

        logging.info(f"Զանգի փորձ դեպի {phone_number}: {result}")
        return result.decode(errors="ignore")

    except Exception as e:
        logging.error(f"Զանգի սխալ: {e}")
        raise
