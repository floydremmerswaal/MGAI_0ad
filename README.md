# Modern Game AI Algorithms Project: PCG and Kiting in 0 A.D.

In order to run the project, you will need to install version 0.23 of 0 A.D., available [here](https://releases.wildfiregames.com/).

You can add pyrogenesis to your environment variables for easier use, otherwise always specify the path to the execution file. 
<br>
In Windows, that file should be: `game_install_path/binaries/system/pyrogenesis.exe` <br>
In MacOS, the file should be: `/Applications/0 A.D..app/Contents/MacOS/pyrogenesis`

You will also need to add the RL-scenarios mod to 0 A.D., which we have provided in the zero_ad_rl folder (zipped folder **_0ad_rl_maps.zip_**). To add the mod to 0 A.D., run `pyrogenesis /path/to/mod/mod.zip` in a terminal.

## Project Setup
We recommend you create a new conda environment to run the project. <br>
To install the project's required packages, you will need to run:

```
python install zero_ad/.
python install -e zero_ad_rl/.
python install -r requirements.txt
```

## Training Agent
### Game Launch
To train an agent in a specific environment, you will first need to start 0 A.D. When training an agent, we suggest that you start 0 A.D. with the graphics disabled as this will speed up the training process. This can be done by running the following command in a terminal: 
```
pyrogenesis --rl-interface=0.0.0.0:6000 --autostart-nonvisual --mod=rl-scenarios --mod=public
```
As you can see, you also need to specify the mods to launch and use, as well as assign a port for the python scripts to connect to.

### Training
To train an agent, you can then use the following command:

```
python -m zero_ad_rl.train --env CavalryVsInfantry --run PPO --checkpoint-freq 25
```
You can change the training algorithm with `--run <algo>` by specifying one of rllib's [built-in algorithms](https://docs.ray.io/en/latest/rllib/rllib-algorithms.html).
You can also switch which environment to train the agent on using `--env <env_name>`. The options are; **_CavalryVsInfantry_**, **_CavalryVsInfantryMaze_** and **_CavalryVsInfantryCity_**.
The code uses rllib to train agents register on a defined environment.

### Rollout
Finally, to perform rollout on the trained agent, we recommend that you stop the current running process of 0 A.D. to run it with graphics enabled (simply remove `--autostart-nonvisual`).<br>
You can then run the rollout function on a specific training checkpoint with the following command:

```
python -m zero_ad_rl.rollout_pcg ~/ray_results/path/to/checkpoint/file --env CavalryVsInfantry --run PPO --pcg --steps 5000
```
By default, the rollout will not generate a new map to evaluate the agent on, simply add/remove `--pcg` to turn this option on/off.

**Note**: an agent can have been trained on an evironment (say **_CavalryVsInfantry_**) and evaluated using a different one (say **_CavalryVsInfantryMaze_**). Simply specify the CavalryVsInfantryMaze enviroment when performing the rollout.