function toggleProfileProfessionHighlight(toggleType){
    if(profileProfessionList.length > 0){
        var lastProfession = profileProfessionList[profileProfessionList.length-1];
        var lastProfessionElementID = "profileProfession_" + lastProfession
        var lastProfessionElement = document.getElementById(lastProfessionElementID);
        if(lastProfessionElement != null){
            if(toggleType === "highlight"){
                lastProfessionElement.style.background = "rgba(0,0,0,0.8)";
                lastProfessionElement.style.color = "#FFF";
                $("[id='" + lastProfessionElementID + "']").find("a").css("color", "#FFF")
                professionHighlighted = true;
            }else{
                lastProfessionElement.style.background = "rgba(0,0,0,0.1)";
                lastProfessionElement.style.color = "rgba(0,0,0,0.8)";
                $("[id='" + lastProfessionElementID + "']").find("a").css("color", "#1e1e1e")
                professionHighlighted = false;
            }
        }
    }
}

function displayProfileProfessionList(chosenContainer, textInputName){
    var container = document.getElementById(chosenContainer);
    if(container != null){
        var containerString = "<ul style='display: inline;' class='filteredProfessionList'>"
        if(profileProfessionList.length > 0){
            for(var i=0; i < profileProfessionList.length; i++){
                containerString += "<li id='profileProfession_" + profileProfessionList[i] + "' style='margin-bottom: 3px; float: left; margin-top: 0px; text-align: left; position: relative; padding-right: 20px;'>" + profileProfessionList[i] + "<a onclick='removeProfileProfession(" + '"' + profileProfessionList[i] + '", "' + chosenContainer + '", "' + textInputName + '");' + "' style='font-size: 1em; font-weight: 800; position: absolute; right: 5px; '>X</a></li>";
            }
        }
        containerString += "<li style='display: none;'></li></ul>"
        container.innerHTML = containerString;

        var textInput = document.getElementById(textInputName);
        if(textInput != null){
            var textMargin =  document.getElementById(chosenContainer).offsetWidth + 5;

            // Set width of text input to parent width minus container width
            textInput.style.left = textMargin + "px";
            textInput.style.width = $("[id='" + textInputName + "']").parent().width() - textMargin + "px"
            if(profileProfessionList.length > 2){
                $("[id='" + textInputName + "']").prop('disabled', true)
            }else{
                $("[id='" + textInputName + "']").prop('disabled', false)
                $("[id='" + textInputName + "']").focus();
            }
        }
    }
}

var performerProfessions = [];
var profileProfessionList = [];
function selectProfileProfession(profession, chosenContainer, textInputName, dropdownName){
    var dropdown = document.getElementById(dropdownName);
    if(dropdown != null){
        dropdown.style.display = "none";
        dropdown.innerHTML = "";
    }

    var textInput = document.getElementById(textInputName);
    if(textInput != null){
        // Reset value and move cursor
        textInput.value = "";
    }

    if(profileProfessionList.indexOf(profession) == -1){
        profileProfessionList.push(profession);
        displayProfileProfessionList(chosenContainer, textInputName);
    }

    if(performerProfessions.length > 0 && performerProfessions.indexOf(profession) > -1){
        toggleDisplayPhysicalAttributesRow("expand");
    }
}

function selectProfileProfessionSingle(profession, textInputName, dropdownName){
    var dropdown = document.getElementById(dropdownName);
    if(dropdown != null){
        dropdown.style.display = "none";
        dropdown.innerHTML = "";
    }

    var textInput = document.getElementById(textInputName);
    if(textInput != null){
        // Reset value and move cursor
        textInput.value = profession;
    }

    /*if(profileProfessionList.indexOf(profession) == -1){
        profileProfessionList.push(profession);
    }*/
}

