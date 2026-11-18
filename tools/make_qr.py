#!/usr/bin/env python3
"""Styled Colab QR for a notebook in this repo (same look as bulgaria_qr.png / hungary_qr.png).

    python tools/make_qr.py greece_forecast.ipynb      # -> greece_qr.png
"""
import os, sys
import qrcode
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers.pil import RoundedModuleDrawer
from qrcode.image.styles.colormasks import RadialGradiantColorMask

REPO = "https://colab.research.google.com/github/piddy376/visits-weather-notebooks/blob/main/"

nb = sys.argv[1]
url = REPO + nb
qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_H, box_size=16, border=3)
qr.add_data(url); qr.make(fit=True)
img = qr.make_image(image_factory=StyledPilImage, module_drawer=RoundedModuleDrawer(),
                    color_mask=RadialGradiantColorMask(back_color=(255, 255, 255),
                                                       center_color=(0, 61, 107), edge_color=(42, 134, 193)))
out = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                   nb.split("_")[0] + "_qr.png")
img.save(out); print(out, "->", url)
