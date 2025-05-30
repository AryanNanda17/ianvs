# How to config testenv

The algorithm developer is able to test his/her own targeted algorithm, he/she should prepare the test environment.
how to config test environment, please to refer to the following configuration information.

## The configuration of testenv

| Property | Required | Description |
|----------|----------|-------------|
|dataset|yes|[The configuration of dataset](https://github.com/kubeedge/ianvs/blob/main/docs/user_interface/how-to-config-testenv.md#the-configuration-of-dataset)|
|model_eval|no|[The configuration of model_eval](https://github.com/kubeedge/ianvs/blob/main/docs/user_interface/how-to-config-testenv.md#the-configuration-of-model_eval)
|metrics|yes|The metrics used for test case's evaluation; Type: list; Value Constraint: the list of [the configuration of metric](https://github.com/kubeedge/ianvs/blob/main/docs/user_interface/how-to-config-testenv.md#the-configuration-of-metric).|
|incremental_rounds|no|Incremental rounds setting for incremental learning paradigm; Type: int; Default value: 2; Value Constraint: the value must be not less than 2. |

For example:

```yaml
testenv:
  # dataset configuration
  dataset:
    ...
  # model eval configuration of incremental learning;
  model_eval:
    ...
  # metrics configuration for test case's evaluation; list type;
  metrics:
    ...
  # incremental rounds setting for incremental learning paradigm; int type; default value is 2;
  # the value must be not less than 2;
  incremental_rounds: 2
```

### The configuration of dataset

| Property | Required | Description |
|----------|----------|-------------|
|train_url|yes|The url address of train dataset index; Type: string|
|test_url|yes|The url address of test dataset index; Type: string|

For example:

```yaml
# dataset configuration
dataset:
  # the url address of train dataset index; string type;
  train_index: "./dataset/train_data/index.txt"
  # the url address of test dataset index; string type;
  test_index: "./dataset/test_data/index.txt"
```

### The configuration of model_eval

| Property | Required | Description |
|----------|----------|-------------|
|model_metric|yes|The Metric used for model evaluation; [The configuration of metric](https://github.com/kubeedge/ianvs/blob/main/docs/user_interface/how-to-config-testenv.md#the-configuration-of-metric).|
|threshold|yes|Threshold of condition for triggering inference model to update; Type: float/int|
|operator|yes|Operator of condition for triggering inference model to update; Type: string; Value Constraint: the values are ">=", ">", "<=", "<" and "=".|

For example:

```yaml
# model eval configuration of incremental learning;
model_eval:
  # metric used for model evaluation
  model_metric:
    ...
  # condition of triggering inference model to update
  # threshold of the condition; types are float/int
  threshold: 0.01
  # operator of the condition; string type;
  # values are ">=", ">", "<=", "<" and "=";
  operator: ">="
```

### The configuration of metric

| Property | Required | Description |
|----------|----------|-------------|
|name|yes|Metric name; Type: string; Value Constraint: a python module name|
|url|no|The url address of python module file; Type: string.|

For example:

```yaml
# metric used for model evaluation
model_metric:
  # metric name; string type;
  name: "f1_score"
  # the url address of python file
  url: "./examples/pcb-aoi/incremental_learning_bench/fault_detection/testenv/f1_score.py"
```

## Show example

```yaml
# testenv.yaml
testenv:
  # dataset configuration
  dataset:
    # the url address of train dataset index; string type;
    train_index: "./dataset/train_data/index.txt"
    # the url address of test dataset index; string type;
    test_index: "./dataset/test_data/index.txt"

  # model eval configuration of incremental learning;
  model_eval:
    # metric used for model evaluation
    model_metric:
      # metric name; string type;
      name: "f1_score"
      # the url address of python file
      url: "./examples/pcb-aoi/incremental_learning_bench/fault_detection/testenv/f1_score.py"

    # condition of triggering inference model to update
    # threshold of the condition; types are float/int
    threshold: 0.01
    # operator of the condition; string type;
    # values are ">=", ">", "<=", "<" and "=";
    operator: ">="

  # metrics configuration for test case's evaluation; list type;
  metrics:
    # metric name; string type;
    - name: "f1_score"
      # the url address of python file
      url: "./examples/pcb-aoi/incremental_learning_bench/fault_detection/testenv/f1_score.py"
    - name: "samples_transfer_ratio"

  # incremental rounds setting for incremental learning paradigm; int type; default value is 2;
  incremental_rounds: 2
```





