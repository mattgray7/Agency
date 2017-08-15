function addSelectProjectForm(postID, username){

}

function getErrorPanel(errors){
    var panelString = "<div class='errorPanel'><div style='text-align: left; margin-top: 5px; margin-left: 5px;'><h3 style='margin-bottom: 5px;'>One or more errors occurred:</h3><div><ul>"
    for(var errorType in errors){
        fieldNames = errors[errorType]
        var errorString = "";

        // TODO other error types that could popup
        if(errorType == "required"){
            errorString += "<li> The following fields are required: ";
            for(var i=0; i < fieldNames.length; i++){
                errorString += fieldNames[i] + ", ";
            }
            // Remove trailing ', '
            errorString = errorString.substring(0, errorString.length-2) + "</li>";
            panelString += errorString;
        }
    }
    panelString += "</ul></div></div>";
    return panelString;
}

var buttonLoadingGifURL;
function setButtonLoadingGifURL(gifURL){
    if(gifURL != null && gifURL.length > 0){
        buttonLoadingGifURL = gifURL;
    }
}

function togglePopup(toggleType, overlayDivID, contentDivID){
    var overlay = document.getElementById(overlayDivID);
    var contentBox = document.getElementById(contentDivID);
    if(overlay && contentBox){
        if(toggleType === "show"){
            overlay.style.height = "1500px";
            overlay.style.width = "118%";
            overlay.style.background = "rgba(0,0,0,0.5)"
            contentBox.style.display = "block";
            contentBox.style.background = "rgba(255,255,255,1)"
        }else if(toggleType === "hide"){
            overlay.style.background = "rgba(0,0,0,0)"
            overlay.style.height = "0%"
            overlay.style.width = "0%"
            contentBox.style.display = "none";
            contentBox.style.background = "rgba(255,255,255,0)"
        }
    }
}

function toggleSelectProjectPopup(toggleType){
    togglePopup(toggleType, "hiddenGrayPopupOverlay", "selectProjectPanel");
}

function toggleEditPicturePopup(toggleType, postIsProject, pictureURL){
    if(postIsProject == null){
        postIsProject = false;
    }
    togglePopup(toggleType, "hiddenGrayPopupOverlay", "editPicturePanel")
    if(toggleType === "show"){
        addEditImageContent("editPicturePanel", postIsProject, pictureURL);
    }
}

function addPopupPictureToBaseForm(tempPictureID, tempPictureURL, isProject){
    var baseFormPictureInput = document.getElementById("mainPostPictureInput")
    var editPicture = document.getElementById("postPicturePanelEditButton")
    if(isProject){
        baseFormPictureInput = document.getElementById("mainProjectPictureInput")
        editPicture = document.getElementById("projectPicturePanelEditButton")
    }
    baseFormPictureInput.innerHTML = "<input type='hidden' name='tempPostPictureID' value='" + tempPictureID + "'>"

    // Update onclick of edit picture button to load tempPicture
    editPicture.onclick = function(){
        toggleEditPicturePopup("show", isProject, tempPictureURL)
    }
    return setBaseFormPicture(tempPictureURL, isProject);
}

var currentBaseFormPicture;
function setBaseFormPicture(pictureURL, isProject){
    var baseFormPicture = document.getElementById("postPictureImg")
    if(isProject){
        baseFormPicture = document.getElementById("projectPictureImg")
    }
    if(baseFormPicture != null && pictureURL.length > 0){
        baseFormPicture.src = pictureURL
        currentBaseFormPicture = pictureURL
        return true;
    }
    return false;
}

function submitPictureForm(formName, isProject){
        var updateButton = document.getElementById("updatePictureButton")
        var updateButtonHTML = updateButton.innerHTML;
        updateButton.innerHTML = "<img id='loadingGif' src='" + buttonLoadingGifURL + "' style='position: absolute; height: 60px; width: 60px; margin-top: -15px;'>"

        var form = addCropToPictureForm(formName, "cropInfoInputs")
        var formData = new FormData(form)
        if(form != null){
            $.ajax({
                url : "/ajax/saveTempPostPicture/",
                data : formData,
                type : 'POST',
                dataType: "json",
                cache: false,
                contentType: false,
                processData: false,
                success : function(data) {
                    if(data["success"]){
                        // Add the temp picture to the base form (input and display)]
                        addPopupPictureToBaseForm(data["tempID"], data["pictureURL"], isProject)
                        updateButton.innerHTML = updateButtonHTML;
                        toggleEditPicturePopup("hide")
                    }
                }
            });
        }
    }


