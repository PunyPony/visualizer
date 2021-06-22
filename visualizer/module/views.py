
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, response
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg
import nibabel as nib
from os.path import join, isfile
import numpy as np
from django.conf import settings
from nilearn.masking import apply_mask

def makeSlice(img_data, axis, slice_nb):
    if axis=="X":
        slice_data = img_data[slice_nb, :, :]
    elif axis=="Y":
        slice_data = img_data[:, slice_nb, :]
    elif axis=="Z":
        slice_data = img_data[:, :, slice_nb]    
    return slice_data

def openFile(file_name, folder_path):
    filepath = join(folder_path,file_name+".nii.gz")
    if not isfile(filepath):
        return HttpResponse(f"<h1>Requested file do not exist<\h1>", status=404)

    img_data = nib.load(filepath).get_fdata()
    return img_data

def makeHist(ax, data, file_name):
    flatten = data.flatten()
    rescale = ((flatten + np.absolute(flatten.min()))/np.absolute(flatten.max())) * 255
    without_zeroes = rescale[np.nonzero(rescale)]
    ax.hist(without_zeroes, bins=np.arange(1, 255))
    ax.set(xlabel=f"{file_name} color histogram")
    return ax


def getSlice(request, axis, slice_nb, file_name):
    if request.method != "GET":
        return HttpResponse("<h1> Wrong request type </h1>",status=405)
    
    slice_nb = int(slice_nb)
    img_data = openFile(file_name, settings.IMAGES_DATA_PATH)
    if isinstance(img_data, HttpResponse):
        return img_data

    maximum_slice_nb = img_data.shape[{"X":0,"Y":1,"Z":2}[axis]] - 1
    
    if maximum_slice_nb < slice_nb:
        return HttpResponse(f"<h1> Not enough slices in the requested axis \
        ({axis}). Max is {maximum_slice_nb}. </h1>", status=405)

    slice_data = makeSlice(img_data, axis, slice_nb)
    fig,ax = plt.subplots()
    ax.imshow(slice_data.T, cmap="gray", origin="lower")
    ax.set(xlabel=f"slice {slice_nb} axis {axis}")

    response = HttpResponse(content_type = 'image/png')
    canvas = FigureCanvasAgg(fig)
    canvas.print_png(response)

    return response

def getHist(request, file_name):
    if request.method != "GET":
        return HttpResponse("<h1> Wrong request type</h1>",status=405)

    img_data = openFile(file_name, settings.IMAGES_DATA_PATH)
    if isinstance(img_data, HttpResponse):
        return img_data

    
    fig,ax = plt.subplots()
    ax = makeHist(ax, img_data, file_name)

    response = HttpResponse(content_type = 'image/png')
    canvas = FigureCanvasAgg(fig)
    canvas.print_png(response)
    
    return response

def getMaskHist(request, file_name, mask_name):
    if request.method != "GET":
        return HttpResponse("<h1>Wrong request type<\h1>", status=405)

    img_data = openFile(file_name, settings.IMAGES_DATA_PATH)
    if isinstance(img_data, HttpResponse):
        return img_data
    mask_data = openFile(mask_name, settings.MASKS_DATA_PATH)
    if isinstance(img_data, HttpResponse):
        return mask_data

    #masked_data = apply_mask(img_data, mask_data)
    #handle weird masks
    if mask_data.shape!=img_data.shape:
        return HttpResponse("<h1> Mask is illformed </h1>", status=404)
    
    mask_data = (mask_data>0)
    masked_data = img_data[mask_data] 
    fig,ax = plt.subplots()
    ax = makeHist(ax, masked_data, file_name)

    response = HttpResponse(content_type = 'image/png')
    canvas = FigureCanvasAgg(fig)
    canvas.print_png(response)
    return response

  
    
    

    


    
