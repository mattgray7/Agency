var newPicture;
var newPictureHeight;
var newPictureWidth;
var displayedPicture = {};
var areas;
//var cropArea;
var pictureExists = false;
var pictureID = "";
var defaultImageURL = "";
var imageLoaded = false;
var defaultAspectRatio = 0.9;


var newPictures = {}
var newPictureHeights = {}
var newPictureWidths = {}

var displayedPictures = {};
var cropAreas = {};
var areas = {}
var pictureMaxDimension = {"profilePicture": 290, "otherMediaPicture": 200, "editPostPicture": 290}

var pictureExistsMap = {}
var imageLoadedMap = {}


function checkIfPictureCanBeLoaded(pictureID, onload){
    // imageLoaded set in previewEditPicture
    if(imageLoadedMap[pictureID]){
        loadImage(pictureID, newPictures[pictureID].src)
        togglePictureLoadingGif(pictureID, "hide")
        if(onload != null){
            onload();
        }
    }
}

function previewEditPicture(pictureID, input, onload) {
    if (input.files && input.files[0]) {
        // Add the loading gif
        togglePictureLoadingGif(pictureID, "show")

        // In min 1 second, check if the image can be loaded (need min 1s so that gif doesn't load for a split second)
        setTimeout(function(){checkIfPictureCanBeLoaded(pictureID, onload)}, 1000);

        var reader = new FileReader();
        reader.onload = function (e) {
            newPictures[pictureID] = new Image()
            // Let the gif start before loading the image, as it lags the gif
            setTimeout(function(){newPictures[pictureID].src = e.target.result}, 500);
            newPictures[pictureID].onload = function(){
                // Need to set width variables once the image is loaded into the js object
                newPictureHeights[pictureID] = this.height;
                newPictureWidths[pictureID] = this.width;
                
                // Image is loaded and ready to be displayed
                imageLoadedMap[pictureID] = true;
                /*if(onload != null){
                    onload()
                }*/
            }
        }
        reader.readAsDataURL(input.files[0]);
    }
}

