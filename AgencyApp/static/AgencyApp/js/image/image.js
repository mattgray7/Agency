var newPicture;
var newPictureHeight;
var newPictureWidth;
var displayedPicture = {};
var areas;
var cropArea;
var pictureExists = false;
var pictureID = "";

function previewPicture(input) {
    if (input.files && input.files[0]) {
        var reader = new FileReader();
        reader.onload = function (e) {
            newPicture = new Image()
            newPicture.src = e.target.result;
            newPicture.onload = function(){
                // Need to set width variables once the image is loaded into the js object
                newPictureHeight = this.height;
                newPictureWidth = this.width;

                // Once the js object is loaded, we can load the image into the page
                loadImage(e.target.result)
                return true;
            }
        }
        reader.readAsDataURL(input.files[0]);
    }
}

function setDoesPictureExist(picture){
    // Can't set using Django variables in separate file, so need a setter function
    if(picture.length > 0){
        pictureExists = true;
    }
}

function setPictureID(newPicID){
    pictureID = newPicID;
}

function setNewPictureObject(imageURL){
    newPicture = new Image();
    newPicture.onload = function(){
        // Need to set width variables once the image is loaded into the js object
        newPictureHeight = this.height;
        newPictureWidth = this.width;

        // Once the js object is loaded, we can load the image into the page
        loadImage(imageURL)
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
}

function createPictureContainer(includeCropHandler){
    pictureHTML = "";
    if(includeCropHandler){
       pictureHTML += '<div class="imageCrop"><div class="wrapper"><div class="image-decorator"><div id="' + pictureID + 'Image"></div></div></div> </div>'
    }else{
    pictureHTML += '<div style="margin-top: 5px;"><div id="' + pictureID + 'Image"></div></div>'
    }
    return pictureHTML
}

function loadImage(imageURL){
    //Load the image into html and display the crop select area
    var imageString = "";
    var newArea = {};
    var aspectRatio = 0.9;
    var pictureDimension = 290;

    // Create the picture container (different if existing pic or not)
    var pictureParentContainer = document.getElementById(pictureID + "Div");
    var pictureContainerString = null;
    if(pictureParentContainer != null){
        if(!pictureExists){
            // If there is an existing picture, create pic container with crop window
            pictureContainerString = createPictureContainer(false)
        }else{
            // Otherwise, create pic container with offset for default image
            pictureContainerString = createPictureContainer(true)
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
    if(pictureExists){
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

function submitPictureFormWithCrop(formName){
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
            var cropInfoDiv = document.getElementById("cropInfoInputs")
            if(cropInfoDiv != null){
                cropInfoDiv.innerHTML += "<input type='hidden' name='crop_x' value='" + sourceX + "'>";
                cropInfoDiv.innerHTML += "<input type='hidden' name='crop_y' value='" + sourceY + "'>";
                cropInfoDiv.innerHTML += "<input type='hidden' name='crop_width' value='" + sourceWidth + "'>";
                cropInfoDiv.innerHTML += "<input type='hidden' name='crop_height' value='" + sourceHeight + "'>";
            }
        }
    }
    return form.submit();
}