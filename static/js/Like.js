function Like(){
	this.likesCountSelector = null;
	this.clickedElement = null;
	this.save = function(){
		var $this = $(this.clickedElement);
		var $form = $this.parents('form');
		var $like = $form.find("button.like");
		var $unlike = $form.find("button.unlike");
		var $likesCount = $form.siblings(this.likesCountSelector);
		var $likesMessage = $likesCount.siblings('.likesMessage')
		var likesCount = Number($likesCount.text());
		var message;
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
				$likesMessage.text(response.message);
			}
		});

	}
}

