function ConvertFormToJSON(form){
    var array = $(form).serializeArray();
    var json = {};
    
    $.each(array, function() {
        json[this.name] = this.value || '';
    });
    
    return json;
}


$(document).ready(function() {
    $("#addNewField").click(function() {
        $.ajax({
            url: $SCRIPT_ROOT + "/shopping_list/modify_add_shopping_list",
            data: JSON.stringify({action: "add", url: window.location.href, form: ConvertFormToJSON("#addShoppingListForm")}),
            type: "POST",
            contentType: "application/json; charset=utf-8",
            success: function(result){
                console.log(result);
                console.log(result.url);
                window.location = result.url;
            }
        });
    });
});

