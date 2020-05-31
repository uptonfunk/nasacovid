from app import app
from flask import send_file

import numpy as np
from netCDF4 import Dataset  # http://code.google.com/p/netcdf4-python/
import matplotlib.pyplot as plt
import xarray as xr
from PIL import Image, ImageEnhance
from matplotlib import cm
import StringIO as strio

from mpl_toolkits.basemap import Basemap, addcyclic, shiftgrid

def serve_pil_image(pil_img):
    img_io = strio.StringIO()
    pil_img.save(img_io, 'PNG', quality=70)
    img_io.seek(0)
    return send_file(img_io, mimetype='image/png')

@app.route('/')
@app.route('/index')
def index():
    return "Hello, World!"

@app.route('/night')
def night():
	nc_f = 'map_nine.nc'
	nc_fid = Dataset(nc_f, 'r', format='NETCDF4')
	observations = nc_fid["observation_data"]
	img = observations.variables["DNB_observations"][::-1,::-1]
	im = Image.fromarray(np.uint8(cm.gist_earth(img)*255.0))
	im.save('out.png')
	im = ImageEnhance.Contrast(im).enhance(2.5)
	print img.shape

	return serve_pil_image(im)

@app.route('/pm')
def pm():
	nc_f = "pm_one.nc"
	nc_fid = Dataset(nc_f, 'r', format='NETCDF4')

	img = nc_fid.variables["Local_albedo_swath_count"][4][0]
	print img
	im = Image.fromarray(np.uint8(cm.gist_earth(img)*255.0))
	im = ImageEnhance.Contrast(im).enhance(2.5)

	return serve_pil_image(im)