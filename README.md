# Django-Authorized

## Nasıl Kullanılır 

### views.py içerisinde allowed_perms decorator fonksiyonu
  
  views.py içerisinde bir fonksiyonun yapacağı işi allowed_perms'e parametre olarak belirtmeliyiz.
  allowed_perms Django'nun kendi Permissions modelini baz alır. Bu sebeple allowed_perms'e vereceğimiz parametreler belli bir standart içerisinde olmalıdır. Bu standart yapılacakİs_isinYapılacağıModel şeklinde olmalıdır. Biz bu yapıya Django Permission'ın da dediği gibi **codename** diyeceğiz. Modelimizin adını Post olarak kabul edersek Django default olarak bize **add_post view_post change_post delete_post** olmak üzere 4 işlem vermektedir. Update, Edit gibi işlemler için **change_post** kullanılmaktadır.
  Örnek bir kullanım şu şekildedir;
  ```
  views.py
  
  @allowed_perms('change_post')
  def edit_post(request,pk):
    ...
    
    return
  ```
  allowed_perms 'in kullanılabilmesi için ```from user.decorator import allowed_perms``` komutunun views.py dosyası içerisinde olması gerekmektedir.

### Kullanım için bazı gereksinimler

  Bu yapıyı kullanabilmek için user modelinin oluşturulacağı model dosyası içerisinde Django'nun **Group** ve **Permission** modellerinin ilgili dosya içerisinde dahil edilmesi gerekmektedir ve user modelinin içerisinde Group modeline bağlanılacak bir **ForeignKey** alanı tanımlanmalıdır. Aynı zamanda **Permission** ve **Group** user app'inin views.py dosyası içerisinde de dahil edilmelidir.
  
  ```
models.py


from django.contrib.auth.models import Group, Permission
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
 
class User(AbstractBaseUser):
    group = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True, related_name='user')
    ...
```

Template hataları almamak için her kullanıcının bir gruba sahip olması gerekmektedir. Bu durumda default olarak kayıt olan her kullanıcıya bir grup ataması yapılmalıdır. Ayrıca bir grup silindiği taktirde o gruptaki tüm kullanıcılar aynı şekilde bir default gruba atanmalıdır ve bu default grubunun silinmesine kesinlikle izin verilmemelidir.
  Bu projedeki views.py dosyasında grup silindiğinde veya bir kullanıcı kayıt olduğunda otomatik olarak kullanıcıyı default bir gruba atama işlemi gerçekleştirilmektedir fakat bu atama için default bir grup oluşturmalı ve oluşturduğunuz grubun name bilgisini settings.py dosyası içerisinde **DEFAULT_GROUP** değişkenine atanmalıdır.
  
  ```
  settings.py
  
  
  DEFAULT_GROUP = 'Default'
  ```
 
  Yöneticinin bu gruplarda yetki düzenlemesi yaparken işini kolaylaştırmak adına bazı yetkilendirmeleri html sayfası içerisinde görüntülerken filtrelemeliyiz. Bunun için yine settings.py içerisinde **APPS = []** listesi içerisinde tıpkı **INSTALLED_APPS** de olduğu gibi oluşturduğumuz appsleri belirtmeliyiz. Şu unutulmamalıdır ki **APPS** listesi içerisine mutlaka **'auth'** değeri girilmelidir, aksi halde yönetici gruplardaki yetkilendirme ve grup yönetimi izinlerini göremez.
  
```
settings.py

APPS = [
    'auth',
    'sliders',
    'blogs',
    'user',
    'picture_storage',
]
```

### HTML Dosyası içerisinde filtreleme

Back end de filtreleme işlemini gerçekleştirdik fakat kullanıcının görmemesi gereken link ve butonlarıda HTML dosyası içerisinde filtrelemeliyiz. Bu durum için yine bu proje içerisindeki user appinin içerisinde bulunan templatetags dosyası içerisindeki **permission_helper.py** den faydalanacağız.

