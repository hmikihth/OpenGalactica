G6Time = {
  TM: null,
  round: 0,
  tick: 0,
  minute: 0,
  calulate: false,

  refresh: function() {
    clearTimeout(G6Time.TM);
    min = new Date().getMinutes();
    G6Time.minute = (min < 10) ? '0'+min:min;

    G6Time.runTickChk();
    time = $("#gal6time").children('div').html('G6T:'+G6Time.round+':'+G6Time.tick+':'+G6Time.minute);
    G6Time.TM = setTimeout(G6Time.refresh, 20000);
  },

  runTickChk: function() {
    $.ajax({
      url: '/gateway/json.php/LocatorService.getTickInfo/',
      success: function(data) {
        calc = data.match(/"zarolt":([0-9])/)[1] == '1';
        if(calc != G6Time.calulate) {
          if(calc) {
            $("#gal6time").addClass('calc');
          }
          else {
            $("#gal6time").removeClass('calc');
          }
          G6Time.tick = data.match(/"ticknum":"([0-9]+)"/)[1];
        }
        G6Time.calulate = calc;
      }
    });
  },

  init: function(round,tick,min) {
    if(!$('#gal6time')) return false;
    G6Time.round = round;
    G6Time.tick = tick;
    G6Time.min = min;

    if(jQuery.fn.flash.hasFlash.playerVersion().match(/([1-9])/)) {
      G6Time.disabelJS();
      $('#gal6time').flash(
      {
        src: '/Themes/flash/gal6Time.swf',
        width: 195,
        height: 30,
        wmode: 'transparent',
        flashvars: {round: G6Time.round, tick: G6Time.tick, minute: G6Time.minute, msg: '<t>Gal6 Time Ticker Message</t>'}
        // flashvars: {round: 9, tick: 0, minute: 0}
      },
      {
        update: false,
        version: '9,0,115',
        expressInstall: true
      });
    }
    else {
      $("#gal6time").append('<div></div>');
      G6Time.refresh();
    }
  },

  disabelJS: function() {
    if($("#gal6time").children("div")) {
      $("#gal6time").children("div").hide();
    }
    clearTimeout(G6Time.TM);
  }
}