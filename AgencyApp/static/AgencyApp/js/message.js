function sendMessage(senderUsername, destUsername, contentInput, clearTextInput, callback){
    var errors = []
    if(senderUsername != null && destUsername != null && senderUsername.length > 0 && destUsername.length > 0){
        var content = document.getElementById(contentInput);
        if(content != null && content.value.length > 0){
            var contentValue = content.value;
            if(clearTextInput){
                content.value= "";
            }
            $.ajax({
                    url : "/ajax/sendNewMessage/",
                    data : {"sender": senderUsername, "recipient": destUsername,"content": contentValue},
                    type : 'POST',
                    dataType: "json",
                    success : function(data) {
                        if(data["success"]){
                            hideBlockingPanel();
                            if(callback != null){
                                callback();
                            }
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

    var minutes = date.getMinutes()
    if(minutes < 10){
        minutes = "0" + minutes;
    }
    //return date.toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'})
    return (hours%12) + ":" + minutes + " " + AMPMString;
}

function checkForNewDateWrite(lastWrittenDate, newDate){
    var write = true;
    var thresholds = {"minutes": 5}
    if(lastWrittenDate.getYear() === newDate.getYear()){
        if(lastWrittenDate.getMonth() === newDate.getMonth()){
            if(lastWrittenDate.getDay() === newDate.getDay()){
                if(lastWrittenDate.getHours() === newDate.getHours()){
                    if(lastWrittenDate.getMinutes() === newDate.getMinutes()){
                        write = false
                    }else{
                        if(Math.abs(lastWrittenDate.getMinutes() - newDate.getMinutes()) > thresholds["minutes"]){
                            write = false
                        }
                    }
                }
            }
        }
    }
    return write;
}