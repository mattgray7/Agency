function getSearchPanel(searchType){
	/*if(searchType === "posts"){
		return getPostsSearchPanel();
	}else if(searchType === "users"){
		return getUsersSearchPanel();
	}else if(searchType === "events"){
		return getEventsSearchPanel();
	}*/
	return getPostsSearchPanel();
}

function getPostsSearchPanel(){
	panelString = "<div id='searchPanelContent' style='position: relative; height: 100%; width: 100%;'>";

	// Add textbox
	panelString += "<div class='browseSearchTextBoxContainer' style='position:absolute; top: 10px; left: 5%; right: 5%;'><div style='position: relative;'><div style='position: absolute; left: 0; right: 80px;'> <input type='text' placeholder='Browse projects, jobs, or roles'></div><div style='position: absolute; right: 0; padding: 4px; margin-top: 7px;' class='whiteButton blackHover'> Search</div></div>"

	panelString += "</div>";
	return panelString;
}

function getUsersSearchPanel(){
	
}

function getEventsSearchPanel(){
	
}