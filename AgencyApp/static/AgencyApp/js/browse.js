
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
	var element = "<li style='width: 100%; height: 150px; position: relative;'>"
	
	// Add picture
	element += "<div style='position: absolute; left: 0; right: 70%; height: 100%; text-align: left;'><img src='" + dataDict["postPictureURL"] + "' style='margin-top: 3.5px; margin-left: 3px; max-height: 95%; max-width: 100%;'/></div>"

	// Add info container
	element += "<div style='position: absolute; left: 30%; right: 8px; top: 5px; height: 95%; text-align: right; color: rgba(0,0,0,0.7);'>"

	// Add info content
	element += "<h2 class='postInfoTitle'><a onclick='redirectToPost(" +'"' + dataDict["postID"] + '");' + "'>" + dataDict["title"] + "</a></h2>"
	element += "<div style='color: rgba(0,0,0,0.5);'>" + dataDict["status"] + "</div>"

	// Add dates
	//element += getDateString(new Date(dataDict["startDate"]), new Date(dataDict["endDate"]));

	// Add compensation
	element += "<div style='color: rgba(0,0,0,0.7);'>"
	if(dataDict["compensationType"] != null && dataDict["compensationType"].length > 0){
		element += dataDict["compensationType"]
		if(dataDict["compensationDescription"] != null){
			element += " - " + dataDict["compensationDescription"]
		}
	}else{
		element += "Compensation unspecified";
	}
	element += "</div>"

	// Add description
	element += "<div style='height: 50px; position: absolute: right: 0; text-align: left;'>" + dataDict["description"] + "</div>"

	element += "</li>";
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