from django.db import models
from django.contrib.auth.models import User,Group

Gabungan_Cabang = (
    ('0','Per Gerai'),
    ('1','Gabungan'),
)

DATACABANG =(
    ('500','GABUNGAN'),('300','BANDUNG'),('301','JAKARTA'),('302','SUCI'),('303','DIPATIUKUR'),('304','BALUBUR'),
    ('306','GERLONG HILIR'),('307','KOPO/JAMIKA'),('308','CIBIRU'),('309','CIPACING'),('310','JATINANGOR'),('327','CIMAHI'),
    ('311','BUAH BATU'),('313','KORDON/CIWASTRA'),('314','CIHANJUANG'),('315','MARANATA'),
    ('316','KIARACONDONG'),('317','CIREBON PERJUANGAN'),('318','CIREBON '),('319','CIUMBELEUIT'),
    ('320','UJUNGBERUNG'),('322','BOJONGSOANG'),('323','CIJERAH'),('324','KATAPANG/KOPO SAYATI'),
    ('325','CIMINDI'),('326','CEMARA'),('329','LEWI GAJAH'),('330','GADAI NIGHT BALUBUR'),('331','GADAI NIGHT JAKARTA'),
    ('333','GADAI NIGHT DIPATIUKUR'),('328','GADAI NIGHT CIBIRU'),('332','TURANGGA'),('334','PADJAJARAN'),('335','AGEN KOPO'),
)

DATACABANG_GLPUSAT =(
    ('','-------'),('300','BANDUNG'),('301','JAKARTA'),('302','SUCI'),('303','DIPATIUKUR'),('304','BALUBUR'),
    ('306','GERLONG HILIR'),('307','KOPO'),('308','CIBIRU'),('309','CIPACING'),('310','JATINANGOR'),
    ('327','CIMAHI'),('311','BUAH BATU'),('313','KORDON'),('314','CIHANJUANG'),('315','MARANATA'),('316','KIARACONDONG'),
    ('317','CIREBON'),('319','CIUMBULEUIT'),('320','UJUNGBERUNG'),('322','BOJONGSOANG'),('323','CIJERAH'),('324','KATAPANG/KOPOSAYATI'),
    ('325','CIMINDI'),('326','CEMARA'),('332','TURANGGA'),('331','GADAI NIGHT JAKARTA'),('330','GADAI NIGHT BALUBUR'),
    ('329','GADAI NIGHT DIPATIUKUR'),('328','GADAI NIGHT CIBIRU'),('333','LEWIGAJAH'),('334','PADJAJARAN'),('335','AGEN KOPO'),
)

COA_KAS=(
    ('4','Kas Besar'),('5','Kas Teller 1'),('6','Kas Teler 2'),('7','Kas Jakarta'), ('8','Kas kecl'),
    ('609','Kas Suci'),('610','Kas Dipatiukur'),('611','Kas Balubur'),('612','Kas Gerlong GIRANG'),('613','Kas GERLONG HILIR'),('614','Kas kopo'),
    ('615','Kas cibiru'),('616','Kas cipacing'),('617','Kas JTN'),('618','Kas CMH'),('619','Kas BB'),('620','Kas Kordon'),('621','Kas Cihabjuang'),
    ('622','Kas MARANATA'),('623','Kas KIRCON'),('624','Kas CP'),('625','Kas CR'),
    ('626','Kas CMLT'),('627','kas UBER'),('628','Kas cws'),('648','Kas bojong soang'),('812','Kas PADJAJARAN'),('825','Kas AGEN KOPO'),
)

COA_KAS_BESAR=(
    ('4','Kas Besar'),
)

COA_BANK =(
    ('132','0'),('133','0'),('134','0'),('135','0'),('136','0'),('137','0'),('138','0'),('139','0'),
    ('140','0'),('141','0'),('142','0'),('143','0'),('144','0'),('145','0'),('146','0'),('147','0'),
    ('148','0'),('149','0'),('150','0'),('151','0'),('649','0'),('650','0'),('813','0'),('826','0'),
)

ID_BALIK =(
    ('1','0'),('2',0),('3',0),('4','0'),('6','0'),('7','0'),
    ('8','0'),('9',0),('10',0),('11','0'),('12','0'),('15','0'),
    ('17','0'),('19',0),('20',0),('21','0'),('22','0'),
)

