#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import asyncio
import base64
import io
import json
import logging
import os
import platform
import re
import shutil
import subprocess
import sys
from collections import OrderedDict
from datetime import datetime
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Tuple, Union

import aiohttp
import dlib
import ezgooey.logging as logging
import fire
import httpx
import numpy as np
import openai
import requests
import sphinx
from gooey import Gooey, GooeyParser
from multinpainter import *
from PIL import Image
from tqdm import tqdm
from ultralytics import YOLO

from multinpainter_gui import *
from multinpainter_gui.__main__ import *

main()
