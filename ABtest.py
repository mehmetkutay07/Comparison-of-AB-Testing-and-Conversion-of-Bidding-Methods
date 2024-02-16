#####################################################
# AB Testi ile BiddingYöntemlerinin Dönüşümünün Karşılaştırılması
#####################################################

#####################################################
# İş Problemi
#####################################################

# Facebook kısa süre önce mevcut "maximumbidding" adı verilen teklif verme türüne alternatif
# olarak yeni bir teklif türü olan "average bidding"’i tanıttı. Müşterilerimizden biri olan bombabomba.com,
# bu yeni özelliği test etmeye karar verdi veaveragebidding'in maximumbidding'den daha fazla dönüşüm
# getirip getirmediğini anlamak için bir A/B testi yapmak istiyor.A/B testi 1 aydır devam ediyor ve
# bombabomba.com şimdi sizden bu A/B testinin sonuçlarını analiz etmenizi bekliyor.Bombabomba.com için
# nihai başarı ölçütü Purchase'dır. Bu nedenle, istatistiksel testler için Purchasemetriğine odaklanılmalıdır.




#####################################################
# Veri Seti Hikayesi
#####################################################

# Bir firmanın web site bilgilerini içeren bu veri setinde kullanıcıların gördükleri ve tıkladıkları
# reklam sayıları gibi bilgilerin yanı sıra buradan gelen kazanç bilgileri yer almaktadır.Kontrol ve Test
# grubu olmak üzere iki ayrı veri seti vardır. Bu veri setleriab_testing.xlsxexcel’ininayrı sayfalarında yer
# almaktadır. Kontrol grubuna Maximum Bidding, test grubuna AverageBiddinguygulanmıştır.

# impression: Reklam görüntüleme sayısı
# Click: Görüntülenen reklama tıklama sayısı
# Purchase: Tıklanan reklamlar sonrası satın alınan ürün sayısı
# Earning: Satın alınan ürünler sonrası elde edilen kazanç



#####################################################
# Proje Görevleri
#####################################################

######################################################
# AB Testing (Bağımsız İki Örneklem T Testi)
######################################################

# 1. Hipotezleri Kur
# 2. Varsayım Kontrolü
#   - 1. Normallik Varsayımı (shapiro)
#   - 2. Varyans Homojenliği (levene)
# 3. Hipotezin Uygulanması
#   - 1. Varsayımlar sağlanıyorsa bağımsız iki örneklem t testi
#   - 2. Varsayımlar sağlanmıyorsa mannwhitneyu testi
# 4. p-value değerine göre sonuçları yorumla
# Not:
# - Normallik sağlanmıyorsa direkt 2 numara. Varyans homojenliği sağlanmıyorsa 1 numaraya arguman girilir.
# - Normallik incelemesi öncesi aykırı değer incelemesi ve düzeltmesi yapmak faydalı olabilir.




#####################################################
# Görev 1:  Veriyi Hazırlama ve Analiz Etme
#####################################################

import itertools
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
# !pip install statsmodels
import statsmodels.stats.api as sms
from scipy.stats import ttest_1samp, shapiro, levene, ttest_ind, mannwhitneyu, \
    pearsonr, spearmanr, kendalltau, f_oneway, kruskal
from statsmodels.stats.proportion import proportions_ztest

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', 10)
pd.set_option('display.float_format', lambda x: '%.5f' % x)

# Adım 1:  ab_testing_data.xlsx adlı kontrol ve test grubu verilerinden oluşan veri setini okutunuz. Kontrol ve test grubu verilerini ayrı değişkenlere atayınız.
df_control = pd.read_excel("C:\\Users\\kdund\\PycharmProjects\\MiuulProject\\datasets\\ab_testing.xlsx", sheet_name="Control Group", engine="openpyxl")
df_test = pd.read_excel("C:\\Users\\kdund\\PycharmProjects\\MiuulProject\\datasets\\ab_testing.xlsx", sheet_name="Test Group", engine="openpyxl")


# Adım 2: Kontrol ve test grubu verilerini analiz ediniz.

