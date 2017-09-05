
//var categoryFunctionMap = {"jobs": createJobElemement, "roles": createRoleElement, "users": createUserElement,}

function getSectionExpandButtonContent(direction){
    if(direction === "expand"){
        return "<div style='margin-top: -7px; margin-left: 1px;'>+</div>"
    }else{
        return "<div style='margin-top: -10px; margin-left: 1px; font-size: 1.2em;'>-</div>"
    }
}

function toggleExpandBrowseSection(direction, section){
    console.log("Toggling in direction " + direction)
    var resultsContainer = document.getElementById(section + "BrowseResultsContainer");
    var expandButton = document.getElementById(section + "BrowseExpandButton");
    if(direction === "expand"){
        if(expandButton != null){
            expandButton.innerHTML = getSectionExpandButtonContent("shrink")
            expandButton.onclick = function(){toggleExpandBrowseSection("shrink", section)}
        }
        if(resultsContainer != null){
            $("[id='" + section + "BrowseResultsContainer']").animate({marginTop: "10px", height: "1000px"}, 500, function(){});
        }
    }else{
        if(expandButton != null){
            expandButton.innerHTML = getSectionExpandButtonContent("expand")
            expandButton.onclick = function(){toggleExpandBrowseSection("expand", section)}
        }
        if(resultsContainer != null){
            $("[id='" + section + "BrowseResultsContainer']").animate({marginTop: "10px", height: "0px"}, 500, function(){});
        }
    }
}


var browseTableElementHeight = 165;
function createSearchResultsDisplay(resultList){
    var displayString = '';
    var tableHeight = 17;
    for(section in resultList){
        // Add section header container
        displayString += "<div style='position: relative; width: 100%; height: 40px;'>"

        // Add shrink/expand section button
        displayString += "<div id='" + section + "BrowseExpandButton' class='browseTableExpandSectionButton' onclick='toggleExpandBrowseSection(" + '"shrink", "' + section + '");' + "' style='position: absolute; top: 20px; left: 5px;'><div style='margin-top: -10px; margin-left: 1px; font-size: 1.2em;'>-</div></div>";

        displayString += "<h1 style='position: absolute; top: 0; left: 25px;'>" + section + " (" + resultList[section].length + ")</h1>";
        displayString += "</div>"
        tableHeight += 48

        // Add results container
        displayString += "<div id='" + section + "BrowseResultsContainer' style='overflow: hidden;'>";
        displayString += "<ul>"
        for(var i=0; i < resultList[section].length; i++){
            displayString += createBrowseListElement(section, resultList[section][i]);
            tableHeight += browseTableElementHeight + 5;
        }
        displayString += "</ul>"
        displayString += "</div>"
    }
    return {"html": displayString, "tableHeight": tableHeight}
}

var createBrowseListElementFunctionMap = {"jobs": createJobElement, "roles": createRoleElement, "projects": createProjectElement, "events": createEventElement, "users": createUserElement}
function createBrowseListElement(elementType, dataDict){
    var element = "<li style='height: " + browseTableElementHeight + "px; position: relative; overflow: hidden;'>"
    
    // Add picture
    element += "<div style='position: absolute; left: 0; right: 75%; height: 100%; text-align: left;'><img src='" + dataDict["postPictureURL"] + "' style='margin-top: 8px; margin-left: 10px; max-height: 90%; max-width: 100%;'/></div>"

    if(elementType in createBrowseListElementFunctionMap){
        element += "<div style='position: absolute; left: 25%; right: 8px; top: 5px; height: 95%; text-align: left; color: rgba(0,0,0,0.7);'>" + createBrowseListElementFunctionMap[elementType](dataDict) + "</div>"
    }else{
        console.log("Could not find elementType " + elementType + " in function map")
    }
    element += "</li>";
    return element;
}

function createRoleElement(dataDict){
    var element = "";
    // Add info content
    element += "<h2 class='postInfoTitle'><a onclick='redirectToPost(" +'"' + dataDict["postID"] + '");' + "'>" + dataDict["title"] + "</a></h2>"
    element += "<div style='color: rgba(0,0,0,0.5);'>" + dataDict["status"] + "</div>"

    // Add characterName
    element += "<div>" + dataDict["characterName"] + "</div>";

    // Add dates
    element += getDateString(new Date(dataDict["startDate"]), new Date(dataDict["endDate"]));

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

    return element
}

function createJobElement(dataDict){
    var element = "";

    // Add info content
    element += "<h2 class='postInfoTitle'><a onclick='redirectToPost(" +'"' + dataDict["postID"] + '");' + "'>" + dataDict["title"] + "</a></h2>"
    element += "<div style='color: rgba(0,0,0,0.5);'>" + dataDict["status"] + "</div>"

    // Add dates
    element += getDateString(new Date(dataDict["startDate"]), new Date(dataDict["endDate"]));

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

    return element
}

