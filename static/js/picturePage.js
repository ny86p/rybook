$(".commentBar2").keydown(function(e){
	if(e.which == 13){
		e.preventDefault();
		var $this = $(this);
		var data = {
			itemId: $(this).parents('form').data('id'),
			type: $(this).siblings('input[name=type]').val(),
			comment: $(this).val()
		};
		$.ajax({
			type: "post",
			url: "/comment",
			data: data,
			success: function(response){
				$(".picComments").append(response.html);
				$this.val('');
			}
		});
	}

});

$("form.likePicture button").click(function(e){
	var like = new Like();
	like.likesCountSelector = ".picLikeCount";
	like.clickedElement = this;
	like.save();
	e.preventDefault();
});

