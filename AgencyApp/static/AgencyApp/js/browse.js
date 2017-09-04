
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

function addProfessionDropdownCallback(callbackFunctionName, secondaryEnterSubmitButton, extraInputs){
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
                previewTextInDropdown("searchTextInput", "professionDropdown", callbackFunctionName, extraInputs);
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
            window[getDataFunctionName](textInput.value, dropdownDiv, extraInputs)
        }
    }
}

function getPreviewProfessionString(professionList){
    var previewString = "<ul id='professionDropdownList' style='margin-bottom: -20px;'>";
    if(professionList.length > 0){
	    for(var i=0; i < professionList.length; i++){
	        previewString += "<li style='border: none;' onclick='selectProfession(" + '"' + professionList[i] + '", "searchTextInput", "professionDropdown");' + "'><div style='position:relative; height: 30px; text-align: left; margin-left: 4px;'>" + professionList[i] + "</div></li>";
	    }
	}else{
		previewString += "No matching professions"
	}
    previewString += "</ul>";
    return previewString;
}

function searchPreviewProfessions(textValue, container, extraInputs){
    if(container != null){
        // TODO get the data
        //container.innerHTML = "<img src='" + buttonLoadingGifURL + "' style='height: 100px; width: 100px;'>";

        var professions = [];
        if(textValue.length != 0){
            container.style.display = "block";
	        if("professionDict" in extraInputs){
				for(section in extraInputs["professionDict"]){
					for(var i=0; i < extraInputs["professionDict"][section].length; i++){
						var currentProfession = extraInputs["professionDict"][section][i];
						if(currentProfession.toLowerCase().startsWith(textValue.toLowerCase())){
							professions.push(currentProfession);
						}
					}
				}
			}
        }else{
            container.style.display = "none";
        }
        var professionString = getPreviewProfessionString(professions)
	    container.innerHTML = professionString;
    }
}