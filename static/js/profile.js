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
	var $this = $(this);
	var $form = $this.parents('form');
	var $like = $form.find("button.like");
	var $unlike = $form.find("button.unlike");
	var $likesCount = $form.siblings(".likesCount");
	var likesCount = Number($likesCount.text());
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
					likesCount--;
				}
				else{
					$unlike.show();
					$like.hide();
					likesCount++;
				}

				$likesCount.text(likesCount);
			}
	});
	e.preventDefault();
});

