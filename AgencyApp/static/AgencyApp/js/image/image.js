var newPicture;
var newPictureHeight;
var newPictureWidth;
var displayedPicture = {};
var areas;
var cropArea;
var pictureExists = false;
var pictureID = "";
var defaultImageURL = "";
var imageLoaded = false;

function checkIfPictureCanBeLoaded(){
    // imageLoaded set in previewEditPicture
    if(imageLoaded){
        loadImage(newPicture.src)
        togglePictureLoadingGif("hide")
    }
}

function previewEditPicture(input, onload) {
    if (input.files && input.files[0]) {
        // Add the loading gif
        togglePictureLoadingGif("show")

        // In min 1 second, check if the image can be loaded (need min 1s so that gif doesn't load for a split second)
        setTimeout(function(){checkIfPictureCanBeLoaded()}, 1000);

        var reader = new FileReader();
        reader.onload = function (e) {
            newPicture = new Image()
            // Let the gif start before loading the image, as it lags the gif
            setTimeout(function(){newPicture.src = e.target.result}, 500);
            newPicture.onload = function(){
                // Need to set width variables once the image is loaded into the js object
                newPictureHeight = this.height;
                newPictureWidth = this.width;
                // Image is loaded and ready to be displayed
                imageLoaded = true;
                if(onload != null){
                    onload()
                }
            }
        }
        reader.readAsDataURL(input.files[0]);
    }
}

function togglePictureLoadingGif(toggleType){
    var loadingGif = document.getElementById("loadingGif")
    var overlay = document.getElementById("loadingPictureGrayOverlay")
    if(overlay != null && loadingGif != null){
        if(toggleType === "show"){
            overlay.style.height = displayedPicture.height + "px";
            overlay.style.width = displayedPicture.width + "px";
            overlay.style.background = "rgba(0,0,0,0.7)"

            // Reset top margin of loading gif as height of displayed picture may have changed
            var gifHeight = loadingGif.style.height.substring(0, loadingGif.style.height.length-2);
            loadingGif.style.marginTop = (displayedPicture.height - gifHeight)/2 + "px";

            // Reset left margin of overlay, as it could change if new pic has diff dimensions
            if(displayedPicture.height > displayedPicture.width){
                var newLeftMargin =((290 - displayedPicture.width)/2 + 5) +"px";
                overlay.style.marginLeft = newLeftMargin;
            }else{
                // 6px accounts for the wrapper border width
                overlay.style.marginLeft = "6px";
            }
            loadingGif.style.display = "block";
        }else{
            overlay.style.background = "rgba(0,0,0,0)"
            overlay.style.height = "0%"
            overlay.style.width = "0%"
            loadingGif.style.display = "none";
        }
    }
}

function setDefaultImageURL(imageURL){
    defaultImageURL = imageURL
}

function setDoesPictureExist(picture){
    // Can't set using Django variables in separate file, so need a setter function
    if(picture.length > 0){
        pictureExists = true;
    }else{
        pictureExists = false;
    }
}

function setPictureID(newPicID){
    pictureID = newPicID;
}

function setNewPictureObject(imageURL, addCrop){
    if(addCrop == null){
        addCrop = true;
    }
    newPicture = new Image();
    newPicture.onload = function(){
        // Need to set width variables once the image is loaded into the js object
        newPictureHeight = this.height;
        newPictureWidth = this.width;

        // Once the js object is loaded, we can load the image into the page
        loadImage(imageURL, addCrop)
        return true;
        }
    newPicture.src = imageURL;
}

function updateCropArea(){
    // Updates the crop values taken from whatever the user set the crop window to
    areas = $("[id='" + pictureID + "']").selectAreas('areas');
    if(areas.length > 0){
        cropArea = areas[0];
    }
}

function selectMainArea(){
    // By default, the select area isn't selected, so show the resize buttons
    updateCropArea();
    var elems = document.getElementsByClassName("select-areas-resize-handler")
    for(var i=0; i < elems.length; i++){
        var elem = elems[i];
        elem.style.display = "block";
        elem.style.zIndex = "1";
    }

    // Since this is fn is called after crop is loaded, image is now finally ready to display
    canDisplayImage = true;
}