function addCreateCastingPost(formDict, formURL, formName){
    var formString = "<form method='post' action='" + formURL + "' id='" + formName + "' class='form-style-1' style='width: 90%; background: none; margin-left: 3.2%;' enctype='multipart/form-data'>";
    formString += "<table style='width: 100%;'><tr>"

    // Fill post picture string
    var pictureField = formDict["postPicture"];
    var pictureColumn = getPostPicturePanel("postPicturePanel", pictureField.value, pictureField.editOnclick, "postPictureImg", pictureField.input, "mainPostPictureInput");


    // Fill text content
    var sectionMap = {"Details": ["title", "project", "characterType", "status", "startDate", "endDate", "hoursPerWeek", "paid"],
                      "Character": ["characterName", "shortCharacterDescription", "description", "skills", "languages"],
                      "Performer": ["actorName"],
                      "Physical": ["hairColor", "eyeColor", "complexion", "height", "build", "gender", "ageRange"],
                      "hidden": ["csrf_token", "postID", "source", "next", "destination", "projectID", "poster", "postType"]}
    var mainLabelsColumn = "<td class='editPostLabelPanel' style='width: 20%; position:relative; line-height: 38.2px;'><ul style='margin-bottom: -14px; margin-top: -40px;'>";
    var mainInputsColumn = "<td class='editPostInputPanel' style='width: 50%; position: relative; line-height: 39px;'><ul style='margin-top: -20px; '>";
    var otherLabelsColumn = "<td class='editPostLabelPanel' style='width: 30%; min-width: 170px; height: 600px; position:relative;'><ul style='margin-top: 5px;'>";
    var otherInputsColumn = "<td class='editPostInputPanel' colspan='2' style='width: 70%;'><div style='margin-top: -6px;'><ul>";
    for(sectionTitle in sectionMap){
        var fieldList = sectionMap[sectionTitle];
        var sectionInputTableElement = null;
        var sectionLabelTableElement = null;
        var sectionClass = null;
        if(sectionTitle === "Details" || sectionTitle === "Production"){
            sectionLabelTableElement = mainLabelsColumn;
            sectionInputTableElement = mainInputsColumn;
            sectionClass = "editPostMainSectionTitle";
        }else{
            sectionLabelTableElement = otherLabelsColumn;
            sectionInputTableElement = otherInputsColumn;
            sectionClass = "editPostOtherSectionTitle";
        }

        if(sectionTitle != "hidden"){
            sectionLabelTableElement += "<div style='position: relative; height: 50px; width: 100%;'> <h2 class='" + sectionClass + "' style='position: absolute; z-index: 1; right: 0; margin-left: 80px;'> " + sectionTitle + "</h2>" + getFormDividerLine() + "</div></div>"
            sectionInputTableElement += "<div style='height: 60px;'></div>";

            for(i in fieldList){
                var fieldName = sectionMap[sectionTitle][i];
                var field = formDict[fieldName];
                if(!field){
                    continue;
                }

                // Add project
                if(fieldName === "project"){
                    sectionLabelTableElement += "<label for='name'>Project</label><br>";
                    if(field.title != null){
                        sectionInputTableElement += "<li style='margin-top: 6px;'><a  onclick='redirectToPost(" + '"' + field.projectID + '"' + ");'>" + field.title + "</a></li>";
                    }else{
                        sectionInputTableElement += "<li style='margin-top: 6px;'>None - <a onclick='" + field.addNewOnclick + "'>Add</a></li>";
                    }
                    continue;
                }else if(fieldName === "actorName"){
                    if(field.value != null && field.value.length > 0){
                        var actorDict = formDict["actor"]

                        // Add actor text panel
                        if(actorDict.cleanName != null && actorDict.username != null){
                            sectionLabelTableElement += "<div style='height: 165px;'></div>";
                            
                            sectionInputTableElement+= "<div style='width: 100%; position: relative; height: 161px;' class='editCastMemberPanel'>"
                            sectionInputTableElement += '<div style="position: absolute; left: 0;"><h2>' + actorDict.cleanName + "</h2></div>";
                            // Add actor profile picture panel
                            sectionInputTableElement += '<div style="position: absolute; right: 0; margin-top: 2px; margin-right: 2px;"><div id="actorPicturePanel" class="postPicture" style="width: 100px; height: 100px; background: #000;"><img id="actorPictureImg" src="' + actorDict.profilePictureURL + '" style="max-width:100%; max-height:100%;"/></div></div>';
                        }else{
                            sectionLabelTableElement += "<label for='name'>Search</label><br>";

                            sectionInputTableElement+= "<div style='width: 100%; position: relative; height: 37px;' class='editCastMemberPanel'>"
                            sectionInputTableElement += '<div style="position: absolute; left: 0;"><input type="text" name="performerSearchText"></div>';
                        }
                        sectionInputTableElement += "</div>";
                    }
                    continue;
                }
                if(!field.hidden || field.name === "status"){
                    if(field.numRows > 1){
                        // stupid hack I hate myself right now
                        sectionLabelTableElement += "<li style='height:" + '' + field.numRows*5.9 + 'px;' + "'><label for='name'>" + field.label + "</label></li>";
                        // TODO replace newlines in description as it will break js
                        sectionInputTableElement += "<li><textarea rows='" + field.numRows + "' name='" + field.name + "' form='" + formName + "' style='height:100px; width: 97.7%; resize: none;' placeholder='" + field.placeholder + "'>" + field.value + "</textarea></li>";
                    }else{
                        sectionLabelTableElement += "<label for='name'>" + field.label + "</label><br>";
                        sectionInputTableElement += "<li>"
                        if(field.options){
                            var selectForm = createSelectForm(formName, field.name + "SelectBar", field.options, field.value);
                            sectionInputTableElement += selectForm;
                            sectionInputTableElement += "<input type='hidden' name='" + field.name + "' id='" + field.name + "SelectInput' >";
                        }else{
                            sectionInputTableElement += field.input;
                        }
                        sectionInputTableElement += '</li>';
                    }
                }else if(field.input != null && field.input.length > 0){
                    sectionInputTableElement += field.input;
                }
            }
        }else{
            for(i in fieldList){
                var fieldName = sectionMap[sectionTitle][i];
                var field = formDict[fieldName];
                if(!field){
                    continue;
                }
                sectionInputTableElement += field.input;
            }
        }
        if(sectionTitle === "Details" || sectionTitle === "Production"){
            mainLabelsColumn = sectionLabelTableElement;
            mainInputsColumn = sectionInputTableElement;
        }else{
            otherLabelsColumn = sectionLabelTableElement + "<div style='height: 20px'></div>";
            otherInputsColumn = sectionInputTableElement + "<div style='height: 10px'></div>";
        }

    }
    mainLabelsColumn += "</ul></div></td>";
    otherLabelsColumn += "</ul></div></td>";
    mainInputsColumn += "</ul></td>";
    otherInputsColumn += "</ul></div></td>";

    // Add title
    formString += "<tr><td colspan='3' style='text-align: center;'><h1 style='font-size: 2.8em; margin-left: 65px; padding: 0em 0em 0.3em 0em; margin-top: 15px;'>";
    if(formDict["newPost"]){
        formString += "Add Role";
    }else{
        formString += "Edit Role";
    }
    formString += "</h1></td></tr>";

    // Add error panel
    formString += "<tr id='formErrorRow'>";
    if(formDict["errors"]){
        formString += "<td colspan='3'>" + getErrorPanel(formDict["errors"]) + "</td>";
    }
    formString += "</tr>";

    // Create the form
    formString += "<tr>" + mainLabelsColumn + mainInputsColumn + pictureColumn + "</tr>"
    formString += "<tr>" + otherLabelsColumn + otherInputsColumn + "</tr></form>"

    // Add buttons
    formString += "<tr><td colspan='3' style='width: 90%; position:relative; height: 70px;'><div style='margin-left: 100px;'><div class='whiteButton blackHover' style='position:absolute; left: 1%; top: 0; right: 50.5%;' onclick='" + formDict["cancelButton"]["onclick"] + "'> Cancel </div><div class='whiteButton blackHover' style='position:absolute; right: -1%; top: 0; left: 50.5%; ' onclick='" + formDict["createButton"].onclickFunction + "(" + '"' + formName + '", ' + !formDict["newPost"] + ');' + "'>"
    if(formDict["newPost"]){
        formString += "Create Post";
    }else{
        formString += "Update Post";
    }
    formString += "</div></div></td></tr>";
    return formString;
}


