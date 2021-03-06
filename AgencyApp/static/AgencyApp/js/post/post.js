function addSelectProjectForm(postID, username){

}

function removePicture(isProject){
    addPopupPictureToBaseForm(null, null, isProject)
    toggleEditPicturePopup("hide", isProject, null);
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
            contentBox.style.display = "inline";
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
    if(tempPictureID != null){
        baseFormPictureInput.innerHTML = "<input type='hidden' name='tempPostPictureID' value='" + tempPictureID + "'>";
    }else{
        baseFormPictureInput.innerHTML = "<input type='hidden' name='tempPostPictureID' value=''><input type='hidden' name='removePostPicture' value='true'>";
        tempPictureURL = defaultPictureURL;
    }

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

var defaultPictureURL;
function setDefaultPicture(pictureURL){
    defaultPictureURL = pictureURL;
}

function submitPictureForm(pictureID, formName, isProject){
        // If button was pressed with no input changed, just close the window
        var editPictureInput = document.getElementById(pictureID + "Image");
        if(editPictureInput != null){
            if(!pictureExistsMap[pictureID]){
                toggleEditPicturePopup("hide")
                return;
            }
        }

        var updateButton = document.getElementById("updatePictureButton")
        var updateButtonHTML = updateButton.innerHTML;
        updateButton.innerHTML = "<img id='" + pictureID + "LoadingGif' src='" + buttonLoadingGifURL + "' style='position: absolute; height: 60px; width: 60px; margin-top: -15px;'>"

        var form = addCropToPictureForm(formName, pictureID, pictureID + "CropInfoInputs")
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

var formPictureMarginInfo = "margin-left: 10px; margin-top: 65px;";
function addCreateCastingPost(formDict, formURL, formName, isProjectSubForm){
    var formString = "<form method='post' action='" + formURL + "' id='" + formName + "' class='form-style-1' style='width: 90%; background: none; margin-left: 3.2%;' enctype='multipart/form-data'>";
    formString += "<table style='width: 100%;'><tr>"

    // Fill post picture string
    var pictureField = formDict["postPicture"];
    var pictureColumn =  getPostPicturePanel("td", "postPicturePanel", pictureField.value, pictureField.editOnclick, "postPictureImg", true, pictureField.input, "mainPostPictureInput", formPictureMarginInfo);

    var postID = formDict["postID"].value

    // Fill text content
    var sectionMap = {"Details": ["project", "title", "status", "startDate", "endDate", "location", "hoursPerWeek", "compensationType"],
                      "Character": ["characterName", "characterType", "gender", "ageRange", "description", "skills", "languages"],
                      "Users": ["participants"],
                      "Physical": ["height", "build", "hairColor", "eyeColor", "ethnicity"],
                      "hidden": ["csrf_token", "postID", "source", "next", "destination", "projectID", "poster", "postType"]}
    var mainLabelsColumn = "<td class='editPostLabelPanel' style='width: 20%; position:relative; line-height: 38.2px;'><ul style='margin-bottom: -14px; margin-top: -40px;'>";
    var mainInputsColumn = "<td class='editPostInputPanel' style='width: 50%; position: relative; line-height: 39px;'><ul style='margin-top: -2px; '>";
    var otherLabelsColumn = "<td class='editPostLabelPanel' style='width: 30%; min-width: 170px; height: 600px; position:relative;'><ul style='margin-top: 5px;'>";
    var otherInputsColumn = "<td class='editPostInputPanel' colspan='2' style='width: 70%;'><div style='margin-top: 10px;'><ul>";
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
            if(sectionTitle === "Details"){
                sectionInputTableElement += "<div style='height: 60px;'></div>";
            }else if(sectionTitle === "Character"){
                sectionLabelTableElement += "<div style='height: 28px;'></div>";
                sectionInputTableElement += "<div style='height: 68px;'></div>";
            }else if(sectionTitle === "Users"){
                sectionLabelTableElement += "<div style='height: 10px;'></div>";
                sectionInputTableElement += "<div style='height: 80px;'></div>";
            }else if(sectionTitle === "Physical"){
                sectionLabelTableElement += "<div style='height: 0px;'></div>";
                sectionInputTableElement += "<div style='height: 75px;'></div>"
            }
            sectionLabelTableElement += "<div style='position: relative; height: 30px; margin-top: 40px; width: 100%;'> <h2 class='" + sectionClass + "' style='position: absolute; bottom: 0; z-index: 1; right: 0; margin-left: 80px; '><div style='margin-top: -10px;'>" + sectionTitle + "</div></h2>" + getFormDividerLine() + "</div></div>"

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
                        sectionInputTableElement += "<li style='margin-top: 0px;'><a  onclick='redirectToPost(" + '"' + field.projectID + '"' + ");'>" + field.title + "</a></li>";
                    }else{
                        sectionInputTableElement += "<li style='margin-top: 4px; height: 36px;'>None - <a onclick='" + field.addNewOnclick + "'>Add</a></li>";
                    }
                    continue;
                }else if(fieldName === "participants"){
                    var participants = formDict["participants"]

                    // Add participants panel
                    var userTableString = '';
                    var containerHeight = participantPanelBaseHeight;
                    if(participants != null){
                        var participantTableInfo = getPostParticipantTable(postID, "casting", participants, formName, isProjectSubForm, formDict["participationSelectFields"]);
                        containerHeight += participantTableInfo["tableHeight"];
                        userTableString += "<div id='castingParticipantTableContainer' style='position: relative; height: " + participantTableInfo["tableHeight"] + "px;'>" + participantTableInfo["html"] + "</div>"
                        sectionLabelTableElement += "<div id='castingParticipantLabelContainer' style='height: " + (participantTableInfo["tableHeight"] - 5) +  "px;'></div>";
                    }

                    // Add label
                    sectionLabelTableElement += "<label for='name'>Add new</label><br>";
                    sectionInputTableElement += "<div id='castingParticipantPanel' style='height: " + containerHeight + "px;'>" + userTableString + getPostParticipantForm(postID, "casting", formName, true, formDict["newPost"], formDict["participationSelectFields"], "Interested") + "</div>";
                    continue;
                }
                if(!field.hidden || field.name === "status"){
                    if(field.numRows > 1){
                        // stupid hack I hate myself right now
                        sectionLabelTableElement += "<li style='height:" + '' + field.numRows*5.95 + 'px;' + "'><label for='name'>" + field.label + "</label></li>";
                        // TODO replace newlines in description as it will break js
                        sectionInputTableElement += "<li><textarea rows='" + field.numRows + "' name='" + field.name + "' form='" + formName + "' style='height:100px; width: 97.7%; resize: none;' placeholder='" + field.placeholder + "'>" + field.value + "</textarea></li>";
                    }else{
                        sectionLabelTableElement += "<label for='name'>" + field.label + "</label><br>";
                        sectionInputTableElement += "<li id='" + field.name + "ContainerRow' ";
                        if(field.options){
                            sectionInputTableElement += 'style="height: 36px; margin-top: 1px;margin-bottom: 2px;">';
                            var selectForm = createSelectForm(formName, field.name + "SelectBar", field.options, field.value);
                            sectionInputTableElement += selectForm;
                            sectionInputTableElement += "<input type='hidden' name='" + field.name + "' id='" + field.name + "SelectInput' >";
                        }else{
                            sectionInputTableElement += 'style="">' + field.input;
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


function addCreateWorkPost(formDict, formURL, formName, isProjectSubForm){
    var formString = "<form method='post' action='" + formURL + "' id='" + formName + "' class='form-style-1' style='width: 90%; background: none; margin-left: 3.2%;' enctype='multipart/form-data'>";
    formString += "<table style='width: 100%;'><tr>"

    // Fill post picture string
    var pictureField = formDict["postPicture"];
    var pictureColumn = getPostPicturePanel("td", "postPicturePanel", pictureField.value, pictureField.editOnclick, "postPictureImg", true, pictureField.input, "mainPostPictureInput", formPictureMarginInfo);

    var postID = formDict["postID"].value

    // Fill text content
    var sectionMap = {"Details": ["project", "title", "profession", "status", "startDate", "endDate", "hoursPerWeek", "compensationType"],
                      "Position": ["description", "location", "skills"],
                      "Users": ["participants"],
                      "Equipment": ["workerNeedsEquipment", "equipmentDescription"],
                      "hidden": ["csrf_token", "postID", "source", "next", "destination", "projectID", "poster"]}
    var mainLabelsColumn = "<td class='editPostLabelPanel' style='width: 20%; position:relative; line-height: 38.2px;'><ul style='margin-bottom: -14px; margin-top: -60px;'>";
    var mainInputsColumn = "<td class='editPostInputPanel' style='width: 50%; position: relative; line-height: 39px;'><ul style='margin-top: 5px; '>";
    var otherLabelsColumn = "<td class='editPostLabelPanel' style='width: 30%; min-width: 170px; position:relative;'><ul style='margin-top: 5px;'>";
    var otherInputsColumn = "<td class='editPostInputPanel' colspan='2' style='width: 70%; vertical-align: top;'><div style='margin-top: 25px;'><ul>";
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
            if(sectionTitle === "Details"){
                sectionInputTableElement += "<div style='height: 58px;'></div>";
            }else if(sectionTitle === "Position"){
                sectionLabelTableElement += "<div style='height: 0px;'></div>";
                sectionInputTableElement += "<div style='height: 55px;'></div>";
            }else if(sectionTitle === "Users"){
                sectionLabelTableElement += "<div style='height: 0px;'></div>";
                sectionInputTableElement += "<div style='height: 80px;'></div>";
            }else if(sectionTitle === "Equipment"){
                sectionLabelTableElement += "<div style='height: 0px;'></div>";
                sectionInputTableElement += "<div style='height: 85px;'></div>"
            }
            sectionLabelTableElement += "<div style='position: relative; margin-top: 40px; height: 40px; width: 100%;'> <h2 class='" + sectionClass + "' style='position: absolute; z-index: 1; right: 0; margin-left: 80px;'><div style='margin-top: -17px;'>" + sectionTitle + "</div></h2>" + getFormDividerLine() + "</div></div>"

            for(i in fieldList){
                var fieldName = sectionMap[sectionTitle][i];
                var field = formDict[fieldName];

                // Add project
                if(fieldName === "project"){
                    sectionLabelTableElement += "<label for='name'>Project</label><br>";
                    if(field.title != null){
                        sectionInputTableElement += "<li style='margin-top: 6px;'><a  onclick='redirectToPost(" + '"' + field.projectID + '"' + ");'>" + field.title + "</a></li>";
                    }else{
                        sectionInputTableElement += "<li style='margin-top: -4px; height: 30px;'>None - <a onclick='" + field.addNewOnclick + "'>Add</a></li>";
                    }
                    continue;
                }else if(fieldName === "participants"){
                    var participants = formDict["participants"]

                    // Add participants panel
                    var userTableString = '';
                    var containerHeight = participantPanelBaseHeight;
                    if(participants != null){
                        var participantTableInfo = getPostParticipantTable(postID, "jobs", participants, formName, isProjectSubForm, formDict["participationSelectFields"]);
                        containerHeight += participantTableInfo["tableHeight"];
                        userTableString += "<div id='jobsParticipantTableContainer' style='position: relative; height: " + participantTableInfo["tableHeight"] + "px;'>" + participantTableInfo["html"] + "</div>"
                        sectionLabelTableElement += "<div id='jobsParticipantLabelContainer' style='height: " + (participantTableInfo["tableHeight"] - 5) +  "px;'></div>";
                    }

                    // Add label
                    sectionLabelTableElement += "<label for='name'>Add new</label><br>";
                    sectionInputTableElement += "<div id='jobsParticipantPanel' style='height: " + containerHeight + "px;'>" + userTableString + getPostParticipantForm(postID, "jobs", formName, true, formDict["newPost"], formDict["participationSelectFields"], "Interested") + "</div>";
                    continue;
                }
                if(!field.hidden || field.name === "status"){
                    if(field.numRows > 1){
                        // stupid hack I hate myself right now
                        sectionLabelTableElement += "<li style='height:" + '' + field.numRows*6 + 'px;' + "'><label for='name'>" + field.label + "</label></li>";
                        // TODO replace newlines in description as it will break js
                        sectionInputTableElement += "<li><textarea rows='" + field.numRows + "' name='" + field.name + "' form='" + formName + "' style='height:100px; width: 97.7%; resize: none;' placeholder='" + field.placeholder + "'>" + field.value + "</textarea></li>";
                    }else{
                        sectionLabelTableElement += "<label for='name'>" + field.label + "</label><br>";

                        sectionInputTableElement += "<li id='" + field.name + "ContainerRow' ";
                        if(field.options){
                            sectionInputTableElement += 'style="height: 36px; margin-top: -1px; margin-bottom: 5px;">';
                            var selectForm = createSelectForm(formName, field.name + "SelectBar", field.options, field.value);
                            sectionInputTableElement += selectForm;
                            sectionInputTableElement += "<input type='hidden' name='" + field.name + "' id='" + field.name + "SelectInput' >";
                        }else{
                            sectionInputTableElement += 'style="">' + field.input;
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
    formString += "<tr id='formErrorRow'>";
    if(formDict["errors"]){
        formString += "<td colspan='3'>" + getErrorPanel(formDict["errors"]) + "</td>";
    }
    formString += "</tr>";

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

function addCreateEventPost(formDict, formURL, formName, isProjectSubForm){
    var formString = "<form method='post' action='" + formURL + "' id='" + formName + "' class='form-style-1' style='width: 90%; background: none; margin-left: 3.2%;' enctype='multipart/form-data'>";
    formString += "<table style='width: 100%;'><tr>"

    // Fill post picture string
    var pictureField = formDict["postPicture"];
    var pictureColumn = getPostPicturePanel("td", "postPicturePanel", pictureField.value, pictureField.editOnclick, "postPictureImg", true, pictureField.input, "mainPostPictureInput", formPictureMarginInfo);

    // Fill text content
    var sectionMap = {"Details": ["title", "project", "eventType", "host","location", "startDate", "startTime", "endDate", "endTime"],
                      "The Event": ["admissionInfo", "description"],
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
                }
                if(field != null){
                    if(!field.hidden){
                        if(field.numRows > 1){
                            // stupid hack I hate myself right now
                            sectionLabelTableElement += "<li style='height:" + '' + field.numRows*5.9 + 'px;' + "'><label for='name'>" + field.label + "</label></li>";
                            // TODO replace newlines in description as it will break js
                            sectionInputTableElement += "<li><textarea rows='" + field.numRows + "' name='" + field.name + "' form='" + formName + "' style='height:100px; width: 97.7%; resize: none;' placeholder='" + field.placeholder + "'>" + field.value + "</textarea></li>";
                        }else{
                            sectionLabelTableElement += "<label for='name'>" + field.label + "</label><br>";
                            sectionInputTableElement += "<li id='" + field.name + "ContainerRow'>";
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
        formString += "Add Event";
    }else{
        formString += "Edit Event";
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
    formString += "<tr><td colspan='3' style='width: 90%; position:relative; height: 70px;'><div style='margin-left: 100px;'><div class='whiteButton blackHover' style='position:absolute; left: 1%; top: 0; right: 50.5%;' onclick='" + formDict["cancelButton"]["onclick"] + "'> Cancel </div><div class='whiteButton blackHover' style='position:absolute; right: -1%; top: 0; left: 50.5%; ' onclick='" + formDict["createButton"].onclickFunction + "(" + '"' + formName  + '", ' + !formDict["newPost"] + ');' + "'>"
    if(formDict["newPost"]){
        formString += "Create Event";
    }else{
        formString += "Update Event"
    }
    formString += "</div></div></td></tr>";
    return formString;
}


function addCreateProjectPost(formDict, formURL, formName){
    var formString = "<form method='post' action='" + formURL + "' id='" + formName + "' class='form-style-1' style='width: 90%; background: none; margin-left: 3.2%;' enctype='multipart/form-data'>";
    formString += "<table style='width: 100%;'><tr>"

    // Fill post picture string
    var pictureField = formDict["postPicture"];
    var pictureColumn = getPostPicturePanel("td", "projectPicturePanel", pictureField.value, pictureField.editOnclick, "projectPictureImg", true, pictureField.input, "mainProjectPictureInput", formPictureMarginInfo);

    var postID = formDict["postID"].value

    // Fill text content
    var sectionMap = {"Details": ["title", "status", "companyName", "union", "startDate", "endDate", "compensation"],
                      "Production": ["projectType", "location", "description", "productionNotes"],
                      "Admins": ["participants"],
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
                if(fieldName === "participants"){
                    var participants = formDict["participants"]

                    // Add participants panel
                    var userTableString = '';
                    var containerHeight = participantPanelBaseHeight;
                    if(participants != null){
                        var participantTableInfo = getPostParticipantTable(postID, "project", participants, formName, false, formDict["participationSelectFields"]);
                        containerHeight += participantTableInfo["tableHeight"];
                        userTableString += "<div id='projectParticipantTableContainer' style='position: relative; height: " + participantTableInfo["tableHeight"] + "px;'>" + participantTableInfo["html"] + "</div>"
                        sectionLabelTableElement += "<div id='projectParticipantLabelContainer' style='height: " + (participantTableInfo["tableHeight"] - 5) +  "px;'></div>";
                    }

                    // Add label
                    sectionLabelTableElement += "<label for='name'>Add new</label><br>";
                    sectionInputTableElement += "<div id='projectParticipantPanel' style='height: " + containerHeight + "px;'>" + userTableString + getPostParticipantForm(postID, "project", formName, true, formDict["newPost"], formDict["participationSelectFields"], "Producer") + "</div>";
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
                        sectionInputTableElement += "<li id='" + field.name + "ContainerRow'>";
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

function getPostPicturePanel(parentTagType, panelName, pictureURL, editOnclick, pictureName, allowEdit, hiddenPictureInput, hiddenPictureInputName, pictureContainerMarginData, imageAlignValue){
    var postString = '';
    var container = document.getElementById("editPostPanel")
    var pictureSizeInfo = resizePicture("expand");
    if(container != null){
        if(container.offsetWidth <= 628){
            pictureSizeInfo = resizePicture("shrink")
        }
    }

    if(pictureContainerMarginData == null){
        pictureContainerMarginData = '';
    }

    postString += '<' + parentTagType + ' class="postPictureContainer" style="position: relative; height: ' + pictureSizeInfo.container.height + '; min-width: ' + pictureSizeInfo.columnMinWidth + ';"><div style="position:absolute; width: ' + pictureSizeInfo.container.width + '; top: 0;"><div id="' + panelName + '" class="postPictureContainer" style="height: ' + pictureSizeInfo.container.height + '; width: ' + pictureSizeInfo.container.width + '; ' + pictureContainerMarginData + '"><img id="' + pictureName + '" src="' + pictureURL + '" style="max-width:100%; max-height:100%; border: 1px solid #000;"'
    if(imageAlignValue){
        postString += "align='" + imageAlignValue + "' ";
    }
    postString += '/></div>';

    if(allowEdit){
        postString += '<div class="formEditPictureButtonContainer" style="width: ' + pictureSizeInfo.container.width + ';"><a id="' + panelName + 'EditButton" onclick="' + editOnclick + '">Edit</a></div><div id="' + hiddenPictureInputName + '" style="display: none;">' + hiddenPictureInput + '</div>';
    }
    postString += '</div></' + parentTagType + '>';
    return postString

}

var formDividerLineScale = 0.91;
function getFormDividerLine(){
    var container = document.getElementById("editPostPanel")
    var width = "380%";
    if(container != null){
        width = container.offsetWidth * formDividerLineScale + "px";
    }
    return "<div class='formLabelDividingLine' style='position: absolute; width:" + width + "; border: 1px solid #7c7b7b; height: 0px; bottom: 0; margin-bottom: 15px; margin-left: 0px;'></div>"
}

function createBrowseTableElement(elementDict, titleFieldName, elementType, allowEdit){
    var elementString = "<div id='browseTablePost_" + elementDict["post"]["postID"]["value"] + "' class='projectContentListElement'>";
    if("addNewPanel" in elementDict){
        elementString += "Add new";
    }else{
        elementString += "<table style='width: 100%;'><tr>";

        // add status bar
        elementString += "<td colspan=2>"
        var status = elementDict["post"]["status"]["value"]
        elementString += "<div style='position: relative; margin-left: -5px; margin-right: -5px; margin-top: -5px; height: 35px; border: 1px solid #000;";
        if(status === "Open" || status === "Hiring" || status === "Today" || status === "Happening Now"){
            // green
            elementString += "background: rgba(7, 196, 23, 0.2);";
        }else if(status === "Opening soon" || status === "Upcoming"){
            // darker green
            elementString += "background: #87bf9a";
        }else if(status === "Cast" || status === "Filled" || status === "Past"){
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
        if(allowEdit){
            elementString += "<div class='addNewPostButton' id='editPostButton_" + elementDict["post"]["postID"]["value"] + "' style='position:absolute; right: 0; bottom: 7%; text-align: center; width: 35px; height: 20px; font-size: 0.9em; font-weight: 500; padding-top: 1px;' onclick='toggleExpandExistingForm(" + '"expand", "' + elementType + '", "' + elementDict["post"]["postID"]["value"] + '");' + "'>Edit</div>";
        }

        elementString += "</div></div></td>";

        elementString += "</tr></table>"
    }
    elementString += "</div>";

    // Add hidden cover
    elementString += "<div id='postPanelBorderCover_" + elementDict["post"]["postID"]["value"] + "' style='position: relative; visibility: hidden;'><div style='position: absolute; top: 0; margin-top: -3px; background: #FFF; height: 9px; width: 98.8%; z-index: 2; border-left: 2px solid #000; border-right: 2px solid #000;'></div></div>"
    return elementString;
}

var tableColCount = 3;
function createBrowseTable(tableType, tableEntries, sectionOrder, displayAddNewPanel, titleFieldName, allowEdit){
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

    // If there are less entries than can fill a single row, add hidden/blank panels of same size to fill the space
    var iterateLength = data.length;
    var addHiddenPanels = false;
    if(data.length < tableColCount){
        addHiddenPanels = true;
        iterateLength = tableColCount;
    }

    var desiredColCount = getBrowseTableNumColumnsFromWindowSize()
    var colCount = 0;
    var rowCount = 0;
    for(var i=0; i < iterateLength; i++){
        if(colCount === 0){
            tableString += "<tr id='browseTableRow_" + rowCount + "'>";
        }
        if(addHiddenPanels && data[i] == null){
            // Add a blank panel to fill out the row
            tableString += "<td style='width: 300px;'><div style='width: 304px;'></div></td>";
        }else{
            tableString += "<td style='width: 300px;'>" + createBrowseTableElement(data[i], titleFieldName, tableType, allowEdit) + "</td>";
        }

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
    var container = {"width": "268px", "height": "298px"}
    var columnMinWidth = "268px";
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
    var formLineWidth = 360;
    if(numColumns === 2){
        base += 28;
        formLineWidth = 340;
    }else if(numColumns === 3){
        base += 37;
        formLineWidth = 380;
    }else if(numColumns === 4){
        base += 45;
        formLineWidth = 360;
    }else if(numColumns === 5){
        base += 52;
        formLineWidth = 360;
    }else{
        base += 60;
        formLineWidth = 360;
    }
    base += "px";
    formLineWidth += "%";

    return {"mainViewPanelWidth": base, "formLineWidth": formLineWidth}
}

var browseElementWidth = 300;
function getBrowseTableNumColumnsFromWindowSize(){
    // Set size between 2 and 3 columns for now
    numColumns = Math.min(Math.max(Math.floor($(window).width() / browseElementWidth), 2), 3);
    return numColumns
}

function getEventStatus(date1, date2){
    var eventStatus;
    if(date1 != null && date2 != null){
        var first;
        var second;
        if(date1 < date2){
            first = date1;
            second = date2;
        }else{
            first = date2;
            second = date1
        }
        if(first > currentDate){
            eventStatus = "Upcoming";
        }else if(first <= currentDate){
            if(second > currentDate){
                eventStatus = "Happening Now";
            }else if(second.toISOString().slice(0,10)  === first.toISOString().slice(0,10)){
                eventStatus = "Today";
            }else{
                eventStatus = "Past";
            }
        }else if(first === currentDate || first.toISOString().slice(0,10) === currentDateString){
            eventStatus = "Today";
        }else{
            eventStatus = "Past";
        }
    }
    return eventStatus
}

function getDateString(date1, date2){
    var dateString;
    if(date1 != null && date2 != null){
        var first;
        var second;
        if(date1 < date2){
            first = date1;
            second = date2;
        }else{
            first = date2;
            second = date1
        }
        var firstString = first.toUTCString();
        var secondString = second.toUTCString();
        if(first.getYear() === second.getYear()){
            if(first.getMonth() === second.getMonth()){
                if(first.getDay() === second.getDay()){
                    dateString = firstString.slice(0, 16);
                }else{
                    dateString = firstString.slice(8,11) + " " + firstString.slice(5,7) + " - " + secondString.slice(5,7) + ", " + second.getFullYear();
                }
            }else{
                dateString = firstString.slice(8, 11) + " " + firstString.slice(5,7) + " - " + secondString.slice(8, 11) + " " + secondString.slice(5,7) + ", " + second.getFullYear();
            }
        }else{
            dateString = firstString.slice(8, 11) + " " + firstString.slice(5,7) + ", " + first.getFullYear() + " - " + secondString.slice(8, 11) + " " + secondString.slice(5,7) + ", " + second.getFullYear();
        }
    }
    return dateString;
}

function getCompensationPanel(value, description){
    var panelString = "<div style='width:98%;'>"

    var tabList = [{"label": "Paid", "value": "Paid"},
                   {"label": "Negotiable", "value": "Negotiable"},
                   {"label": "Unpaid", "value": "Unpaid"}]
    for(var i=0; i < tabList.length; i++){
        if(tabList[i].value === value){
            tabList[i]["active"] = true;
        }else{
            tabList[i]["active"] = false;
        }
    }

    var expandInitially = false;
    compensationPanelExpanded = false
    if(value != null && value.length > 0 && value != "None"){
        compensationType = value;
        expandInitially = true;
    }
    var activeOnclickCallback = "expandCompensationPanel";
    panelString += createMultiTabOption(tabList, "compensationPanelTabs", expandInitially, description, activeOnclickCallback);
    panelString += "</div><div style='display: none;'><input type='text' name='compensationType' id='compensationTypeInput'/></div>";
    return panelString
}

function createMultiTabOption(tabList, panelID, expandInitially, textFieldValue, activeOnclickCallback){
    var panelHeight = 32;       // height of tab input panel
    var dropdownVisibilityStyle = "visibility: hidden; height: 13px; "      // style for dropdown
    var textFieldValueElement = "placeholder='Details...' ";        // default just has placeholder with no value
    if(expandInitially){
        panelHeight = 62;
        compensationPanelExpanded = true;
        dropdownVisibilityStyle = "visibility: visibile; height: 62px; "
        if(textFieldValue != null && textFieldValue.length > 0 && textFieldValue != "None"){
            textFieldValueElement += "value='" + textFieldValue + "' ";     // Add value to placeholder
        }
    }

    var tabs = "<div style='height: 32px;'><div class='formInput' id='" + panelID + "' style='width: 97.5%; margin-top: 6px; padding: 0px 9px; border-radius: 4px; height: " + panelHeight + "px;'>";
    if(tabList.length === 3){
        tabs += "<div style='position: relative; height: 33px; margin: 0px -9px; margin-top: -1px; '>";

        // left
        tabs += "<div class='editCompensationPanelButton";
        if(tabList[0].active){
            tabs += 'Active';
        }
        tabs += "' id='optionTab_" + tabList[0].value + "' style='position: absolute; left: 0; width: 33%; height: 32px;' onclick='changeMultiTabOptionClasses(" + '"' + tabList[0].value + '", "' + panelID + '", "' + activeOnclickCallback + '"' + ");'><div style='margin-top: -4px;'>" + tabList[0].label + '</div></div>';

        // middle
        tabs += "<div class='editCompensationPanelButton";
        if(tabList[1].active){
            tabs += 'Active';
        }
        tabs += "' id='optionTab_" + tabList[1].value + "' style='position: absolute; left: 33.3%; width: 33%; height: 32px;' onclick='changeMultiTabOptionClasses(" + '"' + tabList[1].value + '", "' + panelID + '", "' + activeOnclickCallback + '"' + ");'><div style='margin-top: -4px;'>" + tabList[1].label + '</div></div>';

        // right
        tabs += "<div class='editCompensationPanelButton";
        if(tabList[2].active){
            tabs += 'Active';
        }
        tabs += "' id='optionTab_" + tabList[2].value + "' style='position: absolute; right: 0; width: 33%; height: 32px; margin-right: -1px;' onclick='changeMultiTabOptionClasses(" + '"' + tabList[2].value + '", "' + panelID + '", "' + activeOnclickCallback + '"' + ");'><div style='margin-top: -4px;'>" + tabList[2].label + '</div></div>';

        // Text box below
        tabs += createDropdownTextBox(panelID, dropdownVisibilityStyle, textFieldValueElement, false)

        tabs += "</div>";
    }
    tabs += "</div></div>";
    return tabs;
}

function createDropdownTextBox(panelID, visibilityString, textValueString, addBorder){
    var textPanel = "<div id='" + panelID + "DropdownPanel' style='position: absolute; top: 14px; left: 0; right: 0; border-radius: 3px; margin-left: -2px; margin-right: -2px; " + visibilityString + "overflow: hidden; "
    if(addBorder){
        textPanel += "height: 10px; margin-right: -8px; margin-left: 0px; top: 15px;";
    }else{
        textPanel += "border: none; ";
    }

    textPanel += "' class='formInput'><input class='noFormInputFormatting' type='text' name='compensationDescription' id='compensationDescription' " + textValueString + "style='position: absolute; left: 2px; border: none; margin: -7px 0px 0px 1px; padding: 0px 0px 0px 4px; height: 26px; width: 96%;' /> </div>";
    return textPanel;
}

function changeMultiTabOptionClasses(activePostType, panelID, activeOnclickCallback){
    if(compensationPanelWidthType != "expanded"){
        return;
    }
    if(panelID == null){
        panelID = "compensationPanelTabs";
    }

    if(activeOnclickCallback == null){
        activeOnclickCallback = "expandCompensationTable"
    }

    var tabsPanel = document.getElementById(panelID)
    var activeListItemID = "optionTab_" + activePostType;
    if(tabsPanel != null){
        var tabs = tabsPanel.getElementsByTagName("div");
        for(var i=0; i < tabs.length; i++){
            var tab = tabs[i];
            if(tab.id === activeListItemID){
                tab.className = "editCompensationPanelButtonActive";

                // Call the function name passed with the active id as a parameter
                window[activeOnclickCallback](activePostType);
            }else if(tab.id.startsWith("optionTab_")){
                tab.className = "editCompensationPanelButton"
            }
        }
    }
}

var compensationPanelExpanded = false
var compensationType = "Paid";
var compensationDescription;
function expandCompensationPanel(compType){
    var formInputBox = document.getElementById('compensationPanelTabs');
    if(formInputBox != null){
        compensationType = compType
        if(!compensationPanelExpanded){
            compensationPanelExpanded = true;
            $("#compensationPanelTabs").animate({marginTop: "6px", height: "62px"}, 150, function(){
                document.getElementById("compensationPanelTabsDropdownPanel").style.visibility = "visible";
            });
        }
    }
}

var compensationPanelWidthType;
function resizeCompensationPanel(){
    var panelWidthToggleValue = 280;
    var formInputBox = document.getElementById('compensationPanelTabs');
    var inputRow = document.getElementById('compensationTypeContainerRow');

    var compDescriptionValue;
    var descInput = document.getElementById("compensationDescription")
    if(descInput != null && descInput.value != ""){
        compensationDescription = descInput.value;
    }

    var direction;
    var updateRequired = false;
    var containerRowWidth = $("#compensationTypeContainerRow").width();
    if(compensationPanelWidthType == null){
        updateRequired = true;
        if(containerRowWidth < panelWidthToggleValue){
            direction = "shrink";
        }else{
            direction = "expand";
        }
    }else{
        if(compensationPanelWidthType === "expanded"){
            if(containerRowWidth < panelWidthToggleValue){
                direction = "shrink";
                updateRequired = true;
            }
        }else if(compensationPanelWidthType === "shrunk"){
            if(containerRowWidth >= panelWidthToggleValue){
                direction = "expand"
                updateRequired = true;
            }
        }
    }

    if(updateRequired && direction != null){
        if(direction === "shrink"){
            if(inputRow != null){
                compensationPanelWidthType = "shrunk";

                var selectForm = createSelectForm("blah", "compensationTypeSelectBar", ["Paid", "Negotiable", "Unpaid"], compensationType);

                // Add comp description value if is set
                var inputValueString = "placeholder='Details...' ";
                if(compensationDescription != null && compensationDescription.length > 0){
                    inputValueString += "value='" + compensationDescription + "' ";
                }

                inputRow.innerHTML = "<div id='compensationPanelShrunk' style='position: relative; width: 100%; min-height: 36px; margin-top: -8px;'><div style='position: absolute; left: 0; right: 0; '>" + selectForm + "</div>" + createDropdownTextBox("compensationPanelShrunk", "visibility: visible;", inputValueString, true) + "</div><div style='display: none;'><input type='text' name='compensationType' id='compensationTypeInput'/></div>";

                $("#compensationTypeSelectBar select").val(compensationType);
                // Add listener to update comp type when an option is clicked from the select menu
                $('#compensationTypeSelectBar').on('change', function () {
                    var compType = $(this).val(); // get selected value
                    if(compType != compensationType){
                        compensationType = compType;
                    }
                });
            }
        }else if(direction === "expand"){
            if($("#compensationTypeContainerRow").width() >= panelWidthToggleValue){
                compensationPanelWidthType = "expanded";
                if(inputRow != null){
                    inputRow.innerHTML = getCompensationPanel(compensationType, compensationDescription);
                }
            }
        }
    }
}

function setCompensationInputs(){
    // Only need to do type, as description is an input in the form already
    if(compensationType != null){
        // Set the compensation type
        var typeInput = document.getElementById("compensationTypeInput")
        if(typeInput != null){
            typeInput.value = compensationType;
        }
    }
}

function previewTextInDropdown(textInputDivName, dropdownDivName, getDataFunctionName, extraInputs){
    var textInput = document.getElementById(textInputDivName);
    var dropdownDiv = document.getElementById(dropdownDivName);
    if(textInput != null && dropdownDiv != null){
        if(textInput.value != null){
            window[getDataFunctionName](textInput.value, dropdownDiv, extraInputs)
        }
    }
}

var enterPressed = false;
function addParticipantDropdownCallback(postType, callbackFunctionName, secondaryEnterSubmitButton){
    // Add participant dropdown
    var dropdownDiv = document.getElementById(postType + "ParticipantSearchTextInput");
    if(dropdownDiv != null){
        dropdownDiv.onkeyup = function(event){
            if(event.keyCode != 13){
                enterPressed = false;
            }
            //40 is down, 38 is up
            if(event.keyCode === 40){
                moveDropdownFocus("down", postType + "ParticipantDropdown")
            }else if(event.keyCode === 38){
                moveDropdownFocus("up", postType + "ParticipantDropdown")
            }else if(event.keyCode === 13){
                if(enterPressed){
                    if(secondaryEnterSubmitButton != null){
                        $("[id='" + secondaryEnterSubmitButton + "']").click();
                    }
                }else{
                    selectDropdownFocusElement(postType + "ParticipantDropdown");
                }
                enterPressed = true;
            }else{
                previewTextInDropdown(postType + "ParticipantSearchTextInput", postType + "ParticipantDropdown", callbackFunctionName, {"postType": postType});
            }
        }
    }
}

function addDropdownCallback(callbackFunctionName, secondaryEnterSubmitButton, extraInputs, textInput, dropdownDivName){
    // Add participant dropdown
    var inputDiv = document.getElementById(textInput);
    if(inputDiv != null){
        inputDiv.onkeyup = function(event){
            if(event.keyCode != 13){
                enterPressed = false;
            }
            //40 is down, 38 is up
            if(event.keyCode === 40){
                moveDropdownFocus("down", dropdownDivName)
            }else if(event.keyCode === 38){
                moveDropdownFocus("up", dropdownDivName)
            }else if(event.keyCode === 13){
                if(enterPressed || dropdownFocusIndex === -1){
                    if(secondaryEnterSubmitButton != null){
                        $("[id='" + secondaryEnterSubmitButton + "']").click();
                    }
                }else{
                    selectDropdownFocusElement(dropdownDivName);
                }
                enterPressed = true;
            }else{
                previewTextInDropdown(textInput, dropdownDivName, callbackFunctionName, extraInputs);
            }
        }
    }
}

var dropdownFocusIndex = -1
function moveDropdownFocus(direction, dropdownListID){
    var dropdownList = document.getElementById(dropdownListID)
    if(dropdownList != null){
        var dropdownListItems = $("[id='" + dropdownListID + "'] li")
        var previousFocusIndex = dropdownFocusIndex;

        // Only move the focus if it's not at top or bottom element
        if(direction === "down"){
            if(dropdownFocusIndex < dropdownListItems.length - 1){
                dropdownFocusIndex += 1;
            }else{
                return
            }
        }else{
            if(dropdownFocusIndex > 0){
                dropdownFocusIndex -= 1;
            }else{
                return
            }
        }

        // Update the focus of the previous and current focus elements
        if(dropdownFocusIndex >= 0 && dropdownFocusIndex < dropdownListItems.length){
            dropdownListItems[dropdownFocusIndex].style.background = "rgba(0,0,0,0.05)";
        }
        if(previousFocusIndex >= 0 && previousFocusIndex < dropdownListItems.length){
            dropdownListItems[previousFocusIndex].style.background = "#FFF";
        }
    }
}

function selectDropdownFocusElement(dropdownListID){
    var dropdownList = document.getElementById(dropdownListID)
    if(dropdownList != null){
        var dropdownListItems = $("[id='" + dropdownListID + "'] li")
        if(dropdownFocusIndex > -1 && dropdownFocusIndex < dropdownListItems.length){
            dropdownListItems[dropdownFocusIndex].click()
            dropdownFocusIndex = -1;
        }
    }
}

function searchPreviewUsers(textValue, container, extraInputs){
    if(container != null){
        // TODO get the data
        //container.innerHTML = "<img src='" + buttonLoadingGifURL + "' style='height: 100px; width: 100px;'>";

        if(textValue.length === 0){
            container.style.display = "none";
        }else{
            container.style.display = "block";
        }

        $.ajax({
                url : "/ajax/getSearchPreviewUsers/",
                data : {"text": textValue},
                type : 'POST',
                dataType: "json",
                success : function(data) {
                    if(data["success"]){
                        if(data["users"]){
                            if(extraInputs["postType"] != null){
                                var contentString = getPreviewUsersString(data["users"], extraInputs["postType"]);
                                container.innerHTML = contentString;
                            }
                        }
                    }else{
                        container.innerHTML = "No user found with name " + textValue
                    }
                }
            });
    }
}

function getPreviewUsersString(userList, postType){
    var previewString = "<ul id='" + postType + "ParticipationDropdownList'>";
    for(var i=0; i < userList.length; i++){
        previewString += "<li onclick='selectPostParticipant(" + '"' + userList[i]["username"] + '", "' + userList[i]["cleanName"] + '", "' + postType + 'ParticipantSearchTextInput", "' + postType + 'ParticipantDropdown");' + "'><div style='position:relative; height: 50px;'>"

        // Add user picture if it exists
        previewString += "<img src='" + userList[i]["profilePicture"] + "' style='height: 40px; width:36px; position: absolute; top: 5px; left: 2px; border: 1px solid rgba(0,0,0,0.1); border-radius: 2px;' />";

        // Add name
        previewString += "<div style='position: absolute; left: 45px; top: 0; margin-top: -2px; font-weight: 500;'>" + userList[i]["cleanName"] + "</div>";

        // Add profession
        previewString += "<div style='position: absolute; left: 45px; top: 17px; color: rgba(0,0,0,0.7); font-size: 0.9em;'>" + userList[i]["profession"] + "</div>";

        previewString += "</div></li>";
    }
    previewString += "</ul>";
    return previewString;
}

function selectPostParticipant(username, cleanName, textDivName, dropdownDivName){
    var textDiv = document.getElementById(textDivName);
    var dropdownDiv = document.getElementById(dropdownDivName);
    if(textDiv != null){
        textDiv.value = cleanName;
    }
    if(dropdownDiv != null){
        dropdownDiv.style.display = "none";
        dropdownDiv.innerHTML = "";
    }
}

function addUserToPostParticipants(userDict, postType){
    if(currentPostParticipants[postType].length > 0){
        var userExists = false
        for(var i=0; i < currentPostParticipants[postType].length; i++){
            if(currentPostParticipants[postType][i]["username"] === userDict["username"]){
                userExists = true;
                break;
            }
        }
        if(!userExists){
            currentPostParticipants[postType].push(userDict);
        }else{
            return false;
        }
    }else{
        currentPostParticipants[postType] = [userDict];
    }
    return true;
}

function removeUserFromPostParticipants(username, postType){
    if(currentPostParticipants[postType].length > 0){
        var newList = [];
        var newListIndex = 0;
        for(var i=0; i < currentPostParticipants[postType].length; i++){
            if(currentPostParticipants[postType][i]["username"] != username){
                newList.push(currentPostParticipants[postType][i]);
                newListIndex += 1;
            }
        }
        currentPostParticipants[postType] = newList;
    }
}

var formHeights = {"casting": 1565, "jobs": 1335, "events": 860}
function getSubFormHeight(formType){
    var baseHeight = formHeights[formType];
    if(currentPostParticipants[formType].length > 0){
        baseHeight += 44 * Math.max(currentPostParticipants[formType].length - 1, 0);
    }
    return baseHeight
}

function updateProjectAdmin(projectID, username, updateType){
    var ajaxURL = "/ajax/" + updateType + "ProjectAdmin/";
    $.ajax({
        url : ajaxURL,
        data : {"projectID": projectID, "username": username},
        type : 'POST',
        dataType: "json",
        success : function(data) {}
    });
}

var participantPanelBaseHeight = 40;
function savePostParticipant(postID, postType, inputDivID, labelDivID, parentContainerDivID){
    if(postType === "project"){
        if(confirm("Are you sure you want to add this user? They will be able to edit and delete all related project posts.") == false){
            return;
        }
    }

    var inputDiv = document.getElementById(inputDivID);
    var labelInputDiv = document.getElementById(labelDivID);
    if(inputDiv != null && labelInputDiv != null){
        var inputData = inputDiv.value;
        var labelInputValue = labelInputDiv.value;
        inputDiv.value = '';

        if(postType === "project"){
            labelInputDiv.value = "Producer";
        }else{
            labelInputDiv.value = 'Interested';
        }

        $.ajax({
                url : "/ajax/savePostParticipant/",
                data : {"postID": postID, "name": inputData, "status": labelInputValue, "publicParticipation": false},
                type : 'POST',
                dataType: "json",
                success : function(data) {
                    if(data["success"]){
                        var tableContainer = document.getElementById(postType + "ParticipantTableContainer")
                        var tableLabelContainer = document.getElementById(postType + "ParticipantLabelContainer");
                        var tableTextContainer = document.getElementById(postType + "ParticipantSearchContainer");
                        var panelContainer = document.getElementById(postType + "ParticipantPanel");
                        if(tableContainer != null && tableLabelContainer != null && tableTextContainer != null && panelContainer != null){
                            // Update currentPostParticipants
                            addSuccess = addUserToPostParticipants(data["user"], postType)
                            if(postType === "project"){
                                updateProjectAdmin(postID, data["user"]["username"], "save")
                            }
                            if(addSuccess){
                                // Recreate the table with new info
                                var newTableInfo = getPostParticipantTable(postID, postType, currentPostParticipants[postType], null, true)
                                tableContainer.innerHTML = newTableInfo["html"]

                                if(currentPostParticipants[postType].length > 1){
                                    // Update the label to move with the input table
                                    tableLabelContainer.style.height = (newTableInfo["tableHeight"] - 5) + "px";

                                    // Update the participation panel container height
                                    panelContainer.style.height = (newTableInfo["tableHeight"] + participantPanelBaseHeight) + "px";

                                    // Move the text container input down by 1 panel length
                                    tableTextContainer.style.marginTop = parseInt(tableTextContainer.style.marginTop.slice(0,-2)) + 44 + "px";

                                    // Resize the parent container if necessary
                                    var parentContainerDiv = document.getElementById(parentContainerDivID);
                                    if(parentContainerDiv != null){
                                        parentContainerDiv.style.height = getSubFormHeight(postType) + "px";
                                    }
                                }
                            }else{
                                // Should only be false when adding a user that is already a participant
                            }
                        }
                    }else{
                        console.log("No user found with name " + inputData)
                    }
                }
            });
    }
}

function deletePostParticipant(postID, postType, username, parentContainerDivID){
    if(postType === "project"){
        if(confirm("Are you sure you want to delete this user? They will lose edit access to all related project posts.") == false){
            return;
        }
    }

    $.ajax({
        url : "/ajax/deletePostParticipant/",
        data : {"postID": postID, "username": username},
        type : 'POST',
        dataType: "json",
        success : function(data) {
            if(data["success"]){
                // Delete project admin if necessary
                if(postType === "project"){
                    updateProjectAdmin(postID, data["user"]["username"], "delete")
                }

                var tableContainer = document.getElementById(postType + "ParticipantTableContainer")
                var tableLabelContainer = document.getElementById(postType + "ParticipantLabelContainer");
                var tableTextContainer = document.getElementById(postType + "ParticipantSearchContainer");
                var panelContainer = document.getElementById(postType + "ParticipantPanel");
                if(tableContainer != null && tableLabelContainer != null && tableTextContainer != null && panelContainer != null){
                    // Update currentPostParticipants
                    var previousNumParticipants = currentPostParticipants[postType].length;
                    removeUserFromPostParticipants(data["user"]["username"], postType)

                    // Recreate the table with new info
                    var newTableInfo = getPostParticipantTable(postID, postType, currentPostParticipants[postType], null, true)
                    tableContainer.innerHTML = newTableInfo["html"]

                    if(previousNumParticipants > 1){
                        // Update the label to move with the input table
                        tableLabelContainer.style.height = (newTableInfo["tableHeight"] - 5) + "px";

                        // Update the participation panel container height
                        panelContainer.style.height = (newTableInfo["tableHeight"] + participantPanelBaseHeight) + "px";

                        // Move the text container input down up 1 panel length
                        tableTextContainer.style.marginTop = parseInt(tableTextContainer.style.marginTop.slice(0,-2)) - 44 + "px";

                        // Resize the parent container if necessary
                        var parentContainerDiv = document.getElementById(parentContainerDivID);
                        if(parentContainerDiv != null){
                            parentContainerDiv.style.height = getSubFormHeight(postType) + "px";
                        }
                    }
                }
            }else{
                console.log("Something went wrong removing post participant");
            }
        }
    });
}

function updatePostParticipationStatus(postID, postType, username){
    var userStatus = document.getElementById(postType + 'ParticipationEditStatusSelect_' + username)
    if(userStatus != null){
        $.ajax({
            url : "/ajax/updatePostParticipationStatus/",
            data : {"postID": postID, "username": username, "value": userStatus.value},
            type : 'POST',
            dataType: "json",
            success : function(data) {}
        });
    }
}

function updatePostParticipationPrivacy(postID, postType, username){
    var publicCheckbox = document.getElementById(postType + 'ParticipationPublicCheckbox_' + username)
    if(publicCheckbox != null){
        if(currentPostParticipants[postType] != null){
            for(var i=0; i < currentPostParticipants[postType].length; i++){
                if(currentPostParticipants[postType][i]["username"] === username){
                    if(publicCheckbox.checked){
                        if(currentPostParticipants[postType][i]["publicParticipation"] === "False"){
                            currentPostParticipants[postType][i]["publicParticipation"] = "True";
                        }
                    }else{
                        if(currentPostParticipants[postType][i]["publicParticipation"] === "True"){
                            currentPostParticipants[postType][i]["publicParticipation"] = "False";
                        }
                    }
                }
            }
        }

        $.ajax({
            url : "/ajax/updatePostParticipationPrivacy/",
            data : {"postID": postID, "username": username, "value": publicCheckbox.checked},
            type : 'POST',
            dataType: "json",
            success : function(data) {}
        });
    }
}

var currentPostParticipants = {"casting": [], "jobs": [], "events": [], "project": []};
var postParticipantSelectFields = {};
function getPostParticipantTable(postID, postType, participants, formName, isSubForm, statusSelectFields){
    if(statusSelectFields == null){
        if(postType in postParticipantSelectFields){
            statusSelectFields = postParticipantSelectFields[postType]
        }else{
            return;
        }
    }else{
        if(!(postType in postParticipantSelectFields)){
            postParticipantSelectFields[postType] = statusSelectFields;
        }
    }

    currentPostParticipants[postType] = participants;
    var tableString = "<div style='width: 100%; position: relative; height: " + tableHeight + "px;'><table style='width: 100%;' class='browseTable'><tr><td style='width:35%;'>User</td><td style='width:35%;'>Status</td><td style='text-align: center; width:15%;'>Public</td><td style='text-align: center; width:15%;'>Delete</td></tr>";
    var tableHeight;
    if(participants.length > 0){
        tableHeight = ((participants.length + 1) * 44);
        for(var i=0; i < participants.length; i++){
            var user = participants[i];
            // Add user picture and name
            tableString += "<tr><td style='width:35%; position: relative;'><div style='position: absolute; left: 5px; top: 2px;'><a onclick='redirectToUser(" + '"' + user["username"] + '");' + "'>" + user["cleanName"] + "</div><img style='position: absolute; right: 0; top: 0; width: 32px; height: 36px; border: 1px solid rgba(0,0,0,0.2); border-radius: 2px;' id='actorPictureImg' src='" + user.profilePictureURL + "'/></td>";

            // Add status
            var statusLabel = user["status"];
            if(statusLabel == null || statusLabel.length < 0 || statusLabel === "None"){
                if(postType === "project"){
                    statusLabel = "Producer";
                }else{
                    statusLabel = "Interested"
                }
            }
            var statusLabelID = postType + "ParticipationEditStatusSelect_" + user["username"]
            var selectForm = createSelectForm(formName, statusLabelID, statusSelectFields, statusLabel);
            tableString += "<td style='width: 35%; position: relative; height: 40px;'><div style='position:absolute; left: 0px; top: 1px; right: 2px;' onchange='updatePostParticipationStatus(" + '"' + postID + '", "' + postType + '", "' + user["username"] + '");' + "'>" + selectForm + "</div></td>";

            // Add public toggle
            tableString += "<td style='width: 15%; text-align: center;'><div style='margin-top: -8px;'><input type='checkbox' onclick='updatePostParticipationPrivacy(" + '"' + postID + '", "' + postType + '", "' + user["username"] + '");' + "' id='" + postType + "ParticipationPublicCheckbox_" + user["username"] + "' ";
            if(user["publicParticipation"] === "True" || user["publicParticipation"] === true){
                tableString += "checked ";
            }
            tableString += "/></div></td>";

            // Add delete button
            tableString += "<td style='width: 15%; text-align: center;'><div style='margin-top: 0px;'><a style='font-size: 1.1em; font-weight: 100;' onclick='deletePostParticipant(" + '"' + postID + '", "' + postType + '", "' + user["username"] + '", ';
            if(isSubForm){
                if(typeof expanded !== 'undefined' && expanded){
                    tableString += '"insertNewFormDiv"';
                }else{
                    tableString += '"insertExistingFormDiv"';
                }
            }else{
                tableString += 'null';
            }
            tableString += ');' + "'>X</a></div></td>";

            tableString += "</tr>";
        }
    }else{
        tableHeight = 88;
        tableString += "<tr><td style='width: 100%; position: relative; text-align: center;' colspan=4>No users added</td></tr>";
    }
    tableString += "</table></div>";
    return {"html": tableString, "tableHeight": tableHeight}
}

function getPostParticipantForm(postID, postType, formName, isSubForm, isNewForm, statusSelectFields, defaultStatus){
    if(isSubForm == null){
        isSubForm = false;
    }

    // Add container
    var formString = "<div id='" + postType + "ParticipantSearchContainer' style='width: 100%; position: relative; height: 20px; margin-top: 0px;' class='editCastMemberPanel'>"

    // Add name text box
    formString += '<div style="position: absolute; left: 0; top: 0; right: 60%; padding: 0px;"><input type="text" class="noFocusTextInput" name="participantSearchText" id="' + postType + 'ParticipantSearchTextInput" autocomplete="off" placeholder="Name"></div>';

    // Add status select bar
    var selectForm = createSelectForm(formName, postType + "ParticipantSelectBar", statusSelectFields, defaultStatus);
    formString += '<div style="position: absolute; left: 43.5%; top: 2px; right: 69px; padding: 0px;">' + selectForm + "</div>";

    // Add dropdown div
    formString += '<div id="' + postType + 'ParticipantDropdown" class="previewDropdownPanel" style="position: absolute; left: 0; right: 58%; top: 35px; margin-right: 1px; min-width: 184.5px; display: none; max-width: 234px;"></div>';

    // Add submit button
    formString += '<div class="whiteButton blackHover" id="' + postType + 'AddParticipantSubmitButton" onclick="savePostParticipant(' + "'" + postID + "', '" + postType + "', '" + postType + "ParticipantSearchTextInput', '" + postType + "ParticipantSelectBar', ";
    if(isSubForm){
        if(isNewForm){
            formString += "'insertNewFormDiv'";
        }else{
            formString += "'insertExistingFormDiv'";
        }
    }else{
        formString += "null";
    }
    formString += ');"' + ") style='position: absolute; right: 0; top: 5px; padding: 5px; height: 20px;'><div style='margin-top: -8px;'>Save</div></div></div>";
    return formString;
}

function createProjectFeed(projectDict, showEdit){
    var feedString = ''
    if(projectDict != null && !$.isEmptyObject(projectDict)){
        feedString += "<div id='projectFeedContainer'><ul class='projectFeed' id='projectFeed'>"

        // Sort projects by year
        // Create list of tuples of projectID, year
        var sortedProjectIDs = Object.keys(projectDict).map(function(key){
            return [key, parseInt(projectDict[key]["year"])];
        });

        // Sort the tuple list
        sortedProjectIDs.sort(function(first, second){
            return second[1] - first[1];
        });

        // Create sorted project list from tuple list
        sortedProjectList = [];
        for(var i=0; i < sortedProjectIDs.length; i++){
            sortedProjectList.push(projectDict[sortedProjectIDs[i][0]]);
        }

        for(var i=0; i < sortedProjectList.length; i++){
            feedString += "<li id='projectFeedRow_" + sortedProjectList[i]["projectID"] + "' style='position: relative;' class='projectFeedElement'>" + createProjectFeedElement(sortedProjectList[i], showEdit) + "</li>";
        }
        feedString += "</ul></div>";
    }
    return feedString
}

function createProjectFeedElement(project, showEdit){
    var feedString = '';
    // Add project picture
    feedString += "<div style='position:absolute; left: 5px; top: 5px;'><img src='" + project['postPictureURL'] + "' style='height: 90px;' /></div>"

    // Add edit button
    if(!project["registered"] && showEdit){
        feedString += "<div id='editButton_" + project["projectID"] + "' style='position: absolute; right: 5px; top: 72px;' class='editButton' onclick='toggleExpandEditRecord(" + '"expand", "' + project["projectID"] + '");' + "'>Edit</div>"
    }
    // Add year top right
    feedString += "<div style='position: absolute; right: 5px; top: 7px; color: rgba(0,0,0,0.7); font-size: 1.1em'>" + project["year"] + "</div>"


    // Add text container
    feedString += "<div style='position: absolute; left: 95px; top: 0px; right: 40px; overflow: hidden;'>";

    // Add title
    feedString += "<h2 style='white-space: nowrap;'><a style='font-weight: 400; font-size: 0.9em' "
    if(project["registered"]){
        // Don't add link to unregistered project
         feedString += " onclick='redirectToPost(" + '"' + project["projectID"] + '");' + "' "
    }
    feedString += ">";
    if(project["name"].length > 32){
        var splittedWords = project["name"].split(" ");
        project["name"] = project["name"].substring(0, project["name"].length - splittedWords[splittedWords.length-1].length-1) + "...";
    }
    feedString += project["name"] + "</a>"
    /*if("year" in project){
        feedString += "<font style='font-weight: 400; font-size: 0.9em'> (" + project["year"] + ")</font>";
    }*/
    feedString += "</h2>";

    // Add label
    if(project["labels"]){
        feedString += "<div style='color: rgba(0,0,0,0.8); font-size: 1em; margin-top: -2px;'>"
        var labelString = '';
        for(var j=0; j < project["labels"].length; j++){
            labelString += project["labels"][j]["label"]
            if(project["labels"][j]["extra"]){
                labelString += " (" + project["labels"][j]["extra"] + ")";
            }
            labelString += ' | '
        }
        labelString = labelString.substring(0, labelString.length - 3);
        feedString += labelString;
        feedString += "</div>"
    }

    // Add project type
    feedString += "<div style='color: rgba(0,0,0,0.35);'>" + project["projectType"] + "</div>"
    feedString += "<div style='color: rgba(0,0,0,0.35);'>" + project["status"] + "</div>"
    feedString += "</div>";

    // Add edit form container
    if(!project["registered"] && showEdit){
        feedString += "<div id='editRecordContainer_" + project["projectID"] + "' style='position: absolute; top: 100px; left: 5px; bottom: 5px; right: 5px;' display: none;'></div>"
    }
    return feedString;
}