JENIS_PENGELUARAN_DEBET =(
    ('GL_GL_CABANG','0'),('Pelunasan_gu_kasir_nilai_sblm_lebih_bl','0'),('Pencairan_kasir_kurang','0'),
    ('Pelunasan_gu_kasir_nilai_sblm_kurang_bol','0'),('Pencairan_kasir','0'),
)
####PENDAPATAN
JENIS_PENDAPATAN_KREDIT_FILTER =(
    ('Pelunasan_gu_kasir_nilai_sblm_lebih','0'),('Pelunasan_Gadai_Ulang_kasir','0'),('Pelunasan_gu_kasir_nilai_sblm_kurang','0'),
    ('Pelunasan_kasir','0'),('Pencairan_kasir','0'),('Pelunasan_gu_kasir_nilai_sblm_lebih_pol','0'),
    ('Pelunasan_gu_kasir_nilai_sblm_kurang_pdl','0'),('Pencairan_kasir_sisa','0'),
)
JENIS_PENDAPATAN_KREDIT=(
   ('GL_GL_PENAMBAHAN_KAS','0'),('GL_GL_PENAMBAHAN_BANK','0'),('Penjualan_lelang_kasir','0'),
)
####PENDAPATAN

#####PENGELUARAN
JENIS_PENGELUARAN_DEBET =(
    ('GL_GL_CABANG','0'),('Pelunasan_gu_kasir_nilai_sblm_lebih_bl','0'),('Pencairan_kasir_kurang','0'),
    ('Pelunasan_gu_kasir_nilai_sblm_kurang_bol','0'),('Pencairan_kasir','0'),
    ('Pelunasan_Gadai_Ulang_Kasir_nilai_pinjaman_lebih','0'),('Pelunasan_Gadai_Ulang_kasir_pinjaman_besar_tp','0'),
    ('Pelunasan_gu_kasir_nilai_sblm_lebih_tp','0'),('Pelunasan_gu_kasir_nilai_sblm_kurang','0'),    
)

JENIS_PENGELUARAN_KREDIT=(
    ('GL_GL_PENGELUARAN_KAS_PUSAT','0'),
)
JENIS_SALDO_YG_DISETORKAN =(
    ('GL_GL_PENGEMBALIAN_PUSAT','0'),
)
####PENGELUARAN

############REPORT POSTING JURNAL
JENIS_BANDING_PENCAIRAN =(
    ('Pelunasan_kasir','0'),('Pelunasan_gu_kasir_nilai_sblm_lebih','0'),
)

JENIS_PENCAIRAN_NON_FILTER =(
    ('Pencairan_kasir','0'),
)

JENIS_PENCAIRAN_NON_FILTER_DEBET=(
    ('Pelunasan_Gadai_Ulang_Kasir_nilai_pinjaman_lebih','0'),
    ('Pelunasan_Gadai_Ulang_kasir_pinjaman_besar_tp','0'),('Pelunasan_gu_kasir_nilai_sblm_lebih_tp','0'),
    ('Pelunasan_gu_kasir_nilai_sblm_kurang','0'),
)

JENIS_BANDING_SISA_TRANSAKSI =(
    ('Pelunasan_gu_kasir_nilai_sblm_lebih_pol','0'),('Pelunasan_gu_kasir_nilai_sblm_kurang_pdl','0'),('Pencairan_kasir_sisa','0'),
    ('Pelunasan_kasir','0'),
)

JENIS_BIAYA_GERAI = (
    ('GL_GL_CABANG','0'),('Pelunasan_gu_kasir_nilai_sblm_lebih_bl','0'),('Pencairan_kasir_kurang','0'),
    ('Pelunasan_gu_kasir_nilai_sblm_kurang_bol','0'),
)

JENIS_PENDAPATAN_GERAI_FILTER=(
    ('Pencairan_kasir','0'),('Pelunasan_kasir','0'),('Pelunasan_gu_kasir_nilai_sblm_lebih_pol','0'),
    ('Pelunasan_gu_kasir_nilai_sblm_kurang_pdl','0'),('Pencairan_kasir_sisa','0'),
)
JENIS_PENJUALAN =(
   ('Penjualan_lelang_kasir','0'),
)
############REPORT POSTTING JURNAL

###Pilihan DI Input SALDO

JENIS_DESKRIPSI =(
   ('SALDOKASGERAI','SALDOKASGERAI'),
   ('SALDOBANKGERAI','SALDOBANKGERAI'),
)

class Menu(models.Model):
    objects = models.Manager()
    nama = models.CharField(max_length=100)
    url_utama = models.CharField(max_length=100, blank=True, null=True)
    deskripsi = models.TextField(blank=True, null=True)
    akses_grup = models.ManyToManyField(Group, blank=True)
    status_aktif = models.BooleanField(default=True)

    class Admin:
        pass

    def __unicode__(self):
        return "%s" % self.nama

    class Meta:
        db_table = 'menu'
        verbose_name = 'Menu'
        verbose_name_plural = verbose_name

class MenuItem(models.Model):
    menu = models.ForeignKey(Menu)
    order = models.IntegerField()
    link_url = models.CharField(max_length=100, help_text='http://kspra.co.id')
    judul = models.CharField(max_length=100)
    login_required = models.BooleanField(default=True)
    user = models.ManyToManyField(User, blank=True)
    status_aktif = models.BooleanField(default=True)

    class Admin:
        pass

    class Meta:
        db_table = 'menuitem'
        verbose_name = 'MenuItem'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return "%s. %s" % (self.order, self.judul)