function createProjectElement(dataDict){
    var element = "";
    // Add info content
    element += "<h2 class='postInfoTitle'><a onclick='redirectToPost(" +'"' + dataDict["postID"] + '");' + "'>" + dataDict["title"] + "</a></h2>"
    element += "<div style='color: rgba(0,0,0,0.8);'>"

    element += "<div>" + dataDict["projectType"] + "</div>"
    element += "<div>" + dataDict["status"] + "</div>"


    // Add description
    element += "<div style='height: 50px; color: rgba(0,0,0,0.5); position: absolute: right: 0; text-align: left;'>" + dataDict["description"] + "</div>"

    return element
}

function createEventElement(dataDict){
    var element = "";
    // Add info content
    element += "<h2 class='postInfoTitle'><a onclick='redirectToPost(" +'"' + dataDict["postID"] + '");' + "'>" + dataDict["title"] + "</a></h2>"
    element += "<div style='color: rgba(0,0,0,0.8);'>"

    // Add dates
    element += getDateString(new Date(dataDict["startDate"]), new Date(dataDict["endDate"]));

    // Add description
    element += "<div style='height: 50px; color: rgba(0,0,0,0.5); position: absolute: right: 0; text-align: left;'>" + dataDict["description"] + "</div>"

    return element
}

function createUserElement(dataDict){
    var element = "";
    // Add info content
    element += "<h2 class='postInfoTitle'><a onclick='redirectToProfile(" +'"' + dataDict["username"] + '");' + "'>" + dataDict["cleanName"] + "</a></h2>"
    element += "<div style='color: rgba(0,0,0,0.8);'>"

    // Add dates
    element += "<div>" + dataDict["profession"] + "</div>";

    // Add bio
    element += "<div style='height: 50px; color: rgba(0,0,0,0.5); position: absolute: right: 0; text-align: left;'>" + dataDict["bio"] + "</div>"

    return element
}

function addBrowseDropdownCallback(callbackFunctionName, secondaryEnterSubmitButton, extraInputs){
    // Add participant dropdown
    var dropdownDiv = document.getElementById("searchTextInput");
    if(dropdownDiv != null){
        dropdownDiv.onkeyup = function(event){
            if(event.keyCode != 13){
                enterPressed = false;
            }
            //40 is down, 38 is up
            if(event.keyCode === 40){
                moveDropdownFocus("down", "browseDropdown")
            }else if(event.keyCode === 38){
                moveDropdownFocus("up", "browseDropdown")
            }else if(event.keyCode === 13){
                if(enterPressed){
                    if(secondaryEnterSubmitButton != null){
                        $("[id='" + secondaryEnterSubmitButton + "']").click();
                    }
                }else{
                    selectDropdownFocusElement("browseDropdown");
                }
                enterPressed = true;
            }else{
                previewTextInDropdown("searchTextInput", "browseDropdown", callbackFunctionName, extraInputs);
            }
        }
    }
}

function selectBrowseSuggestion(value, textDivName, dropdownDivName){
    var textDiv = document.getElementById(textDivName);
    var dropdownDiv = document.getElementById(dropdownDivName);
    if(textDiv != null){
        textDiv.value = value;
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

function getPreviewBrowseSuggestionsString(suggestions){
    var previewString = "<ul id='browseSuggestionDropdownList' style='margin-bottom: -20px;'>";
    if(suggestions != null){
        for(type in suggestions){
            for(var i=0; i < suggestions[type].length; i++){
                var functionInput = suggestions[type][i]
                var displayString = suggestions[type][i] + "<div style='color: rgba(0,0,0,0.5); display: inline;'> - " + type + "</div>"

                // User values are dict
                if(type === "User"){
                    functionInput = suggestions[type][i]["cleanName"]
                    displayString = suggestions[type][i]["cleanName"] + "<div style='color: rgba(0,0,0,0.5); display: inline;'> - " + suggestions[type][i]["profession"] + "</div>"
                }
                previewString += "<li style='border: none;' onclick='selectBrowseSuggestion(" + '"' + functionInput + '", "searchTextInput", "browseDropdown");' + "'><div style='position:relative; height: 30px; text-align: left; margin-left: 4px;'>" + displayString + "</div></div></li>";
            }
        }
    }else{
        previewString += "No suggestions"
    }
    previewString += "</ul>";
    return previewString;
}

function searchPreviewBrowseSuggestions(textValue, container, extraInputs){
    if(container != null){
        // TODO get the data
        //container.innerHTML = "<img src='" + buttonLoadingGifURL + "' style='height: 100px; width: 100px;'>";
        
        if(textValue.length != 0){
            container.style.display = "block";
            var suggestions;
            $.ajax({
                url : "/ajax/getSearchSuggestions/",
                data : {"text": textValue},
                type : 'POST',
                dataType: "json",
                success : function(data) {
                    if(data["success"]){
                        if(data["suggestions"] != null){
                            suggestions = data["suggestions"];
                        }
                    }else{
                        container.innerHTML = "No user found with name " + textValue
                    }
                    var suggestionsString = getPreviewBrowseSuggestionsString(suggestions)
                    container.innerHTML = suggestionsString;
                }
            });
        }else{
            container.style.display = "none";
        }
        
    }
}