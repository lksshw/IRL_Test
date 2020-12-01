# Apprenticeship IRL

Traditional reinforcement learning algorithms involve defining an explicit feedback signal/reward. This feedback signal, directs an agent to recover optimal behavior for the task at hand. A major problem of this form of explicit preemptive goal definition is that it breaks down at slightly complex tasks. The confusion lies in deciding what the right reward is, whether to assign a +/- reward as in Atari, or to define a reward _function_ which is dependent on several variables (position, velocity etc.). Such explicit goal definitions will always be biased to what we think is the correct reward to assign. This may be trivial, redundant or may not be robust enough to recover optimal behavior. Moreover, biological learning systems do not work this way. The plasticity of the brain ensures that rewards are flexible, morphing its credit assignment to the task at hand. Inspired by this behavior, the domain of Inverse Reinforcement Learning (IRL) enables an agent to discover what the correct reward function is on its own. For it to do so, the agent is provided with an ideal and near optimal policy to begin with. This optimal policy is nothing but a human navigating the agent manually and recording their action and reward at each state. Given that such an optimal policy is available, the task of inverse reinforcement learning is to recover the reward function underlying this optimal policy. Such recovery is usually implicit--- in the form of a learned neural network that takes in frame inputs and spews out a reward. This new direction of research of IRL has developed quite rapidly over the past few years. However, it all began with a paper by Pieter Abbeel and Andrew N.G titled Apprenticeship learning. This repository is an experiment and benchmark of the apprenticeship learning IRL algorithm. It is setup in a slightly complex navigation environment that contains dynamic obstacles (the environment is displayed below). You can read the full paper and methodology **[here](https://ai.stanford.edu/~ang/papers/icml04-apprentice.pdf)** 


![](media/output.gif)

The best policy recovered after training. A noteworthy moment is when the agent avoids the rotating bar. Even though promising, apprenticeship IRL is not robust enough for navigation in dynamic environments.
---

## Replication

Please use a virtualenv to replicate my results. We can't have you creating a mess of your packages. Once you're on your virtualenv you'll need to install the following dependencies. 

* Pygame
* Pymunk
* Python3
* Keras (2.1.x)
* Tensorflow (1.1x)

---

- Once setup simply run:
    ```bash
    $ python3 playing.py '2'
    ```

This command will fetch policy no.2 from the saved_policies folder.


### Training

In case you are interested in training the agent from scratch, you will first need to provided some expert trajectories to the model. 

These expert trajectories are set when you manually drive around the obstacles using your arrow keys.

- Get a single expert trajectory by running:
    ```bash
    $ python3 manualControl.py
    ```
After you finish navigating, copy the sensor weights and paste it as one of the W's in *policyEvaluation.py*

You will need to get 7-10 such expert policies and paste their sensor weights in *policyEvaluation.py*

- To train using apprenticeship IRL run:
    ```bash
    $ python3 learning.py
    ```
    
The weights are saved to the *saved-models* folder 


### References


* The original Apprenticeship IRL implementation on a simple static environment [toyCarIRL](https://github.com/jangirrishabh/toyCarIRL)

* Apprenticeship learning by [NG Et al.](https://ai.stanford.edu/~ang/papers/icml04-apprentice.pdf)

