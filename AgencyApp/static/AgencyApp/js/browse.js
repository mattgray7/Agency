
//var categoryFunctionMap = {"jobs": createJobElemement, "roles": createRoleElement, "users": createUserElement,}

function getSectionExpandButtonContent(direction){
    if(direction === "expand"){
        return "<div style='margin-top: -7px; margin-left: 1px;'>+</div>"
    }else{
        return "<div style='margin-top: -10px; margin-left: 1px; font-size: 1.2em;'>-</div>"
    }
}

function getBrowseResultsTableHeight(){
    var tableHeight = activeTabs.length * 45 + 5;
    for(section in expandedTabDict){
        if(expandedTabDict[section]){
            if(section in expandedSectionHeights && expandedSectionHeights[section] != 0 && activeTabs.indexOf(section) > -1){
                tableHeight += expandedSectionHeights[section];
            }
        }
    }
    return tableHeight
}

function getSearchPanelHeight(){
    var height = 5;
    var searchPanel = document.getElementById("searchPanel");
    if(searchPanel != null){
        height += searchPanel.offsetHeight ;
    }else{
        height += 180;      // No filter height of searchPanel
    }
    return height;
}

function updateBrowseContentHeight(){
    var newBrowseContentHeight = getBrowseResultsTableHeight() + getSearchPanelHeight();   // 180 is for search panel height
    $("#browseContent").animate({marginTop: "0px", height: newBrowseContentHeight + "px"}, browseAnimateSpeed, function(){});
}

var expandedSectionHeights = {"jobs": 0, "roles": 0, "users": 0, "projects": 0, "events": 0}
function saveExpandedBrowseSectionHeights(){
    for(section in expandedTabDict){
        if(expandedTabDict[section]){
            var container = document.getElementById(section + "BrowseResultsContainer")
            if(container != null && container.offsetHeight != 0){
                expandedSectionHeights[section] = container.offsetHeight;
            }
        }
    }
}

var browseAnimateSpeed = 400;
function toggleExpandBrowseSection(direction, section){
    var resultsContainer = document.getElementById(section + "BrowseResultsContainer");
    var expandButton = document.getElementById(section + "BrowseExpandButton");

    if(direction === "expand"){
        expandedTabDict[section] = true;
        if(expandButton != null){
            expandButton.innerHTML = getSectionExpandButtonContent("shrink")
            expandButton.onclick = function(){toggleExpandBrowseSection("shrink", section)}
        }
        if(resultsContainer != null){
            $("[id='" + section + "BrowseResultsContainer']").animate({marginTop: "0px", height: expandedSectionHeights[section] + "px"}, browseAnimateSpeed, function(){});
        }
    }else{
        expandedTabDict[section] = false;
        currentMaxNumResults[section] = defaultNumResults;      // Why is it still showing 9 results after toggle?
        if(expandButton != null){
            expandButton.innerHTML = getSectionExpandButtonContent("expand")
            expandButton.onclick = function(){toggleExpandBrowseSection("expand", section)}
        }
        if(resultsContainer != null){
            $("[id='" + section + "BrowseResultsContainer']").animate({marginTop: "0px", height: "0px"}, browseAnimateSpeed, function(){});
        }
    }
    if(resultsContainer != null){
        updateBrowseContentHeight();
    }
}

var getFiltersMap = {"jobs": getJobsFilterValues, "roles": getJobsFilterValues, "users": getJobsFilterValues, "projects": getJobsFilterValues, "events": getJobsFilterValues}
function getSearchFilterValues(){
    var filterDict = {}
    for(var i=0; i < activeTabs.length; i++){
        if(activeTabs[i] in getFiltersMap){
            filterDict[activeTabs[i]] = getFiltersMap[activeTabs[i]]();
        }
    }
    return filterDict
}

function getJobsFilterValues(){
    var filters = {"professions": filteredProfessions, "status": null, "compensation": null, "dates": {"start": null, "end": null}}

    var statusSelect = document.getElementById("jobStatusSelect");
    if(statusSelect != null && statusSelect.value != defaultSelectValues["status"]){
        filters["status"] = statusSelect.value;
    }

    var compensationSelect = document.getElementById("jobCompensationSelect");
    if(compensationSelect != null && compensationSelect.value != defaultSelectValues["compensation"]){
        filters["compensation"] = compensationSelect.value;
    }

    var startDate = document.getElementById("jobStartDate");
    var endDate = document.getElementById("jobEndDate");
    if(startDate != null && endDate != null){
        if(startDate.value != null && startDate.value.length > 0){
            filters["dates"]["start"] = startDate.value;
        }
        if(endDate.value != null && endDate.value.length > 0){
            filters["dates"]["end"] = endDate.value;
        }
    }
    return filters
}

function getRoleFilters(){}

function getUserFilters(){}

function getProjectFilters(){}

function getEventFilters(){}

// Number of results to display for each section
var defaultNumResults = 3;
var currentMaxNumResults = {"jobs": defaultNumResults, "roles": defaultNumResults, "users": defaultNumResults, "projects": defaultNumResults, "events": defaultNumResults}
function addResultsToSection(section){
    var searchValue = ''
    var searchInput = document.getElementById("searchTextInput");
    if(searchInput != null && searchInput.value != null && searchInput.value.length > 0){
        searchValue = searchInput.value;
    }

    currentMaxNumResults[section] += 3;
    $.ajax({
        url : "/ajax/getSearchResults/",
        data : {"categories": [section], "searchValue": searchValue, "numResults": currentMaxNumResults[section], "filters": JSON.stringify(getSearchFilterValues())},
        type : 'POST',
        dataType: "json",
        success : function(data) {
            if(data["success"]){
                // Update the search results just for this section
                currentSearchResults[section] = data["results"][section]
                updateBrowseResults(currentSearchResults)
            }
        }
    });
}

