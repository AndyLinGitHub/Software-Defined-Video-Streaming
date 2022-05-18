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