function createPictureContainer(includeCropHandler, addCrop){
    pictureHTML = "";
    if(includeCropHandler){
        pictureHTML += '<div class="imageCrop"><div class="wrapper"><div class="image-decorator"'
        if(!addCrop){
            pictureHTML += " style='padding: 5px 5px 0px 5px;'";
        }
        pictureHTML += '><div id="' + pictureID + 'Image"></div></div></div> </div>'
    }else{
        pictureHTML += '<div style="margin-top: 5px;"><div class="no-picture-image-decorator"><div id="' + pictureID + 'Image"></div></div></div>'
    }
    return pictureHTML
}

function loadImage(imageURL, addCrop){
    //Load the image into html and display the crop select area
    var imageString = "";
    var newArea = {};
    var aspectRatio = 0.9;
    var pictureDimension = 290;
    if(addCrop == null){
        addCrop = true;
    }

    // Create the picture container (different if existing pic or not)
    var pictureParentContainer = document.getElementById(pictureID + "Div");
    var pictureContainerString = null;
    if(pictureParentContainer != null){
        if(!pictureExists){
            // If there is an existing picture, create pic container with crop window
            pictureContainerString = createPictureContainer(false, addCrop)
        }else{
            // Otherwise, create pic container with offset for default image
            pictureContainerString = createPictureContainer(true, addCrop)
        }
        // Write the new picture container
        pictureParentContainer.innerHTML = pictureContainerString;
    }

    // Should have been created by the container
    var pictureContainer = document.getElementById(pictureID + "Image")
    if(pictureContainer != null){
        if(newPictureHeight != null && newPictureWidth != null){
            // Set highest dimension (h or w) to 300px
            if(newPictureHeight > newPictureWidth){
                imageString = '<img id="' + pictureID + '" src="' + imageURL + '" style="left: 0; background: #ededed; max-width: 290px; max-height: 290px;"/>'
                // height is bigger, so set display height to max (300)
                displayedPicture.height = pictureDimension;
                displayedPicture.width = (pictureDimension / newPictureHeight) * newPictureWidth

                //if pic height is bigger, area should have width of pic (with space above and below)
                newArea.width = displayedPicture.width;

                // Special case causing errors for square photos
                newArea.height = newArea.width / aspectRatio;
                if(newArea.height > pictureDimension){
                    newArea.height = pictureDimension
                }
            }else{
                imageString = '<img id="' + pictureID + '" src="' + imageURL + '" style="left: 0; background: #ededed; max-height: 290px; max-width: 290px;"/>'

                //width is bigger, so set display width to max (300)
                displayedPicture.width = pictureDimension;
                displayedPicture.height = (pictureDimension / newPictureWidth) * newPictureHeight
                
                //if pic width is bigger, area should have height of pic (with space on the sides)
                newArea.height = displayedPicture.height;
                newArea.width = newArea.height * 0.9;
            }
            pictureContainer.innerHTML = imageString;
        }
    }

    if(pictureExists && addCrop){
        $("[id='" + pictureID + "']").selectAreas({
            minSize: [10, 10],
            onLoaded: selectMainArea,
            allowSelect: false,
            aspectRatio: aspectRatio,
            areas: [
                {
                    x: 0,
                    y: 0,
                    width: newArea.width,
                    height: newArea.height,
                            }
                        ]
                    });
        }
    }

function addCropToPictureForm(formName, cropInputDivID){
    var form = document.getElementById(formName)
    if(form != null){
        updateCropArea();
        var scaleFactorWidth = newPictureWidth / displayedPicture.width;
        var scaleFactorHeight = newPictureHeight / displayedPicture.height;

        // draw cropped image
        if(cropArea != null){
            var sourceX = cropArea.x * scaleFactorWidth;
            var sourceY = cropArea.y * scaleFactorHeight;
            var sourceWidth = cropArea.width * scaleFactorWidth;
            var sourceHeight = cropArea.height * scaleFactorHeight;
            var cropInfoDiv = document.getElementById(cropInputDivID)
            cropInfoDiv.innerHTML = "";
            if(cropInfoDiv != null){
                cropInfoDiv.innerHTML += "<input type='hidden' name='crop_x' value='" + sourceX + "'>";
                cropInfoDiv.innerHTML += "<input type='hidden' name='crop_y' value='" + sourceY + "'>";
                cropInfoDiv.innerHTML += "<input type='hidden' name='crop_width' value='" + sourceWidth + "'>";
                cropInfoDiv.innerHTML += "<input type='hidden' name='crop_height' value='" + sourceHeight + "'>";
            }
        }
    }
    return form;
}

function submitPictureFormWithCrop(formName){
    var form = addCropToPictureForm(formName, "cropInfoInputs")
    return form.submit();
}