function addCreateWorkPost(formDict, formURL, formName){
    var formString = "<form method='post' action='" + formURL + "' id='" + formName + "' class='form-style-1' style='width: 90%; background: none; margin-left: 3.2%;' enctype='multipart/form-data'>";
    formString += "<table style='width: 100%;'><tr>"

    // Fill post picture string
    var pictureField = formDict["postPicture"];
    var pictureColumn = getPostPicturePanel("postPicturePanel", pictureField.value, pictureField.editOnclick, "postPictureImg", pictureField.input, "mainPostPictureInput");

    // Fill text content
    var sectionMap = {"Details": ["title", "project", "profession", "status", "startDate", "endDate", "hoursPerWeek", "paid"],
                      "The Job": ["shortDescription", "description", "location", "skills"],
                      "Worker": ["workerName"],
                      "Equipment": ["workerNeedsEquipment", "equipmentDescription"],
                      "hidden": ["csrf_token", "postID", "source", "next", "destination", "projectID", "poster"]}
    var mainLabelsColumn = "<td class='editPostLabelPanel' style='width: 20%; position:relative; line-height: 38.2px;'><ul style='margin-bottom: -14px; margin-top: -40px;'>";
    var mainInputsColumn = "<td class='editPostInputPanel' style='width: 50%; position: relative; line-height: 39px;'><ul style='margin-top: -20px; '>";
    var otherLabelsColumn = "<td class='editPostLabelPanel' style='width: 30%; min-width: 170px; position:relative;'><ul style='margin-top: 5px;'>";
    var otherInputsColumn = "<td class='editPostInputPanel' colspan='2' style='width: 70%;'><div style='margin-top: -6px;'><ul>";
    for(sectionTitle in sectionMap){
        var fieldList = sectionMap[sectionTitle];
        var sectionInputTableElement = null;
        var sectionLabelTableElement = null;
        var sectionClass = null;
        if(sectionTitle === "Details"){
            sectionLabelTableElement = mainLabelsColumn;
            sectionInputTableElement = mainInputsColumn;
            sectionClass = "editPostMainSectionTitle";
        }else{
            sectionLabelTableElement = otherLabelsColumn;
            sectionInputTableElement = otherInputsColumn;
            sectionClass = "editPostOtherSectionTitle";
        }

        if(sectionTitle != "hidden"){
            sectionLabelTableElement += "<div style='position: relative; height: 50px; width: 100%;'> <h2 class='" + sectionClass + "' style='position: absolute; z-index: 1; right: 0; margin-left: 80px;'> " + sectionTitle + "</h2>" + getFormDividerLine() + "</div></div>"
            sectionInputTableElement += "<div style='height: 60px;'></div>";

            for(i in fieldList){
                var fieldName = sectionMap[sectionTitle][i];
                var field = formDict[fieldName];

                // Add project
                if(fieldName === "project"){
                    sectionLabelTableElement += "<label for='name'>Project</label><br>";
                    if(field.title != null){
                        sectionInputTableElement += "<li style='margin-top: 6px;'><a  onclick='redirectToPost(" + '"' + field.projectID + '"' + ");'>" + field.title + "</a></li>";
                    }else{
                        sectionInputTableElement += "<li style='margin-top: 6px;'>None - <a onclick='" + field.addNewOnclick + "'>Add</a></li>";
                    }
                    continue;
                }else if(fieldName === "workerName"){
                    if(field.value != null && field.value.length > 0){
                        var workerDict = formDict["worker"]

                        // Add actor text panel
                        if(workerDict.cleanName != null && workerDict.username != null){
                            sectionLabelTableElement += "<div style='height: 165px;'></div>";
                            
                            sectionInputTableElement+= "<div style='width: 100%; position: relative; height: 161px;' class='editCastMemberPanel'>"
                            sectionInputTableElement += '<div style="position: absolute; left: 0;"><h2>' + workerDict.cleanName + "</h2></div>";
                            // Add actor profile picture panel
                            sectionInputTableElement += '<div style="position: absolute; right: 0; margin-top: 2px; margin-right: 2px;"><div id="actorPicturePanel" class="postPicture" style="width: 100px; height: 100px; background: #000;"><img id="actorPictureImg" src="' + workerDict.profilePictureURL + '" style="max-width:100%; max-height:100%;"/></div></div>';
                        }else{
                            sectionLabelTableElement += "<label for='name'>Search</label><br>";

                            sectionInputTableElement+= "<div style='width: 100%; position: relative; height: 37px;' class='editCastMemberPanel'>"
                            sectionInputTableElement += '<div style="position: absolute; left: 0;"><input type="text" name="performerSearchText"></div>';
                        }
                        sectionInputTableElement += "</div>";
                    }
                    continue;
                }
                if(!field.hidden || field.name === "status"){
                    if(field.numRows > 1){
                        // stupid hack I hate myself right now
                        sectionLabelTableElement += "<li style='height:" + '' + field.numRows*5.9 + 'px;' + "'><label for='name'>" + field.label + "</label></li>";
                        // TODO replace newlines in description as it will break js
                        sectionInputTableElement += "<li><textarea rows='" + field.numRows + "' name='" + field.name + "' form='" + formName + "' style='height:100px; width: 97.7%; resize: none;' placeholder='" + field.placeholder + "'>" + field.value + "</textarea></li>";
                    }else{
                        sectionLabelTableElement += "<label for='name'>" + field.label + "</label><br>";
                        sectionInputTableElement += "<li>"
                        if(field.options){
                            var selectForm = createSelectForm(formName, field.name + "SelectBar", field.options, field.value);
                            sectionInputTableElement += selectForm;
                            sectionInputTableElement += "<input type='hidden' name='" + field.name + "' id='" + field.name + "SelectInput' >";
                        }else{
                            sectionInputTableElement += field.input;
                        }
                        sectionInputTableElement += '</li>';
                    }
                }else if(field.input != null && field.input.length > 0){
                    sectionInputTableElement += field.input;
                }
            }
        }else{
            for(i in fieldList){
                var fieldName = sectionMap[sectionTitle][i];
                var field = formDict[fieldName];
                sectionInputTableElement += field.input;
            }
        }
        if(sectionTitle === "Details"){
            mainLabelsColumn = sectionLabelTableElement;
            mainInputsColumn = sectionInputTableElement;
        }else{
            otherLabelsColumn = sectionLabelTableElement + "<div style='height: 20px'></div>";
            otherInputsColumn = sectionInputTableElement + "<div style='height: 10px'></div>";
        }

    }
    mainLabelsColumn += "</ul></div></td>";
    otherLabelsColumn += "</ul></div></td>";
    mainInputsColumn += "</ul></td>";
    otherInputsColumn += "</ul></div></td>";

    // Add title
    formString += "<tr><td colspan='3' style='text-align: center;'><h1 style='font-size: 2.8em; margin-left: 65px; padding: 0em 0em 0.3em 0em; margin-top: 15px;'>";
    if(formDict["newPost"]){
        formString += "Add Job Post";
    }else{
        formString += "Edit Job Post";
    }
    formString += "</h1></td></tr>";

    // Add error panel
    if(formDict["errors"]){
        formString += "<tr><td colspan='3'>" + getErrorPanel(formDict["errors"]) + "</td></tr>";
    }

    // Create the form
    formString += "<tr>" + mainLabelsColumn + mainInputsColumn + pictureColumn + "</tr>"
    formString += "<tr>" + otherLabelsColumn + otherInputsColumn + "</tr></form>"

    // Add buttons
    formString += "<tr><td colspan='3' style='width: 90%; position:relative; height: 70px;'><div style='margin-left: 100px;'><div class='whiteButton blackHover' style='position:absolute; left: 1%; top: 0; right: 50.5%;' onclick='" + formDict["cancelButton"]["onclick"] + "'> Cancel </div><div class='whiteButton blackHover' style='position:absolute; right: -1%; top: 0; left: 50.5%; ' onclick='" + formDict["createButton"].onclickFunction + "(" + '"' + formName  + '", ' + !formDict["newPost"] + ');' + "'>"
    if(formDict["newPost"]){
        formString += "Create Post";
    }else{
        formString += "Update Post"
    }
    formString += "</div></div></td></tr>";
    return formString;
}

