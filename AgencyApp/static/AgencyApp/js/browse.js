
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