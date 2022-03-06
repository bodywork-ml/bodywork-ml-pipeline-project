# Deploy ML Pipelines on Kubernetes with Bodywork

![bodywork](https://bodywork-media.s3.eu-west-2.amazonaws.com/ml_pipeline.png)

This repository demonstrates how to run a continuous training pipeline on Kubernetes, using Bodywork. The example ML pipeline has two stages:

1. Run a batch job to train a model.
2. Deploy the trained model as service with a REST API.

For information on this demo, take a look [here](https://bodywork.readthedocs.io/en/latest/quickstart_ml_pipeline/). To run this project, follow the steps below. If you are new to Kubernetes, then take a look at our [Kubernetes Quickstart Guide](https://bodywork.readthedocs.io/en/latest/kubernetes/#quickstart).

## Install Bodywork

Bodywork is distributed as a Python package that can be installed using Pip,

```shell
$ pip install bodywork
```

## Run the ML Pipeline

To test the pipeline defined in thie repository run,

```shell
$ bodywork create deployment https://github.com/bodywork-ml/bodywork-ml-pipeline-project
```

Logs will be streamed to your terminal until the job has been successfully completed.

## Make this Project Your Own

This repository is a [GitHub template repository](https://docs.github.com/en/free-pro-team@latest/github/creating-cloning-and-archiving-repositories/creating-a-repository-from-a-template) that can be automatically copied into your own GitHub account by clicking the `Use this template` button above.

After you've cloned the template project, use official [Bodywork documentation](https://bodywork.readthedocs.io/en/latest/) to help modify the project to meet your own requirements.
