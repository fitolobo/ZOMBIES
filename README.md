# 🧟 Zombies Apocalypse Simulation

This project simulates population dynamics between humans (`L`) and zombies (`Z`) using discrete-time and continuous time Lotka-Volterra model type with periodic zombie removal events based on [this paper](https://www.scielo.br/j/rbef/a/YSy6tP3JBSZ3CVgVYTtp5VG/?lang=en&format=html). We modify the based model idea for receiving Dirac delta-like interventions (in parameters or directly on populations). The tests were applied computationally. The analysis was made just for reviewing the paper model. These interventions (called vaccines in this experiments) are modeled as **Dirac delta-like pulses** that reduce the zombie population at fixed intervals, simulating vaccines or external control mechanisms.

## 🧪 How to Run the Simulation

### 1. 🐍 Create environment and install dependencies

If you don't have Poetry installed yet:

```bash
    pip install poetry
``` 
Then install dependencies defined in pyproject.toml:
```
    poetry install
``` 
2. ▶️ Run the simulation
Use the following command to run the main script (from the project root):

```
    poetry run python zombies_apocalypse_vaccine_normal.py
``` 

After the simulation, a plot will be saved automatically under ./results/ with the same name as the script:

```
    results/zombies_apocalypse_vaccine_normal.png
````

📈 What is being simulated?
L (humans): susceptible population.
Z (zombies): infected/hostile population.

Two different possibilities for exogenous intervetions: 

1 - (Normal)Vaccine/Intervention: every vaccine_period time steps, 10% of the zombie population is removed instantly, like a Dirac delta impulse.

![Normal Vaccine Diagram](./diagrams/normal.png)

2 - (New or different) Vaccine/Intervention: every vaccine_period time steps, to modify the effectivenss or ratio of L,Z interaction converting humans into zombies. --> this version seems to be more realistic in terms of interaction.

![Modifying Gamma Diagram](./diagrams/modifying_infection_rate.png)

Comparisons: plots show both the model with and without interventions.

🔧 Modify parameters
To customize simulation parameters, edit the values in:

# In zombies_apocalypse_vaccine_normal.py
```
vaccine_period = 20         # how often the intervention is applied
zombie_removal_ratio = 0.1  # how much of Z is removed
time_steps = 1000           # total simulation steps
```
📤 Output
The script saves a .png plot showing:

Human and zombie populations over time with intervention.
Comparison against a baseline without intervention.
Vertical impulses representing intervention events (Dirac delta-like).

📚 Requirements
All dependencies are managed via Poetry:
```
    Python 3.11+

    NumPy

    SciPy

    Matplotlib
```
You can find and modify them in the [tool.poetry.dependencies] section of pyproject.toml.

👨‍🔬 Author
Rodolfo Lobo
University of Chile
📧 rodolfolobo@ug.uchile.cl