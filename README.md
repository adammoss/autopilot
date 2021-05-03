# autopilot

Template code for the AutoPilot self-driving software on the PiCar. 

![alt text](https://github.com/adammoss/github/blob/main/test.png?raw=true)

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

In test mode the code will a supplied test.png image, rather than live images from the car.

We have included a base model to show how to inferface with your code. To test using this base model

```
python run.py --model base
```

You should get an angle of 88 and a speed of 35, with an inference time of around 30 milliseconds (depending on hardware).


## Modifying

1. Create another directory in the models directory, with the directory name your group name. 

2. Create a file called model.py. This must define a Model class with a predict method, which takes the image from the car and outputs the speed and angle (in `car' units). You can use models/base/model.py as a guide.

Your model.py can contain anything you like. If you use additional packages, please edit the 'requirements.txt' file so we can install them. 

To test using your model

```
python run.py --model name_of_your_model
```

The code will raise an error if you get unrealistic values.
