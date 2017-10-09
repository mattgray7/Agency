function sendMessage(senderUsername, destUsername, recipientsInput, subjectInput, contentInput){
	var errors = []
	if(senderUsername != null && destUsername != null && senderUsername.length > 0 && destUsername.length > 0){
		var subject = document.getElementById(subjectInput);
		var content = document.getElementById(contentInput);
		if(subject != null){
			if(content != null && content.value.length > 0){
				$.ajax({
                    url : "/ajax/sendNewMessage/",
                    data : {"sender": senderUsername, "recipient": destUsername, "subject": subject.value, "content": content.value},
                    type : 'POST',
                    dataType: "json",
                    success : function(data) {
                        console.log(data)
                    }
                });

			}else{
				errors.push("You must add text to the message");
			}
		}
	}else{
		errors.push("You must add a message recipient")
	}
}