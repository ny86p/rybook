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
	var $this = $(this);
	var $form = $this.parents('form');
	var $like = $form.find("button.like");
	var $unlike = $form.find("button.unlike");
	var data = {};
	data.itemId = $form.data('id');
	data.typeId = $form.data("type-id");
	$.ajax({
			type: "post",
			url: "/like",
			data: data,
			success: function(response){
				if(response.like === 0){
					$like.show();
					$unlike.hide();
				}
				else{
					$unlike.show();
					$like.hide();
				}
			}
	});
	e.preventDefault();
});