function removeProfileProfession(profession, chosenContainer, textInputName){
    var professionIndex = profileProfessionList.indexOf(profession)
    if(professionIndex > -1){
        profileProfessionList.splice(professionIndex, 1)
    }
    displayProfileProfessionList(chosenContainer, textInputName);
    if(performerProfessions.length > 0 && performerProfessions.indexOf(profession) > -1){
        // Removing performer profession, check all other chosen to see if physical attribute row needs to be hidden
        var shrinkPhysicalAttributeRow = true;
        for(var i=0; i < profileProfessionList; i++){
            if(performerProfessions.indexOf(profileProfessionList[i]) > -1){
                shrinkPhysicalAttributeRow = false;
            }
        }
        if(shrinkPhysicalAttributeRow){
            toggleDisplayPhysicalAttributesRow("shrink")
        }
    }
}

var professionHighlighted = false
function addProfileProfessionDropdownCallback(callbackFunctionName, extraInputs, textInput, dropdownDivName, multipleEntries){
    // Add participant dropdown
    var inputDiv = document.getElementById(textInput);

    // To support multiple profession dropdowns on 1 page, need to pass div info to the previewFunction (for the onclick)
    extraInputs["multipleEntries"] = multipleEntries;
    extraInputs["textInput"] = textInput;
    extraInputs["dropdownDivName"] = dropdownDivName;
    if(inputDiv != null){
        // Need to put backspace on key down so that it runs before text is removed (otherwise inputDiv.value.length is meaningless)
        if(multipleEntries){
            inputDiv.onkeydown = function(event){
                if(event.keyCode === 8){
                    // backspace
                    if(inputDiv.value.length === 0){
                        if(professionHighlighted){
                            removeProfileProfession(profileProfessionList[profileProfessionList.length-1], "profileProfessionContainer", textInput)
                            professionHighlighted = false
                        }else{
                            toggleProfileProfessionHighlight("highlight")
                        }
                    }
                }else if(professionHighlighted){
                    // If highlighted, and anything else is typed, remove highlight
                    toggleProfileProfessionHighlight("remove")
                }
            }
        }
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
                if(multipleEntries){
                    if(enterPressed || dropdownFocusIndex === -1){
                        if(inputDiv.value.length > 0){
                            selectProfileProfession(inputDiv.value, "profileProfessionContainer", textInput, dropdownDivName)
                        }
                    }else{
                        selectDropdownFocusElement(dropdownDivName);
                    }
                }else{
                    selectDropdownFocusElement(dropdownDivName);
                }
                enterPressed = true;
            }else if(event.keyCode != 39 && event.keyCode != 37){
                previewTextInDropdown(textInput, dropdownDivName, callbackFunctionName, extraInputs);
            }
        }
    }
}

function searchPreviewProfessions(textValue, container, extraInputs){
    if(container != null){
        // TODO get the data
        //container.innerHTML = "<img src='" + buttonLoadingGifURL + "' style='height: 100px; width: 100px;'>";
        $.ajax({
                url : "/ajax/getSearchPreviewProfessions/",
                data : {"text": textValue},
                type : 'POST',
                dataType: "json",
                success : function(data) {
                    if(data["success"]){
                        if(data["professions"]){
                            var contentString = getPreviewProfessionsString(data["professions"], extraInputs["multipleEntries"], extraInputs["textInput"], extraInputs["dropdownDivName"]);
                            container.innerHTML = contentString;
                            if(contentString.length > 0 && textValue.length > 0){
                                container.style.display = "block";
                            }else{
                                container.style.display = "none";
                            }
                        }
                    }else{
                        container.innerHTML = "No professions found"
                    }
                }
            });
    }
}


