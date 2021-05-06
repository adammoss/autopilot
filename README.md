# autopilot

Template code for the AutoPilot self-driving software on the PiCar. 

![alt text](https://github.com/adammoss/autopilot/blob/main/test.png?raw=true)

## Installation

Set up a virtual environment using Anaconda

```
conda create -n autopilot python=3.6
```

Activate the environment and install the requirements

```
conda activate autopilot
pip install -r requirements.txt
```

## Testing

In test mode AutoPilot will use a supplied test image, rather than live images from the car. This image has exactly the same dimensions as live images.

We have included a base model to show how to interface with your code. To test using this base model

```
python run.py --model base
```

You should get an angle of 88 and a speed of 35, with an inference time of around 30 milliseconds (depending on hardware).


## Modifying

1. Create another directory in the models directory, with the directory name the same as your group name (no spaces please, use an underscore). 

2. Create a file called model.py in this directory. Your model.py file can contain anything you like, the only restriction is it *must* define a Model class with a predict method, which takes an image as input and outputs the speed and angle (in 'car' units). 

3. You can use models/base/model.py as a guide. Remember to change any image preprocessing to match what you did in training.

 If you use additional packages, please edit the 'requirements.txt' file so we can install them. 

To test using your model

```
python run.py --model name_of_your_model
```

The code will raise an error if you get unrealistic values for the speed and angle. Please also ensure your inference time is reasonable.
