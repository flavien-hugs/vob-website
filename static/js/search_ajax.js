$(function() {
    
    var searchForm = $('#search-form');

    $('#search').keyup(function (e) {
        e.preventDefault();

        $.ajax({
            type: searchForm.attr('method'),
            url: searchForm.attr('action'),
            data: {
                'search': $('#search').val().toLowerCase(),
                'csrfmiddlewaretoken': $("input[name=csrfmiddlewaretoken]").val()
            },
            success: searchSuccessResponse,
            dataType: 'html'
        });
    });
});

function searchSuccessResponse(data, textStatus, XHR)
{
    $('#search-results-list').html(data);
}