function getPreviewProfessionsString(professionList, multipleEntries, textInput, dropdownDivName){
    var previewString = '';
    if(professionList.length > 0){
        previewString += "<ul id='professionDropdownList'>";
        for(var i=0; i < professionList.length; i++){
            previewString += "<li style='margin-top: 0px; border: none; padding: 5px;' onclick='"
            if(multipleEntries){
                previewString += "selectProfileProfession(" + '"' + professionList[i] + '", "profileProfessionContainer", "profileProfessionTextInput", "profileProfessionDropdown");'
            }else{
                previewString += "selectProfileProfessionSingle(" + '"' + professionList[i] + '", "' + textInput + '", "' + dropdownDivName + '");'
            }
            previewString += "'><div style='position:relative; height: 20px;'>"
            // Add name
            previewString += "<div style='position: absolute; left: 2px; top: 0; font-weight: 500; '>" + professionList[i] + "</div>";

            previewString += "</div></li>";
        }
        previewString += "<li style='display: none;'></li></ul>";
    }
    return previewString;
}

// On profile page
function getProfileMediaPictureString(pictureID, pictureURL, description){
    var pictureString = "<div class='profileMediaPicturePanel' style='height: 250px; width: 225px'>"

    // Add picture panel
    pictureString += "<div style='display: table; position: absolute; top: 0px; left: 0; right: 0; margin: 0 auto; background: rgba(0,0,0,0.9); border: 1px solid rgba(0,0,0,0.05); overflow: hidden; height: 250px; max-height: 250px; width: 225px;'><div style='display: table-cell; vertical-align: middle;'><img src='" + pictureURL + "' style='max-height: 248px; max-width: 223px; margin-bottom: -5px;' /></div></div>"

    pictureString += "</div>"
    return pictureString

}

// On edit media page
function getOtherMediaPictureString(pictureID, pictureURL, description, featured){
    var listString = "<div class='profileMediaPicturePanel'>"

    // Add picture panel
    listString += "<div style='display: table; position: absolute; top: 10px; left: 0; right: 0; margin: 0 auto; background: rgba(0,0,0,0.0); border: 1px solid rgba(0,0,0,0.05); overflow: hidden; height: 130px; max-height: 130px; width: 117px;'><div style='display: table-cell; vertical-align: middle;'><img src='" + pictureURL + "' style='max-height: 128px; max-width: 117px; margin-bottom: -5px;' /></div></div>"

    // Add description
    listString += "<div style='position: absolute; top: 147px; left: 15px; text-align: left; right: 0; margin: 0 auto; border: 0px solid #000; white-space: nowrap; overflow: hidden;'>"
    if(description != null && description.length > 0){
        if(description.length > 15){
            description = description.substring(0, 15) + "..."
        }
        listString += description
    }else{
        listString += "<font style='color: rgba(0,0,0,0.5); font-style: italic;font-size: 0.9em;'>No description</font>"
    }
    listString += "</div>"

    // Add buttons
    listString += "<div style='position: absolute; bottom: 10px; height: 22px; left: 15px; right: 35px;'><div class='editButton' onclick='deleteOtherMediaPicture(" + '"' + pictureID + '");' + "'>Delete</div></div>"
    listString += "<div style='position: absolute; bottom: 10px; height: 22px; right: 10px;'><input type='checkbox' name='featuredCheckbox_" + pictureID + "' onclick='updateFeaturedPhotoStatus(this);' "
    if(featured == true || featured === "True"){
        listString += "checked "
    }
    listString += "/></div>"
    listString += "</div>"

    return listString;
}

function getEmptyMediaPictureList(){
    var listString = "<div style='text-align: left; height: 30px; margin: 5px;'> No media added.</div>";
    return listString;
}

function getOtherMediaPictureList(){
    var listString = "";
    if(existingOtherMediaPictures.length > 0){
        for(var i=0; i < existingOtherMediaPictures.length; i++){
            listString += getOtherMediaPictureString(existingOtherMediaPictures[i]["id"], existingOtherMediaPictures[i]["pictureURL"], existingOtherMediaPictures[i]["description"], existingOtherMediaPictures[i]["featured"]);
        }
    }else{
        listString = getEmptyMediaPictureList();
    }
    return listString;
}