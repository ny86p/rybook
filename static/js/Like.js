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
		debugger
		$.ajax({
			type: "post",
			url: "/like",
			data: data,
			success: function(response){
				if(response.like === 0){
					$like.show();
					$unlike.hide();
					likesCount--;
					debugger
					if(likesCount > 0)
						message = response.friend_likers + "and " +  likesCount + "others like this"
					else
						message = "No Likes";

				}
				else{
					$unlike.show();
					$like.hide();
					likesCount++;

					if(likesCount == 0)
						message = "No Likes";
					else if(likesCount == 1)
						message = "you  like this";
					else if(likesCount == 2)
						message = "you and 1 other like this";
					else
						message = "you and " + (likesCount - 1) + "others like this";
				}



				$likesCount.text(likesCount);
				$likesMessage.text(message);
			}
		});

	}
}