df_control.head()
df_control.shape
df_control.isnull().sum() # Değişkenlerdeki null değerlerin kontrolü

df_test.head()
df_test.shape
df_test.isnull().sum() # Değişkenlerdeki null değerlerin kontrolü



# Adım 3: Analiz işleminden sonra concat metodunu kullanarak kontrol ve test grubu verilerini birleştiriniz.

df_combined = pd.concat([df_control, df_test], ignore_index=True)
df_combined.head()



#####################################################
# Görev 2:  A/B Testinin Hipotezinin Tanımlanması
#####################################################

# Adım 1: Hipotezi tanımlayınız.

# H0: M1 = M2
# H1: M1 != M2

# Adım 2: Kontrol ve test grubu için purchase(kazanç) ortalamalarını analiz ediniz

df_control["Purchase"].mean()
df_test["Purchase"].mean()


#####################################################
# GÖREV 3: Hipotez Testinin Gerçekleştirilmesi
#####################################################

######################################################
# AB Testing (Bağımsız İki Örneklem T Testi)
######################################################


# Adım 1: Hipotez testi yapılmadan önce varsayım kontrollerini yapınız.Bunlar Normallik Varsayımı ve Varyans Homojenliğidir.

# Kontrol ve test grubunun normallik varsayımına uyup uymadığını Purchase değişkeni üzerinden ayrı ayrı test ediniz

# H0: Normal dağılım varsayımı sağlanmaktadır.
# H1:..sağlanmamaktadır.

test_stat, pvalue = shapiro(df_control["Purchase"].values)
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))

test_stat, pvalue = shapiro(df_test["Purchase"].values)
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))



# H0: Varyanslar Homojendir
# H1: Varyanslar Homojen Değildir

test_stat, pvalue = levene(df_control["Purchase"].values,
                           df_test["Purchase"].values)
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))


# Adım 2: Normallik Varsayımı ve Varyans Homojenliği sonuçlarına göre uygun testi seçiniz

test_stat, pvalue = ttest_ind(df_control["Purchase"].values,
                              df_test["Purchase"].values,
                              equal_var=True)

print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))

# Adım 3: Test sonucunda elde edilen p_value değerini göz önünde bulundurarak kontrol ve test grubu satın alma
# ortalamaları arasında istatistiki olarak anlamlı bir fark olup olmadığını yorumlayınız.



##############################################################
# GÖREV 4 : Sonuçların Analizi
##############################################################

# Adım 1: Hangi testi kullandınız, sebeplerini belirtiniz.

# Shapiro testine bakıldığında normallik varsayımı sağlanıyor.
# Levene testine baktığımızda da varjans homojenliği sağlanmış durumdadır.
# Her iki varsayım da sağlandığı için parametrik T-Testini kullanabiliriz


# Adım 2: Elde ettiğiniz test sonuçlarına göre müşteriye tavsiyede bulununuz.

# H0 reddedilemez p-değeri = 0,3493 < 0,05 değildir
#
# H0: M1 = M2 - İki grup arasında istatistiksel olarak anlamlı bir fark yok.
# Yani maksimum teklif kullanımı ile ortalama teklif kullanımı arasında gelirlerimizde anlamlı bir fark yaratmadı.

"""
İstatistiksel olarak anlamlı bir fark olmasa da, her iki stratejiyi daha geniş bir bağlamda değerlendirebiliriz. 
Belki de gelir farkı istatistiksel olarak anlamlı olmasa da, başka açılardan stratejilerin kullanımı değerlendirilebilir.
Veri setindeki purchase,click,impressions ve earning değişkenlerini beraber değerlendirmek önemli olabilir.
Ayrıca bu değişkenlerden yola çıkılarak dönüşüm oranları da hesaplanıp değişken olarak veri setine eklenebilir.

Belki de test dönemi boyunca gelirlerde bir değişim olmamıştır, ancak uzun vadeli dönemde stratejilerin performansı değişebilir. 
Stratejiler uzun vadeli olarak da değerlendirilebilir.
"""