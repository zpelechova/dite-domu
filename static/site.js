// pokud se zmeni hodnota ve formularovem poli verify_password_nr
     $('#verify_password_nr').change(function () {
        // ziskej hodnoty z formulare a uloz do promennych
        var password = $('#input_password_nr').val();
        var passwordVerify = $('#verify_password_nr').val();
        
        // pokud jsou hesla stejna
        if(password == passwordVerify){
          // najdi na stance div s id password-error a smaz z nej vsechen text
          $('#password-error').html('');
        }
        // poud se hesla lisi
        else{
          // najdi na stance div s id password-error a vloz do nej text
            $('#password-error').html('Zadane heslo se neshoduje!');
        }
     });

// pokud se zmeni hodnota ve formularovem poli verify_password_officer
$('#verify_password_officer').change(function () {
  // ziskej hodnoty z formulare a uloz do promennych
  var password = $('#input_password_officer').val();
  var passwordVerify = $('#verify_password_officer').val();
  
  // pokud jsou hesla stejna
  if(password == passwordVerify){
    // najdi na stance div s id pasword-error a smaz z nej vsechen text
    $('#password-error').html('');
  }
  // poud se hesla lisi
  else{
    // najdi na stance div s id pasword-error a vloz do nej text
      $('#password-error').html('Zadané heslo se neshoduje! Zkuste to prosím znovu.');
  }
});
