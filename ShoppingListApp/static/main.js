$(document).ready(function() {
    $("#addNewField").click(function() {
        console.log("---> in button click")
        var newInput = $("<input required type='text' value=''></input>")
            .attr("id", "newInput")
            .attr("name", "newInput")
        var item = $("<h1>new Item</h1>");
        $("#Shopping-list-class").append(item);
    })
});