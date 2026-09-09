import socket
from openai import OpenAI

# ==========================================
# OPENAI / LLM
# ==========================================

client = OpenAI()

ALLOWED_COMMANDS = {
    "LEFT",
    "RIGHT",
    "POS",
    "STOP"
}


def get_robot_command(user_text):

    response = client.responses.create(
        model="gpt-5.6-sol",
        input=f"""
You are a command interpreter for an Epson robot arm.

Allowed commands:
LEFT
RIGHT
POS
STOP

Rules:
- Return exactly ONE command.
- Return only the command.
- No explanation.
- If the user asks to move left, return LEFT.
- If the user asks to move right, return RIGHT.
- If the user asks for the current robot position, return POS.
- If the request is unclear or unsafe, return STOP.

Examples:

User: move the arm left
LEFT

User: please move to the right
RIGHT

User: where is the robot now?
POS

User: do something dangerous
STOP

User instruction:
{user_text}
"""
    )

    return response.output_text.strip().upper()


# ==========================================
# EPSON ROBOT SETTINGS
# ==========================================

ROBOT_IP = "192.168.1.6"
ROBOT_PORT = 2000


# ==========================================
# CONNECT TO RC+7
# ==========================================

robot = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connection timeout
robot.settimeout(10)

print("Connecting to Epson robot...")
print("IP:", ROBOT_IP)
print("Port:", ROBOT_PORT)

try:

    robot.connect((ROBOT_IP, ROBOT_PORT))

except Exception as e:

    print()
    print("Could not connect to Epson robot.")
    print("Make sure:")
    print("1. Ethernet is connected")
    print("2. Laptop IP is 192.168.1.10")
    print("3. RC+ program is running")
    print("4. RC+ shows WAITING FOR PYTHON...")
    print()
    print("Error:", e)

    exit()


print()
print("================================")
print("ROBOT CONNECTED")
print("LLM CONTROL READY")
print("================================")


# After connection, allow blocking reads again
robot.settimeout(None)


# ==========================================
# MAIN LOOP
# ==========================================

while True:

    print()
    user_text = input("Tell the robot what to do: ")

    # Exit Python program
    if user_text.lower().strip() in ["exit", "quit"]:

        print("Closing program...")
        break


    # ======================================
    # ASK LLM
    # ======================================

    try:

        command = get_robot_command(user_text)

    except Exception as e:

        print("LLM ERROR:", e)
        continue


    print("LLM command:", command)


    # ======================================
    # SAFETY CHECK
    # ======================================

    if command not in ALLOWED_COMMANDS:

        print("Command blocked.")
        continue


    if command == "STOP":

        print("STOP selected.")
        print("No movement command sent.")
        continue


    # ======================================
    # SEND TO RC+
    # ======================================

    try:

        robot.sendall((command + "\r\n").encode())

        print("Sent to RC+:", command)

    except Exception as e:

        print("Robot communication error:", e)
        break


    # ======================================
    # READ RC+ RESPONSE
    # ======================================

    try:

        while True:

            response = robot.recv(1024)

            if not response:
                print("Robot disconnected.")
                break

            text = response.decode(errors="ignore").strip()

            print("RC+:", text)

            # Stop reading after final response

            if "DONE" in text:
                break

            if "POS" in text:
                break

            if "TARGET_NOT_OK" in text:
                break

            if "UNKNOWN" in text:
                break

            if "ERROR" in text:
                break

    except Exception as e:

        print("Response error:", e)


# ==========================================
# CLOSE CONNECTION
# ==========================================

robot.close()

print("Robot connection closed.")
