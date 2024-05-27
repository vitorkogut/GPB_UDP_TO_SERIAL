<h1>GP Bikes UDP data reader</h1>

This project is a simple example/tutorial on how to get and use the data provided by GP Bikes (and other common engine games from Piboso) through its own UDP server. 
With this base code you can create your own real time custom GUI, HUD or external dashboards using serial data and microcontrollers. The process itself is simple, but for the newcomers can be a bit confusing, so this can be a good starting point.

<h2>Basic operation</h2>
![image](https://github.com/vitorkogut/GPB_UDP_TO_SERIAL/assets/49065277/802deea5-7c9a-4ffa-92c5-851041603a09)


<h2>Code structure</h2>

<h4>SERVER CONFIG</h4>
Defines the UDP connection properties, follow this tutorial (https://forum.piboso.com/index.php?topic=6063.0) to enable your UDP server and set the values accordingly. 

<h4>DATA CONTROL</h4>
Here you can define wich values will be collected, just as a control step.

<h4>GUI CONFIG</h4>
Here the GUi is defined, if you are doing a GUI dashboard you can add dials and various others displays options in here. I recommend maintaining the default content, as it's used to establish and monitor the connection.

<h4>Main loop</h4>
At the main loop the incoming data is decoded and added to the main object (keep scroling to find out how to add your own!), if you need to update a GUI component based on the incoming data do it at line 152 (if enable_GUI is true).
