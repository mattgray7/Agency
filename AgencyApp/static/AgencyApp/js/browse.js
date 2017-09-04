
//var categoryFunctionMap = {"jobs": createJobElemement, "roles": createRoleElement, "users": createUserElement,}

function createSearchResultsDisplay(resultList){
	var displayString = '';
	for(section in resultList){
		displayString += "<h1 style='position: relative; width: 100%; height: 40px;'><div style='position: absolute; top: 0; left: 5px;'>" + section + "</div></h1>";
		displayString += "<ul>"
		for(var i=0; i < resultList[section].length; i++){
			displayString += createJobElement(resultList[section][i]);
		}
		displayString += "</ul>"
	}
	return displayString
}

function createJobElement(dataDict){
	var element = "<li>" + dataDict["title"] + "</li>";
	return element
}

function addProfessionDropdownCallback(callbackFunctionName, secondaryEnterSubmitButton){
    // Add participant dropdown
    var dropdownDiv = document.getElementById("searchTextInput");
    if(dropdownDiv != null){
        dropdownDiv.onkeyup = function(event){
            if(event.keyCode != 13){
                enterPressed = false;
            }
            //40 is down, 38 is up
            if(event.keyCode === 40){
                moveDropdownFocus("down", "professionDropdown")
            }else if(event.keyCode === 38){
                moveDropdownFocus("up", "professionDropdown")
            }else if(event.keyCode === 13){
                if(enterPressed){
                    if(secondaryEnterSubmitButton != null){
                        $("[id='" + secondaryEnterSubmitButton + "']").click();
                    }
                }else{
                    selectDropdownFocusElement("professionDropdown");
                }
                enterPressed = true;
            }else{
                previewTextInDropdown("searchTextInput", "professionDropdown", callbackFunctionName);
            }
        }
    }
}

function selectProfession(profession, textDivName, dropdownDivName){
	var textDiv = document.getElementById(textDivName);
    var dropdownDiv = document.getElementById(dropdownDivName);
    if(textDiv != null){
        textDiv.value = profession;
    }
    if(dropdownDiv != null){
        dropdownDiv.style.display = "none";
        dropdownDiv.innerHTML = "";
    }
}

function previewTextInDropdown(textInputDivName, dropdownDivName, getDataFunctionName, extraInputs){
    var textInput = document.getElementById(textInputDivName);
    var dropdownDiv = document.getElementById(dropdownDivName);
    if(textInput != null && dropdownDiv != null){
        if(textInput.value != null){
        	console.log(getDataFunctionName)
            window[getDataFunctionName](textInput.value, dropdownDiv, extraInputs)
        }
    }
}

function getPreviewProfessionString(professionList){
    var previewString = "<ul id='professionDropdownList'>";
    for(var i=0; i < professionList.length; i++){
        previewString += "<li onclick='selectProfession(" + '"' + professionList[i] + '", "searchTextInput", "professionDropdown");' + "'><div style='position:relative; height: 30px;'>"

        /*// Add user picture if it exists
        previewString += "<img src='" + userList[i]["profilePicture"] + "' style='height: 40px; width:36px; position: absolute; top: 5px; left: 2px; border: 1px solid rgba(0,0,0,0.1); border-radius: 2px;' />";

        // Add name
        previewString += "<div style='position: absolute; left: 45px; top: 0; margin-top: -2px; font-weight: 500;'>" + userList[i]["cleanName"] + "</div>";

        // Add profession
        previewString += "<div style='position: absolute; left: 45px; top: 17px; color: rgba(0,0,0,0.7); font-size: 0.9em;'>" + userList[i]["profession"] + "</div>";*/
        previewString += professionList[i];

        previewString += "</div></li>";
    }
    previewString += "</ul>";
    return previewString;
}

function searchPreviewProfessions(textValue, container, extraInputs){
    if(container != null){
        // TODO get the data
        //container.innerHTML = "<img src='" + buttonLoadingGifURL + "' style='height: 100px; width: 100px;'>";

        if(textValue.length === 0){
            container.style.display = "none";
        }else{
            container.style.display = "block";
        }

        var professions = ["Actor", "director", "person"];
        var professionString = getPreviewProfessionString(professions)
        container.innerHTML = professionString;
        /*$.ajax({
                url : "/ajax/getSearchPreviewUsers/",
                data : {"text": textValue},
                type : 'POST',
                dataType: "json",
                success : function(data) {
                    if(data["success"]){
                        if(data["users"]){
                            if(extraInputs["postType"] != null){
                                var contentString = getPreviewProfessionString(data["users"], extraInputs["postType"]);
                                container.innerHTML = contentString;
                            }
                        }
                    }else{
                        container.innerHTML = "No user found with name " + textValue
                    }
                }
            });*/

    }
}