function togglePictureLoadingGif(pictureID, toggleType){
    var loadingGif = document.getElementById(pictureID + "LoadingGif")
    var overlay = document.getElementById(pictureID + "LoadingPictureGrayOverlay")
    if(overlay != null && loadingGif != null){
        if(toggleType === "show"){
            overlay.style.height = displayedPictures[pictureID].height + "px";
            overlay.style.width = displayedPictures[pictureID].width + "px";
            overlay.style.background = "rgba(0,0,0,0.7)"

            // Reset top margin of loading gif as height of displayed picture may have changed
            var gifHeight = loadingGif.style.height.substring(0, loadingGif.style.height.length-2);
            loadingGif.style.marginTop = (displayedPictures[pictureID].height - gifHeight)/2 + "px";

            // Reset left margin of overlay, as it could change if new pic has diff dimensions
            var newLeftMargin = 6;
            if(displayedPictures[pictureID].height > displayedPictures[pictureID].width){
                newLeftMargin = ((pictureMaxDimension[pictureID] - displayedPictures[pictureID].width)/2 + 5);
                if(pictureID === "otherMediaPicture"){
                    // Special case, otherMediaPicture always fits to edge
                    newLeftMargin = 5;
                }
            }

            overlay.style.marginLeft = newLeftMargin + "px";
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

function setDoesPictureExist(pictureID, pictureURL){
    // Can't set using Django variables in separate file, so need a setter function
    if(pictureURL.length > 0){
        pictureExistsMap[pictureID] = true;
    }else{
        pictureExistsMap[pictureID] = false;
    }
}

function setNewPictureObject(imageID, imageURL, addCrop){
    if(addCrop == null){
        addCrop = true;
    }
    newPictures[imageID] = new Image();
    newPictures[imageID].onload = function(){
        // Need to set width variables once the image is loaded into the js object
        newPictureHeights[imageID] = this.height;
        newPictureWidths[imageID] = this.width;

        // Once the js object is loaded, we can load the image into the page
        loadImage(imageID, imageURL, addCrop)
        return true;
        }
    newPictures[imageID].src = imageURL;
}

function updateCropArea(pictureID){
    // Updates the crop values taken from whatever the user set the crop window to
    areas[pictureID] = $("[id='" + pictureID + "']").selectAreas('areas');
    if(areas[pictureID].length > 0){
        cropAreas[pictureID] = areas[pictureID][0];
    }
}

function selectMainArea(pictureID){
    // By default, the select area isn't selected, so show the resize buttons
    //pictureID = "profilePicture"
    updateCropArea(pictureID);
    var elems;

    var picture = document.getElementById(pictureID + "Image")
    if(picture != null){
        elems = picture.getElementsByClassName("select-areas-resize-handler")
        if(elems == null || elems.length === 0){
            console.log("Warning: getting all resize handlers")
            elems = document.getElementsByClassName("select-areas-resize-handler")
        }
    }

    //var elems = document.getElementsByClassName("select-areas-resize-handler")
    for(var i=0; i < elems.length; i++){
        var elem = elems[i];
        elem.style.display = "block";
        elem.style.zIndex = "1";
    }

    // Since this is fn is called after crop is loaded, image is now finally ready to display
    canDisplayImage = true;
}

function createPictureContainer(pictureID, includeCropHandler, addCrop){
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

function loadImage(pictureID, imageURL, addCrop){
    //Load the image into html and display the crop select area
    var imageString = "";
    var newArea = {};
    var aspectRatio = defaultAspectRatio;
    var pictureDimension = pictureMaxDimension[pictureID]
    if(addCrop == null){
        addCrop = true;
    }

    // Create the picture container (different if existing pic or not)
    var pictureParentContainer = document.getElementById(pictureID + "Div");
    var pictureContainerString = null;
    if(pictureParentContainer != null){
        if(!pictureExistsMap[pictureID]){
            // If there is an existing picture, create pic container with crop window
            pictureContainerString = createPictureContainer(pictureID, false, addCrop)
        }else{
            // Otherwise, create pic container with offset for default image
            pictureContainerString = createPictureContainer(pictureID, true, addCrop)
        }
        // Write the new picture container
        pictureParentContainer.innerHTML = pictureContainerString;
    }

    // Should have been created by the container
    var pictureContainer = document.getElementById(pictureID + "Image")
    if(pictureContainer != null){
        if(newPictureHeights[pictureID] != null && newPictureWidths[pictureID] != null){
            // Set highest dimension (h or w) to 300px
            if(!(pictureID in displayedPictures)){
                displayedPictures[pictureID] = {};
            }
            if(newPictureHeights[pictureID] > newPictureWidths[pictureID]){
                imageString = '<img id="' + pictureID + '" src="' + imageURL + '" style="left: 0; background: #ededed; max-width: ' + pictureDimension + 'px; max-height: ' + pictureDimension + 'px;"/>'
                // height is bigger, so set display height to max (300)
                displayedPictures[pictureID].height = pictureDimension;
                displayedPictures[pictureID].width = (pictureDimension / newPictureHeights[pictureID]) * newPictureWidths[pictureID]

                //if pic height is bigger, area should have width of pic (with space above and below)
                newArea.width = displayedPictures[pictureID].width;

                // Special case causing errors for square photos
                newArea.height = newArea.width / aspectRatio;
                if(newArea.height > pictureDimension){
                    newArea.height = pictureDimension
                }
            }else{
                imageString = '<img id="' + pictureID + '" src="' + imageURL + '" style="left: 0; background: #ededed; max-height: ' + pictureDimension + 'px; max-width: ' + pictureDimension + 'px;"/>'

                //width is bigger, so set display width to max (300)
                displayedPictures[pictureID].width = pictureDimension;
                displayedPictures[pictureID].height = (pictureDimension / newPictureWidths[pictureID]) * newPictureHeights[pictureID]
                
                //if pic width is bigger, area should have height of pic (with space on the sides)
                newArea.height = displayedPictures[pictureID].height;
                newArea.width = newArea.height * 0.9;
            }
            pictureContainer.innerHTML = imageString;
        }
    }

    if(pictureExistsMap[pictureID] && addCrop){
        $("[id='" + pictureID + "']").selectAreas({
            minSize: [10, 10],
            onLoaded: function(){selectMainArea(pictureID)},
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

function addCropToPictureForm(formName, pictureID, cropInputDivID){
    var form = document.getElementById(formName)
    if(form != null){
        updateCropArea(pictureID);
        var scaleFactorWidth = newPictureWidths[pictureID] / displayedPictures[pictureID].width;
        var scaleFactorHeight = newPictureHeights[pictureID] / displayedPictures[pictureID].height;

        // draw cropped image
        var cropArea = cropAreas[pictureID];
        if(cropArea != null){
            var sourceX = cropArea.x * scaleFactorWidth;
            var sourceY = cropArea.y * scaleFactorHeight;
            var sourceWidth = cropArea.width * scaleFactorWidth;
            var sourceHeight = cropArea.height * scaleFactorHeight;
            var cropInfoDiv = document.getElementById(cropInputDivID)
            if(cropInfoDiv != null){
                cropInfoDiv.innerHTML = "";
                cropInfoDiv.innerHTML += "<input type='hidden' name='crop_x' value='" + sourceX + "'>";
                cropInfoDiv.innerHTML += "<input type='hidden' name='crop_y' value='" + sourceY + "'>";
                cropInfoDiv.innerHTML += "<input type='hidden' name='crop_width' value='" + sourceWidth + "'>";
                cropInfoDiv.innerHTML += "<input type='hidden' name='crop_height' value='" + sourceHeight + "'>";
            }
        }
    }
    return form;
}

function submitPictureFormWithCrop(formName, pictureID){
    var form = addCropToPictureForm(formName, pictureID, pictureID + "CropInfoInputs")
    return form.submit();
}