<h1>GP Bikes UDP data reader</h1>

This project is a simple example/tutorial on how to get and use the data provided by GP Bikes (and other common engine games from Piboso) through its own UDP server. 
With this base code you can create your own real time custom GUI, HUD or external dashboards using serial data and microcontrollers. The process itself is simple, but for the newcomers can be a bit confusing, so this can be a good starting point.

<h2>Basic operation</h2>
Running the script will open the following screen:

![image](https://github.com/vitorkogut/GPB_UDP_TO_SERIAL/assets/49065277/4550fa43-7cb4-4229-9e15-0b0b93847470)

GPBikes connection status = Connection status with GP Bikes UDP server, can be:
- Connected: all good to go
- Connected (simulation stopped): The UDP connection is up, but the game engine is stopped (normal in menu)
- Disconnected: if your game is open and you get this status, check you UDP server (https://forum.piboso.com/index.php?topic=6063.0) and the variables under 'SEVER CONFIG' in the code (they should be exactly the same) 

Serial data PORT: If you are using a custom external dash that supports serial data you can set their adress in here (COM10, COM02, COM12, ...)

<h2>Code structure</h2>

<h4>SERVER CONFIG</h4>
Defines the UDP connection properties, follow this tutorial (https://forum.piboso.com/index.php?topic=6063.0) to enable your UDP server and set the values accordingly. 

<h4>DATA CONTROL</h4>
Here you can define wich values will be collected, just as a control step.

<h4>GUI CONFIG</h4>
Here the GUi is defined, if you are doing a GUI dashboard you can add dials and various others displays options in here. I recommend maintaining the default content, as it's used to establish and monitor the connection.

<h4>Main loop</h4>
At the main loop the incoming data is decoded and added to the main object (keep scroling to find out how to add your own!), if you need to update a GUI component based on the incoming data do it at line 152 (if enable_GUI is true).

<h2>"i need XXXX value! How can i acess it?"</h2>
This code only covers the basic data, mostly engine and angle stuff You can follow the examples in the main loop and get the data adress from this table: 

[Here](https://docs.google.com/spreadsheets/d/e/2PACX-1vS18UEQNpEU2HBeow4vLLdK1zVo_zaWiFcbfYtYPVfc5iBW8MUbQV0WM2Ggimd8raGg7uQRtndnew6v/pubhtml)

If you need extra details, you can find the C struct here: https://gp-bikes.com/downloads/gpb_example.c

For data not on the table: Just calculate the byte offset, if the value you need is declared after other 5 float values (at the struct named SPluginsBikeData_t), just offset the position by `sizeOf(float)` * 5


<h2>Serial data</h2>
If you are using an arduino for a external custom dashboard the process is really straight forward!
All you need to do is listen for serial data and process it. After putting your COM port and connecting (GUI) a TEST message will be sent to verify the conenction, no need to worry about it. 
After that a datagram defined in line 143 will be sent, fell free to modify it, in the arduino side, just create a string from the incoming buffer and split it at the commas, then use those values for servos, leds or anything else.

<h3> 
  
  [use case example in video!](https://youtube.com/shorts/fW0gZF4tQHk?feature=share) 

</h3> 