function addCreateProjectPost(formDict, formURL, formName){
    var formString = "<form method='post' action='" + formURL + "' id='" + formName + "' class='form-style-1' style='width: 90%; background: none; margin-left: 3.2%;' enctype='multipart/form-data'>";
    formString += "<table style='width: 100%;'><tr>"

    // Fill post picture string
    var pictureField = formDict["postPicture"];
    var pictureColumn = getPostPicturePanel("projectPicturePanel", pictureField.value, pictureField.editOnclick, "projectPictureImg", pictureField.input, "mainProjectPictureInput");

    // Fill text content
    var sectionMap = {"Details": ["title", "projectType", "status", "location", "union", "length"],
                      "The Project": ["shortDescription", "description"],
                      "hidden": ["csrf_token", "postID", "source", "next", "destination", "projectID", "poster"]}
    var mainLabelsColumn = "<td class='editPostLabelPanel' style='width: 20%; position:relative; line-height: 38.2px;'><ul style='margin-bottom: -14px; margin-top: -40px;'>";
    var mainInputsColumn = "<td class='editPostInputPanel' style='width: 50%; position: relative; line-height: 39px;'><ul style='margin-top: -20px; '>";
    var otherLabelsColumn = "<td class='editPostLabelPanel' style='width: 30%; min-width: 170px; position:relative;'><ul style='margin-top: 5px;'>";
    var otherInputsColumn = "<td class='editPostInputPanel' colspan='2' style='width: 70%;'><div style='margin-top: -6px;'><ul>";
    for(sectionTitle in sectionMap){
        var fieldList = sectionMap[sectionTitle];
        var sectionInputTableElement = null;
        var sectionLabelTableElement = null;
        var sectionClass = null;
        if(sectionTitle === "Details"){
            sectionLabelTableElement = mainLabelsColumn;
            sectionInputTableElement = mainInputsColumn;
            sectionClass = "editPostMainSectionTitle";
        }else{
            sectionLabelTableElement = otherLabelsColumn;
            sectionInputTableElement = otherInputsColumn;
            sectionClass = "editPostOtherSectionTitle";
        }

        if(sectionTitle != "hidden"){
            sectionLabelTableElement += "<div style='position: relative; height: 50px; width: 100%;'> <h2 class='" + sectionClass + "' style='position: absolute; z-index: 1; right: 0; margin-left: 80px;'> " + sectionTitle + "</h2>" + getFormDividerLine() + "</div>"
            sectionInputTableElement += "<div style='height: 60px;'></div>";

            for(i in fieldList){
                var fieldName = sectionMap[sectionTitle][i];
                var field = formDict[fieldName];

                if(!field.hidden || field.name === "status"){
                    if(field.numRows > 1){
                        // stupid hack I hate myself right now
                        sectionLabelTableElement += "<li style='height:" + '' + field.numRows*5.9 + 'px;' + "'><label for='name'>" + field.label + "</label></li>";
                        // TODO replace newlines in description as it will break js
                        sectionInputTableElement += "<li><textarea rows='" + field.numRows + "' name='" + field.name + "' form='" + formName + "' style='height:100px; width: 97.7%; resize: none;' placeholder='" + field.placeholder + "'>" + field.value + "</textarea></li>";
                    }else{
                        sectionLabelTableElement += "<label for='name'>" + field.label + "</label><br>";
                        sectionInputTableElement += "<li>"
                        if(field.options){
                            var selectForm = createSelectForm(formName, field.name + "SelectBarProject", field.options, field.value);
                            sectionInputTableElement += selectForm;
                            sectionInputTableElement += "<input type='hidden' name='" + field.name + "' id='" + field.name + "SelectInputProject' >";
                        }else{
                            sectionInputTableElement += field.input;
                        }
                        sectionInputTableElement += '</li>';
                    }
                }else if(field.input != null && field.input.length > 0){
                    sectionInputTableElement += field.input;
                }
            }
        }else{
            for(i in fieldList){
                var fieldName = sectionMap[sectionTitle][i];
                var field = formDict[fieldName];
                sectionInputTableElement += field.input;
            }
        }
        if(sectionTitle === "Details"){
            mainLabelsColumn = sectionLabelTableElement;
            mainInputsColumn = sectionInputTableElement;
        }else{
            otherLabelsColumn = sectionLabelTableElement + "<div style='height: 20px'></div>";
            otherInputsColumn = sectionInputTableElement + "<div style='height: 10px'></div>";
        }

    }
    mainLabelsColumn += "</ul></div></td>";
    otherLabelsColumn += "</ul></div></td>";
    mainInputsColumn += "</ul></td>";
    otherInputsColumn += "</ul></div></td>";

    // Add title
    formString += "<tr><td colspan='3' style='text-align: center;'><h1 style='font-size: 2.8em; margin-left: 65px; padding: 0em 0em 0.3em 0em; margin-top: 15px;'>";
    if(formDict["newPost"]){
        formString += "Add Project";
    }else{
        formString += "Edit Project";
    }
    formString += "</h1></td></tr>";

    // Add error panel
    if(formDict["errors"]){
        formString += "<tr><td colspan='3'>" + getErrorPanel(formDict["errors"]) + "</td></tr>";
    }

    // Add main inputs & picture
    formString += "<tr>" + mainLabelsColumn + mainInputsColumn + pictureColumn + "</tr>"

    // Add spacing below main inputs to make up for picture being longer than detail list
    formString += "<tr><td style='height: 50px;'></td></tr>";

    // Other inputs
    formString += "<tr>" + otherLabelsColumn + otherInputsColumn + "</tr></form>"

    // Add buttons
    formString += "<tr><td colspan='3' style='width: 90%; position:relative; height: 70px;'><div style='margin-left: 100px;'><div class='whiteButton blackHover' style='position:absolute; left: 1%; top: 0; right: 50.5%;' onclick='" + formDict["cancelButton"]["onclick"] + "'> Cancel </div><div class='whiteButton blackHover' style='position:absolute; right: -1%; top: 0; left: 50.5%; ' onclick='" + formDict["createButton"].onclickFunction + "(" + '"' + formName + '");' + "'>"
    if(formDict["newPost"]){
        formString += "Create";
    }else{
        formString += "Update"
    }
    formString += "</div></div></td></tr>";
    return formString;
}

