
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, response
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg
import nibabel as nib
from os.path import join, isfile
from os import listdir
import numpy as np
from django.conf import settings
from nilearn.masking import apply_mask
from django.template.response import TemplateResponse
from module.forms import Display
from django.shortcuts import render
from io import StringIO,BytesIO
import base64

def makeSlice(img_data, axis, slice_nb):
    if axis=="X":
        slice_data = img_data[slice_nb, :, :]
    elif axis=="Y":
        slice_data = img_data[:, slice_nb, :]
    elif axis=="Z":
        slice_data = img_data[:, :, slice_nb]    
    return slice_data

def openFile(file_name, folder_path):
    filepath = join(folder_path,file_name)
    if not isfile(filepath):
        return HttpResponse(f"<h1>Requested file do not exist</h1>", status=404)

    img_data = nib.load(filepath).get_fdata()
    return img_data

def makeHist(ax, data, label):
    def nan_ptp(a):
        return np.ptp(a[np.isfinite(a)])
    
    # data = 255*((data - np.nanmin(data))/nan_ptp(data))
    # data -= np.nanmin(data)
    # data *= 255/nan_ptp(data)
    # ax.hist(data.flatten(), bins=np.arange(0, 255), histtype='step')

    #reshape or ravel ?
    values, counts = np.unique(data.ravel(), return_counts=True)
    values -= np.nanmin(values)
    values *= 255/nan_ptp(values)
    ax.hist(values, bins=np.arange(0, 255), histtype='step', weights=counts)
    ax.set(xlabel=label)
    return ax

def drawSlice(axis, slice_nb, file_name):
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
    canvas = FigureCanvasAgg(fig)
    return canvas

def drawHist(file_name):
    img_data = openFile(file_name, settings.IMAGES_DATA_PATH)
    if isinstance(img_data, HttpResponse):
        return img_data

    fig,ax = plt.subplots()
    ax = makeHist(ax, img_data, f"{file_name} grey scale histogram")

    canvas = FigureCanvasAgg(fig)
    return canvas


@csrf_exempt
def home(request):
    files = sorted(
        filter(
        lambda s: s.endswith(".nii.gz") and isfile(join(settings.IMAGES_DATA_PATH, s)),
        listdir(settings.IMAGES_DATA_PATH))
        )

    if request.method == 'POST':
        display_form = Display(request.POST)
        if display_form.is_valid():
            graphic = BytesIO()
            func = display_form.cleaned_data["func"]
            if func=="slice":
                canvas = drawSlice(display_form.cleaned_data["axis"], 
                display_form.cleaned_data["slice_nb"], 
                display_form.cleaned_data["file_name"])
                if isinstance(canvas, HttpResponse):
                    return canvas
            elif func=="hist":
                if not display_form.cleaned_data["use_mask"]:
                    canvas = drawHist( 
                    display_form.cleaned_data["file_name"])
                    if isinstance(canvas, HttpResponse):
                        return canvas
                
                else:
                    canvas = drawMaskHist(
                    display_form.cleaned_data["file_name"], 
                    display_form.cleaned_data["file_name"])
                    if isinstance(canvas, HttpResponse):
                        return canvas
            else:
                return HttpResponse("<h1> Func do not exist </h1>",status=404)

            canvas.print_png(graphic)
            encoded_graphic = base64.b64encode(graphic.getvalue())
            return render(request, "files_previewer.html", {"img": str(encoded_graphic)[2:-1], "files":files})

    return render(request, "files_previewer.html", {"img": None, "files":files})


def getSlice(request, axis, slice_nb, file_name):
    if request.method != "GET":
        return HttpResponse("<h1> Wrong request type </h1>",status=405)
    
    slice_nb = int(slice_nb)
    canvas = drawSlice(axis, slice_nb, file_name)
    if isinstance(canvas, HttpResponse):
        return canvas

    response = HttpResponse(content_type = 'image/png')
    canvas.print_png(response)

    return response


def getHist(request, file_name):
    if request.method != "GET":
        return HttpResponse("<h1> Wrong request type</h1>",status=405)

   
    canvas = drawHist(file_name)
    if isinstance(canvas, HttpResponse):
        return canvas
    
    response = HttpResponse(content_type = 'image/png')
    canvas.print_png(response)
    return response

def drawMaskHist(file_name, mask_name):
    img_data = openFile(file_name, settings.IMAGES_DATA_PATH)
    if isinstance(img_data, HttpResponse):
        return img_data
    mask_data = openFile(mask_name, settings.MASKS_DATA_PATH)
    if isinstance(mask_data, HttpResponse):
        return mask_data

    #masked_data = apply_mask(img_data, mask_data)
    #handle weird masks
    if mask_data.shape!=img_data.shape:
        return HttpResponse("<h1> Mask is illformed </h1>", status=404)
    
    mask_data = mask_data.astype(bool)
    masked_data = img_data[mask_data] 
    fig,ax = plt.subplots()
    ax = makeHist(ax, masked_data, f"{file_name} masked grey scale histogram")    
    canvas = FigureCanvasAgg(fig)
    return canvas

def getMaskHist(request, file_name, mask_name):
    if request.method != "GET":
        return HttpResponse("<h1>Wrong request type</h1>", status=405)

    canvas = drawMaskHist(file_name, mask_name)
    if isinstance(canvas, HttpResponse):
        return canvas
    response = HttpResponse(content_type = 'image/png')
    canvas.print_png(response)
    return response