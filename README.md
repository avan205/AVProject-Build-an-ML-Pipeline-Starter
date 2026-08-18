# Build an ML Pipeline for Short-Term Rental Prices in NYC
You are working for a property management company renting rooms and properties for short periods of 
time on various rental platforms. You need to estimate the typical price for a given property based 
on the price of similar properties. Your company receives new data in bulk every week. The model needs 
to be retrained with the same cadence, necessitating an end-to-end pipeline that can be reused.

In this project you will build such a pipeline.

## Table of contents

- [Preliminary steps](#preliminary-steps)
  * [Fork the Starter Kit](#fork-the-starter-kit)
  * [Create environment](#create-environment)
  * [Get API key for Weights and Biases](#get-api-key-for-weights-and-biases)
  * [The configuration](#the-configuration)
  * [Running the entire pipeline or just a selection of steps](#Running-the-entire-pipeline-or-just-a-selection-of-steps)
  * [Pre-existing components](#pre-existing-components)

## Preliminary steps

### Supported Operating Systems

This project is compatible with the following operating systems:

- **Ubuntu 22.04** (Jammy Jellyfish) - both Ubuntu installation and WSL (Windows Subsystem for Linux)
- **Ubuntu 24.04** - both Ubuntu installation and WSL (Windows Subsystem for Linux)
- **macOS** - compatible with recent macOS versions

Please ensure you are using one of the supported OS versions to avoid compatibility issues.

### Python Requirement

This project requires **Python 3.13**. Please ensure that you have Python 3.13 installed and set as the default version in your environment to avoid any runtime issues.

### Fork the Starter kit
Go to [https://github.com/udacity/Project-Build-an-ML-Pipeline-Starter](https://github.com/udacity/Project-Build-an-ML-Pipeline-Starter)
and click on `Fork` in the upper right corner. This will create a fork in your Github account, i.e., a copy of the
repository that is under your control. Now clone the repository locally so you can start working on it:

```
git clone https://github.com/[your github username]/Project-Build-an-ML-Pipeline-Starter.git
```

and go into the repository:

```
cd Project-Build-an-ML-Pipeline-Starter
```
Commit and push to the repository often while you make progress towards the solution. Remember 
to add meaningful commit messages.

### Create environment
Make sure to have conda installed and ready, then create a new environment using the ``environment.yaml``
file provided in the root of the repository and activate it:

```bash
> conda env create -f environment.yml
> conda activate nyc_airbnb_dev
```

### Get API key for Weights and Biases
Let's make sure we are logged in to Weights & Biases. Get your API key from W&B by going to 
[https://wandb.ai/authorize](https://wandb.ai/authorize) and click on the + icon (copy to clipboard), 
then paste your key into this command:

```bash
> wandb login [your API key]
```

You should see a message similar to:
```
wandb: Appending key for api.wandb.ai to your netrc file: /home/[your username]/.netrc
```


### The configuration
As usual, the parameters controlling the pipeline are defined in the ``config.yaml`` file defined in
the root of the starter kit. We will use Hydra to manage this configuration file. 
Open this file and get familiar with its content. Remember: this file is only read by the ``main.py`` script 
(i.e., the pipeline) and its content is
available with the ``go`` function in ``main.py`` as the ``config`` dictionary. For example,
the name of the project is contained in the ``project_name`` key under the ``main`` section in
the configuration file. It can be accessed from the ``go`` function as 
``config["main"]["project_name"]``.

NOTE: do NOT hardcode any parameter when writing the pipeline. All the parameters should be 
accessed from the configuration file.

### Running the entire pipeline or just a selection of steps
In order to run the pipeline when you are developing, you need to be in the root of the starter kit, 
then you can execute as usual:

```bash
>  mlflow run .
```
This will run the entire pipeline.

When developing it is useful to be able to run one step at the time. Say you want to run only
the ``download`` step. The `main.py` is written so that the steps are defined at the top of the file, in the 
``_steps`` list, and can be selected by using the `steps` parameter on the command line:

```bash
> mlflow run . -P steps=download
```
If you want to run the ``download`` and the ``basic_cleaning`` steps, you can similarly do:
```bash
> mlflow run . -P steps=download,basic_cleaning
```
You can override any other parameter in the configuration file using the Hydra syntax, by
providing it as a ``hydra_options`` parameter. For example, say that we want to set the parameter
modeling -> random_forest -> n_estimators to 10 and etl->min_price to 50:

```bash
> mlflow run . \
  -P steps=download,basic_cleaning \
  -P hydra_options="modeling.random_forest.n_estimators=10 etl.min_price=50"
```

### Pre-existing components
In order to simulate a real-world situation, we are providing you with some pre-implemented
re-usable components. While you have a copy in your fork, you will be using them from the original
repository by accessing them through their GitHub link, like:

```python
_ = mlflow.run(
                f"{config['main']['components_repository']}/get_data",
                "main",
                version='main',
                env_manager="conda",
                parameters={
                    "sample": config["etl"]["sample"],
                    "artifact_name": "sample.csv",
                    "artifact_type": "raw_data",
                    "artifact_description": "Raw file as downloaded"
                },
            )
```
where `config['main']['components_repository']` is set to 
[https://github.com/udacity/Project-Build-an-ML-Pipeline-Starter/tree/main/components](https://github.com/udacity/Project-Build-an-ML-Pipeline-Starter/tree/main/components).
You can see the parameters that they require by looking into their `MLproject` file:

- `get_data`: downloads the data. [MLproject](https://github.com/udacity/Project-Build-an-ML-Pipeline-Starter/blob/main/components/get_data/MLproject)
- `train_val_test_split`: segrgate the data (splits the data) [MLproject](https://github.com/udacity/Project-Build-an-ML-Pipeline-Starter/blob/main/components/train_val_test_split/MLproject)

## In case of errors

### Environments
When you make an error writing your `conda.yml` file, you might end up with an environment for the pipeline or one
of the components that is corrupted. Most of the time `mlflow` realizes that and creates a new one every time you try
to fix the problem. However, sometimes this does not happen, especially if the problem was in the `pip` dependencies.
In that case, you might want to clean up all conda environments created by `mlflow` and try again. In order to do so,
you can get a list of the environments you are about to remove by executing:

```
> conda info --envs | grep mlflow | cut -f1 -d" "
```

If you are ok with that list, execute this command to clean them up:

**_NOTE_**: this will remove *ALL* the environments with a name starting with `mlflow`. Use at your own risk

```
> for e in $(conda info --envs | grep mlflow | cut -f1 -d" "); do conda uninstall --name $e --all -y;done
```

This will iterate over all the environments created by `mlflow` and remove them.

### MLflow & Wandb

If you see the any error while running the command:

```
> mlflow run .
```

Please, make sure all steps are using **the same** python version and that you have **conda installed**. Additionally, *mlflow* and *wandb* packages are crucial and should have the same version.


## License

[License](LICENSE.txt)


Project Links

GitHub: https://github.com/avan205/AVProject-Build-an-ML-Pipeline-Starter

W&B: https://wandb.ai/avan205-western-governors-university/nyc_airbnb


Sources: 
References

Can someone explain what weights and biases are? (2023, July 23). DeepLearning.AI. https://community.deeplearning.ai/t/can-someone-explain-what-weights-and-biases-are/394280
Chauhan, A. (2021, February 23). Random Forest Classifier and its hyperparameters. medium.com. Retrieved August 17, 2026, from https://medium.com/analytics-vidhya/random-forest-classifier-and-its-hyperparameters-8467bec755f6
Contributors, P. (2023, January 1). Optimizing model parameters. https://docs.pytorch.org/tutorials/beginner/basics/optimization_tutorial.html
GeeksforGeeks. (2024, July 19). mindepth and maxdepth in Linux find() command for limiting search to a specific directory. GeeksforGeeks. https://www.geeksforgeeks.org/linux-unix/mindepth-maxdepth-linux-find-command-limiting-search-specific-directory/
GeeksforGeeks. (2025a, July 3). Hyperparameters of random forest classifier. GeeksforGeeks. https://geeksforgeeks.org/machine-learning/hyperparameters-of-random-forest-classifier/
GeeksforGeeks. (2025b, July 23). How to Fix Git Error: There is No Tracking Information for the Current Branch. GeeksforGeeks. https://www.geeksforgeeks.org/git/how-to-fix-git-error-there-is-no-tracking-information-for-the-current-branch/#google_vignette
GeeksforGeeks. (2026, May 2). Random Forest hyperparameter tuning in Python. GeeksforGeeks. https://www.geeksforgeeks.org/machine-learning/random-forest-hyperparameter-tuning-in-python/
GitLab. (n.d.). What is YAML: Understanding the Basics. GitLab. https://about.gitlab.com/topics/devops/what-is-yaml/
Hanson, J. (2015, November 5). What does the GREP command do? Ubuntu. Retrieved August 12, 2026, from https://askubuntu.com/questions/349523/what-does-the-grep-command-do
Has anyone completed D501 - Machine Learning DevOps? (2023). reddit. https://www.reddit.com/r/WGUIT/comments/18rmgcb/has_anyone_completed_d501_machine_learning_devops/
Kavlakoglu, E. (2025, November 20). What is random forest? IBM. Retrieved August 12, 2026, from https://www.ibm.com/think/topics/random-forest
kedion. (2021, December 14). Managing machine learning lifecycles with MLFlow. medium.com. Retrieved August 12, 2026, from https://kedion.medium.com/managing-machine-learning-lifecycles-with-mlflow-d4ce3d91ee10
Managing environments — conda 26.7.1.dev40 documentation. (n.d.). https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html
Mandepudi, M. K. (2025, January 19). The Ultimate guide to parameters, hyperparameters, and hyperparameter tuning in machine learning. www.medium.com. Retrieved August 17, 2026, from https://blog.devgenius.io/the-ultimate-guide-to-parameters-hyperparameters-and-hyperparameter-tuning-in-machine-learning-aadeaf3d2438
Mlflow. (n.d.). Releases · mlflow/mlflow. GitHub. https://github.com/mlflow/mlflow/releases
MLFlow — open source AI platform for agents, LLMs & models. (n.d.). MLflow. https://mlflow.org/docs/latest/ml/model/dependencies/
MLFlow on DataBricks | DataBricks on AWS. (2026, August 5). https://docs.databricks.com/aws/en/mlflow/
Mondal, S. (2024, August 16). Understanding MAE, MSE, and RMSE: Key metrics in Machine Learning. medium.com. Retrieved August 18, 2026, from https://medium.com/@mondalsabbha/understanding-mae-mse-and-rmse-key-metrics-in-machine-learning-eeeff8bd1fac
Multi-run | Hydra. (n.d.). https://hydra.cc/docs/tutorials/basic/running_your_app/multi-run/
New York City Department of City Planning (DCP). (2026). New York City Borough boundary. https://s-media.nyc.gov/agencies/dcp/assets/files/pdf/data-tools/bytes/nybb_metadata.pdf
Optuna - A hyperparameter optimization framework. (n.d.). Optuna. https://optuna.org/
Patru, G. (2026, June 5). Git Detached Head - 3f7d516d-7076-49d1-9089-656dd3c5f971. Git Detached Head: What This Means and How to Recover. Retrieved August 18, 2026, from https://www.cloudbees.com/blog/git-detached-head
PIP Install. (n.d.). https://docs.mantidproject.org/v6.9.0/concepts/PipInstall.html
Python and Conda | High Performance Computing | Washington State University. (n.d.). https://hpc.wsu.edu/programmers-guide/python/
Riad, A. (2025, July 22). Build a Production-Ready ML pipeline in 12 steps [Online forum post]. LinkedIn. https://www.linkedin.com/posts/riadanas_build-a-production-ready-ml-pipeline-in-12-activity-7353311174974705665-RG68
Sharma, K. (2024, November 10). Mastering random forest hyperparameter tuning for enhanced machine learning models. www.medium.com. Retrieved August 17, 2026, from https://medium.com/@kalpit.sharma/mastering-random-forest-hyperparameter-tuning-for-enhanced-machine-learning-models-2d1a8c6c426f
Shell programming with bash: by example, by counter-example. (n.d.). https://matt.might.net/articles/bash-by-example/
The ML Engineering Guy. (2024, February 9). Hydra: An Advanced Configuration Management tool for ML/Python Code. Medium.com. Retrieved August 12, 2026, from https://medium.com/mlops-io/hydra-an-advanced-configuration-management-tool-for-ml-python-code-411169628477
Udacity. (n.d.). GitHub - udacity/Project-Build-an-ML-Pipeline-Starter: This is a custom project for WGU, the original project repo is https://github.com/udacity/nd0821-c2-build-model-workflow-starter. GitHub. https://github.com/udacity/Project-Build-an-ML-Pipeline-Starter
Udacity. (2026). Marvin AI 
Understanding TF-IDF (Term Frequency-Inverse Document Frequency). (2026, July 2). Geeksforgeeks. Retrieved August 18, 2026, from https://www.geeksforgeeks.org/machine-learning/understanding-tf-idf-term-frequency-inverse-document-frequency/
W3Schools.com. (n.d.-a). https://www.w3schools.com/bash/bash_commands.php
W3Schools.com. (n.d.-b). https://www.w3schools.com/bash/bash_sed.php
Weights and Biases in machine learning | H2O.ai Wiki. (n.d.). https://h2o.ai/wiki/weights-and-biases/
What is YAML? (n.d.). https://www.redhat.com/en/topics/automation/what-is-yaml

