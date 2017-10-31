
//var categoryFunctionMap = {"jobs": createJobElemement, "roles": createRoleElement, "users": createUserElement,}


var searchPanelBaseHeight = 200;

function getSectionExpandButtonContent(direction){
    if(direction === "expand"){
        return "<div style='margin-top: -7px; margin-left: 1px;'>+</div>"
    }else{
        return "<div style='margin-top: -10px; margin-left: 1px; font-size: 1.2em;'>-</div>"
    }
}

function getBrowseResultsTableHeight(){
    var tableHeight;
    if(activeResultTab != null){
        var container = document.getElementById(activeResultTab + "BrowseResultsContainer")
        if(container != null){
            tableHeight = container.offsetHeight + 45;
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
        height += searchPanelHeight;      // No filter height of searchPanel
    }
    return height;
}

function updateBrowseContentHeight(){
    var newBrowseContentHeight = getBrowseResultsTableHeight() + getSearchPanelHeight();   // 180 is for search panel height
    $("#browseContent").animate({marginTop: "0px", height: newBrowseContentHeight + "px"}, browseAnimateSpeed, function(){});
}
var browseAnimateSpeed = 400;
var getFiltersMap = {"jobs": getJobsFilterValues, "roles": getRolesFilterValues, "users": getUsersFilterValues, "projects": getProjectsFilterValues, "events": getEventsFilterValues}
function getSearchFilterValues(){
    var filterDict = {}
    for(var i=0; i < activeTabs.length; i++){
        if(activeTabs[i] in getFiltersMap){
            filterDict[activeTabs[i]] = getFiltersMap[activeTabs[i]]();
        }
    }
    return filterDict
}

function _getDatesFilterValues(filterType){
    var dateFilters = {"start": null, "end": null}
    var startDate = document.getElementById(filterType + "StartDate");
    var endDate = document.getElementById(filterType + "EndDate");
    if(startDate != null && endDate != null){
        if(startDate.value != null && startDate.value.length > 0){
            dateFilters["start"] = startDate.value;
        }
        if(endDate.value != null && endDate.value.length > 0){
            dateFilters["end"] = endDate.value;
        }
    }
    return dateFilters
}

function _addSelectFilterValues(existingFilters, selectID, filterName){
    var select = document.getElementById(selectID);
    if(select != null && select.value != defaultSelectValues[filterName]){
        existingFilters[filterName] = select.value;
    }
    return existingFilters;
}

function getJobsFilterValues(){
    var filters = {"professions": filteredProfessions["jobs"], "status": null, "compensation": null, "dates": {"start": null, "end": null}}
    filters = _addSelectFilterValues(filters, "jobsStatusSelect", "status")
    filters = _addSelectFilterValues(filters, "jobsCompensationSelect", "compensation")
    filters["dates"] = _getDatesFilterValues("jobs")
    return filters
}

function getRolesFilterValues(){
    var filters = {"status": null, "roleType": null, "gender": null, "ageRange": null, "build": null, "hairColor": null, "eyeColor": null, "ethnicity": null, "compensation": null, "dates": {"start": null, "end": null}}
    filters = _addSelectFilterValues(filters, "rolesStatusSelect", "status")
    filters = _addSelectFilterValues(filters, "rolesTypeSelect", "roleType")
    filters = _addSelectFilterValues(filters, "rolesGenderSelect", "gender")
    filters = _addSelectFilterValues(filters, "rolesAgeRangeSelect", "ageRange")
    filters = _addSelectFilterValues(filters, "rolesCompensationSelect", "compensation")
    filters = _addSelectFilterValues(filters, "rolesBuildSelect", "build")
    filters = _addSelectFilterValues(filters, "rolesHairColorSelect", "hairColor")
    filters = _addSelectFilterValues(filters, "rolesEyeColorSelect", "eyeColor")
    filters = _addSelectFilterValues(filters, "rolesEthnicitySelect", "ethnicity")
    filters["dates"] = _getDatesFilterValues("roles")
    return filters
}

function getUsersFilterValues(){
    var filters = {"professions": filteredProfessions["users"], "interest": null, "imdb": null, "resume": null, "gender": null, "ageRange": null, "build": null, "hairColor": null, "eyeColor": null, "ethnicity": null, "dates": {"start": null, "end": null}}
    filters = _addSelectFilterValues(filters, "usersInterestSelect", "interest")
    filters = _addSelectFilterValues(filters, "usersIMDBSelect", "imdb")
    filters = _addSelectFilterValues(filters, "usersResumeSelect", "resume")
    filters = _addSelectFilterValues(filters, "usersGenderSelect", "gender")
    filters = _addSelectFilterValues(filters, "usersAgeRangeSelect", "ageRange")
    filters = _addSelectFilterValues(filters, "usersBuildSelect", "build")
    filters = _addSelectFilterValues(filters, "usersHairColorSelect", "hairColor")
    filters = _addSelectFilterValues(filters, "usersEyeColorSelect", "eyeColor")
    filters = _addSelectFilterValues(filters, "usersEthnicitySelect", "ethnicity")
    filters["dates"] = _getDatesFilterValues("users")
    return filters
}

function getProjectsFilterValues(){
    var filters = {"status": null, "projectType": null, "union": null, "compensation": null, "dates": {"start": null, "end": null}}
    filters = _addSelectFilterValues(filters, "projectsStatusSelect", "status")
    filters = _addSelectFilterValues(filters, "projectsTypeSelect", "projectType")
    filters = _addSelectFilterValues(filters, "projectsUnionSelect", "union")
    filters = _addSelectFilterValues(filters, "projectsCompensationSelect", "compensation")
    filters["dates"] = _getDatesFilterValues("projects")
    return filters
}

function getEventsFilterValues(){
    var filters = {"status": null, "eventType": null, "dates": {"start": null, "end": null}}
    //filters = _addSelectFilterValues(filters, "eventsStatusSelect", "status")
    filters = _addSelectFilterValues(filters, "eventsTypeSelect", "eventType")
    filters["dates"] = _getDatesFilterValues("events")
    return filters
}

// Number of results to display for each section
var defaultNumResults = 6;
var currentMaxNumResults = {"jobs": defaultNumResults, "roles": defaultNumResults, "users": defaultNumResults, "projects": defaultNumResults, "events": defaultNumResults}
function addResultsToSection(section){
    var searchValue = ''
    var searchInput = document.getElementById("searchTextInput");
    if(searchInput != null && searchInput.value != null && searchInput.value.length > 0){
        searchValue = searchInput.value;
    }

    currentMaxNumResults[section] += defaultNumResults;
    $.ajax({
        url : "/ajax/getSearchResults/",
        data : {"categories": [section], "searchValue": searchValue, "numResults": currentMaxNumResults[section], "filters": JSON.stringify(getSearchFilterValues())},
        type : 'POST',
        dataType: "json",
        success : function(data) {
            if(data["success"]){
                // Update the search results just for this section
                currentSearchResults[section] = data["results"][section]
                updateBrowseResults(currentSearchResults, section)
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

function getSearchResultsSectionTab(resultList, activeTab){
    var displayString = '';

    displayString += "<div style='position: relative; width: 100%; height: 45px;'><ul class='profileTabButtonList' id='browseResultTabButtonList' style=''>"
    for(var i=0; i < activeTabs.length; i++){
        // Specify margin for each button in order (TODO create a functino to create a 4 tab list)
        var styleString = "position: absolute;"
        if(i === 0){
            styleString += "left: -4px;"
        }else if(i === 1){
            styleString += "left: 19.5%;"
        }else if(i === 2){
            styleString += "left: 39.7%;"
        }else if(i === 3){
            styleString += "left: 60%;"
        } else if(i === 4){
            styleString += "right: 0px;"
        }

        var tabButton = '<li style="width: 19%; height: 40px;' + styleString + '" '
        var borderCoverOpacity = 0
        if(activeTabs[i] === activeTab){
            tabButton += 'class="active" ';
            borderCoverOpacity = 1;
        }
        tabButton += ' id="' + activeTabs[i] + 'ResultsButton" onclick="selectBrowseResultTab(' + "'" + activeTabs[i] + "');" + '"><div style="margin-top: 5px;">' + activeTabs[i] + ' (' + resultList[activeTabs[i]]["numResults"] + ')</div><div id="' + activeTabs[i] + 'BorderCover" class="profileTabButtonBorderCover" style="margin-top: 8px; opacity: ' + borderCoverOpacity + ';"></div></li>';
        displayString += tabButton;
    }

    displayString += "</ul></div>"
    return displayString
}

var browseTableElementHeight = 165;
function createSearchResultsDisplay(resultList, activeTab){
    var displayString = '<div style="margin-left: 0px; margin-right: 2px;">';

    displayString += getSearchResultsSectionTab(resultList, activeTab);

    displayString += "<div style='position: relative; width: 100%; min-height: 200px;'>"

    // Add results container
    if(resultList[activeTab]["results"].length > 0){
        displayString += "<div id='" + activeTab + "BrowseResultsContainer' style='overflow: hidden; border: 1px solid #000; background: #FFF; border-radius: 2px;'>";
        displayString += getBrowseResultsList(activeTab, resultList[activeTab]["results"])
        if(resultList[activeTab]["moreResults"]){
            displayString += "<div style='text-align: center; height: 30px; margin-top: -4px;'><a style='font-weight: 300; font-size: 1.1em;' onclick='addResultsToSection(" + '"' + activeTab + '");' + "'>Show More</a></div>"
        }
    }else{
        displayString += "<div id='" + activeTab + "BrowseResultsContainer' style='height: 30px; overflow: hidden; border: 1px solid #000; border-radius: 2px; background: #FFF; text-align: center; padding: 15px 0px 10px 0px;'>No results matching search.";
    }
    displayString += "</div></div>"
    return displayString
}

var createBrowseListElementFunctionMap = {"jobs": createJobElement, "roles": createRoleElement, "projects": createProjectElement, "events": createEventElement, "users": createUserElement}
function createBrowseListElement(elementType, dataDict){
    var element = "<li style='height: " + browseTableElementHeight + "px; position: relative; overflow: hidden; background: #FFF;'>"
    
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

    // Add message button
    if(loggedInUser != null && dataDict["username"] != loggedInUser){
        element += "<div class='editButton' onclick='displayMessagePanel(" + '"' + dataDict["username"] + '", "' + dataDict["cleanName"] + '");' + "' style='position: absolute; top: 0px; right: 0px;'>Message</div>";
    }

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

/*function previewTextInDropdown(textInputDivName, dropdownDivName, getDataFunctionName, extraInputs){
    var textInput = document.getElementById(textInputDivName);
    var dropdownDiv = document.getElementById(dropdownDivName);
    if(textInput != null && dropdownDiv != null){
        if(textInput.value != null){
            window[getDataFunctionName](textInput.value, dropdownDiv, extraInputs)
        }
    }
}*/

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
        if(textValue.length != 0){
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
                    if($.isEmptyObject(suggestions)){
                        container.innerHTML = "";
                        container.style.display = "none";
                    }else{
                        var suggestionsString = getPreviewBrowseSuggestionsString(suggestions)
                        container.innerHTML = suggestionsString;
                        container.style.display = "block";
                    }
                }
            });
        }else{
            container.style.display = "none";
        }
        
    }
}