function getPostPicturePanel(panelName, pictureURL, editOnclick, pictureName, hiddenPictureInput, hiddenPictureInputName){
    var container = document.getElementById("editPostPanel")
    var pictureSizeInfo = resizePicture("expand");
    if(container != null){
        if(container.offsetWidth <= 628){
            pictureSizeInfo = resizePicture("shrink")
        }
    }
    return '<td class="formPicturePanelColumn" style="position: relative; min-width: ' + pictureSizeInfo.columnMinWidth + ';"><div style="position:absolute; width: ' + pictureSizeInfo.container.width + '; top: 0;"><div id="' + panelName + '" class="postPictureContainer" style="background: #000; margin-left: 10px; margin-top: 47px; height: ' + pictureSizeInfo.container.height + '; width: ' + pictureSizeInfo.container.width + ';"><img id="' + pictureName + '" src="' + pictureURL + '" style="max-width:100%; max-height:100%;"/></div><div class="formEditPictureButtonContainer" style="width: ' + pictureSizeInfo.container.width + ';"><a id="' + panelName + 'EditButton" onclick="' + editOnclick + '">Edit</a></div><div id="' + hiddenPictureInputName + '" style="display: none;">' + hiddenPictureInput + '</div></div></td>';
}

var formDividerLineScale = 0.93;
function getFormDividerLine(){
    var container = document.getElementById("editPostPanel")
    var width = "380%";
    if(container != null){
        width = container.offsetWidth * formDividerLineScale + "px";
    }
    return "<div class='formLabelDividingLine' style='position: absolute; width:" + width + "; border: 1px solid #7c7b7b; height: 0px; bottom: 0; margin-bottom: 15px; margin-left: 0px;'></div>"
}

