# Deploy ML Pipelines on Kubernetes with Bodywork

![bodywork](https://bodywork-media.s3.eu-west-2.amazonaws.com/ml_pipeline.png)

This repository contains a Bodywork project that demonstrates how to run a ML pipeline on Kubernetes, with Bodywork. The example ML pipeline has two stages:

1. Run a batch job to train a model.
2. Deploy the trained model as service with a REST API.

To run this project, follow the steps below.

## Get Access to a Kubernetes Cluster

In order to run this example project you will need access to a Kubernetes cluster. To setup a single-node test cluster on your local machine you can use [minikube](https://minikube.sigs.Kubernetes.io/docs/) or [docker-for-desktop](https://www.docker.com/products/docker-desktop). Check your access to Kubernetes by running,

```shell
$ kubectl cluster-info
```

Which should return the details of your cluster.

## Install the Bodywork Python Package

```shell
$ pip install bodywork
```

## Setup a Kubernetes Namespace for use with Bodywork

```shell
$ bodywork setup-namespace ml-pipeline
```

## Run the ML Pipeline

To test the ML pipeline, using a workflow-controller running on your local machine and interacting with your Kubernetes cluster, run,

```shell
$ bodywork workflow \
    --namespace=ml-pipeline \
    https://github.com/bodywork-ml/bodywork-ml-pipeline-project \
    master
```

The workflow-controller logs will be streamed to your shell's standard output until the job has been successfully completed.

## Testing the Model-Scoring Service

Service deployments are accessible via HTTP from within the cluster - they are not exposed to the public internet, unless you have [installed an ingress controller](https://bodywork.readthedocs.io/en/latest/kubernetes/#configuring-ingress) in your cluster. The simplest way to test a service from your local machine, is by using a local proxy server to enable access to your cluster. This can be achieved by issuing the following command,

```shell
$ kubectl proxy
```

Then in a new shell, you can use the curl tool to test the service. For example,

```shell
$ curl http://localhost:8001/api/v1/namespaces/ml-pipeline/services/bodywork-ml-pipeline-project--stage-2-scoring-service/proxy/iris/v1/score \
    --request POST \
    --header "Content-Type: application/json" \
    --data '{"sepal_length": 5.1, "sepal_width": 3.5, "petal_length": 1.4, "petal_width": 0.2}'
```

Should return,

```json
{
    "species_prediction":"setosa",
    "probabilities":"setosa=1.0|versicolor=0.0|virginica=0.0",
    "model_info": "DecisionTreeClassifier(class_weight='balanced', random_state=42)"
}
```

According to how the payload has been defined in the `stage-2-scoring-service/serve_model.py` module.

If an ingress controller is operational in your cluster, then the service can be tested via the public internet using,

```shell
$ curl http://YOUR_CLUSTERS_EXTERNAL_IP/ml-pipeline/bodywork-ml-pipeline-project--stage-2-scoring-service/iris/v1/score \
    --request POST \
    --header "Content-Type: application/json" \
    --data '{"sepal_length": 5.1, "sepal_width": 3.5, "petal_length": 1.4, "petal_width": 0.2}'
```

See [here](https://bodywork.readthedocs.io/en/latest/kubernetes/#connecting-to-the-cluster) for instruction on how to retrieve `YOUR_CLUSTERS_EXTERNAL_IP`.

## Running the ML Pipeline on a Schedule

If you're happy with the test results, you can schedule the workflow-controller to operate remotely on the cluster on a pre-defined schedule. For example, to setup the the workflow to run every hour, use the following command,

```shell
$ bodywork cronjob create \
    --namespace=ml-pipeline \
    --name=train-and-deploy \
    --schedule="0 * * * *" \
    --git-repo-url=https://github.com/bodywork-ml/bodywork-ml-pipeline-project \
    --git-repo-branch=master
```

Each scheduled workflow will attempt to re-run the batch-job, as defined by the state of this repository's `master` branch at the time of execution.

To get the execution history for all `train-and-deploy` jobs use,

```shell
$ bodywork cronjob history \
    --namespace=ml-pipeline \
    --name=train-and-deploy
```

Which should return output along the lines of,

```text
JOB_NAME                                START_TIME                    COMPLETION_TIME               ACTIVE      SUCCEEDED       FAILED
train-and-deploy-1605214260             2020-11-12 20:51:04+00:00     2020-11-12 20:52:34+00:00     0           1               0
```

Then to stream the logs from any given cronjob run (e.g. to debug and/or monitor for errors), use,

```shell
$ bodywork cronjob logs \
    --namespace=ml-pipeline \
    --name=train-and-deploy-1605214260
```

## Cleaning Up

To clean-up the deployment in its entirety, delete the namespace using kubectl - e.g. by running,

```shell
$ kubectl delete ns ml-pipeline
```

## Make this Project Your Own

This repository is a [GitHub template repository](https://docs.github.com/en/free-pro-team@latest/github/creating-cloning-and-archiving-repositories/creating-a-repository-from-a-template) that can be automatically copied into your own GitHub account by clicking the `Use this template` button above.

After you've cloned the template project, use official [Bodywork documentation](https://bodywork.readthedocs.io/en/latest/) to help modify the project to meet your own requirements.
