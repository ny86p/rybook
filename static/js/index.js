$('.left button').click(function(e){
    var email= $('.left input[name=email]').val();
    var password= $('.left input[name=password]').val();
    $.ajax({
      url: '/login',
      data: {
          email:email,
          password: password
      },
      type: 'post',
      success: function(response){
        location.href = response.url
      },
      error: function(){
          window.alert('Failed Login')
      }
    });
    e.preventDefault();
});

$('.right button').click(function(e){
    e.preventDefault();
    var email= $('.right input[name=email]').val();
    var password= $('.right input[name=password]').val();
    var f_Name= $('.right input[name=f_Name]').val();
    var l_Name= $('.right input[name=l_Name]').val();
    var bday= $('.right input[name=bday]').val();
    if(!(email && f_Name && l_Name && bday && password)){
      window.alert("All fields are required");
      return;
    }
    $.ajax({
        url: '/submit_registration',
        data: {
            email:email,
            password: password,
            f_Name: f_Name,
            l_Name: l_Name,
            bday: bday
        },
        type: 'post',
        success: function(response){
          if(response.error){
            window.alert(response.error);
          }
          else if(response.url){
            location.href = response.url;
          }
        },
        error: function(){
            window.alert('Failed Register');
        }
    });
});