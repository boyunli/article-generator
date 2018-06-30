$(document).ready(function () {

    $("#search-form").submit(function (event) {

        //stop submit the form, we will post it manually.
        event.preventDefault();

        fire_ajax_submit();

    });

});

function fire_ajax_submit() {

    var search = {}
    search["keyword"] = $("#keyword").val();
    search["wechat"] = $("#wechat").val();
    search["category"] = $("#category").val();
    // search["category"] = "手表";

    $("#btn-search").prop("disabled", true);

    $.ajax({
        type: "POST",
        contentType: "application/json",
        url: "/search",
        data: JSON.stringify(search),
        dataType: 'json',
        cache: false,
        timeout: 600000,
        success: function (data) {

            // var newsContent = "<h4>伪原创列表:</h4><pre>"
            var newsContent = "";
            //     + JSON.stringify(data, null, 4) + "</pre>";
            // $('#feedback').html(json);
            //
            var json = data.result
            console.log("json : ", json);
            $.each(json, function (i, obj) {
                newsContent = newsContent + "<article class=\"format-standard type-post hentry clearfix\">";
                newsContent = newsContent + "<header class=\"clearfix\"><h3 class=\"post-title\"><a href=\"#\">";
                newsContent = newsContent + obj.title;
                newsContent = newsContent + "</a></h3><div class=\"post-meta clearfix\">";
                newsContent + newsContent + "<span class=\"date\">25 Feb, 2013</span>";
                newsContent = newsContent + "<span class=\"category\"><a href=\"#\" title=\"news tag\">";
                newsContent = newsContent + obj.tag;
                newsContent = newsContent + "</a></span></div></header><p>"
                newsContent = newsContent + obj.content;
                newsContent = newsContent + "</p></article>"
            })
            $('#feedback').html(newsContent);

            console.log("SUCCESS : ", data);
            $("#btn-search").prop("disabled", false);

        },
        error: function (e) {

            var json = "<h4>Ajax Response</h4><pre>"
                + e.responseText + "</pre>";
            $('#feedback').html(json);

            console.log("ERROR : ", e);
            $("#btn-search").prop("disabled", false);

        }
    });


    function showNews(data) {

        $('#feedback').append("<h4>伪原创列表:</h4><pre>");
        for ( var i = 0, len = data.length; i < len; ++i) {
            var news = data[i];
            console.log(i + ":" + news);
            $('#feedback').append("<p>" + news.content + "</p>");
        }
    }
}