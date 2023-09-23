import os
import argparse
import warnings

import numpy as np
import matplotlib.pyplot as plt

import shap
import torch
import torchvision
from torch.utils.data import DataLoader

from accelerate import (
    Accelerator,
    DeepSpeedPlugin,
    FullyShardedDataParallelPlugin,
    find_executable_batch_size
)
from torch.distributed.fsdp.fully_sharded_data_parallel import FullStateDictConfig

import utils


def explain_model(args: argparse.Namespace) -> None:
    """
    Explain the predictions of a given model on a dataset using SHAP values.

    Args:
        args (argparse.Namespace): Arguments passed to the script. Argument definitions are as follows:
            - dataset (str): Path to the dataset directory or the name of a HuggingFace dataset, defining the data source for model training and evaluation.
            - dataset_kwargs (str): Optional. JSON file containing keyword arguments (kwargs) specific to a HuggingFace dataset.
            - model_output_dir (str): Output directory where the model is contained.
            - feat_extract (bool): Include this flag to enable feature extraction during training, useful when using pretrained models.
            - grayscale (bool): Optional. Use this flag to indicate that grayscale images should be used during training.
            - crop_size (int): Size to which input images will be cropped.
            - batch_size (int): Batch size for both training and evaluation stages.
            - num_workers (int): Number of workers for training and evaluation.
            - dropout (float): Dropout rate for the classifier head of the model.
            - n_samples (int): Number of samples used for model explanation.
            - max_evals (int): Maximum number of evaluations, commonly used for model explanation.
            - topk (int): Number of top predictions to consider during model explanation.

    Returns:
        None

    Side Effects:
        - Plots the SHAP value interpretation for the model predictions on a subset of images from the dataset.

    Example:
        >>> args = get_args()
        >>> explain_model(args)
        # The function will use the provided arguments to load the model, dataset, and then explain the model
        # predictions using SHAP values. It will plot the SHAP value interpretation for the top-k predictions on
        # a subset of n_samples images from the dataset. The results will be displayed in the console or as a
        # visualization, depending on the implementation.
    """
    def predict(img: np.ndarray) -> torch.Tensor:
        """
        Predict the class probabilities for an image.

        Parameters:
            - img (np.ndarray): Input image.

        Returns:
            - torch.Tensor: Class probabilities.
        """
        img = utils.to_channels_first(torch.Tensor(img))
        img = img.to(device)
        output = model(img)
        return output

    deepspeed_plugin = DeepSpeedPlugin(gradient_accumulation_steps=2, gradient_clipping=1.0)
    fsdp_plugin = FullyShardedDataParallelPlugin(
        state_dict_config=FullStateDictConfig(offload_to_cpu=False, rank0_only=False),
    )
    accelerator = Accelerator(even_batches=True,
                              gradient_accumulation_steps=2,
                              mixed_precision="fp16",
                              deepspeed_plugin=deepspeed_plugin,
                              fsdp_plugin=fsdp_plugin
                              )

    device = accelerator.device
    transform, inv_transform = utils.get_explanation_transforms()

    image_dataset = utils.load_image_dataset(args)
    classes = utils.get_classes(image_dataset["train"])

    augmentation = torchvision.transforms.Compose([
        torchvision.transforms.RandomResizedCrop(args.crop_size),
        torchvision.transforms.PILToTensor(),
    ])
    def preprocess_val(example_batch):
        example_batch["pixel_values"] = [
            augmentation(image.convert("RGB")) for image in example_batch["image"]
        ]
        return example_batch

    test_dataset = image_dataset["test"].with_transform(preprocess_val)

    data_loader = DataLoader(test_dataset,
                             batch_size=args.batch_size,
                             shuffle=True,
                             num_workers=args.num_workers,
                             collate_fn=utils.collate_fn
                             )

    batch = next(iter(data_loader))
    images, labels = batch["pixel_values"], batch["labels"]
    images = images.permute(0, 2, 3, 1)
    images = transform(images)

    if args.model_output_dir.endswith("/"):
        model_name = args.model_output_dir.split("/")[-2]
    else:
        model_name = args.model_output_dir.split("/")[-1]

    model = utils.get_pretrained_model(args, model_name=model_name, num_classes=len(classes))

    checkpoint_file = os.path.join(os.path.join(args.model_output_dir, "best_model.pth"))
    checkpoint = torch.load(checkpoint_file, map_location="cpu")
    if "n_averaged" in checkpoint["model"]:
        del checkpoint["model"]["n_averaged"]
        torch.nn.modules.utils.consume_prefix_in_state_dict_if_present(checkpoint["model"], "module.")
    model.load_state_dict(checkpoint["model"])

    model.eval()
    model.to(device)

    masker_blur = shap.maskers.Image("blur(128,128)", images[0].shape)
    explainer = shap.Explainer(predict, masker_blur, output_names=classes)

    shap_values = explainer(images[:args.n_samples],
                            max_evals=args.max_evals,
                            batch_size=args.batch_size,
                            outputs=shap.Explanation.argsort.flip[:args.topk]
                            )

    if args.n_samples == 1:
        shap_values.data = inv_transform(shap_values.data).cpu().numpy()[0]
        shap_values.values = [val for val in np.moveaxis(shap_values.values[0], -1, 0)]
    else:
        shap_values.data = inv_transform(shap_values.data).cpu().numpy()
        shap_values.values = [val for val in np.moveaxis(shap_values.values, -1, 0)]

    fig, ax = plt.subplots(figsize=(7.5, 7.5))
    shap.image_plot(shap_values=shap_values.values,
                    pixel_values=shap_values.data,
                    labels=shap_values.output_names,
                    true_labels=[classes[idx] for idx in labels[:len(labels)]],
                    aspect=0.15,
                    hspace=0.15,
                    show=False,
                    )

    filename = f"{args.model_output_dir}/explanation.png"

    # Save the SHAP explanation plot as a PNG image
    plt.savefig(filename, bbox_inches='tight', format='png')
    plt.close(fig)


