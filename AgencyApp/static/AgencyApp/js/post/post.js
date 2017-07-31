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

function toggleEditPicturePopup(toggleType, postIsProject){
    if(postIsProject == null){
        postIsProject = false;
    }
    togglePopup(toggleType, "hiddenGrayPopupOverlay", "editPicturePanel")
    if(toggleType === "show"){
        addEditImageContent("editPicturePanel", postIsProject);
    }
}

function addPopupPictureToBaseForm(tempPictureID, tempPictureURL, isProject){
    var baseFormPictureInput = document.getElementById("mainPostPictureInput")
    if(isProject){
        baseFormPictureInput = document.getElementById("mainProjectPictureInput")
    }
    baseFormPictureInput.innerHTML = "<input type='hidden' name='tempPostPictureID' value='" + tempPictureID + "'>"
    return setBaseFormPicture(tempPictureURL, isProject);
}

function setBaseFormPicture(pictureURL, isProject){
    var baseFormPicture = document.getElementById("postPictureImg")
    if(isProject){
        baseFormPicture = document.getElementById("projectPictureImg")
    }
    if(baseFormPicture != null && pictureURL.length > 0){
        baseFormPicture.src = pictureURL
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
    //var pictureColumn = '<td style="text-align: center; width: 30%;"><div id="postPicturePanel" class="postPicture" style="width: 270px; height: 298px; background: #000; margin-left: 10px; margin-top: 50px;"><img id="postPictureImg" src="' + pictureField.value + '" style="max-width:100%; max-height:100%;"/></div><div style="width: 60%; margin-left: 25%; overflow: hidden;">' + pictureField.input + "</div></td>";
    var pictureColumn = '<td style="text-align: center; width: 30%;"><div id="postPicturePanel" class="postPicture" style="width: 270px; height: 298px; background: #000; margin-left: 10px; margin-top: 50px;"><img id="postPictureImg" src="' + pictureField.value + '" style="max-width:100%; max-height:100%;"/></div><div style="width: 60%; margin-left: 23%; overflow: hidden;"><a onclick="' + pictureField.editOnclick + '">Edit</a></div><div id="mainPostPictureInput" style="display: none;">' + pictureField.input + '</div></td>';


    // Fill text content
    var sectionMap = {"Details": ["title", "project", "characterType", "status", "startDate", "endDate", "hoursPerWeek", "paid"],
                      "Character": ["characterName", "shortCharacterDescription", "description", "skills", "languages"],
                      "Performer": ["actorName"],
                      "Physical": ["hairColor", "eyeColor", "complexion", "height", "build", "gender", "ageRange"],
                      "hidden": ["csrf_token", "postID", "source", "next", "destination", "projectID", "poster"]}
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
            sectionLabelTableElement += "<div style='position: relative; height: 50px; width: 100%;'> <h2 class='" + sectionClass + "' style='position: absolute; z-index: 1; right: 0; margin-left: 80px;'> " + sectionTitle + "</h2><div style='position: absolute; z-index: 0; min-width: 720px; width: 389%; border: 1px solid #7c7b7b; height: 0px; bottom: 0; margin-bottom: 15px; margin-left: 0px;'></div></div>"
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
    formString += "<tr><td colspan='3' style='width: 90%; position:relative; height: 70px;'><div style='margin-left: 100px;'><div class='whiteButton blackHover' style='position:absolute; left: 1%; top: 0; right: 50.5%;' onclick='" + formDict["cancelButton"]["onclick"] + "'> Cancel </div><div class='whiteButton blackHover' style='position:absolute; right: -1%; top: 0; left: 50.5%; ' onclick='" + formDict["createButton"].onclickFunction + "(" + '"' + formName + '");' + "'>"
    if(formDict["newPost"]){
        formString += "Create Post";
    }else{
        formString += "Update Post"
    }
    formString += "</div></div></td></tr>";
    return formString;
}


function addCreateWorkPost(formDict, formURL, formName){
    var formString = "<form method='post' action='" + formURL + "' id='" + formName + "' class='form-style-1' style='width: 90%; background: none; margin-left: 3.2%;' enctype='multipart/form-data'>";
    formString += "<table style='width: 100%;'><tr>"

    // Fill post picture string
    var pictureField = formDict["postPicture"];
    //var pictureColumn = '<td style="text-align: center; width: 30%;"><div id="postPicturePanel" class="postPicture" style="width: 270px; height: 298px; background: #000; margin-left: 10px; margin-top: 50px;"><img id="postPictureImg" src="' + pictureField.value + '" style="max-width:100%; max-height:100%;"/></div><div style="width: 60%; margin-left: 25%; overflow: hidden;">' + pictureField.input + "</div></td>";
    var pictureColumn = '<td style="text-align: center; width: 30%; min-width: 270px; position: relative;"><div style="position:absolute; width: 270px; top: 0;"><div id="postPicturePanel" class="postPicture" style="width: 270px; height: 298px; background: #000; margin-left: 10px; margin-top: 47px;"><img id="postPictureImg" src="' + pictureField.value + '" style="max-width:100%; max-height:100%;"/></div><div style="width: 60%; margin-left: 25%; overflow: hidden;"><a onclick="' + pictureField.editOnclick + '">Edit</a></div><div id="mainPostPictureInput" style="display: none;">' + pictureField.input + '</div></div></td>';

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
            sectionLabelTableElement += "<div style='position: relative; height: 50px; width: 100%;'> <h2 class='" + sectionClass + "' style='position: absolute; z-index: 1; right: 0; margin-left: 80px;'> " + sectionTitle + "</h2><div style='position: absolute; z-index: 0; min-width: 720px; width: 389%; border: 1px solid #7c7b7b; height: 0px; bottom: 0; margin-bottom: 15px; margin-left: 0px;'></div></div>"
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
    formString += "<tr><td colspan='3' style='width: 90%; position:relative; height: 70px;'><div style='margin-left: 100px;'><div class='whiteButton blackHover' style='position:absolute; left: 1%; top: 0; right: 50.5%;' onclick='" + formDict["cancelButton"]["onclick"] + "'> Cancel </div><div class='whiteButton blackHover' style='position:absolute; right: -1%; top: 0; left: 50.5%; ' onclick='" + formDict["createButton"].onclickFunction + "(" + '"' + formName + '");' + "'>"
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
    //var pictureColumn = '<td style="text-align: center; width: 30%;"><div id="postPicturePanel" class="postPicture" style="width: 270px; height: 298px; background: #000; margin-left: 10px; margin-top: 50px;"><img id="postPictureImg" src="' + pictureField.value + '" style="max-width:100%; max-height:100%;"/></div><div style="width: 60%; margin-left: 25%; overflow: hidden;">' + pictureField.input + "</div></td>";
    var pictureColumn = '<td style="text-align: center; width: 30%; min-width: 270px; position: relative;"><div style="position:absolute; width: 270px; top: 0;"><div id="projectPicturePanel" class="postPicture" style="width: 270px; height: 298px; background: #000; margin-left: 10px; margin-top: 47px;"><img id="projectPictureImg" src="' + pictureField.value + '" style="max-width:100%; max-height:100%;"/></div><div style="width: 60%; margin-left: 25%; overflow: hidden;"><a onclick="' + pictureField.editOnclick + '">Edit</a></div><div id="mainProjectPictureInput" style="display: none;">' + pictureField.input + '</div></div></td>';

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
            sectionLabelTableElement += "<div style='position: relative; height: 50px; width: 100%;'> <h2 class='" + sectionClass + "' style='position: absolute; z-index: 1; right: 0; margin-left: 80px;'> " + sectionTitle + "</h2><div style='position: absolute; z-index: 0; min-width: 720px; width: 389%; border: 1px solid #7c7b7b; height: 0px; bottom: 0; margin-bottom: 15px; margin-left: 0px;'></div></div>"
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

function createBrowseTable(tableType, tableEntries, sectionOrder){
    var tableString = "<div id='browseTableContainer'><table>"

    // Format data in section order
    var data = [];
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

    var colCount = 0;
    for(var i=0; i < data.length; i++){
        if(colCount === 0){
            tableString += "<tr>"
        }
        tableString += "<td>";

        tableString += "</td>";

        colCount += 1;
        if(colCount === 3){
            tableString += "</tr>";
            colCount = 0;
        }


    }

}


