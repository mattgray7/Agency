'use strict';
function loadCalendar(calendarID){
		var $dayNumber = $('#' + calendarID + ' .header-current-day-number');
		$(document).keyup(function(e) {
			/*if (e.keyCode == 27) {
          		$dayNumber.text(', ' + $('#' + calendarID + ' .gotcha').text());
				$//('.gotcha').animate({'top':'-50px', 'opacity': '0'},300, function(){});
				$('#' + calendarID + ' .small-wrapper').slideUp(300);
				$('#' + calendarID + ' .header-current-day-number').animate({'top':'0'}, 500, 'easeInOutBack', function(){
				$(this).animate({'right':'0'});
				$('#' + calendarID + ' .calendar-header').animate({'color':'black'});
				$('#' + calendarID + ' .month-wrapper').animate({'margin-right':'0'}, 500, 'easeInOutBack');
				$('#' + calendarID + ' .header-prev-month, ' + '#' + calendarID + ' .header-next-month, ' + '#' + calendarID + ' .header-prev-year, ' + '#' + calendarID + ' .header-next-year').animate({'width':'0'});

				//$('.gotcha').parent().animate({'color':'#808080'});
				//$('.gotcha').remove();
			});*/

				//$('.gotcha').animate({});
				$('#' + calendarID + '.calendar-header').on('click',function(e){
					console.log("header clicked")
					if(activeCalendar === calendarID){
						clickCalendar(e);
						$dayNumber.text(', ' + getRandomArbitrary(1,30));//
					}
				});		
			//};
		});
	
	

		function clickCalendar(e){
			console.log("Calendar clicked")
			e.stopPropagation();
			$('#' + calendarID + ' .calendar-header').animate({'color':'#808080'});
			var t = $('#' + calendarID + ' .header-current-month').text();
			$('#' + calendarID + ' .header-current-month').text(t.replace(',',''));
			$('#' + calendarID + ' .header-prev-month, ' + '#' + calendarID + ' .header-next-month, ' + '#' + calendarID + ' .header-prev-year, ' + '#' + calendarID + ' .header-next-year').animate({'width':'12px'},400, 'easeInOutBack');
			$('#' + calendarID + ' .header-current-day-number').animate({'right':'6px'});
			$('#' + calendarID + ' .month-wrapper').animate({'margin-right':'50px'},400, 'easeInOutBack', function(){
				$('#' + calendarID + ' .small-wrapper').slideDown(250, function(){});
        		$('#' + calendarID + ' .header-current-day-number').animate({'top':'60px'});
				var res = $dayNumber.text().replace(',','');
				//findItem(parseInt(res));		
			});
			$('#' + calendarID + ' .calendar-header').off('click');
		};	


		function getRandomArbitrary(min, max) {
				return Math.floor(Math.random() * (max - min) + min);
		}
		
    function findItem(val){
				//$('.gotcha').remove();
		    $('#' + calendarID + ' .column-item').not('.weekday, .prev-month, .next-month').each( function() {
		        if($(this).text() == val){
								$(this).append('<div class="gotcha"></div>');
								$(this).animate({'color':'white'},250);
								var pos = $(this).position();
								 var block = $(this).find('.gotcha').first();
				block.text($(this).text());
        var pos = $(this).position();
        block.css({'top': '-50px', 
									 'left': pos.left, 
									 'opacity': 0})
						 .animate({'top':pos.top,
											'opacity': '1'}, 400, 'easeInOutBack');
            }
        });
    }
	
		$('#' + calendarID + ' .calendar-header').on('click',function(e){
			clickCalendar(e);
		});	
	

    $('#' + calendarID + ' .column-item').not('.weekday').on('click', function(){
    	console.log(calendarID + ", " + activeCalendar)
    		if(calendarID === activeCalendar){
				/*$('.gotcha').fadeOut(300,function(){
						$(this).remove();
				});*/
			    //$(this).find('.gotcha').remove();
				$(this).css({'color':'white'});
				$('#' + calendarID + ' .gotcha').parent().animate({'color':'#808080'}, 250);
			    //$('.gotcha').remove();
        		$(this).prepend('<div class="gotcha"></div>');
        		var block = $(this).find('.gotcha').first();
				block.text($(this).text());
        		var pos = $(this).position();
        		block.css({'top': 0, 
						   'left': pos.left, 
						   'opacity': 0}).animate({'top':pos.top,
												   'opacity': '1'}, 350, 'easeInOutBack');
    			//});
  
			  	$('#' + calendarID + ' .calendar-base').on('click', function(e){
			  		if(e.stopPropogation){
			      		e.stopPropogation();
			      	}
			    });
			}
		});
};
 