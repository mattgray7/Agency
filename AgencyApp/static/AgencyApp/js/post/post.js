function addCreateCastingPost(formDict, formURL, formName){
	var formString = "<form method='post' action='" + formURL + "' id='" + formName + "' class='form-style-7' style='width: 90%; background: none;'><ul>";
	var pictureURL = null;
	for(var i=0; i < formDict.length; i++){
		var name = "";
		var input = "";
		var hidden = true;
		var value = "";
		var label = "";
		for(var j=0; j < formDict[i].length; j++){
			var formElement = formDict[i][j];
			if(formElement["key"] == "name"){
				name = formElement["value"];
			}else if(formElement["key"] == "input"){
				input = formElement["value"];
			}else if(formElement["key"] == "hidden"){
				hidden = formElement["value"];
			}else if(formElement["key"] == "value"){	
				value = formElement["value"]
			}else if(formElement["key"] == "label"){
				label = formElement["value"]
			}
		}
		if(name === "postPicture"){
			pictureURL = value;
		}
		if(!hidden){
			formString += "<li><label for='name' style='background: #efefef;'>" + label + "</label>";
			if(name === "description"){
				formString += "<textarea cols='100' rows ='20' name='description' form='" + formName + "' style='height:100px; font-size: 0.9em;'>" + value + "</textarea></li>"
			}else{
				formString += "<div style='background: #efefef; border: 2px solid #FFF; border-radius: 4px;'>" + input + '</div>'; 
			}
			formString += "</li>";
		}else{
			formString += input;
		}		
	}
	formString += "</ul></form>";
	return formString;
}