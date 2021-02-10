# Django-Authorized

## Nasıl Kullanılır 

### views.py içerisinde allowed_perms decorator fonksiyonu
  
  views.py içerisinde bir fonksiyonun yapacağı işi allowed_perms'e parametre olarak belirtmeliyiz.
  allowed_perms Django'nun kendi Permissions modelini baz alır. Bu sebeple allowed_perms'e vereceğimiz parametreler belli bir standart içerisinde olmalıdır. Bu standart yapılacakİs_isinYapılacağıModel şeklinde olmalıdır. Modelimizin adını Post olarak kabul edersek Django default olarak bize **add_post view_post change_post delete_post** olmak üzere 4 işlem vermektedir. 
