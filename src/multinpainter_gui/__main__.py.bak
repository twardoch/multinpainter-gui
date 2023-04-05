#!/usr/bin/env python3

import asyncio
from pathlib import Path
import sys
from typing import Union

# from ezgooey.ez import *
from gooey import Gooey, GooeyParser

GUI_NAME = "Multinpainter GUI"
CLI_NAME = "multinpainter-gui"


from gooey import Gooey, GooeyParser
from multinpainter_gui import __version__
from multinpainter import Multinpainter_OpenAI, DESCRPTION_MODEL
from typing import Optional

COLOR_BG_DARK = "#2b2b2b"
COLOR_BG_LIGHT = "#383838"
COLOR_TEXT1 = "#dedede"
COLOR_TEXT2 = "#a4a4a4"
STD_OPTIONS = {"label_color": COLOR_TEXT1, "help_color": COLOR_TEXT2}

import sys, os
from pathlib import Path


def get_pictures_folder():
    platform = sys.platform
    home = Path.home()

    if platform.startswith(("win", "darwin")):
        return home / "Pictures"
    elif platform.startswith("linux"):
        return Path(os.environ.get("XDG_PICTURES_DIR", home))
    else:
        return home


@Gooey(
    # language_dir=getResourcePath("languages"),
    # terminal_font_family=None,
    # terminal_font_size=None,
    # terminal_font_weight=None,
    advanced=True,
    auto_start=False,
    body_bg_color=COLOR_BG_DARK,
    clear_before_run=False,
    default_size=(960, 600),
    disable_progress_bar_animation=False,
    disable_stop_button=False,
    dump_build_config=False,
    error_bg_color=COLOR_BG_LIGHT,
    error_color="#ea7878",
    footer_bg_color=COLOR_BG_LIGHT,
    force_stop_is_error=True,
    fullscreen=False,
    group_by_type=True,
    header_bg_color=COLOR_BG_DARK,
    header_height=40,
    header_image_center=False,
    header_show_subtitle=False,
    header_show_title=False,
    header_width=90,
    help_bg_color=COLOR_BG_DARK,
    help_color=COLOR_TEXT1,
    hide_progress_msg=False,
    image_dir="::gooey/default",
    label_bg_color=COLOR_BG_DARK,
    label_color=COLOR_TEXT2,
    language="english",
    load_build_config=None,
    navigation="Tabbed",
    optional_cols=2,
    poll_external_updates=False,
    program_description=None,
    program_name=GUI_NAME,
    progress_expr=None,
    progress_regex=None,
    required_cols=1,
    requires_shell=True,
    return_to_config=False,
    richtext_controls=True,
    show_failure_modal=True,
    show_preview_warning=False,
    show_restart_button=True,
    show_sidebar=True,
    show_stop_warning=True,
    show_success_modal=False,
    sidebar_bg_color=COLOR_BG_LIGHT,
    sidebar_title="Actions",
    suppress_gooey_flag=True,
    tabbed_groups=True,
    target=None,
    terminal_font_color=COLOR_TEXT1,
    terminal_panel_color=COLOR_BG_LIGHT,
    use_legacy_titles=False,
    menu=[
        {
            "name": "Help",
            "items": [
                {
                    "type": "AboutDialog",
                    "menuTitle": "About",
                    "name": GUI_NAME,
                    "description": "Click the link for more info",
                    "website": "https://github.com/twardoch/multinpainter-gui",
                    "license": "Apache 2.0",
                },
                {
                    "type": "Link",
                    "menuTitle": f"{GUI_NAME} Help",
                    "url": "https://github.com/twardoch/multinpainter-py",
                },
            ],
        }
    ],
)
def get_parser():
    common_parser = GooeyParser(add_help=False)
    common_parser.add_argument(
        "-i",
        "--image",
        required=True,
        type=Union[Path, str],
        dest="image",
        metavar="Input image",
        help="Path to the input image file",
        widget="FileChooser",
        gooey_options={
            **STD_OPTIONS,
            **{
                "wildcard": "PNG Images|*.png|JPG Images|*.jpg|JPEG Images|*.jpeg",
                "default_dir": str(get_pictures_folder()),
                "message": "Choose an image",
                "full_width": True,
            },
        },
    )
    common_settings_group = common_parser.add_argument_group("Preferences")
    common_settings_group.add_argument(
        "-O",
        "--openai-api-key",
        type=str,
        dest="openai_api_key",
        metavar="OpenAI API key",
        help="Not needed if OPENAI_API_KEY environment variable is set",
        gooey_options={
            **STD_OPTIONS,
            **{},
        },
    )
    common_settings_group.add_argument(
        "-F",
        "--hf-api-key",
        type=str,
        dest="hf_api_key",
        metavar="Huggingface API key",
        help="Not needed if HUGGINGFACEHUB_API_TOKEN environment variable is set",
        gooey_options={
            **STD_OPTIONS,
            **{},
        },
    )
    common_settings_group.add_argument(
        "-v",
        "--verbose",
        dest="verbose",
        action="store_true",
        default=True,
        metavar="Verbose",
        help=" Print detailed info and save intermediate images",
        gooey_options={
            **STD_OPTIONS,
            **{},
        },
    )
    common_settings_group.add_argument(
        "-P",
        "--prompt-model",
        type=str,
        dest="prompt_model",
        metavar="Image description model",
        default=DESCRPTION_MODEL,
        help="The Huggingface model to describe image",
        gooey_options={
            **STD_OPTIONS,
            **{},
        },
    )

    parser = GooeyParser(
        prog="",
        description="Perform iterative inpainting on an image file using OpenAI's DALL-E 2 model.",
    )
    subparsers = parser.add_subparsers(dest="command", help="commands")

    inpaint_parser = subparsers.add_parser(
        "inpaint",
        help="Perform iterative inpainting on an image file",
        parents=[common_parser],
    )
    inpaint_parser.add_argument(
        "-o",
        "--output",
        type=Union[Path, str],
        dest="output",
        metavar="Output image",
        help="Path to the output image file",
        widget="FileSaver",
        gooey_options={
            **STD_OPTIONS,
            **{
                "wildcard": "PNG Images|*.png",
                "default_dir": str(get_pictures_folder()),
                "message": "Choose the image destination",
                "full_width": True,
            },
        },
    )
    inpaint_parser.add_argument(
        "-w",
        "--width",
        type=int,
        dest="width",
        metavar="Width",
        help="Output image width",
        widget="IntegerField",
        gooey_options={
            **STD_OPTIONS,
            **{'max': 32768},
        },
    )
    inpaint_parser.add_argument(
        "-H",
        "--height",
        type=int,
        dest="height",
        metavar="Height",
        help="Output image height",
        widget="IntegerField",
        gooey_options={
            **STD_OPTIONS,
            **{'max': 32768},
        },
    )
    inpaint_parser.add_argument(
        "-u",
        "--humans",
        dest="humans",
        metavar="Detect humans",
        action="store_true",
        help=" Apply default prompt if human is found and fallback prompt if not",
        gooey_options={
            **STD_OPTIONS,
            **{
                "full_width": True,
            },
        },
    )
    inpaint_parser.add_argument(
        "-p",
        "--prompt",
        type=str,
        dest="prompt",
        metavar="Prompt",
        help="Default prompt for inpainting or prompt if human is found",
        gooey_options={
            **STD_OPTIONS,
            **{},
        },
    )
    inpaint_parser.add_argument(
        "-f",
        "--fallback",
        type=str,
        dest="fallback",
        metavar="Fallback prompt",
        help="Prompt to use if no human is found (autogenerated if empty)",
        gooey_options={
            **STD_OPTIONS,
            **{},
        },
    )
    inpaint_settings_group = inpaint_parser.add_argument_group("Inpainting")
    inpaint_settings_group.add_argument(
        "-S",
        "--square",
        type=int,
        dest="square",
        metavar="Inpainting square",
        default=1024,
        choices=[1024, 512, 256],
        help="The size of the square window to use for inpainting (1024, 512, 256)",
        gooey_options={
            **STD_OPTIONS,
            **{},
        },
    )
    inpaint_settings_group.add_argument(
        "-s",
        "--step",
        type=int,
        dest="step",
        metavar="Inpainting step size",
        help="The step size in pixels to move the window (default: 50% of square)",
        widget="IntegerField",
        gooey_options={
            **STD_OPTIONS,
            **{'max': 32768},
        },
    )

    describe_parser = subparsers.add_parser(
        "describe",
        help="Describe the image",
        parents=[common_parser],
    )

    return parser


def main():
    parser = get_parser()
    args = parser.parse_args()

    inpainter = Multinpainter_OpenAI(
        image_path=args.image,
        out_path=args.output,
        out_width=args.width,
        out_height=args.height,
        prompt=args.prompt,
        fallback=args.fallback,
        step=args.step,
        square=args.square,
        humans=args.humans,
        verbose=args.verbose,
        openai_api_key=args.openai_api_key,
        hf_api_key=args.hf_api_key,
        prompt_model=args.prompt_model,
    )
    asyncio.run(inpainter.inpaint())
    print("Output image saved at:", inpainter.out_path)


if __name__ == "__main__":
    main()
