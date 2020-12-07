"""
HW 6: Flask web development

Name: Nicolas Corona

PennKey: njcorona

Number of hours spent on homework: 7

Collaboration is NOT permitted.

In the functions below the "NotImplementedError" exception is raised, for
you to fill in. The interpreter will not consider the empty code blocks
as syntax errors, but the "NotImplementedError" will be raised if you
call the function. You will replace these raised exceptions with your
code completing the function as described in the docstrings.
"""
# built-in modules
import json
import os

# web dev modules
from flask import Flask, flash, render_template, request, url_for, redirect
from werkzeug.utils import secure_filename

# deep learning/image modules
from PIL import Image
import torch
from torchvision import models, transforms

# For simplicity, we'll just store the model as a global
mobilenet = models.mobilenet_v2(pretrained=True)
mobilenet.eval()

# Flask constants, do not change!
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
app = Flask(__name__)
app.secret_key = 'ax9o4klasi-0oakdn'  # random secret key (needed for flashing)


def transform_image(image_file):
    """Transforms an input image_file to a standardized Pytorch Tensor.

    Args:
        image_file (str): the filename of the image

    Returns:
        Tensor: 4D tensor (batch_size=1, RGB=3, height, width) representing the
                input image
    """
    # resize to the shape that mobilenet is expecting, as well as applying
    # standardization according to the ImageNet mean and std
    img_transform = transforms.Compose([transforms.Resize(255),
                                        transforms.CenterCrop(224),
                                        transforms.ToTensor(),
                                        transforms.Normalize(
                                            [0.485, 0.456, 0.406],
                                            [0.229, 0.224, 0.225])])
    # remove the alpha channel if it is present
    image = Image.open(image_file).convert('RGB')
    img_tensor = img_transform(image).unsqueeze(0)
    return img_tensor


def get_prediction(img_tensor, model):
    """
    Get the model's prediction of the img_tensor.

    Like HW 5, the predicted class is the index of the class with the highest
    score, so torch.argmax() is useful here.

    NOTE: Be sure to convert your return value from a Tensor to an int!

    Args:
        img_tensor (Tensor): the 4D (batch_size=1, RGB=3, height, width)
                             input image sensor
        model: a Torch model that can evaluate images

    Returns:
        int: the integer index of the predicted class
    """
    preds = model(img_tensor)
    return torch.argmax(preds, dim=1).item()


def is_bird(torch_label):
    """
    Returns whether the given PyTorch class label corresponds to a bird class.

    Args:
        torch_label (int): PyTorch class label, 0-999
    Returns:
        bool: whether the label is a bird class according to bird_synset.txt
    """
    imgnet = json.load(open("imagenet_class_index.json"))
    possible_bird = imgnet[str(torch_label)][0]
    with open("bird_synset.txt") as f:
        for line in f:
            if possible_bird == line.strip():
                return True
    return False


@app.route("/", methods=['GET'])
def home():
    """
    Redirect the user from the root URL to the /upload URL.

    Args:
        None

    Returns:
        The required return by Flask so the user is redirected to the /upload
        URL
    """
    return redirect("/upload")


@app.route("/upload", methods=['GET', 'POST'])
def handle_upload():
    """
    Method that handles the /upload route.

    GET requests
        1. render upload_template.html

    POST requests
        1. flash and redirect back to /upload if file.filename is empty string
        2. flash and redirect back to /upload if file.filename doesn't have the
           an extension in ALLOWED_EXTENSIONS
        3. save the user's image to static/ directory and redirect to /result
           with the image_name query parameter set to the image file name

    NOTE: remember to create a directory called "static/" in the same
          directory as your hw6.py file so that flask can save user images!

    Args:
        None

    Returns:
        The required returns by Flask for the specified redirect/file upload
        behavior for both GET and POST requests as described above.
    """
    if request.method == 'GET':
        return render_template("upload_template.html")
    elif request.method == 'POST':
        user_file = request.files['file']

        if not user_file.filename:
            flash("No selected file")
            return redirect("/upload")

        if not user_file.filename.endswith(tuple(ALLOWED_EXTENSIONS)):
            flash("file extension not allowed")
            return redirect("/upload")

        user_file.save(os.path.join("static/", user_file.filename))

        return redirect(url_for("handle_result",
                        image_name="static/"+user_file.filename))


@app.route("/result", methods=['GET'])
def handle_result():
    """
    Method that handles the /result route.

    The name of the uploaded image should come as the query parameter
    "image_name".

    GET requests:
        1. flash and redirect back to /uploads if image_name query parameter
           is not specified
        2. Use mobilenet, is_bird(), transform_image(), is_bird() to figure out
           if image is bird or not
        3. render result_template.html with appropriate context variables

    Args:
        None

    Returns:
        The required returns by Flask for the specified redirect/rendering
        behavior for GET requests as described above.
    """
    image_name = request.args.get("image_name")

    if not image_name:
        flash("image_name query parameter is not specified")
        return redirect("/upload")

    bird = is_bird(get_prediction(transform_image(image_name), mobilenet))
    return render_template("result_template.html",
                           image_name=image_name,
                           is_bird=bird)


if __name__ == "__main__":
    app.run(port=5000, debug=True)
