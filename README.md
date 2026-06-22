Proof-of-Work Feedback Simulation Code

This repository contains the simulation code used for the master’s thesis on Proof-of-Work as a feedback-regulated event-generation mechanism.

The code models and simulates difficulty-adjustment mechanisms inspired by Bitcoin and Ethereum Homestead. The main purpose is to study how Proof-of-Work systems regulate event generation under stochastic event arrivals, changing hash-rate, and feedback-based difficulty adjustment.

Project overview

The repository includes code for:

* Bitcoin-style windowed difficulty adjustment
* Ethereum Homestead-style incremental difficulty adjustment
* Stochastic event-generation simulations
* Hash-rate shock experiments
* Monte Carlo simulations
* Validation plots based on real Bitcoin inter-event data
* Analysis of bias under exponential hash-rate growth

Main files

main.py

Runs the main Bitcoin and Ethereum validation-simulations with generalized parameter settings. Running different simulations with different parameters is therefore easy. 

validation_of_average_mechanism.py

Tests how the averaging window size affects the observed inter-event time.

validation_of_control_properties_btc.py

Runs a Bitcoin-style hash-rate shock test.

This is used to validate the control properties of the windowed Bitcoin-inspired difficulty-adjustment mechanism. Also implemented with generalized shocks, different simulations with different shocks is therefore easy. 

pow_model_monte_carlo_shock_test.py

Runs Monte Carlo simulations for the Ethereum Homestead-inspired mechanism under a hash-rate shock. Also implemented with generalized shocks, different simulations with different shocks is therefore easy. 

plot_bias_under_exp_hashrate_growth.py

Plots the analytical bias in averaged inter-event time under exponential hash-rate growth.


Install dependencies with:

requirements.txt

Data availability

The repository contains both real blockchain datasets and generated datasets used for experimental studies.

Real Bitcoin and Ethereum datasets are pre-processed before simulation using the scripts defined in `data_pre_process`.

Reproducing results

To reproduce the model validation simulations, run:

main.py

To reproduce closed-loop dynamics , run following scripts:

validation_of_average_mechanism.py
validation_of_control_properties_btc.py
pow_model_monte_carlo_shock_test.py
plot_bias_under_exp_hashrate_growth.py

Reproducibility note

Several simulations rely on stochastic event generation. Exact numerical results may therefore vary between runs 

Thesis context

This code was developed as part of a master’s thesis investigating Proof-of-Work as a self-regulated event-generation mechanism.

The thesis studies how difficulty adjustment can be interpreted as a feedback controller that regulates the event-generation rate under changing computational power and stochastic event arrivals.

Citation

If you use this code in academic work, please cite the associated master’s thesis:

T. Vitsø, Proof-of-Work as a Self-Regulated Event-Generation Mechanism, Master’s thesis, Norwegian University of Science and Technology (NTNU), 2026.

The simulation code is available at:

https://github.com/torbjornvitso/pow_model_thesis

If you use this code in academic work, please cite:

T. Vitsø, *Proof-of-Work as a Self-Regulated Event-Generation Mechanism: Simulation Code*, GitHub repository, 2026. Available: https://github.com/torbjornvitso/pow_model_thesis

Please also cite the associated master's thesis when referencing the scientific results.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

Author

Torbjørn Vitsø
Master’s thesis, NTNU