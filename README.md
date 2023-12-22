<h1> bezel </h1>

<h2>A python based data aquisition and visualisation program.</h2>
<br>

 - &nbsp; client (data acquisition) / server (data storage and visualisation) based architecture
 - &nbsp; data transfer over sockets
 - &nbsp; using pygame for realtime visualisation
 - &nbsp; fully configurable without programming 
 - &nbsp; configure multiple gauges on the same place and toggle between them
 - &nbsp; create new dashboard designs only with graphics and Configuration files
 - &nbsp; change between multiple dasboards in realtime
 - &nbsp; and many other features....
 
 <br>
 
<p align="center">
<img align="center" width="300px" src=https://user-images.githubusercontent.com/127665398/224561861-86d23091-c696-4a30-a730-828b612c1af3.png>
<img align="center" width="325px" src=https://user-images.githubusercontent.com/127665398/224564486-f98d2f4d-043e-4726-b157-ba72ad76789b.png>
</p>
<br>
<br>
<p align="center">
<img align="center" width="400px" src=https://user-images.githubusercontent.com/127665398/224564917-dc598c0c-0f65-4280-9800-3906699deb8b.png>
<img align="center" width="348px" src=https://user-images.githubusercontent.com/127665398/224566344-4e7b78f4-7377-4d01-8c6c-d1ccef669da3.png>


</p>
<br>
<h3>Install</h3>
<br>
I'm using the Pycharm IDE for development. So, install pycharm local.
The Community Edition is free for use in non commercial environments.

The Application is tested with the following Versions:<br>
Python 3.7.1<br>
numpy 1.20.0<br>
pygame 2.2.0<br>

After installing Pycham, install Python, git, numpy, pyqt5 and pygame from the
pycham ide with the Package Explorer.

Edit under "Run/Edit Configurations/
set the main.py under ./server as executable.
<br>

<h3>Defaultsettings</h3>

Once, the server started sucessfully, you see the image above. In the default configuration use the "up / down" keys to increase oder decrease the velocity.
All keyboard interactions are defined in the file keyboard.cfg under ./cfg  and can be edit. The client application under ./client can be used to simulate incomming data messages. Use the "q" key to terminate the application. change between multiple dasboards with the keys "1", "2", ... (defined in keyboard.cfg)
Toggle between the inner gauges with the "o" key.
<br>

<h3>Configuration</h3>
all gauges are defined in seperate Configurationfiles. Gauges are assigned to dashboards in dashboards Configurationfiles. Multiple Dashboards are defined in the main Configurationfile main.cfg under ./cfg . All graphics are located under ./pic
<br>

<h3>Future</h3>
The next steps for this project are:
<br>
<br>

- &nbsp; write an documentation how to use it an create new gauges
- &nbsp; the network connection must be more reliable and structured
- &nbsp; create more different gauges and dashboards
- &nbsp; write a better universal client to simulate all gauges
- &nbsp; create a client for data aquisition 
- &nbsp; seperate the data storage and delivery from the visualisation (implement visualisation client / data storage and delivery server) 

<br>

<h2>Warning</h2>
This project is not bugfree, ready and no professional application. It will be developed in my person when i have time for this. 
