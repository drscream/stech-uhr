Date.prototype.getISOWeek = function () {
	var target = new Date(this.valueOf());

	var dayNr = (this.getDay() + 6) % 7;
	target.setDate(target.getDate() - dayNr + 3);
	var firstThursday = target.valueOf();

	target.setMonth(0, 1);
	if (target.getDay() != 4) {
		target.setMonth(0, 1 + ((4 - target.getDay()) + 7) % 7);
	}

	return 1 + Math.ceil((firstThursday - target) / 604800000);
}

Date.prototype.getISOYear = function () {
	var target	= new Date(this.valueOf());
	target.setDate(target.getDate() - ((this.getDay() + 6) % 7) + 3);

	return target.getFullYear();
}


$('#date-picker-day')
	.datepicker({
		weekStart: 1,
		minViewMode: 0,
		todayBtn: "linked",
		calendarWeeks: true
	})
	.on('changeDate', function(action){
		var year = action.date.getFullYear();
		var month =  action.date.getMonth() + 1;
		var day = action.date.getDate()
		var url_base = '/stechuhr/reports/day/';
		window.location = url_base + year + '/' + month + '/' + day + '/';
	});

$('#date-picker-week')
	.datepicker({
		weekStart: 1,
		minViewMode: 0,
		todayBtn: "linked",
		calendarWeeks: true
	})
	.on('changeDate', function(action){
		var year = action.date.getISOYear();
		var week = action.date.getISOWeek();
		var url_base = '/stechuhr/reports/week/';
		window.location = url_base + year + '/' + week + '/';
	});

$('#date-picker-month')
	.datepicker({
		weekStart: 1,
		minViewMode: 1,
		todayBtn: "linked"
	})
	.on('changeDate', function(action){
		var year = action.date.getFullYear();
		var month = action.date.getMonth() + 1;
		var url_base = '/stechuhr/reports/month/';
		window.location = url_base + year + '/' + month + '/';
	});

/** vim: set ft=javascript ts=4 sw=4 : */
