#!/usr/bin/env python3

import asyncio
from pathlib import Path
import sys, os
from PIL import Image
import platform
import subprocess


def is_dark_mode():
    def is_windows_dark_mode():
        try:
            import winreg

            with winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize",
            ) as key:
                value, _ = winreg.QueryValueEx(key, "AppsUseLightTheme")
            return value == 0
        except (FileNotFoundError, ValueError):
            return False

    def is_macos_dark_mode():
        try:
            result = subprocess.check_output(
                "defaults read -g AppleInterfaceStyle 2>/dev/null",
                shell=True,
                text=True,
            ).strip()
            return result == "Dark"
        except subprocess.CalledProcessError:
            return False

    system = platform.system()

    if system == "Windows":
        return is_windows_dark_mode()
    elif system == "Darwin":
        return is_macos_dark_mode()
    else:
        return False


# from ezgooey.ez import *
import ezgooey.logging as logging

from gooey import Gooey, GooeyParser  # , Events
from multinpainter_gui import __version__

short_version = ".".join(__version__.split(".")[:2])
from multinpainter import DESCRPTION_MODEL
from multinpainter.__main__ import *

dark = is_dark_mode()

GUI_NAME = f"Multinpainter GUI {short_version}"
CLI_NAME = "multinpainter-gui"
COLOR_BG_DARK = "#1e1e1e" if dark else "#f6f6f6"
COLOR_BG_LIGHT = "#1e1e1e" if dark else "#f6f6f6"
COLOR_TEXT1 = "#dedede" if dark else "#2b2b2b"
COLOR_TEXT2 = "#a4a4a4" if dark else "#2b2b2b"
STD_OPTIONS = {"label_color": COLOR_TEXT1, "help_color": COLOR_TEXT2}


def get_pictures_folder():
    platform = sys.platform
    home = Path.home()

    if platform.startswith(("win", "darwin")):
        return home / "Pictures"
    elif platform.startswith("linux"):
        return Path(os.environ.get("XDG_PICTURES_DIR", home))
    else:
        return home


def check_image(image_path):
    try:
        with Image.open(image_path) as image:
            width, height = img.size
            print(f"{width} x {height}")
        return image_path
    except Exception as e:
        raise ValueError(f"{image_path} is not an image") from e


