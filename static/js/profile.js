$(".commentBar").keydown(function(e){
	if(e.which === 13){
		var $this = $(this);
		var data = {};
		data.itemId = $(this).parents('form').data('id');
		data.type = $(this).siblings('input[name=type]').val();
		data.comment = $(this).val();
		$.ajax({
			type: "post",
			url: "/comment",
			data: data,
			success: function(response){
				$(".commentSection").append(response.html);
				$this.val('');
			}
		});
		return false;
	} 
});

$("form.likeStatus button").click(function(e){
	var like = new window.Like();
	like.clickedElement = this;
	like.save();
	e.preventDefault();

});

$("form.likeComment button").click(function(e){
	var like = new window.Like();
	like.clickedElement = this;
	like.save();
	e.preventDefault();

});

