G6Time = {
  data: new Object(),

  refresh: function() {
    $.ajax({
      url: '/gateway/json.php/LocatorService.getTickInfo/',
      dataType: 'json',
      success: function(data) {
        G6Time.data = data[0];
        if(G6Time.data.zarolt == 1) {
          if ( !$("#gal6time").hasClass('calc') ) {
            $("#gal6time").addClass('calc');
          }
        } else {
          if ( $("#gal6time").hasClass('calc') ) {
            $("#gal6time").removeClass('calc');
          }
        }

        //min = new Date().getMinutes();
        min = G6Time.data.currentMin;
        G6Time.data.min = min;

        $("#gal6time").children('div').html('GXT:'+G6Time.data.round+':'+G6Time.data.ticknum+':'+G6Time.data.min);
      }
    });
    setTimeout(G6Time.refresh, 20000);
  },

  init: function(round, ticknum, min) {
    if(!$('#gal6time')) return false;
    $("#gal6time").append('<div></div>');
    $("#gal6time").children('div').html('GXT:'+round+':'+ticknum+':'+min);
    G6Time.refresh();
  }
}