@Gooey(
    # language_dir=getResourcePath("languages"),
    # terminal_font_family=None,
    # terminal_font_size=None,
    # terminal_font_weight=None,
    advanced=True,
    auto_start=False,
    body_bg_color=COLOR_BG_DARK,
    clear_before_run=False,
    default_size=(800, 580),
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
    header_image_center=True,
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
    navigation="TABBED",
    optional_cols=2,
    poll_external_updates=False,
    program_description=None,
    program_name=GUI_NAME,
    progress_expr=None,
    progress_regex=None,
    required_cols=1,
    # requires_shell=True,
    return_to_config=False,
    richtext_controls=True,
    show_failure_modal=True,
    show_preview_warning=False,
    show_restart_button=True,
    show_sidebar=False,
    show_stop_warning=True,
    show_success_modal=False,
    sidebar_bg_color=COLOR_BG_LIGHT,
    sidebar_title="Actions",
    suppress_gooey_flag=False,
    tabbed_groups=False,
    target=None,
    terminal_font_color=COLOR_TEXT1,
    terminal_panel_color=COLOR_BG_LIGHT,
    # use_events=[Events.VALIDATE_FORM],
    use_legacy_titles=True,
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
def gui():
    return cli()


def cli():
    top_parser = GooeyParser(
        add_help=False,
    )
    top_group = top_parser.add_argument_group(
        "",
        gooey_options={
            **STD_OPTIONS,
            **{},
        },
    )
    top_group.add_argument(
        "-i",
        "--image",
        type=str,
        dest="image",
        metavar="Input image",
        help="Image that you want to process",
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

    adv_parser = GooeyParser(
        add_help=False,
    )
    adv_group = adv_parser.add_argument_group(
        "",
        gooey_options={
            **STD_OPTIONS,
            **{
                "collapsible": True,
            },
        },
    )
    adv_group.add_argument(
        "-O",
        "--openai-api-key",
        type=str,
        dest="openai_api_key",
        default=os.environ.get("OPENAI_API_KEY"),
        metavar=" ",
        help="OpenAI API key (OPENAI_API_KEY env variable)",
        widget="PasswordField",
        gooey_options={
            **STD_OPTIONS,
            **{},
        },
    )
    adv_group.add_argument(
        "-F",
        "--hf-api-key",
        type=str,
        dest="hf_api_key",
        default=os.environ.get("HUGGINGFACEHUB_API_TOKEN"),
        metavar=" ",
        help="Huggingface API key (HUGGINGFACEHUB_API_TOKEN env variable)",
        widget="PasswordField",
        gooey_options={
            **STD_OPTIONS,
            **{},
        },
    )
    adv_group.add_argument(
        "-v",
        "--verbose",
        dest="verbose",
        action="store_true",
        default=True,
        metavar=" ",
        help=" Print detailed info and save intermediate images",
        gooey_options={
            **STD_OPTIONS,
            **{},
        },
    )
    adv_group.add_argument(
        "-P",
        "--prompt-model",
        type=str,
        dest="prompt_model",
        metavar=" ",
        default=DESCRPTION_MODEL,
        help="Huggingface model to describe image",
        gooey_options={
            **STD_OPTIONS,
            **{},
        },
    )

    mid_parser = GooeyParser(
        add_help=False,
        prog="",
        description="Perform iterative inpainting on an image file using OpenAI's DALL-E 2 model.",
        # parents=[top_parser],
    )
    mid_subparsers = mid_parser.add_subparsers(dest="command", help="commands")
    mid_inpaint_parser = mid_subparsers.add_parser(
        "Inpaint",
        help="Perform iterative inpainting on an image file",
        description="Iterative inpanting with Dall-E",
        parents=[top_parser],
        add_help=False,
    )
    mid_inpaint_group = mid_inpaint_parser.add_argument_group(
        "",
        gooey_options={
            **STD_OPTIONS,
            **{},
        },
    )

    mid_inpaint_group.add_argument(
        "-o",
        "--output",
        type=str,
        dest="output",
        metavar="Output image",
        help="If empty, image (and intermediate images) will be saved in source folder",
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
    mid_inpaint_group.add_argument(
        "-W",
        "--width",
        type=int,
        default=1920,
        dest="width",
        metavar="Output image width",
        widget="IntegerField",
        gooey_options={
            **STD_OPTIONS,
            **{"max": 32768},
        },
    )
    mid_inpaint_group.add_argument(
        "-H",
        "--height",
        type=int,
        default=1080,
        dest="height",
        metavar="Output image height",
        widget="IntegerField",
        gooey_options={
            **STD_OPTIONS,
            **{"max": 32768},
        },
    )
    mid_inpaint_group.add_argument(
        "-p",
        "--prompt",
        type=str,
        dest="prompt",
        metavar="Prompt",
        help="Default prompt for inpainting or for human in square",
        gooey_options={
            **STD_OPTIONS,
            **{},
        },
    )
    mid_inpaint_group.add_argument(
        "-f",
        "--fallback",
        type=str,
        dest="fallback",
        metavar=" ",
        help="Fallback prompt (autogenerate if empty)",
        gooey_options={
            **STD_OPTIONS,
            **{},
        },
    )
    mid_inpaint_group.add_argument(
        "-u",
        "--humans",
        dest="humans",
        metavar=" ",
        action="store_true",
        help=" Use fallback prompt if human not in square",
        gooey_options={
            **STD_OPTIONS,
            **{
                "full_width": True,
            },
        },
    )
    mid_inpaint_settings_group = mid_inpaint_parser.add_argument_group(
        "",
        gooey_options={
            **STD_OPTIONS,
            **{
                "collapsible": True,
            },
        },
    )
    # mid_inpaint_settings_group = adv_group
    mid_inpaint_settings_group.add_argument(
        "-S",
        "--square",
        type=int,
        dest="square",
        metavar=" ",
        default=1024,
        choices=[1024, 512, 256],
        help="Size of inpainting square",
        gooey_options={
            **STD_OPTIONS,
            **{},
        },
    )
    mid_inpaint_settings_group.add_argument(
        "-s",
        "--step",
        type=int,
        dest="step",
        metavar=" ",
        help="Step size to move square (0 = 50% of square)",
        widget="IntegerField",
        gooey_options={
            **STD_OPTIONS,
            **{"max": 32768},
        },
    )

    mid_describe_parser = mid_subparsers.add_parser(
        "Describe",
        help="Describe the image",
        description="Generate simple prompt for image",
        parents=[top_parser],
        add_help=False,
    )

    parser = GooeyParser(
        add_help=False,
        prog="",
        description="Perform iterative inpainting on an image file using OpenAI's DALL-E 2 model.",
        # parents=[top_parser],
    )

    subparsers = parser.add_subparsers(dest="command", help="commands")
    inpaint_parser = subparsers.add_parser(
        "Inpaint",
        help="Perform iterative inpainting on an image file",
        description="Iterative inpanting with Dall-E",
        parents=[mid_inpaint_parser, adv_parser],
        add_help=False,
    )

    describe_parser = subparsers.add_parser(
        "Describe",
        help="Describe the image",
        description="Generate simple prompt for image",
        parents=[mid_describe_parser, adv_parser],
        add_help=False,
    )

    return parser


def main(*args, **kwargs):
    if args := gui(*args, **kwargs).parse_args():
        args = vars(args)
        if args.get("verbose", True):
            logging.init(level=logging.DEBUG)
        else:
            logging.init(level=logging.WARN)
        log = logging.logger(CLI_NAME)
        command = args.pop("command")
        if command == "Inpaint":
            log.success(inpaint(**args))
        elif command == "Describe":
            log.success(describe(**args))


if __name__ == "__main__":
    main()
