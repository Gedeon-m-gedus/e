# State-Of-The-Art Binary and Multi-class Image Classification

## Table of Contents

* [Getting Started](#getting-started)
    * [Prerequisites](#prerequisites)
    * [Installation](#installation)
    * [Usage](#usage)
* [Documentation](#documentation)
* [License](#license)
* [Citation](#citation)

## Usage
### July 2023
Integrated <span style="color:green;font-weight:700;font-size:16px"> **HuggingFace's Accelerate and Datasets Libraries** </span> 
1. Users can now perform single or distributed model training on CPUs, GPUs and TPUs
2. Users can now pass a path to a local dataset directory or a Hugging Face dataset name (or an HTTPS URL for a remote dataset)
3. The optimizers used during training now comes from the Timm library, giving the opportunity for several SOTA options
4. All files in the repository have been updated accordingly.
5. To Do: tune.py file for hyperparameter tuning is undergoing updates 

### June 25, 2023
Added <span style="color:green;font-weight:700;font-size:16px"> **CutMix Data Augmentation** </span> functionality.\
<span style="color:red;font-weight:700;font-size:15px">
    **Example**:
</span>
to train an `xcit_nano_12_p8_224.fb_dist_in1k` model with cutmix, run the following code

```
accelerate launch train.py \
    --dataset_dir weather_data \
    --output_dir sample_run_1 \   
    --experiment_name exp_1 \
    --model_name xcit_nano_12_p8_224.fb_dist_in1k \ 
    --crop_size 224 \
    --batch_size 16 \
    --epochs 33 \
    --cutmix \
    --cutmix_alpha 1.0
```

Added <span style="color:green;font-weight:700;font-size:16px"> **MixUp Data Augmentation** </span> functionality.\
<span style="color:red;font-weight:700;font-size:15px">
    **Example**:
</span>
to train an `xcit_nano_12_p8_224.fb_dist_in1k` model with mixup, run the following code

```
accelerate launch train.py \
    --dataset_dir weather_data \
    --output_dir sample_run_1 \   
    --experiment_name exp_1 \
    --model_name xcit_nano_12_p8_224.fb_dist_in1k \ 
    --crop_size 224 \
    --batch_size 16 \
    --epochs 33 \
    --mixup \
    --mixup_alpha 1.0
```

### June 18, 2023
Added <span style="color:green;font-weight:700;font-size:16px"> **Model Pruning** </span> functionality.\
<span style="color:red;font-weight:700;font-size:15px">
    **Example**:
</span>
to train an `xcit_nano_12_p8_224.fb_dist_in1k` model and prune the model, run the following code

```
accelerate launch train.py \
    --dataset_dir weather_data \
    --output_dir sample_run_1 \   
    --experiment_name exp_1 \
    --model_name xcit_nano_12_p8_224.fb_dist_in1k \ 
    --crop_size 224 \
    --batch_size 16 \
    --epochs 33 \
    --prune \
    --pruning_rate 0.25
```
Note: the pruning is global (i.e. `<pruning_rate>` percent of weak connections are removed across the entire, instead of `<pruning_rate>` percent in each layer). Also, the pruning is performed after every epoch, and uses L1 (Lasso) unstructured approach.

### June 13, 2023
Added <span style="color:green;font-weight:700;font-size:16px"> **Adversarial Training (Fast Gradient Sign Method (FGSM) Attack)** </span> functionality.\
<span style="color:red;font-weight:700;font-size:15px">
    **Example**:
</span>
to train an `xcit_nano_12_p8_224.fb_dist_in1k` model with FGSM attack, run the following code

```
accelerate launch train.py \
    --dataset_dir weather_data \
    --output_dir sample_run_1 \   
    --experiment_name exp_1 \
    --model_name xcit_nano_12_p8_224.fb_dist_in1k \ 
    --crop_size 224 \
    --batch_size 16 \
    --epochs 33 \
    --fgsm \
    --epsilon 0.03
```

### June 7, 2023
Added <span style="color:green;font-weight:700;font-size:16px"> **Best Checkpoints Averaging** </span> functionality.\
<span style="color:red;font-weight:700;font-size:15px">
    **Example**:
</span>
 to train an `xcit_nano_12_p8_224.fb_dist_in1k` model and average the best 5 checkpoints to be used for inference, run the following code

```
accelerate launch train.py \
    --dataset_dir weather_data \
    --output_dir sample_run_1 \   
    --experiment_name exp_1 \
    --model_name xcit_nano_12_p8_224.fb_dist_in1k \ 
    --crop_size 224 \
    --batch_size 16 \
    --epochs 33 \
    --avg_ckpts \
    --num_ckpts 5 \
```

Added <span style="color:green;font-weight:700;font-size:16px"> **Best Checkpoints Saving** </span> functionality.\
<span style="color:red;font-weight:700;font-size:15px">
    **Example**:
</span>
 to train an `xcit_nano_12_p8_224.fb_dist_in1k` model and save the best 5 model checkpoints based on the specified 
evaluation metric, run the following code

```
accelerate launch train.py \
    --dataset_dir weather_data \
    --output_dir sample_run_1 \   
    --experiment_name exp_1 \
    --model_name xcit_nano_12_p8_224.fb_dist_in1k \ 
    --crop_size 224 \
    --batch_size 16 \
    --epochs 33 \
    --num_ckpts 5
```

Added <span style="color:green;font-weight:700;font-size:16px"> **Exponential Moving Average (EMA)** </span> functionality.\
<span style="color:red;font-weight:700;font-size:15px">
    **Example**:
</span>
 to train an `xcit_nano_12_p8_224.fb_dist_in1k` model with EMA, run the following code

```
accelerate launch train.py \
    --dataset_dir weather_data \
    --output_dir sample_run_1 \   
    --experiment_name exp_1 \
    --model_name xcit_nano_12_p8_224.fb_dist_in1k \ 
    --crop_size 224 \
    --batch_size 16 \
    --epochs 33 \
    --ema \
    --ema_steps 32 \
    --ema_decay 0.99998 
```

Now by default, the script checks for the availability of a cuda device to run Automatic Mixed Precision (AMP) or not.
### Feb 11, 2023
Added <span style="color:green;font-weight:700;font-size:16px"> **training logging** </span> using [MLflow](https://mlflow.org/)\
<span style="color:red;font-weight:700;font-size:15px">
    **Example**:
</span>
 to check logged items, run
```
cd <training_output_dir>
mlflow ui
```

### Feb 10, 2023
Added <span style="color:green;font-weight:700;font-size:16px"> [app.py](https://github.com/etetteh/low-code-ml-dl/blob/main/deep_learning/image_classification/app.py) </span> to run inference with [FastAPI](https://fastapi.tiangolo.com/) on a single or multiple images by passing a JSON file.\
**Sample JSON file**
```
{
  "onnx_model_path": "nano/coatnet_nano_rw_224.sw_in1k/best_model.onnx",
  "img_path": "/datasets/weather_data/val/cloudy/cloudy104.jpg",
  "dataset_dir_or_classes_file": "/datasets/weather_data/",
  "grayscale": False
  "crop_size": 224,
  "val_resize": 256
}
```

<span style="color:red;font-weight:700;font-size:15px">**Example**:</span>
to predict the class and probability score of the images in the JSON file, run

```
uvicorn app:app --reload
```

**Sample output**:
```
{
    "cloudy104.jpg": [
        {
            "Predicted class": "cloudy",
            "Probability": 0.99
        },
        {
            "Predicted class": "shine",
            "Probability": 0.0
        },
        {
            "Predicted class": "rain",
            "Probability": 0.0
        }
    ]
}
```

### Feb 07, 2023
Added <span style="color:green;font-weight:700;font-size:16px"> [inference.py](https://github.com/etetteh/low-code-ml-dl/blob/main/deep_learning/image_classification/inference.py) </span> to run inference on a single or multiple images using the best model saved in [ONNX](https://onnx.ai/) format.\
<span style="color:red;font-weight:700;font-size:15px">
    **Example**:
</span>
 to predict the class and probability score of an image using a `swinv2_cr_tiny_ns_224` model, run
```
accelerate launch inference.py \
    --onnx_model_path tiny/swinv2_cr_tiny_ns_224/best_model.onnx \
    --img_path datasets/weather_data/val/cloudy/cloudy104.jpg \
    --dataset_dir_or_classes_file datasets/weather_data \
    --output_dir infer
```
Note that `dataset_dir_or_classes_file` takes as argument your dataset directory or a text file containing the classes 
### Jan 29, 2023
Added <span style="color:green;font-weight:700;font-size:16px"> [tune.py](https://github.com/etetteh/low-code-ml-dl/blob/main/deep_learning/image_classification/tune.py) </span> for hyperparameter tuning functionality using [Ray Tune](https://www.ray.io/ray-tune).\
<span style="color:red;font-weight:700;font-size:15px">
    **Example**:
</span> to tune the batch size, learning rate and weight decay (passing tune_opt by default tunes the learning rate and weight decay, and also momentum in the case of using SGD optimizer) using population based training algorithm and a `swinv2_cr_tiny_ns_224` model, run:
```
python tune.py \
    --name <experiment name> \
    --output_dir <model_checkpoint_dir> \
    --dataset_dir <dataset_dir> \
    --model_name swinv2_cr_tiny_ns_224 \
    --tune_batch_size \
    --tune_opt \
    --pbt 
```

### Jan 25, 2023
Added <span style="color:green;font-weight:700;font-size:16px"> [explain.py](https://github.com/etetteh/low-code-ml-dl/blob/main/deep_learning/image_classification/explainability.py) </span> for model explainability functionality using [SHAP](https://shap.readthedocs.io/en/latest/index.html#). You can now understand the decision or prediction made by the best performing model.\
<span style="color:red;font-weight:700;font-size:15px">
    **Example**:
</span> to explain the performance of a `swinv2_cr_tiny_ns_224` model on 4 samples of the validation data, run the following in a notebook

```
accelerate launch explain.py \
    --dataset weather_data/ \
    --model_output_dir tiny/swinv2_cr_tiny_ns_224 \
    --feat_extract \ 
    --batch_size 128 \
    --n_samples 2 \
    --max_evals 999 \
    --topk 2
```

### Jan 17, 2023
The train script uses models from the [timm](https://github.com/rwightman/pytorch-image-models) library.
1. Specify any model you'd like to use. You can pass a single model name or a list of model names.\
<span style="color:red;font-weight:700;font-size:15px">
  Example:
</span> to train with the models `swinv2_cr_tiny_ns_224` and `vit_large_patch14_clip_224`, run
```
accelerate launch train.py \
    --dataset_dir weather_data \
    --output_dir sample_run_1 \   
    --experiment_name exp_1 \
    --model_name swinv2_cr_tiny_ns_224 vit_large_patch14_clip_224 \
```
Please, ensure that when passing a list of models, all the models should have been trained on the same image size.

2. Train all models with specific size and specific image size. This is useful for model selection.\
<span style="color:red;font-weight:700;font-size:15px">
    Example:
</span> to finetune all `tiny` models from the `timm` library that were pre-trained with image size 224, run

```
accelerate launch train.py \
    --dataset_dir weather_data \
    --output_dir sample_run_1 \   
    --experiment_name exp_1 \
    --model_size tiny \
    --crop_size 224 \
    --feat_extract
```

You can also pass `nano`, `small`, `base`, `large` or `giant` to train all models with that respective size

Run `accelerate launch train.py --help` to see all the arguments you can pass during training. 


The training script:
* Checkpoints the model, which can be used to resume training
* Saves the best model weights, which can be used for inference or deployment
* Plots a confusion matrix and ROC curve of the best validation metrics

All results are on the validation dataset, and are saved in `output_dir/<model_name>`.

<span style="color:red;font-weight:700;font-size:15px">
    Example:
</span> Sample output on the validation set after running the following code is shown below

```
accelerate launch train.py \
    --dataset_dir weather_data \
    --output_dir sample_run_1 \   
    --experiment_name exp_1 \
    --model_size tiny \
    --crop_size 224 \
```

**Sample Results**:
```
                                         model  accuracy     auc      f1  recall  precision
0           vit_tiny_r_s16_p8_224.augreg_in21k    1.0000  0.9998  1.0000  1.0000     1.0000
1                        swinv2_cr_tiny_ns_224    1.0000  0.9999  1.0000  1.0000     1.0000
2                 swin_tiny_patch4_window7_224    0.9917  0.9988  0.9909  0.9917     0.9904
3                             swin_s3_tiny_224    0.9817  0.9970  0.9817  0.9817     0.9817
4                     xcit_tiny_12_p8_224_dist    0.9762  0.9965  0.9746  0.9762     0.9743
5   vit_tiny_r_s16_p8_224.augreg_in21k_ft_in1k    0.9750  0.9983  0.9737  0.9750     0.9745
6            vit_tiny_patch16_224.augreg_in21k    0.9750  0.9988  0.9737  0.9750     0.9745
7              deit_tiny_distilled_patch16_224    0.9762  0.9968  0.9736  0.9762     0.9732
8    vit_tiny_patch16_224.augreg_in21k_ft_in1k    0.9717  0.9963  0.9724  0.9717     0.9735
9                         xcit_tiny_24_p16_224    0.9690  0.9949  0.9664  0.9690     0.9648
10                       deit_tiny_patch16_224    0.9679  0.9960  0.9660  0.9679     0.9654
11                    xcit_tiny_24_p8_224_dist    0.9650  0.9959  0.9658  0.9650     0.9676
12                     maxvit_tiny_tf_224.in1k    0.9674  0.9953  0.9651  0.9674     0.9639
13                   xcit_tiny_24_p16_224_dist    0.9662  0.9960  0.9650  0.9662     0.9641
14                        xcit_tiny_12_p16_224    0.9579  0.9920  0.9570  0.9579     0.9564
15                         xcit_tiny_12_p8_224    0.9579  0.9970  0.9570  0.9579     0.9564
16                         xcit_tiny_24_p8_224    0.9467  0.9931  0.9486  0.9467     0.9520
17                   xcit_tiny_12_p16_224_dist    0.9290  0.9857  0.9295  0.9290     0.9303

```

Model explanation\
<img src="https://github.com/etetteh/low-code-ml-dl/blob/main/deep_learning/image_classification/plots/model_explainability.png" height="550" width="900">

Confusion Matrix\
<img src="https://github.com/etetteh/low-code-ml-dl/blob/main/deep_learning/image_classification/plots/confusion_matrix.png" height="550" width="900">

ROC Curve\
<img src="https://github.com/etetteh/low-code-ml-dl/blob/main/deep_learning/image_classification/plots/roc_curve.png" height="550" width="900">


## Getting Started
The goal of this project is to provide a simple but efficient approach to image classification research by leveraging SOTA image models

## Prerequisites
1. Knowledge of Python programming to understand the code
2. Knowledge of machine learning and image classification
3. Knowledge to interpret metrics or results

## Installation
The script makes use of the following libraries, which can be installed following their respective instructions:
1. Python 3.10 or earlier. I recommend installing through [Miniconda](https://docs.conda.io/en/latest/miniconda.html) 
2. Latest stable release of [Pytorch](https://pytorch.org/get-started/locally/). Earlier versions should be okay.
3. Pre-release version of [timm](https://github.com/rwightman/pytorch-image-models) for the models used in this research project
4. [TorchMetrics](https://torchmetrics.readthedocs.io/en/stable/) for computing metrics
5. [SHAP](https://shap.readthedocs.io/en/latest/index.html#) for model explainability
6. [ONNX](https://onnx.ai/) for exporting model for inference
7. [FastAPI](https://fastapi.tiangolo.com/) for running inference on single or multiple images 
8. [MLflow](https://mlflow.org/) for logging training 

## Documentation
Coming soon!

## License

## Citation
```
@misc{etetteh2023,
  author = {Enoch Tetteh},
  title = {Low Code Machine Learning And Deep Learning},
  year = {2023},
  publisher = {GitHub},
  journal = {GitHub repository},
  doi = {},
  howpublished = {\url{https://github.com/etetteh/low-code-ml-dl}}
} 
```
