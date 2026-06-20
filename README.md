Proof-of-Work Feedback Simulation Code

This repository contains the simulation code used for the master’s thesis on Proof-of-Work as a feedback-regulated event-generation mechanism.

The code models and simulates difficulty-adjustment mechanisms inspired by Bitcoin and Ethereum Homestead. The main purpose is to study how Proof-of-Work systems regulate event generation under stochastic block arrivals, changing hash-rate, and feedback-based difficulty adjustment.

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

Runs the main Bitcoin and Ethereum simulations.

The Bitcoin simulation uses a windowed bounded proportional controller with:

* Window size N = 2016
* Reference inter-event time T_ref = 600 seconds
* Difficulty adjustment bounds corresponding to Bitcoin’s adjustment limits

The Ethereum Homestead simulation uses an incremental bounded proportional controller with:

* Window size N = 1
* Quantized timing index phi = 10
* Correction term bounds u_min = -99, u_max = 1

Run with:

python main.py

Implements the Bitcoin-inspired windowed feedback mechanism.

The model:

1. Reads pre-processed Bitcoin hash-rate and difficulty data.
2. Computes the probability of success from difficulty.
3. Simulates stochastic timestamps from the event rate.
4. Computes observed inter-event times.
5. Applies a bounded correction map.
6. Updates difficulty according to a Bitcoin-style adjustment rule.
7. Writes simulation results and generates plots.

pow_model_incremental.py

Implements the Ethereum Homestead-inspired incremental difficulty mechanism.

The model:

1. Reads pre-processed Ethereum Homestead data.
2. Computes stochastic event generation from hash-rate and difficulty.
3. Estimates observed inter-event time.
4. Applies the quantized Ethereum timing correction.
5. Updates difficulty recursively.
6. Writes simulation results and generates plots.

validation_of_average_mechanism.py

Tests how the averaging window size affects the observed inter-event time.

This script compares different window sizes:

N_list = [10, 20, 50, 100, 500, 1500, 2016]

and generates:

validation_of_average_mechanism.png

validation_of_control_properties_btc.py

Runs a Bitcoin-style hash-rate shock test.

This is used to validate the control properties of the windowed Bitcoin-inspired difficulty-adjustment mechanism.

pow_model_monte_carlo_shock_test.py

Runs Monte Carlo simulations for the Ethereum Homestead-inspired mechanism under a hash-rate shock.

The script generates plots for:

* Mean difficulty response
* Difficulty percentile band
* Correction term response
* Inter-event time response
* Mean recovery under hash-rate shock

The main simulation is run with:

python pow_model_monte_carlo_shock_test.py

plot_real_btc_model_validation.py

Generates validation plots based on real Bitcoin data.

The script produces:

* Real Bitcoin inter-event time distribution
* Windowed averaged inter-event time distribution
* Evolution of averaged inter-event time over adjustment windows

Run with:

python plot_real_btc_model_validation.py

plot_bias_under_exp_hashrate_growth.py

Plots the analytical bias in averaged inter-event time under exponential hash-rate growth.

Run with:

python plot_bias_under_exp_hashrate_growth.py

Dependencies

The code mainly depends on:

numpy
pandas
matplotlib

Install dependencies with:

pip install -r requirements.txt

Data availability

The repository contains both real blockchain datasets and synthetically generated datasets used throughout the thesis.

Real Bitcoin and Ethereum datasets are pre-processed before simulation using the scripts defined in `data_pre_process.py`.

Data

The simulations use pre-processed Bitcoin and Ethereum data files defined in data_io.py.

Typical data paths include:

* Bitcoin node data
* Ethereum Homestead data
* Generated hash-rate shock data
* Simulation result files

Some scripts generate synthetic shock-test data before running the simulations.

Reproducing results

To reproduce the main thesis simulations, run:

python main.py

To reproduce individual validation figures, run the corresponding plotting or validation script:

python validation_of_average_mechanism.py
python validation_of_control_properties_btc.py
python pow_model_monte_carlo_shock_test.py
python plot_real_btc_model_validation.py
python plot_bias_under_exp_hashrate_growth.py

Generated figures are saved as .png files in the working directory unless otherwise specified in the script.

Reproducibility note

Several simulations rely on stochastic event generation. Exact numerical results may therefore vary between runs 

Thesis context

This code was developed as part of a master’s thesis investigating Proof-of-Work as a feedback-regulated event-generation mechanism.

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