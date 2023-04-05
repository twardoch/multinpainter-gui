# Multinpainter

Iterative image outpainting powered by OpenAI Dall-E API.

## Introduction

Multinpainter is a Python library and a CLI tool that can iteratively outpaint an input image using OpenAI’s API. 

You can specify an input image, the size of the output image, and optionally a prompt. Multinpainter will then iteratively call the OpenAI API to outpaint the image step-by-step until the entire output image is filled with content. 

You need an [OpenAI API key](https://platform.openai.com/account/api-keys). The tool performs a call to the GPT 3.5 API and then multiple calls to the Dall-E 2 API. 

If you don’t provide a prompt, Multinpainter will try to generate a prompt using the [`Salesforce/blip2-opt-2.7b`](https://huggingface.co/Salesforce/blip2-opt-2.7b) model on Huggingface. For that, you also need a [Huggingface access token](https://huggingface.co/settings/tokens). 

## Installation

```
python3 -m pip install --upgrade git+https://github.com/twardoch/multinpainter-py
```

## Usage

### Command-line

```
NAME
    multinpainter-py

SYNOPSIS
    multinpainter-py IMAGE OUTPUT WIDTH HEIGHT <flags>

DESCRIPTION
    Perform iterative inpainting on an image file using OpenAI's DALL-E 2 model.

POSITIONAL ARGUMENTS
    IMAGE
        Type: str
        Path to the input image file.
    OUTPUT
        Type: str
        Path to the output image file.
    WIDTH
        Type: int
        Width of the output image in pixels.
    HEIGHT
        Type: int
        Height of the output image in pixels.

FLAGS
    -p, --prompt=PROMPT
        Type: Optional[str]
        Default: None
        A prompt to guide the image generation.
    -f, --fallback=FALLBACK
        Type: Optional[str]
        Default: None
        A fallback prompt to use if no human is found in the image. 
        If not provided but `humans` is specified, the tool will 
        autogenerate the fallback prompt based on the main prompt.
    --step=STEP
        Type: Optional[int]
        Default: None
        The step size in pixels to move the window during the 
        inpainting process. If not provided, the window will 
        move by half the square size. Defaults to None.
    --square=SQUARE
        Type: int
        Default: 1024
        The size of the square window to use for inpainting. 
        Must be 1024 (default) or 512 or 256.
    -h, --humans=HUMANS
        Type: bool
        Default: False
        If specified, the algorithm will detect humans and apply 
        the main prompt for squares with a human, and the fallback 
        prompt for squares without a human.
    -v, --verbose=VERBOSE
        Type: bool
        Default: False
        If specified, prints verbose info.
    -a, --openai_api_key=API_KEY
        Type: Optional[str]
        Default: None
        Your OpenAI API key. If not provided, the API key will 
        be read from the OPENAI_API_KEY environment variable.
    --hf_api_key=HF_API_KEY
        Type: Optional[Str]
        Default: None
        The Huggingface API key. Defaults to None.
    --prompt_model=PROMPT_MODEL
        Type: Optional[str]
        Default: None
        The Huggingface model to describe image.

NOTES
    You can also use flags syntax for POSITIONAL ARGUMENTS
```

See below for explanation of the arguments. 

You can also use `python3 -m multinpainter` instead of `multinpainter-py`. 

### Python

In Python, you can also do: 

```python
import asyncio
from multinpainter import Multinpainter_OpenAI
inpainter = Multinpainter_OpenAI(
    image_path="input_image.png",
    out_path="output_image.png",
    out_width=1920,
    out_height=1080,
    prompt="Asian woman in front of blue wall",
    fallback="Solid blue wall",
    square=1024,
    step=256,
    humans=True,
    verbose=True,
    openai_api_key="sk-NNNNNN",
    hf_api_key="hf_NNNNNN",
    prompt_model="Salesforce/blip2-opt-2.7b"
)
asyncio.run(inpainter.inpaint())
```

When you initialize an instance of the `Multinpainter_OpenAI` class, it will: 

- Set up logging configurations.
- Open the input image and create an output image.
- Optionally detect humans in the input image using the YOLO model.
- Optionally detect faces in the input image using the Dlib library.
- Find the center of focus of the image (center of input image or the face if found).
- Calculate the expansion of the output image.
- Paste the input image onto the output image.
- Create the outpainting plan by generating a list of square regions in different directions.

You then call the `inpaint()` **async** method, which will:

- Optionally infer the prompt from the image.
- Perform outpainting for each square in the outpainting plan.
- Save the output image.
- Return the output image path.

### Arguments

Here’s an explanation of the arguments: 

| CLI                           | Python           | Explanation                                                                                                |
| ----------------------------- | ---------------- | ---------------------------------------------------------------------------------------------------------- |
| `IMAGE`                       | `image_path`     | The path of the input image to be outpainted.                                                              |
| `OUTPUT`                      | `out_path`       | The path where the output image will be saved.                                                             |
| `WIDTH`                       | `out_width`      | The desired width of the output image.                                                                     |
| `HEIGHT`                      | `out_height`     | The desired height of the output image.                                                                    |
| `-p PROMPT`                   | `prompt`         | The main prompt that will guide the outpainting process.                                                   |
| `-f FALLBACK`                 | `fallback`       | A fallback prompt used for outpainting when no humans are detected in the image.                           |
| `--square=SQUARE`             | `square`         | The size of the square region that will be outpainted during each step , must be `1024` or `512` or `256`. |
| `--step=STEP`                 | `step`           | The step size used to move the outpainting square, half of square by default.                              |
| `--humans`                    | `humans`         | A boolean flag indicating whether to detect humans in the image and adapt the prompt accordingly.          |
| `--verbose`                   | `verbose`        | If given, prints verbose output and saves intermediate outpainting images.                                 |
| `-a API_KEY`                  | `openai_api_key` | OpenAI API key or OPENAI_API_KEY env variable.                                                             |
| `--hf_api_key=HF_API_KEY`     | `hf_api_key`     | Huggingface API key or `HUGGINGFACEHUB_API_TOKEN` env variable.                                            |
| `--prompt_model=PROMPT_MODEL` | `prompt_model`   | The Huggingface model to describe image. Defaults to `Salesforce/blip2-opt-2.7b`.                          |

See docstrings inside the code for more detailed info.

## Authors & License

- Copyright (c) 2023 Adam Twardoch, licensed under [Apache 2.0](./LICENSE.txt).
- Written with significant assistance from ChatGPT-4.

## Note

This project has been set up using PyScaffold 4.4. For details and usage
information on PyScaffold see https://pyscaffold.org/.
