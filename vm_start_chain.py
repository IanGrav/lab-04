import paho.mqtt.client as mqtt
import time

"""This function (or "callback") will be executed when this client receives 
a connection acknowledgement packet response from the server. """
def on_connect(client, userdata, flags, rc):
    print("Connected to server (i.e., broker) with result code "+str(rc))
    # subscribing to the pong topic
    client.subscribe("gravalle/pong")

def on_message(client, userdata, message):
    print("Default callback - topic: " + message.topic + "   msg: " + str(message.payload, "utf-8"))

def on_message_from_pong(client, userdata, message):
    print("Custom callback  - Pong: "+message.payload.decode())
    # receive the message, cast it as an int, and add 1
    num = int(message.payload.decode()) + 1
    # wait one second
    time.sleep(1)
    # publish the new num value with the topic "ping"
    client.publish("gravalle/ping", num)


if __name__ == '__main__':

    # create a client object
    client = mqtt.Client()
    #attach the on_connect() callback function defined above to the mqtt client
    client.on_connect = on_connect
    #attach a default callback which we defined above for incoming mqtt messages
    client.on_message = on_message
    # register a custom callback for ping:
    client.message_callback_add("gravalle/pong", on_message_from_pong)
    # connect to my RPI as a host, with the default MQTT port number
    client.connect(host="172.20.10.13", port=1883, keepalive=60)
    # Take an initial integer from the user to begin Ping-Pong
    inputNum = int(input("Enter an Integer to begin Ping-Pong: "))
    # publish that initial integer under topic "ping"
    client.publish("gravalle/ping", f"{str(inputNum)}")
    
    client.loop_forever()