def get_args():
    """
    Parse command-line arguments for running model explanation.

    Returns:
        argparse.Namespace: Parsed command-line arguments.
    """
    parser = argparse.ArgumentParser(description="Run Model Explanation")

    parser.add_argument(
        "--dataset",
        required=True,
        type=str,
        help="Specify the path to the dataset directory or the name of a HuggingFace dataset, defining the data source for model training and evaluation."
    )

    parser.add_argument(
        "--dataset_kwargs",
        type=str,
        default="",
        help="Optional: Provide a JSON file containing keyword arguments (kwargs) specific to a HuggingFace dataset."
    )

    parser.add_argument(
        "--model_output_dir",
        required=True,
        type=str,
        help="Specify the output directory where the model is contained."
    )

    parser.add_argument(
        "--feat_extract",
        action="store_true",
        help="Include this flag to enable feature extraction during training, useful when using pretrained models."
    )

    parser.add_argument(
        "--grayscale",
        action="store_true",
        help="Optional: Use this flag to indicate that grayscale images should be used during training."
    )

    parser.add_argument(
        "--crop_size",
        default=224,
        type=int,
        help="Define the size to which input images will be cropped."
    )

    parser.add_argument(
        "--batch_size",
        default=16,
        type=int,
        help="Define the batch size for both training and evaluation stages."
    )

    parser.add_argument(
        "--num_workers",
        default=4,
        type=int,
        help="Specify the number of workers for training and evaluation."
    )

    parser.add_argument(
        "--dropout",
        type=float,
        default=0.2,
        help="Define the dropout rate for the classifier head of the model."
    )

    parser.add_argument(
        "--n_samples",
        required=True,
        type=int,
        help="Specify the number of samples used for model explanation."
    )

    parser.add_argument(
        "--max_evals",
        required=True,
        type=int,
        help="Set the maximum number of evaluations, commonly used for model explanation."
    )

    parser.add_argument(
        "--topk",
        required=True,
        type=int,
        help="Specify the number of top predictions to consider during model explanation."
    )

    return parser.parse_args()


if __name__ == "__main__":
    warnings.filterwarnings("ignore", category=UserWarning)

    args = get_args()

    print(f"Model explanation in progress")
    explain_model(args)

    print(f"Model explanation complete. Result has been saved to {args.model_output_dir}/explanation.png")