function getBrowseResultsList(section, results){
    var listString = "<ul id='" + section + "BrowseResultsList'>";
    for(var i=0; i < results.length; i++){
        listString += createBrowseListElement(section, results[i]);
    }
    listString += "</ul>";
    return listString;
}

var browseTableElementHeight = 165;
function createSearchResultsDisplay(resultList){
    var displayString = '';
    for(section in resultList){
        // Add section header container
        displayString += "<div style='position: relative; width: 100%; height: 45px;'>"

        var onclickDirection;
        if(expandedTabDict[section]){
            onclickDirection = "shrink";
        }else{
            onclickDirection = "expand"
        }

        displayString += "<div id='" + section + "BrowseExpandButton' class='browseTableExpandSectionButton' onclick='toggleExpandBrowseSection(" + '"' + onclickDirection + '", "' + section + '");' + "' style='position: absolute; top: 20px; left: 5px;'>" + getSectionExpandButtonContent(onclickDirection) + "</div>";

        displayString += "<h1 style='position: absolute; top: 0; left: 25px;'>" + section + " (" + resultList[section]["numResults"] + ")</h1>";
        displayString += "</div>"

        // Add results container
        if(resultList[section]["results"].length > 0 && expandedTabDict[section]){
            displayString += "<div id='" + section + "BrowseResultsContainer' style='overflow: hidden;'>";
        }else{
            displayString += "<div id='" + section + "BrowseResultsContainer' style='height: 0px; overflow: hidden;'>";
        }
        displayString += getBrowseResultsList(section, resultList[section]["results"])

        if(resultList[section]["moreResults"]){
            displayString += "<div style='text-align: center; height: 30px; margin-top: -4px;'><a style='font-weight: 300; font-size: 1.1em;' onclick='addResultsToSection(" + '"' + section + '");' + "'>Show More</a></div>"
        }
        displayString += "</div>"
    }
    return displayString
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

    // Add project link
    if("projectName" in dataDict){
        element += "<div>Project: <a onclick='redirectToPost(" + '"' + dataDict["projectID"] + '");' + "'>" + dataDict["projectName"] + "</a></div>";
    }

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
    //element += "<div style='height: 50px; position: absolute: right: 0; text-align: left;'>" + dataDict["description"] + "</div>"

    return element
}

function createJobElement(dataDict){
    var element = "";

    // Add info content
    element += "<h2 class='postInfoTitle'><a onclick='redirectToPost(" +'"' + dataDict["postID"] + '");' + "'>" + dataDict["title"] + "</a></h2>"

    // Add status
    element += "<div style='color: rgba(0,0,0,0.5);'>" + dataDict["profession"] + " - " + dataDict["status"] + "</div>"

    // Add project link
    if("projectName" in dataDict){
        element += "<div>Project: <a onclick='redirectToPost(" + '"' + dataDict["projectID"] + '");' + "'>" + dataDict["projectName"] + "</a></div>";
    }

    // Add dates
    element += "<div>" + getDateString(new Date(dataDict["startDate"]), new Date(dataDict["endDate"])) + "</div>";

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

    // Add project link
    if("projectName" in dataDict){
        element += "<div>Project: <a onclick='redirectToPost(" + '"' + dataDict["projectID"] + '");' + "'>" + dataDict["projectName"] + "</a></div>";
    }

    // Add dates
    element += getDateString(new Date(dataDict["startDate"]), new Date(dataDict["endDate"]));

    // Add description
    element += "<div style='height: 50px; color: rgba(0,0,0,0.5); position: absolute: right: 0; text-align: left;'>" + dataDict["description"] + "</div>"

    return element
}

function createUserElement(dataDict){
    var element = "";
    // Add info content
    element += "<h2 class='postInfoTitle'><a onclick='redirectToUser(" +'"' + dataDict["username"] + '");' + "'>" + dataDict["cleanName"] + "</a></h2>"
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
                if(enterPressed || dropdownFocusIndex === -1){
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
    var resultCount = 0
    var suggestionHeight = 30
    if(suggestions != null && !$.isEmptyObject(suggestions)){
        for(type in suggestions){
            for(var i=0; i < suggestions[type].length; i++){
                resultCount += 1
                var functionInput = suggestions[type][i]
                var displayString = suggestions[type][i] + "<div style='color: rgba(0,0,0,0.5); display: inline;'> - " + type + "</div>"

                // User values are dict
                if(type === "User"){
                    functionInput = suggestions[type][i]["cleanName"]
                    displayString = suggestions[type][i]["cleanName"] + "<div style='color: rgba(0,0,0,0.5); display: inline;'> - " + suggestions[type][i]["profession"] + "</div>"
                }
                previewString += "<li style='border: none;' onclick='selectBrowseSuggestion(" + '"' + functionInput + '", "searchTextInput", "browseDropdown");' + "'><div style='position:relative; height: " + suggestionHeight + "px; text-align: left; margin-left: 4px;'>" + displayString + "</div></li>";
            }
        }
    }else{
        previewString += "<li style='height: " + suggestionHeight + "px; border: none;'>No suggestions</li>"
    }
    previewString += "</ul>";

    // Add container around list with proper height of results
    previewString = "<div style='height: " + resultCount*suggestionHeight + "px;'>" + previewString + "</div>"
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