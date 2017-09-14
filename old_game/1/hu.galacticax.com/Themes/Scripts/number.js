function NumberConverter(evt)
{
   var charCode = (evt.which) ? evt.which : event.keyCode
         if (charCode > 31 && (charCode < 48 || charCode > 57))
            return false;

         return true;
}

function Planet_Search(id){
     var input_field2 = document.getElementById(id);
}

function Planet_Search1(id){
    var input_field3 = document.getElementById(id);
    NumberConverter(id)
}

function PSrefresh(id){
    var searchedplanet = document.getElementById(id);
    alert(searchedplanet)
}

function PSdelet(id){
    alert(id)
}

function PSsearchstart(id){
    var searchedplanet = document.getElementById(id);
    searchedplanet.style.display = "block";
    $.ajax({
        type: "POST",
        cache: false,
        url: "/ps.php",
        data: {
            proba: "ezaz"
        },
        success: function(data){
            $("#ps_data").html(data);
        },
        error: function(){
            
        },
        complete: function(){
            
        }
    });
}
function PSsearchstop(id){
    var searchedplanet = document.getElementById(id);
    searchedplanet.style.display = "none";
}

function clear_all(id){
    $("#sname").val('');
    $("#pr_coord").val('');
    $("#px_coord").val('');
    $("#py_coord").val('');
    $("#pz_coord").val('');
}

function Planet_Search(id){
     var input_field2 = document.getElementById(id);
}

function Planet_Search1(id){
    var input_field3 = document.getElementById(id);
    NumberConverter(id)
}

function PSrefresh(id){
    var searchedplanet = document.getElementById(id);
    alert(searchedplanet)
}

function PSdelet(id){
    alert(id)
}

function PSsearchstart(id){
    var searchedplanet = document.getElementById(id);
    searchedplanet.style.display = "block";
    $.ajax({
        type: "POST",
        cache: false,
        url: "/ps.php",
        data: {
            proba: "ezaz"
        },
        success: function(data){
            $("#ps_data").html(data);
        },
        error: function(){
            
        },
        complete: function(){
            
        }
    });
}
function PSsearchstop(id){
    var searchedplanet = document.getElementById(id);
    searchedplanet.style.display = "none";
}

function clear_all(id){
    $("#sname").val('');
    $("#pr_coord").val('');
    $("#px_coord").val('');
    $("#py_coord").val('');
    $("#pz_coord").val('');
}