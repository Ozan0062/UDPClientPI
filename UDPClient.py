from pynput.keyboard import Key, Listener
from socket import *
import time
import RPi.GPIO as GPIO

serverName = '192.168.36.100'
serverPort = 12000
clientSocket = socket(AF_INET, SOCK_DGRAM)
GPIO.setwarnings(False)

expected_password = "UUUUUUUU"
entered_chars = 0
user_password = ""

print('Password:')

def on_key_release(key):
    global entered_chars, user_password, expected_password

    if key == Key.right:
        user_password += "R"
        entered_chars += 1
        print("    Right key clicked")
    elif key == Key.left:
        user_password += "L"
        entered_chars += 1
        print("    Left key clicked")
    elif key == Key.up:
        user_password += "U"
        entered_chars += 1
        print("    Up key clicked")
    elif key == Key.down:
        user_password += "D"
        entered_chars += 1
        print("    Down key clicked")
    elif key == Key.enter:
        print("    Middle key clicked")
        user_password += "M"
        entered_chars += 1
 if entered_chars == len(expected_password):
        authenticate_user()

def authenticate_user():
    global user_password
    print(f"Authenticating user with password: {user_password}")
    clientSocket.sendto(user_password.encode(), (serverName, serverPort))
    modifiedMessage, serverAddress = clientSocket.recvfrom(2048)
    print(f"Server response: {modifiedMessage.decode()}")
    modifiedMessage2, serverAddress = clientSocket.recvfrom(2048)
    print(f"Server response: {modifiedMessage2.decode()}")

    if modifiedMessage2.decode()=="FEJL":
      user_password = ""
      global entered_chars
      entered_chars = 0
      print(f"STOP")

    elif modifiedMessage2.decode()== "OK CREATED":
      in1 = 17
      in2 = 18
      in3 = 27
      in4 = 22

      # careful lowering this, at some point you run into the mechanical limitation of how quick your motor can move
      step_sleep = 0.001

      step_count = 1024 # 5.625*(1/64) per step, 4096 steps is 360°

      direction = True # True for clockwise, False for counter-clockwise

      # defining stepper motor sequence (found in documentation http://www.4tronix.co.uk/arduino/Stepper-Motors.php)
      step_sequence = [[1,0,0,1],
                 [1,0,0,0],
                 [1,1,0,0],
                 [0,1,0,0],
                 [0,1,1,0],
                 [0,0,1,0],
                 [0,0,1,1],
                 [0,0,0,1]]
 # setting up
      GPIO.setmode( GPIO.BCM )
      GPIO.setup( in1, GPIO.OUT )
      GPIO.setup( in2, GPIO.OUT )
      GPIO.setup( in3, GPIO.OUT )
      GPIO.setup( in4, GPIO.OUT )

      # initializing
      GPIO.output( in1, GPIO.LOW )
      GPIO.output( in2, GPIO.LOW )
      GPIO.output( in3, GPIO.LOW )
      GPIO.output( in4, GPIO.LOW )

      motor_pins = [in1,in2,in3,in4]
      motor_step_counter = 0 ;

      def cleanup():
       GPIO.output( in1, GPIO.LOW )
       GPIO.output( in2, GPIO.LOW )
       GPIO.output( in3, GPIO.LOW )
       GPIO.output( in4, GPIO.LOW )
       GPIO.cleanup()

      # the meat
      try:
       i = 0
       for i in range(step_count):
         for pin in range(0, len(motor_pins)):
            GPIO.output( motor_pins[pin], step_sequence[motor_step_counter][pin])
         if direction==True:
            motor_step_counter = (motor_step_counter + 1) % 8
         time.sleep( step_sleep )
       j = 0
       for j in range(step_count):
         for pin in range(0, len(motor_pins)):
            GPIO.output( motor_pins[pin], step_sequence[motor_step_counter][pin])
         if direction == True:
            motor_step_counter = (motor_step_counter - 1) % 8
         else: # defensive programming
            print( "uh oh... direction should always be either True or False" )
            cleanup()
            exit( 1 )
         time.sleep( step_sleep )



      except KeyboardInterrupt:
       cleanup()
       exit( 1 )

       cleanup()
       exit( 0 )

    user_password = ""  # Nulstil password efter brug
    entered_chars = 0

# Start tastaturlytter
with Listener(on_release=on_key_release) as listener:
    listener.join()
