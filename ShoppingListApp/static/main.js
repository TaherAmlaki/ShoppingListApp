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
            data: JSON.stringify({
                action: "add", 
                url: window.location.href, 
                form: ConvertFormToJSON("#addShoppingListForm")
            }),
            type: "POST",
            contentType: "application/json; charset=utf-8",
            success: function(result){
                window.location = result.url;
            }
        });
    });

    $('[id*="removeItem-"]').click(function(){
        var itemInd = $(this).attr('id').replace('removeItem-','');
        $.ajax({
            url: $SCRIPT_ROOT + "/shopping_list/modify_add_shopping_list",
            data: JSON.stringify({
                action: "remove", 
                url: window.location.href, 
                form: ConvertFormToJSON("#addShoppingListForm"),
                itemIndex: itemInd
            }),
            type: "POST",
            contentType: "application/json; charset=utf-8",
            success: function(result){
                window.location = result.url;
            }
        });
    });
});