function createBrowseTableElement(elementDict, titleFieldName, elementType){
    var elementString = "<div id='browseTablePost_" + elementDict["post"]["postID"]["value"] + "' class='projectContentListElement'>";
    if("addNewPanel" in elementDict){
        elementString += "Add new";
    }else{
        elementString += "<table style='width: 100%;'><tr>";

        // add status bar
        elementString += "<td colspan=2>"
        var status = elementDict["post"]["status"]["value"]
        elementString += "<div style='position: relative; margin-left: -5px; margin-right: -5px; margin-top: -5px; height: 35px; border: 1px solid #000;";
        if(status === "Open" || status === "Hiring"){
            // green
            elementString += "background: rgba(7, 196, 23, 0.2);";
        }else if(status === "Opening soon"){
            // darker green
            elementString += "background: #87bf9a";
        }else if(status === "Cast" || status === "Filled"){
            // grey
            elementString += "background: #d1d1d1;";
        }else{
            // red
            elementString += "rgba(214, 0, 0, 0.2);"
        }
        elementString += "'><div style='position: absolute; left: 0; margin-top: 0px; margin-left: 5px;'><h2><a onclick='redirectToPost(" + '"' + elementDict["post"]["postID"]["value"] + '");' + "'>" + elementDict["post"][titleFieldName]["value"] + "</a></h2></div><div style='position: absolute; right: 5px; margin-top: 7px;'>" + status + "</div></div></td></tr><tr>";

        // add picture column
        elementString += "<td style='width: 50%; '><img src='" + elementDict["post"]["postPicture"]["value"] + "' style='height: 166px; margin-left: -5px; margin-top: -5px; '></td>";

        // add element data
        elementString += "<td style='width: 50%;'><div style='width: 100%; text-align: left;'><div style='position: relative; height: 165px;'><ul style='position: absolute; top: 0; right: 0; height: 180px; width: 100%;'>";
        for(var field in elementDict["post"]){
            var value = elementDict["post"][field]["value"];
            if(!elementDict["post"][field]["hidden"] && field != "postPicture" && field != titleFieldName){
                elementString += "<li>"
                if(field === "characterName"){
                    elementString += "<h2><a onclick='redirectToPost(" + '"' + elementDict["post"]["postID"]["value"] + '");' + "'>" + value + "</a></h2>";
                }else{
                    elementString += "<div style='font-size: 0.9em'>" + value + "</div>";
                }
                elementString += "</li>";
            }
        }
        elementString += "</ul>";

        // add edit button
        elementString += "<div class='addNewPostButton' id='editPostButton_" + elementDict["post"]["postID"]["value"] + "' style='position:absolute; right: 0; bottom: 7%; text-align: center; width: 35px; height: 20px; font-size: 0.9em; font-weight: 500; padding-top: 1px;' onclick='toggleExpandExistingForm(" + '"expand", "' + elementType + '", "' + elementDict["post"]["postID"]["value"] + '");' + "'>Edit</div>";

        elementString += "</div></div></td>";

        elementString += "</tr></table>"
    }
    elementString += "</div>";

    // Add hidden cover
    elementString += "<div id='postPanelBorderCover_" + elementDict["post"]["postID"]["value"] + "' style='position: relative; visibility: hidden;'><div style='position: absolute; top: 0; margin-top: -3px; background: #FFF; height: 9px; width: 98.8%; z-index: 2; border-left: 2px solid #000; border-right: 2px solid #000;'></div></div>"
    return elementString;
}

