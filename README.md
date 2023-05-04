# autopilot

Template code for the AutoPilot self-driving software on the PiCar. 

![alt text](https://github.com/adammoss/autopilot/blob/main/test.png?raw=true)

## Installation

Set up a virtual environment using Anaconda (here we have used python 3.8, we recommend 3.7+)

```
conda create -n autopilot python=3.8
```

Activate the environment and install the requirements

```
conda activate autopilot
pip install -r requirements.txt
```

## Testing

In test mode AutoPilot will use a supplied test image, rather than live images from the car. This image has exactly the same dimensions as live images.

We have included a base model to show how to interface with your code. To test using this model

```
python3 run.py --model base
```

You should get an angle of 88 and a speed of 35, with an inference time of around 30 milliseconds (depending on hardware).

Other available models are 

```
python3 run.py --model maggie
```

and a model converted to tflite

```
python3 run.py --model maggie_tpu
```

## Modifying

1. Create another directory in the models directory, with the directory name the same as your group name (no spaces please, use an underscore). 

2. Create a file called model.py in this directory. Your model.py file can contain anything you like (use pytorch or jax if you want to!), the only restriction is it *must* define a Model class with a predict method, which takes an image as input and outputs the speed and angle (in 'car' units). 

3. You can use models/base/model.py as a guide. Remember to change any image preprocessing to match what you did in training.

 If you use additional packages, please edit the 'requirements.txt' file so we can install them. 

To test using your model

```
python3 run.py --model name_of_your_model
```

The code will raise an error if you get unrealistic values for the speed and angle. Please also ensure your inference time is reasonable.

## Running 

To run on the car you will need to transfer your model to the car and run using python3 (note the drive mode option)

```
python3 run.py --model name_of_your_model --mode drive --duration 60
```

There may be a conflict with the camera already running with the remote control inferface. In this case find the process(es) of the webserver

```
ps aux | grep runserver
```

Then look for any process IDs (second number). Next kill these by 

```
kill process_id
```

for any process IDs (there are normally 2 running). You should now be able to run autopilot.

Note that to use remote control you will need to restart the car. 

If invoking the edge-TPU and you encounter something like:

```
libedgetpu.1.dylib' (open() failed with errno=13)
```

This means there is a failed connection with the eTPU. Make sure the the eTPU is plugged in and the light on

## Inference time issues

If you are expering long inference times on the car, you should try to reduce your model complexity or reduce the size of images processed by your model. If you still have issues, you can run the car at a reduced speed by setting the max_speed argument, for example

```
python3 run.py --model name_of_your_model --mode drive --duration 60 --max_speed 30
```

Pratically, we have found this needs to be > 25 in order for the car to still move. Please note that running at a reduced speed will mean it fails one of the challenges, which is to drive round the oval track at a speed of 50. 
