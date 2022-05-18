# Introduction

## Overview
[Demo Video](https://www.youtube.com/watch?v=oNIMCVECFBY)

In this project, we used the software components learned in the class to build an intelligent video streaming application that allows users to change the video processing algorithm applied on the raw streaming video on the fly, and show the processed video content in real-time. The user can send control signal to the jetson nano through gRPC to tell the device to change the underlying video processing algorithm applied on the streaming data. The processed streaming video is streamed to the user’s laptop through RTMP protocol.

## Architecture
<p align="center">
<img src="https://github.com/AndyLinGitHub/Software-Defined-Video-Streaming/blob/main/Architecture.png" width=100% height=100%>
</p>

## Devices
- Local machine
- [Jetson Nano](https://www.nvidia.com/zh-tw/autonomous-machines/embedded-systems/jetson-nano/)
- [Raspberry Pi Camera V2](https://www.raspberrypi.com/products/camera-module-v2/)

# Install project dependencies
## gRPC-with-protobuf (On Jetson Nano and local machine)

```bash
# Install protobuf compiler
$ sudo apt-get install protobuf-compiler

# Install buildtools
$ sudo apt-get install build-essential make

# Install grpc packages
$ pip3 install -r grpc_requirements.txt
```

## Gstreamer (On local machine)
```bash
$ sudo apt-get install libgstreamer1.0-dev libgstreamer-plugins-base1.0-dev
 libgstreamer-plugins-bad1.0-dev gstreamer1.0-plugins-base
 gstreamer1.0-plugins-good gstreamer1.0-plugins-bad gstreamer1.0-plugins-ugly
 gstreamer1.0-libav gstreamer1.0-doc gstreamer1.0-tools gstreamer1.0-x
 gstreamer1.0-alsa gstreamer1.0-gl gstreamer1.0-gtk3 gstreamer1.0-qt5
 gstreamer1.0-pulseaudio
```

## NGINX (On Jetson Nano)
```bash
$ wget -O nginx-install.zip
https://www.dropbox.com/s/o6d7r72km1zmwuf/nginx-install.zip?dl=1

$ unzip nginx-install.zip $ ./nginx-rtmp.sh
```

## Google Mediapipe (On Jetson Nano)
```bash
# Download the precompiled python wheel pakcage of mediapipe. 
$ wget -O mediapipe-0.8-cp36-cp36m-linux_aarch64.whl https://www.dropbox.com/s/calsimvsabmhycm/mediapipe-0.8-cp36-cp36m-linux_aarch64.whl?dl=0

# Install the packages with pip tool
$ python3 -m pip install --upgrade pip
$ python3 -m pip install mediapipe-0.8-cp36-cp36m-linux_aarch64.whl $ python3 -m pip install dataclasses

# Add environment variable
$ echo “export OPENBLAS_CORETYPE=ARMV8” >> ~/.bashrc && source ~/.bashrc 

# Check if you can import the package
$ python3 -c "import mediapipe as mp"

# Uninstall opencv packages along with the mediapipe. They are precompiled versions and disable gstreamer by default.
$ cd [site-package folder] $ rm -rf opencv* cv2
```

# Usage
Download codes to your Jetson Nano and local machine
```bash
$ git clone https://github.com/AndyLinGitHub/Software-Defined-Video-Streaming
```

Run the gRPC server on your Jetson Nano
```bash
$ python3 server.py --ip 0.0.0.0 --port 8080
```

Run the following code on your local machine to see the streaming  
```bash
$ ffplay -fflags nobuffer rtmp://192.168.55.1/rtmp/live
```

Run the gRPC client on your local machine to start the streaming and change the video processing algorithm.
```bash
# Start the streaming
$ python3 client.py --ip 192.168.55.1 --port 8080 --algo start

# Apply object detection
$ python3 client.py --ip 192.168.55.1 --port 8080 --algo od

# Apply hand pose tracking
$ python3 client.py --ip 192.168.55.1 --port 8080 --algo hpt

# Apply pose estimation
$ python3 client.py --ip 192.168.55.1 --port 8080 --algo pe

# Apply face detection
$ python3 client.py --ip 192.168.55.1 --port 8080 --algo fd

# Terminate the streaming
$ python3 client.py --ip 192.168.55.1 --port 8080 --algo terminate
```

# Error might encounter
## Opencv gstreamer pipeline not working
- problem:
	- https://forums.developer.nvidia.com/t/opencv-gstreamer-pipeline-not-working/198471
	- https://stackoverflow.com/questions/56150919/gstreamer-is-installed-but-not-built-with-opencv

- solution:
	- https://medium.com/@galaktyk01/how-to-build-opencv-with-gstreamer-b11668fa09c
	- https://forums.developer.nvidia.com/t/unable-to-install-opencv-with-cuda-in-jetson-nano/72994

## Opencv blocking mode error
- problem:
	- https://forums.developer.nvidia.com/t/cannot-open-gstreamer-pipeline-with-opencv-on-jetson-nano/111478/5

- solution:
	```bash
	# Look for related python process
	$ ps aux | grep python

	# Kill the process
	$ kill PID

	# Restart nvargus-daemon
	$ sudo systemctl restart nvargus-daemon
	```

# References
- https://github.com/johnnylord/gRPC-with-protobuf
- https://gist.github.com/johnnylord/b5f003e62c1f4eb9c6e2ae9567c4f3d0
- https://google.github.io/mediapipe/solutions/solutions.html
- https://shengyu7697.github.io/python-opencv-save-video/
- https://www.dropbox.com/s/5099n7p5s28sjk9/template.py?dl=1