var tableColCount = 3;
function createBrowseTable(tableType, tableEntries, sectionOrder, displayAddNewPanel, titleFieldName){
    tableColCount = getBrowseTableNumColumnsFromWindowSize()
    var tableString = "<div id='browseTableContainer'><table id='browseTable' style='width: '" + tableColCount * browseElementWidth + "px'>"

    // Format data in section order
    var data = [];
    /*if(displayAddNewPanel){
        data.push({"addNewPanel": true});
    }*/
    if(sectionOrder != null){
        for(var i=0; i < sectionOrder.length; i++){
            var section = sectionOrder[i];
            if(tableEntries[section] != null){
                for(var j=0; j < tableEntries[section].length; j++){
                    data.push(tableEntries[section][j])
                }
            }
        }
    }else{
        console.log("Error: no section order passed to create browse table")
    }

    var desiredColCount = getBrowseTableNumColumnsFromWindowSize()
    var colCount = 0;
    var rowCount = 0;
    for(var i=0; i < data.length; i++){
        if(colCount === 0){
            tableString += "<tr id='browseTableRow_" + rowCount + "'>";
        }
        tableString += "<td style='width: 300px;'>" + createBrowseTableElement(data[i], titleFieldName, tableType) + "</td>";

        colCount += 1;
        if(colCount === tableColCount){
            tableString += "</tr>";
            colCount = 0;
            rowCount += 1;
        }
    }
    return tableString;
}

