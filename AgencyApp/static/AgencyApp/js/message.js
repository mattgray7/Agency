function sendMessage(senderUsername, destUsername, recipientsInput, contentInput){
    var errors = []
    if(senderUsername != null && destUsername != null && senderUsername.length > 0 && destUsername.length > 0){
        var content = document.getElementById(contentInput);
        if(content != null && content.value.length > 0){
            $.ajax({
                    url : "/ajax/sendNewMessage/",
                    data : {"sender": senderUsername, "recipient": destUsername,"content": content.value},
                    type : 'POST',
                    dataType: "json",
                    success : function(data) {
                        if(data["success"]){
                            hideBlockingPanel();
                        }
                    }
            });
        }else{
            errors.push("You must add text to the message");
        }
    }else{
        errors.push("You must add a message recipient")
    }
}

function getMessageDate(epochTime){
    // Initialize date with ms, epochTime is in s
    var date = new Date(epochTime * 1000);
    var hours = date.getHours()
    var AMPMString = "AM";
    if(hours > 12){
        AMPMString = "PM";
    }
    //return date.toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'})
    return (hours%12) + ":" + date.getMinutes() + " " + AMPMString;
}