Bu filtreyi kullanabilmek için ilk olarak **settings.py** içerisinde bu filteryi tanımlamalıyız.

```
settings.py

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [ BASE_DIR / 'templates' ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],

            'libraries':{
                'permission_helper' : 'user.templatetags.permission_helper',
            }

        },
    },
]

```
Burada görüldüğü üzere filtremiz **libraries** sözlük yapısı içerisinde tanımlanmıştır. Artık HTML dosyası içerisinde ```{% load permission_helper %}``` şeklinde filtremiz dahil edilerek kullanılabilir.

#### permission_helper kullanımı
permission_helper içerisinde **dropdown_filter** ve **is_authorized** olmak üzere 2 adet filtre barındırmaktadır.
Bu filtrelerden ilk olarak **is_authorized** filtresinin kullanımına bakalım.

##### is_authorized
Bu filtre 2 parametre almaktadır ve amacı kullanıcının erişim yetkisi olmadığı sayfa linkerlini veya butonları görmesini engellemektedir. Bu filtrenin ilk parametresi user objesi, ikinci parametresi ise link veya butonun yapacağı işin **Permission** daki codename karşılığıdır.

```
in HTML file

{% load permission_helper %}
<html>

{% if request.user|is_authorized:'delete_post' %}
<a href="{% url 'delete-post' pk %}" class="btn btn-danger">Delete Post </a>
{% endif %}

</html>
```
Yukarıdaki örnekte görüldüğü üzere Delete Post butonunu sadece Post modeli üzerinde silme yetkisi olan kullanıcılar görebilecektir.

##### dropdown_filter
Bu filtre, kullanıcı bir dropdown veya benzeri bir menü altında görebileceği hiç bir tag olmazsa bu tagı da filtrelemek için kullanılacak bir filtredir.

Örnek bir senaryo düşünürsek;
Bir dropdown menümüz olduğunu ve bunun altında View Post, Add Post ve Add Category şeklinde 3 adet link düşünelim ve giriş yapmış kullanıcının bu 3 alanda da bir yetkisi olmadığını varsayalım. Bu durumda içerisi boş bir dropdown menümüz olacaktır. Bu durumu engellemek için **dropdown_filter** kullanılmalıdır. Bu filtrede tıpkp **is_authorized** gibi iki adet parametre almaktadır. Bunlardan ilki User objesi ikinci parametre ise dropdown menünün altında tüm link veya butonların iş.

```
in HTML file

{% load permission_helper %}
<html>

{% if request.user|dropdown_filter:'add_category add_myblog view_myblog' %}
<ul class="nav nav-treeview" style="display: none;">
{% if request.user|is_authorized:'add_category' %}
  <li class="nav-item">
    <a href="{% url 'blog-category' %}" class="{% if nbar == 'blog-category' %} nav-link active {% else %} nav-link {% endif %}">
      <i class="far fa-circle nav-icon"></i>
      <p>Kategori</p>
    </a>
  </li>
  {% endif %}
  {% if request.user|is_authorized:'add_myblog' %}          
  <li class="nav-item">
    <a href="{% url 'blog-add' %}" class="{% if nbar == 'blog-add' %} nav-link active {% else %} nav-link {% endif %}">
      <i class="far fa-circle nav-icon"></i>
      <p>Blog ekle</p>
    </a>
  </li>
  {% endif %}
  {% if request.user|is_authorized:'view_myblog' %}
  <li class="nav-item">
    <a href="{% url 'blog-list' %}" class="{% if nbar == 'blog-list' %} nav-link active {% else %} nav-link {% endif %}">
      <i class="far fa-circle nav-icon"></i>
      <p>Blog Listele</p>
    </a>
  </li>
  {% endif %}
</ul>
{% endif %}

</html>
```

Bu filtre sayesinde içi boş dropdown menülerin görüntülenmesi engellenmektedir.
