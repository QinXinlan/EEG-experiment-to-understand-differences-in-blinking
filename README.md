# EEG-experiment-to-understand-differences-in-blinking

The provided codes could be used for any BCI experiment in which several devices are needed to record simultaneously.

This Brain-Computer Interface (BCI) experiment has been designed and carried out as part of my Ph.D. in Computational Neuroscience at Shanghai Jiaotong University. For a full description of the dataset, please refer to
🔗 Guttmann-Flury, E., Sheng, X. & Zhu, X. Dataset combining EEG, eye-tracking, and high-speed video for ocular activity analysis across BCI paradigms. Sci Data 12, 587 (2025). https://doi.org/10.1038/s41597-025-04861-9.

The dataset is available online at:
📂 https://www.synapse.org/Synapse:syn64005218/wiki/630018

The goal of the present design is to find a blink model explaining the physiology by non-invasively recording various aspects of blinking, eye movements and their impacts on Electroencephalographic (EEG) signals. The hypothesis that eyelid movements substantially alter the EEG potential leads to the necessity to record the EEG, the eyelid position, as well as the eyeball movements. Hence, three devices were recording simultaneously, while the E-Prime software was sending triggers and displaying instructions on the Presentation screen.

# Global setup
* 2 computers: 
  * one with Neuroscan and Phantom softwares
  * one with E-Prime and Tobii softwares
* 1 wifi router to provide a LAN network between computers (not mandatory but easier for automation)
* 1 Arduino to convert the binary trigger from E-Prime to a square trigger for the high-speed camera
* 1 StimTracker to convert light trigger to binary trigger readable by Tobii software
* lots of cables...

![name-of-you-image](https://raw.githubusercontent.com/QinXinlan/EEG-experiment-to-understand-differences-in-blinking/master/Experiment%20setup/Enviromental%20setup.png)

# EEG recording device: Neuroscan
During this experiment, subjects were seated in an electrically-shielded noise-proof chamber, designed specifically for EEG recordings. A 65 channel Quik-cap acquired signals through a SynAmps2 system connected to an amplifier (Compumedics, Neuroscan). 62 EEG electrodes were placed according to the extended 10/20 system. The reference was located on the right mastoid with the ground electrode on the forehead. A bipolar vertical electrooculographic (EOG) channel records the potentials around the left eye, whereas two electromyographic (EMG) electrodes were attached at the middle of the upper and lower right eyelid. The EEG/EOG/EMG signals were recorded at a 1000 Hz sampling frequency directly on the Neuroscan software.

# High-speed video camera: Phantom
The Phantom Miro M310 high-speed camera captures a single eye with a resolution of 320 x 240 pixels. This is the smallest mode allowing for a whole eye to be framed with a little margin in case of minor head movements. The focus is on the left eye considering that the attached electrodes are further away from the eyelids compared to the ones on the right eye. The eyelid position can then be extracted from the video and extrapolated to represent both eyes. 
Limitations: maximum internal memory of 10 GB

# Eye-tracker: Tobii
The Tobii TX300 eye-tracker collects gaze-related data at ~300 Hz. Eyeball position is calculated using the data from bright and dark pupil eye tracking system. This system uses an illuminator first placed closer then further away to the optical axis of the imaging device, causing the pupil to appear subsequently lit up and black, respectively. 
Limitations: cannot receive triggers on a miliseconds basis 

# Solution
All sampling rates should be proportional to the ~300 Hz from Tobii TX300. To prevent data loss, the video sampling frequency is consequently chosen at ~150 fps. Therefore, a binary trigger is sent from E-Prime every 6 milliseconds to an Arduino Nano (Atmega 328). The same E-Prime-based trigger is also sent directly to the Neuroscan software allowing for synchronousness between EEG and video recordings. 

# Automated Python code
A Python code is launched at the beginning of the experiment. The E-Prime computer is designated as the control station, sending commands to the Tobii computer and to the computer for Neuroscan and Phantom. Thereby, recordings are automatically started and stopped. At the beginning of each task, input the name of the file you want to create. When the recording has stopped, write "copy". Beware not to move the mouse or write anything on the computer, while the code is running.

![name-of-you-image](https://raw.githubusercontent.com/QinXinlan/EEG-experiment-to-understand-differences-in-blinking/master/Experiment%20setup/Experiment%20flowchart.png)