function resizePicture(resizeType){
    //Reduce picture size
    var container = {"width": "270px", "height": "298px"}
    var columnMinWidth = "270px";
    if(resizeType === "shrink"){
        container = {"width": "203px", "height": "226px"};
        columnMinWidth = "200px"
    }
    var pictureContainers = document.getElementsByClassName("postPictureContainer")
    for(var i=0; i < pictureContainers.length; i++){
        pictureContainers[i].style.width = container.width;
        pictureContainers[i].style.height = container.height;
    }

    //Reduce picture column width to make text fields larger
    var pictureColumns = document.getElementsByClassName("formPicturePanelColumn")
    for(var i=0; i < pictureColumns.length; i++){
        pictureColumns[i].style.minWidth = columnMinWidth;
    }

    // Move edit picture button to be recentred
    var editButtons = document.getElementsByClassName("formEditPictureButtonContainer");
    for(var i=0; i< editButtons.length; i++){
        editButtons[i].style.width = container.width;
    }
    return {"container": container, "columnMinWidth": columnMinWidth}
}

function resizeBrowseTable(changeCallback){
    numColumns = getBrowseTableNumColumnsFromWindowSize()
    if(tableColCount != numColumns){
        tableColCount = numColumns
        mainViewPanel = document.getElementById("mainViewPanel")
        var newPanelSizeInfo = getPanelInfoFromNumColumns(tableColCount)
        if(mainViewPanel != null){
            mainViewPanel.style.width = newPanelSizeInfo["mainViewPanelWidth"]
        }
        if(tableColCount === 1){
            document.getElementById("jobsButton").style.marginLeft = "2px";
        }else{
            document.getElementById("jobsButton").style.marginLeft = "0px";
        }
        document.getElementById("browseTableContainer").style.width = tableColCount * browseElementWidth + "px";

        // Change width of form divider lines
        var newLineWidth = newPanelSizeInfo["formLineWidth"];
        var formContainer = document.getElementById("editPostPanel")
        if(formContainer != null){
            newLineWidth = formContainer.offsetWidth * formDividerLineScale + "px";
        }
        var formLines = document.getElementsByClassName("formLabelDividingLine");
        for(var i=0; i < formLines.length; i++){
            formLines[i].style.width = newLineWidth;
        }

        if(tableColCount === 2){
            resizePicture("shrink");
        }else{
            resizePicture("expand");
        }

        changeCallback();
    }
}

function getPanelInfoFromNumColumns(numColumns){
    var base = numColumns * browseElementWidth;
    var formLineWidth;
    if(numColumns === 2){
        base += 28;
        formLineWidth = "340%";
    }else if(numColumns === 3){
        base += 37;
        formLineWidth = "380%";
    }else if(numColumns === 4){
        base += 45; 
        formLineWidth = "360%";
    }else if(numColumns === 5){
        base += 52;
        formLineWidth = "360%";
    }else{
        base += 60;
        formLineWidth = "360%";
    }
    base += "px";

    return {"mainViewPanelWidth": base, "formLineWidth": formLineWidth}
}

var browseElementWidth = 300;
function getBrowseTableNumColumnsFromWindowSize(){
    numColumns = Math.max(Math.round($(window).width() / browseElementWidth), 2);
    return numColumns
}


