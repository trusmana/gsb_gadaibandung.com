from django.db import models
from django.db.models import Sum
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.contrib.auth.models import User
from datetime import datetime
import datetime
import calendar
import decimal
from dateutil.relativedelta import *
from gadai.appgadai.templatetags.number_format import number_format
from gadai.appkeuangan.models import *
from datetime import timedelta
from django.conf import settings
AUTH_USER_MODEL = getattr(settings, 'AUTH_USER_MODEL', User)

JENIS_AGUNAN = (
    ('1','HP'),('2','LAPTOP'),('3','KAMERA'),('4','PS'),('5','LCD'),('6','MOTOR'),('7','MOBIL'),
    )

CHOICES_PRODUK_PARAM =(
    ('1','1 Minggu'),('2','2 Minggu'),('3','3 Minggu'),('4','4 Minggu'),('5','1 Bulan'),('6','2 Bulan'),
    ('7','3 Bulan'),    
)

GERAI_KEMBALI =(('','---------'),
    ('0','PUSAT'),('1','JAKARTA'),('2','SUCI'),('3','DIPATIUKUR'),('4','BALUBUR'),
    ('5','GERLONG HILIR'),('6','KOPO'),('7','CIBIRU'),('8','CIPACING'),('9','JATINANGOR'),
    ('10','CIMAHI'),('12','BUAHBATU'), ('15','MARANATA'),
    ('17','CIREBON PERJUANGAN'),('19','CIUMBULEUIT'),('20','UJUNGBERUNG'),('21','CIWASTRA'),('22','BOJONGSOANG')
)

GERAI_PILIH =(
    ('1','PUSAT'),('2','JAKARTA'),('3','SUCI'),('4','DIPATIUKUR'),('5','BALUBUR'),
    ('7','GERLONG HILIR'),('8','KOPO'),('9','CIBIRU'),('10','CIPACING'),('11','JATINANGOR'),
    ('12','CIMAHI'),('13','BUAHBATU'), ('16','MARANATA'),
    ('18','CIREBON PERJUANGAN'),('19','CIUMBULEUIT'),('20','UJUNGBERUNG'),('21','CIWASTRA'),('22','BOJONGSOANG')
)


STATUS = (
    ('1','CAIR'),
    ('2','NONE CAIR'),
)

JENIS_TRANSAKSI = (
    ('1','KAS'),
    ('2','BANK'),
)

STATUS_PENCAIRAN_NASABAH=(
    ('0','PENCAIRAN BARU'),
    ('1','PENCAIRAN GADAI ULANG'),
    
)
class KasirGeraiPelunasan(models.Model):
    kasir_lunas = models.OneToOneField('AkadGadai',null=True, blank=True)
    status = models.CharField(max_length=1, choices=STATUS)
    tanggal = models.DateField()
    nilai_pembulatan_lunas = models.DecimalField(max_digits=12,decimal_places=2,default=0,null=True,blank=True)
    selisih_lunas = models.DecimalField(max_digits=12,decimal_places=2,default=0,null=True,blank=True)
    jenis_transaksi_lunas = models.CharField(max_length=1, choices=JENIS_TRANSAKSI)
    coa_sisa = models.CharField(max_length=30,null =True,blank=True)
    val_lunas = models.CharField(max_length = 3, null =True, blank=True)
    nilai_lunas = models.DecimalField(max_digits=12,decimal_places=2,default=0,null=True,blank=True)
    sisa_bayar_lunas = models.DecimalField(max_digits=12,decimal_places=2,default=0,null=True,blank=True)
    rek_tab = models.CharField(max_length=50,null =True,blank=True)
    nilai_titipan = models.DecimalField(max_digits=12,decimal_places=2,default=0,null=True,blank=True)
    cu = models.ForeignKey(User, related_name='+', editable=False, null=True, blank=True)
    mu = models.ForeignKey(User, related_name='+', editable=False, null=True, blank=True)

    class Meta:
        db_table = 'kasirgeraipelunasan'
        verbose_name = 'KasirGeraiPelunasan'
        verbose_name_plural = verbose_name
   
    def get_absolute_url(self):
        return "/kasirgeraipelunasan/" % self.id

    def kwlunas_validasi(self):
        return "KL %s 21.03.01 %s 11.01.04 %s WIB %s" % ((self.kasir_lunas.norek()),self.nilai_lunas,self.kasir_lunas.mdate,(str(self.kasir_lunas.gerai.init_cabang))) 

class KasirGerai(models.Model):
    kasir = models.OneToOneField('AkadGadai',null=True, blank=True)
    kasir_lunas = models.OneToOneField('Pelunasan',null=True,blank=True)
    status = models.CharField(max_length=1, choices=STATUS)
    tanggal = models.DateField()
    nilai_pembulatan = models.DecimalField(max_digits=12,decimal_places=2,default=0,null=True,blank=True)
    nilai_pembulatan_lunas = models.DecimalField(max_digits=12,decimal_places=2,default=0,null=True,blank=True)
    selisih = models.DecimalField(max_digits=12,decimal_places=2,default=0,null=True,blank=True)
    selisih_lunas = models.DecimalField(max_digits=12,decimal_places=2,default=0,null=True,blank=True)
    jenis_transaksi = models.CharField(max_length=1, choices=JENIS_TRANSAKSI)
    coa_sisa = models.CharField(max_length=30,null =True,blank=True)
    val = models.CharField(max_length = 3, null =True, blank=True)
    val_lunas = models.CharField(max_length=3,null=True,blank=True)
    cu = models.ForeignKey(User, related_name='c_kasirgerai', editable=False, null=True, blank=True)
    mu = models.ForeignKey(User, related_name='m_kasirgerai', editable=False, null=True, blank=True)
    nilai = models.DecimalField(max_digits=12,decimal_places=2,default=0,null=True,blank=True)
    sisa_bayar = models.DecimalField(max_digits=12,decimal_places=2,default=0,null=True,blank=True)

    nilai_lunas = models.DecimalField(max_digits=12,decimal_places=2,default=0,null=True,blank=True)
    sisa_bayar_lunas = models.DecimalField(max_digits=12,decimal_places=2,default=0,null=True,blank=True)
    tanggal_lunas = models.DateField(null=True, blank=True)
    jenis_transaksi_lunas = models.CharField(max_length=1, choices=JENIS_TRANSAKSI, null=True, blank=True)
    rek_tab = models.CharField(max_length=50,null =True,blank=True)

    class Meta:
        db_table = 'kasirgerai'
        verbose_name = 'KasirGerai'
        verbose_name_plural = verbose_name

    def get_absolute_url(self):
        return "/kasirgerai/" % self.id

    def __unicode__(self):
        return "%s-%s-%s" %(self.kasir.agnasabah.nama, self.kasir, self.id)


    def slip_validasi(self):
        sekarang=self.tanggal
        h=sekarang.day
        m=sekarang.month
        y=sekarang.year
        if self.selisih >= 0:
            return "|%s|%s|%s|%s|%s|%s" % ((self.kasir.mdate),(str(self.kasir.gerai.init_cabang)),self.nilai_pembulatan,self.kasir.nocoa_kas,self.selisih,self.coa_sisa)
        elif self.selisih < 0:
            return "|%s|%s|%s|%s|%s|%s" % ((self.kasir.mdate),(str(self.kasir.gerai.init_cabang)),self.nilai_pembulatan,self.kasir.nocoa_kas,(self.selisih * (-1)),self.coa_sisa)

def add_months(dt,months):
    month = dt.month - 1 + months
    year = dt.year + month / 12
    month = month % 12 + 1
    day = min(dt.day,calendar.monthrange(year,month)[1])
    return dt.replace(year=year, month=month, day=day)

JANGKA_WAKTU = (
    ('0','--- PILIH ---'),
    ('15','2 minggu'),
    ('31','31'),
)

JANGKA_WAKTU_KENDARAAN = (
    ('0','--- PILIH ---'),
    ('1','1'),
    #('2','2'),
    #('3','3'),
    #('4','4'),
)  

MERK_KENDARAAN_CHOICES = (
    ('0','--- PILIH ---'),
    ('1','HONDA'),
    ('2','SUZUKI'),
    ('3','TOYOTA'),
    ('4','NISAN'),
    ('5','MITSUBISHI'),
    ('6','DAIHATSHU'),
    ('7','YAMAHA'),
    ('8','CHEVROLET'),
    ('9','HYUNDAI'),
    ('10','KAWASAKI'),
    ('11','MAZDA'),
    ('12','PIAGGIO'),
    ('13','KIA'),
    ('14','FORD'),
    ('15','ISUZU'),
) 

GERAI = (
    ('1','1'),('2','2'),
    ('3','3'),('4','4'),
    ('5','5'),('6','6'),
    ('7','7'),('8','8'),
    ('9','9'),('10','10'),
    ('11','11'),('12','12'),    
    ('13','13'),('14','14'),
    ('15','15'),('16','16'),
    ('17','17'),('18','18'),
    ('19','19'),('20','20'),
    ('21','21'),('22','22'),
    ('23','23'),('24','24'),
)

AKUN = (
    ('3','3'),('4','4'),('5','5'),('6','6'),('7','7'),('8','8'),('131','131'),('132','132'),('133','133'),('134','134'),('135','135'),('136','137'),('138','138'),('139','139'),
    ('139','139'),('140','140'),('141','141'),('142','142'),('143','143'),('144','144'),('145','145'),('146','146'),('147','147'),('148','149'),('150','150'),('151','151'),
    ('152','152'),('153','153'),('154','154'),('155','155'),('156','156'),('157','157'),('158','158'),('159','159'),('160','160'),('161','161'),('162','162'),
    ('163','163'),('164','164'),('165','165'),('166','166'),('167','167'),('168','168'),('169','169'),('170','170'),('171','171'),('172','172'),('173','173'),
    ('174','174'),('175','175'),('176','176'),('177','177'),('178','178'),('178','178'),('179','179'),('180','180'),('181','181'),('182','182'),('183','183'),
    ('184','184'),('185','185'),('186','186'),('187','187'),('188','188'),('189','189'),('190','190'),('191','191'),('192','192'),('193','193'),('194','194'),
    ('195','195'),('196','196'),('197','197'),('198','198'),('199','199'),('200','200'),('201','201'),('202','202'),('203','203'),('204','204'),('205','205'),
    ('206','206'),('207','207'),('208','208'),('209','209'),('210','210'),('211','211'),('212','212'),('213','213'),('214','214'),('215','215'),('216','216'),
    ('217','217'),('218','218'),('219','219'),('220','220'),('221','221'),('222','222'),('223','223'),('224','224'),('225','225'),('226','226'),('227','227'),
    ('228','228'),('229','229'),('230','230'),('231','231'),('232','232'),('233','233'),('234','234'),('235','235'),('243','243'),('244','244'),('245','245'),
    ('246','246'),('247','247'),('248','248'),('249','249'),('250','250'),('251','251'),('252','252'),('253','253'),('254','254'),('255','255'),('256','256'),
    ('257','257'),('258','258'),('259','259'),('260','260'),('265','265'),('266','266'),('267','267'),('268','268'),('269','269'),('270','270'),('271','271'),
    ('272','272'),('273','273'),('274','274'),('286','286'),('287','287'),('288','288'),('293','293'),('294','294'),('295','295'),('297','297'),('298','298'),
    ('307','307'),('308','308'),('311','311'),('312','312'),('313','313'),('314','314'),('315','315'),('316','316'),('317','317'),('318','318'),('319','319'),
    ('320','320'),('321','321'),('322','322'),('323','323'),('324','324'),('325','325'),('326','326'),('327','327'),('328','328'),('329','329'),('330','330'),
    ('331','331'),('332','332'),('333','333'),('334','334'),('335','335'),('336','336'),('337','337'),('359','359'),('360','360'),('361','361'),('362','362'),
    ('363','363'),('364','364'),('365','365'),('366','366'),('367','367'),('368','368'),('369','369'),('370','370'),('371','371'),('372','372'),('373','373'),
    ('374','374'),('375','375'),('376','376'),('377','377'),('378','378'),('379','379'),('380','380'),('381','381'),('382','382'),('383','383'),('384','384'),
    ('385','385'),('386','386'),('387','387'),('388','388'),('389','389'),('390','390'),('390','390'),('390','390'),('390','390'),('390','390'),('390','390'),
    ('390','390'),('390','390'),('390','390'),('390','390'),('390','390'),('390','390'),('390','390'),('391','391'),('392','392'),('393','393'),('394','394'),
    ('394','394'),('395','395'),('396','396'),('397','397'),('398','398'),('399','399'),('400','400'),('401','401'),('402','402'),('403','403'),('404','404'),
    ('405','405'),('406','406'),('407','407'),('408','408'),('409','409'),('410','410'),('411','411'),('412','412'),('413','413'),('414','414'),('415','415'),
    ('416','416'),('417','417'),('418','418'),('419','419'),('420','420'),('429','429'),('430','430'),('431','431'),('432','432'),('439','439'),('440','440'),
    ('441','441'),('442','442'),('443','443'),('444','444'),('445','445'),('446','446'),('447','447'),('448','448'),('449','449'),('450','450'),('451','451'),
    ('452','452'),('453','453'),('454','454'),('455','455'),('456','456'),('457','457'),('458','458'),('459','459'),('460','460'),('461','461'),('462','462'),
    ('463','463'),('464','464'),('465','465'),('466','466'),('467','467'),('468','468'),('469','469'),('470','470'),('471','471'),('472','472'),('473','473'),
    ('474','474'),('475','475'),('476','476'),('477','477'),('478','478'),('479','479'),('480','480'),('481','481'),('482','482'),('483','483'),('484','484'),
    ('485','485'),('486','486'),('487','487'),('488','488'),('489','489'),('490','490'),('491','491'),('492','492'),('493','493'),('494','494'),('495','495'),
    ('496','496'),('497','497'),('498','498'),('499','499'),('500','500'),('501','501'),('502','502'),('503','503'),('504','504'),('505','505'),('506','506'),
    ('507','507'),('508','508'),('509','509'),('510','510'),('511','511'),('512','512'),('513','513'),('514','514'),('515','515'),('516','516'),('517','517'),
    ('518','518'),('519','519'),('520','520'),('521','521'),('522','522'),('523','523'),('524','524'),('525','525'),('526','526'),('527','527'),('528','528'),
    ('529','529'),('530','530'),('531','531'),('532','532'),('533','533'),('534','534'),('535','535'),('536','536'),('537','537'),('538','538'),('539','539'),
    ('540','540'),('541','541'),('542','542'),('543','543'),('544','544'),('545','545'),('546','546'),('547','547'),('548','548'),('549','549'),('550','550'),('551','551'),
    ('552','552'),('553','553'),('554','554'),('555','555'),('556','556'),('557','557'),('558','558'),('559','559'),('560','560'),('560','560'),('560','560'),
    ('561','561'),('562','562'),('563','563'),('564','564'),('565','565'),('595','595'),('596','596'),('597','597'),('598','598'),('599','599'),('600','600'),
    ('601','601'),('602','602'),('603','603'),('604','604'),('605','605'),('606','606'),('607','607'),('608','608'),('609','609'),('610','610'),
    ('611','611'),('612','612'),('613','613'),('614','614'),('615','615'),('616','616'),('617','617'),('618','618'),('619','619'),('620','620'),
    ('621','621'),('622','622'),('623','623'),('624','624'),('625','625'),('626','626'),('627','627'),('628','628'),('629','629'),('630','630'),
    ('631','631'),('648','648'),('649','649'),('635','635'),('636','637'),('638','638'),('684','684'),('685','685'),('686','686'),('687','687'),
    ('688','688'),('689','689'),('690','690'),('691','691'),('692','692'),('693','693'),('694','694'),('695','695'),('696','696'),('697','697'),
    ('698','698'),('699','699'),('700','700'),('701','701'),('702','702'),('703','673'),('704','704'),('705','705'),('706','706'),('707','707'),
    ('708','708'),('709','709'),('710','710'),('711','711'),('712','712'),('713','713'),('713','713'),('714','714'),('715','715'),('716','716'),
    ('717','717'),('718','718'),('719','719'),('720','720'),('721','721'),('722','722'),('730','730'),
)

KELAMIN = (
    ('0','---PILIH---'),
    ('Pria','Pria'),
    ('Wanita','Wanita'),
)

JENIS_PEKERJAAN =(
    ('1','PEGAWAI SWASTA'),
    ('2','PNS/TNI/POLRI'),
    ('3','PROFESI'),
    ('4','MAHASISWA/PELAJAR'),
    ('5','WIRASWASTA'),
    ('6','IBU RUMAH TANGGA'),
)

JENIS_DOKUMEN= (
    ('1','Photo copy KTP'),
    ('2','Faktur Pembelian'),
    ('3','Kartu Garasi'),
    ('4','Manual Book'),
    ('5','STNK'),
    ('6','BPKB'),
    ('7','SIM'),
)

JENIS_BARANG = (
    ('0','--- PILIH ---'),
    ('1','HP'),
    ('2','LAPTOP/NB'),
    ('3','KAMERA'),
    ('4','PS'),
    ('5','TV LCD'),
)

JENIS_KENDARAAN = (
    ('0','--- PILIH ---'),
    ('1','MOTOR'),
    ('2','MOBIL'),
)

TAHUN_KENDARAAN_CHOICES = (
    ('0','--- PILIH ---'),
    ('20','1990'),('25','1992'),('26','1995'),
    ('12','1996'),('10','1997'),('13','1998'),
    ('14','1999'),('15','2000'),('11','2001'),
    ('16','2002'),('17','2003'),('18','2004'),
    ('1','2005'), ('2','2006'), ('3','2007'),
    ('4','2008'), ('5','2009'), ('6','2010'),
    ('7','2011'), ('8','2012'), ('9','2013'),
    ('19','2014'),('21','2015'),('22','2016'),
    ('23','2017'),('24','2018'),('25','2019'),
)

RAK_CHOICES = (
    ('1','1'),
    ('2','2'),
    ('3','3'),
    ('4','4'),
    ('5','5'),
    ('6','6'),
    ('7','7'),
    ('8','8'),('9','9'),('10','10'),('11','11'),('12','12'),('13','13'),('14','14'),('15','15')
)

RUANGAN_CHOICES = (
    ('1','A'),
    ('2','B'),
    ('3','C'),
    ('4','D'),
    ('5','E'),
    ('6','1'),
    ('7','2'),
    ('8','3'),
    ('9','4'),
    ('16','5'),
    ('10','K1'),
    ('11','K2'),
    ('12','K3'),
    ('13','K4'),
    ('14','K5'),
    ('15','K6'),
)
LEMARI_CHOICES = (
    ('1','L1'),
    ('2','L2'),
    ('3','L3'),
    ('4','L4'),
    ('5','L5'),
    ('6','L6'),
    ('7','L7'),
    ('8','L8'),('9','L9'),('10','L10'),('11','L11'),('12','L12'),('13','L13'),('14','L14'),('15','L15'),
)
ROW_CHOICES = (
    ('1','1'),
    ('2','2'),
    ('3','3'),
    ('4','4'),
    ('5','5'),
    ('6','6'),
    ('7','7'),
)

JENIS_KEANGGOTAAN= (
    ('1','ANGGOTA'),
    ('2','NON ANGGOTA'),
)

CHOICES_BARANG=(
    ('1','ADA'),
    ('2','TIDAK ADA')
)

CHOICES_KONDISI_BARANG=(
    ('1','BAGUS SEKALI'),
    ('2','BAGUS'),
    ('3','CUKUP BAGUS'),
    ('4','SEDANG'),
    ('5','KURANG'),
)

BUKA_OTO =(
    ('99','KUNCI'),('0','BUKA')
)

CHOICES_JENIS_TRANSAKSI=(
    ('1','Elektronik'),
    ('2','Motor'),
    ('3','Mobil')
)

class Barang(models.Model):
    jenis_barang = models.CharField(max_length=4 ,choices=JENIS_BARANG, null =True, blank=True,default=0)
    merk = models.CharField(max_length=500)   
    type = models.CharField(max_length=500)
    sn = models.CharField(max_length=20)
    warna = models.CharField(max_length=200)
    tahun_pembuatan = models.CharField(max_length=10)
    bulan_produksi = models.CharField(max_length=10)   
    accesoris_barang1 = models.CharField(max_length=500)
    lampiran_dokumen = models.CharField(max_length = 2,choices =JENIS_DOKUMEN)
    barang_masuk= models.DateField(null=True, blank=True)
    barang_keluar= models.DateField(null=True, blank=True)
    ruangan = models.CharField(null=True, blank=True,max_length=2,choices=RUANGAN_CHOICES)
    no_rak =models.CharField(null=True, blank=True,max_length=2,choices=RAK_CHOICES)
    row = models.CharField(null=True, blank=True,max_length=2,choices=ROW_CHOICES)
    lemari = models.CharField(null=True, blank=True,max_length=2,choices=LEMARI_CHOICES)
    kolom = models.CharField(null=True, blank = True,max_length=2)
    ###form kendaraan
    jenis_kendaraan = models.CharField(max_length=4 ,choices=JENIS_KENDARAAN,default=0)
    merk_kendaraan = models.CharField(max_length=10,choices =MERK_KENDARAAN_CHOICES,null=True, blank=True,default=0)
    type_kendaraan =  models.CharField(max_length=100,default=0)
    no_polisi = models.CharField(max_length=15,default=0)
    no_rangka = models.CharField(max_length=200,default=0)
    no_mesin = models.CharField(max_length=200,default=0)
    tahun_pembuatan_kendaraan = models.CharField(max_length=10,choices =TAHUN_KENDARAAN_CHOICES,default=0)
    warna_kendaraan = models.CharField(max_length=200,default=0)
    no_bpkb = models.CharField(max_length=30,default=0)
    stnk_atas_nama = models.CharField(max_length=30,default=0)
    no_faktur = models.CharField(max_length=20,default=0)
    ####### update input barang 31 maret 2015
    fungsi_sistem = models.CharField(max_length = 70,null=True,blank=True)
    charger = models.CharField(max_length = 5, choices = CHOICES_BARANG)
    kondisi_charger = models.CharField(max_length = 5, choices = CHOICES_KONDISI_BARANG)
    batre = models.CharField(max_length = 5, choices = CHOICES_BARANG)
    kondisi_batre = models.CharField(max_length = 5, choices = CHOICES_KONDISI_BARANG)
    keybord= models.CharField(max_length = 5, choices = CHOICES_BARANG)
    kondisi_keybord = models.CharField(max_length = 5, choices = CHOICES_KONDISI_BARANG)
    cassing = models.CharField(max_length = 5, choices = CHOICES_BARANG)
    kondisi_cassing = models.CharField(max_length = 5, choices = CHOICES_KONDISI_BARANG)
    layar = models.CharField(max_length = 5, choices = CHOICES_BARANG)
    kondisi_layar = models.CharField(max_length = 5, choices = CHOICES_KONDISI_BARANG)
    password  = models.CharField(max_length = 5, choices = CHOICES_BARANG)
    password_barang  = models.CharField(max_length=150,null=True, blank=True)

    lensa  = models.CharField(max_length = 5, choices = CHOICES_BARANG)
    kondisi_lensa = models.CharField(max_length = 5, choices = CHOICES_KONDISI_BARANG)
    batre_kamera  = models.CharField(max_length = 5, choices = CHOICES_BARANG)
    kondisi_batre_kamera = models.CharField(max_length = 5, choices = CHOICES_KONDISI_BARANG)
    cassing_kamera  = models.CharField(max_length = 5, choices = CHOICES_BARANG)
    kondisi_cassing_kamera = models.CharField(max_length = 5, choices = CHOICES_KONDISI_BARANG)

    optik_ps  = models.CharField(max_length = 5, choices = CHOICES_BARANG)
    kondisi_optik_ps = models.CharField(max_length = 5, choices = CHOICES_KONDISI_BARANG)
    harddisk  = models.CharField(max_length = 5, choices = CHOICES_BARANG)
    kondisi_harddisk = models.CharField(max_length = 5, choices = CHOICES_KONDISI_BARANG)
    stick  = models.CharField(max_length = 5, choices = CHOICES_BARANG)
    kondisi_stick = models.CharField(max_length = 5, choices = CHOICES_KONDISI_BARANG)
    hdmi  = models.CharField(max_length = 5, choices = CHOICES_BARANG)
    kondisi_hdmi = models.CharField(max_length = 5, choices = CHOICES_KONDISI_BARANG)

    layar_tv = models.CharField(max_length = 5, choices = CHOICES_BARANG)
    kondisi_layar_tv = models.CharField(max_length = 5, choices = CHOICES_KONDISI_BARANG)
    remote = models.CharField(max_length = 5, choices = CHOICES_BARANG)
    kondisi_remote = models.CharField(max_length = 5, choices = CHOICES_KONDISI_BARANG)

    bpkb = models.CharField(max_length = 5, choices = CHOICES_BARANG,null=True,blank=True)
    stnk = models.CharField(max_length = 5, choices = CHOICES_BARANG,null=True,blank=True)
    faktur = models.CharField(max_length = 5, choices = CHOICES_BARANG,null=True,blank=True)
    gesek_nomesin = models.CharField(max_length = 5, choices = CHOICES_BARANG,null=True,blank=True)
    gesek_norangka = models.CharField(max_length = 5, choices = CHOICES_BARANG,null=True,blank=True)
    dus = models.CharField(max_length = 5, choices = CHOICES_BARANG,null=True,blank=True)
    tas = models.CharField(max_length = 5, choices = CHOICES_BARANG,null=True,blank=True)
    akad_ulang = models.IntegerField(null=True, blank=True,default=0)
    buka_tutup_gu = models.CharField(max_length = 5, choices = BUKA_OTO,null=True,blank=True)

    class Meta:
        db_table='barang'
        verbose_name = 'Barang'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return "%s-%s-%s-%s" %(self.id, self.merk, self.type, self.sn)

    def unicode__(self):
        return "%s-%s-%s-%s" %(self.id, self.merk, self.type, self.sn)

    def __unic__kendaraan__(self):
        return "%s-%s-%s-%s-%s-%s" %(self.get_jenis_kendaraan_display(), self.get_merk_kendaraan_display(), \
            self.type_kendaraan, self.no_rangka, self.no_mesin, self.id,)

    def get_absolute_url(self):
        return "/barang/"

    #def __unicode__(self):
        #return "%s - %s" %(self.merk,self.id,)

    def totallebih(self):
        a = self.akadgadai_set.all().count()
        return a

AKTIFASI_PARAMETER =(
    ('1','Non Aktif'),
    ('2','Aktif'),    
)

class ParameterAkadUlang(models.Model):
    jml_akad = models.IntegerField(null=True, blank=True)
    aktif = models.CharField(null=True, blank = True,max_length=200,choices=AKTIFASI_PARAMETER)
    tanggal = models.DateField(null=True, blank=True)

    jangka_waktu= models.CharField(max_length=4 ,choices=JANGKA_WAKTU, null=True,blank=True)
    jangka_waktu_kendaraan= models.CharField(max_length=4 ,choices=JANGKA_WAKTU_KENDARAAN, null=True,blank=True)
    jenis_transaksi = models.CharField(max_length=20 ,choices=CHOICES_JENIS_TRANSAKSI, null=True, blank=True)
    class Meta:
        db_table='parameterakadulang'
        verbose_name = 'ParameterAkadUlang'
        verbose_name_plural = verbose_name

BARANG_HISTORY_GU=(
    ('1','HP'),
    ('2','LAPTOP/NB'),
    ('3','KAMERA'),
    ('4','PS'),
    ('5','TV LCD'),
    ('6','MOTOR'),
    ('7','MOBIL'), 
)

class HistoryAkadUlang(models.Model):
    nama = models.CharField(max_length=75)
    norek = models.CharField(max_length=75)
    barang = models.CharField(max_length=500)
    id_barang = models.CharField(max_length=75)
    nilai_pinjaman = models.FloatField()
    jenis_barang = models.CharField(max_length=4 ,choices=BARANG_HISTORY_GU, null =True, blank=True,default=0)
    merk = models.CharField(max_length=700)   
    type = models.CharField(max_length=700)
    cu = models.ForeignKey(User, related_name='+',editable=False, null=True, blank=True)
    mu = models.ForeignKey(User, related_name='+',editable=False, null=True, blank=True)    

    class Meta:
        db_table='historyakadulang'
        verbose_name = 'HistoryAkadUlang'
        verbose_name_plural = verbose_name

class HistoryBarang(models.Model):
    agbarang = models.ForeignKey(Barang)
    tgl_barang_masuk = models.DateField(null=True, blank=True)
    tgl_barang_keluar = models.DateField(null=True, blank=True)
    ruang_barang = models.CharField(null=True, blank = True,max_length=200,choices=RUANGAN_CHOICES)
    lemari_barang = models.CharField(null=True, blank = True,max_length=200,choices=LEMARI_CHOICES)
    kolom_barang = models.CharField(null=True, blank = True,max_length=200)
    rak_barang = models.CharField(null=True, blank = True,max_length=200,choices=RAK_CHOICES)
    row_barang = models.CharField(null=True, blank = True,max_length=200,choices=ROW_CHOICES)
    cu = models.ForeignKey(User, related_name='+',editable=False, null=True, blank=True)
    mu = models.ForeignKey(User, related_name='+',editable=False, null=True, blank=True)    
    class Meta:
        db_table='historybarang'
        verbose_name = 'HistoryBarang'
        verbose_name_plural = verbose_name
        
    def __unicode__(self):
        return "%s-%s" %(self.id,self.agbarang.id)

STS_NSB=(
    ('1','WHITELIST'),
    ('2','BLACKLIST'),
)

class Nasabah(models.Model):
    nama = models.CharField(max_length=75)
    tgl_lahir = models.DateField(help_text="Tahun-Bulan-Tanggal", null=True)
    tempat = models.CharField(max_length=15)
    
    no_ktp = models.CharField(max_length= 16, null=True)
    alamat_ktp = models.CharField(max_length=300,null=True)
    no_rumah_ktp = models.CharField(max_length=10,null=True)
    rt_ktp = models.CharField(max_length=6,null=True)
    rw_ktp=models.CharField(max_length=6,null=True)
    telepon_ktp =models.CharField(max_length=30, null=True)
    hp_ktp =models.CharField(max_length=30, null=True)
    kelurahan_ktp = models.CharField(max_length=100,null=True)
    kecamatan_ktp = models.CharField(max_length=100,null=True)
    kotamadya_ktp = models.CharField(max_length=100,blank=True,null=True)
    kabupaten_ktp = models.CharField(max_length=100,blank=True,null=True)
    
    no_sim = models. CharField(max_length= 20, null=True, blank=True)
    alamat_sim = models.CharField(max_length=300,null=True, blank=True)
    rt_sim = models.CharField(max_length=6,null=True, blank=True)
    rw_sim=models.CharField(max_length=6,null=True, blank=True)
    kelurahan_sim = models.CharField(max_length=100,null=True, blank=True)
    kecamatan_sim = models.CharField(max_length=100,null=True, blank=True)
    ###domisili
    alamat_domisili = models.CharField(max_length=100,null=True)
    no_rumah_domisili = models.CharField(max_length=10,null=True)
    rt_domisili = models.CharField(max_length=6,null=True)
    rw_domisili=models.CharField(max_length=6,null=True)
    telepon_domisili =models.CharField(max_length=30, null=True)
    hp_domisili =models.CharField(max_length=30, null=True,blank=True)
    kelurahan_domisili = models.CharField(max_length=100,null=True)
    kecamatan_domisili = models.CharField(max_length=100,null=True)
    kotamadya_domisili = models.CharField(max_length=100,blank=True,null=True)
    kabupaten_domisili = models.CharField(max_length=100,blank=True,null=True)
    
    jenis_pekerjaan= models.CharField(max_length=20 ,choices=JENIS_PEKERJAAN)
    alamat_kantor = models.CharField(max_length=100)
    kode_pos = models.CharField(max_length = 10)
    telepon_kantor =models.CharField(max_length=30)
    email = models.CharField(max_length=30,blank=True)

    jenis_kelamin= models.CharField(max_length=10 ,choices=KELAMIN)
    cu = models.ForeignKey(User, related_name='c_nasabah', editable=False, null=True, blank=True)
    mu = models.ForeignKey(User, related_name='m_nasabah', editable=False, null=True, blank=True)
    cdate = models.DateTimeField(auto_now_add=True)
    mdate = models.DateTimeField(auto_now=True)
    jenis_keanggotaan = models.CharField(max_length=20 ,choices=JENIS_KEANGGOTAAN)
    # Data Pasangan
    nama_pasangan = models.CharField(max_length=30,blank=True,null=True)
    alamat_pasangan = models.CharField(max_length=100,blank=True,null=True)
    jekel_pasangan = models.CharField(max_length=25,choices=KELAMIN)
    tlp_pasangan = models.CharField(max_length=30,blank=True,null=True)
    no_rumah_pas = models.CharField(max_length=5,blank=True,null=True)
    no_rt_pas = models.CharField(max_length=6,blank=True,null=True)
    no_rw_pas = models.CharField(max_length=6,blank=True,null=True)
    status_nasabah = models.CharField(max_length=25,blank=True,null=True,choices = STS_NSB)
    klik_keanggotaan = models.CharField(max_length=25,blank=True,null=True)
    class Meta:
        db_table='nasabah'
        verbose_name = 'Nasabah'
        verbose_name_plural = verbose_name

    def akad_gadai(self):
        pn = 0
        for p in self.akadgadai_set.all():
            try:
                pn = p
            except:
                pass
            return pn
    akad_gadai = property(akad_gadai)

    def nilai_plafon(self):
        return sum([p.nilai for p in self.akadgadai_set.all()])
    nilai_plafon = property(nilai_plafon)

    def nomor_id_nasabah(self):
        pn = 0
        for p in self.akadgadai_set.all():
            try:
                pn = p.agnasabah.id
            except:
                pass
            return pn
        
    def __unicode__(self):
        return "%s-%s" %(self.nomor(),self.nama)

    def sn(self):
        pn = 0
        a = self.akadgadai_set.latest()
        for p in self.akadgadai_set.all():
            try:
                pn = p.barang.sn
            except:
                pass
            return pn
        
    def jenis_barang(self):
        pn = 0
        for p in self.akadgadai_set.all():
            try:
                pn = p.barang.jenis_barang
            except:
                pass
            return pn
        
    def jenis_transaksi(self):
        pn = 0
        a = self.akadgadai_set.latest()
        for p in self.akadgadai_set.filter(id = a.id):
            try:
                pn = p.jenis_transaksi
            except:
                pass
            return pn
        
    def __unicode__(self):
        return "%s-%s" %(self.nomor(),self.nama)
### AKAD BARU
    def ro(self):
        return self.akadgadai_set.all().count()

    def taksir(self):
        for p in self.akadgadai_set.all():
            return p.taksir
    
    def jenis_trans(self):
        for p in self.akadgadai_set.all():
            return p.jenis_transaksi
        
    def jenis_barang(self):
        for p in self.akadgadai_set.all():
            return p.barang

    def kreditterakhir(self):
        a = self.akadgadai_set.all()
        b = list(a)
        return b[-1]
    
    def lunasakadterakhir(self, ):
        if self.kreditterakhir().status_transaksi == u'1':
            return 'Lunas'
        else:
            return 'Belum Lunas'
### akad bari akhir

    def get_absolute_url(self):
        return "/akadgadai/%s/show/" % self.id
    
    def cek_number_ktp(value):
        if value % 2 != 0:
            raise ValidationError(u'%s is not an even number' % value)
    
    def lebih(self):
        a = self.akadgadai_set.all().count()
        return a

    def nomor(self):
        pn = 0
        for p in self.akadgadai_set.all():
            try:
                pn = p.norek()
            except:
                pass
            return pn

    ###17042013
    def nomor_nasabah(self):
        pn = 0
        for p in self.akadgadai_set.all():
            try:
                pn = p.nonas()
            except:
                pass
            return pn

    def geraigadai(self):
        for p in self.akadgadai_set.all():
            return p.gerai

    def baranggerai(self):
        for p in self.akadgadai_set.all():
            return p.barang

    def jatuh_tempo(self):
        pn = 0
        for p in self.akadgadai_set.all():
            try:
                pn = p.jatuhtempo
            except:
                pass
            return pn
    
    def status_lunas(self):
        pn = 0
        for p in self.akadgadai_set.all():
            try:
                pn = p.lunas
            except:
                pass
            return pn


CHOICES_TRANSAKSI=(
    ('1','Lunas'),
    ('2','Lelang'),
    ('3','Aktif'),
    ('4','BATAL'),
    ('5','TOLAK'),
    ('6','Lunas Ayda'),
    ('7','Lunas Terjual'),
    ('8','WO'),
    ('9','HILANG'),
    ('10','LAIN LAIN'),
)

CHOICES_JENIS_IDENTITAS=(
    ('1','Elektronik'),
    ('2','Motor'),
    ('3','Mobil')
)


STATUS_PERMINTAAN=(
    ('1','PESAN'),
    ('2','RETUR'),
    ('3','KIRIM'),
    ('4','BELUM DITEMUKAN'),
)

STATUS_TAKSIR=(
    ('1','SESUAI NILAI TAKSIR'),
    ('2','MELEBIHI NILAI TAKSIR'),
)

JASABARU = (('1','4 %'), ('2','7 %'),)

STATUS_TANDATERIMA = (('None','None'), ('1','OK'),)

class LogAkadGadai(models.Model):
    nama_nasabah = models.CharField(max_length=100)
    nilai = models.FloatField()
    nilai_jasa = models.DecimalField(max_digits=12, decimal_places=2,null=True,blank=True,default=0)
    nilai_jasa_kendaraan = models.DecimalField(max_digits=12, decimal_places=2,null=True,blank=True,default=0)
    nilai_denda = models.DecimalField(max_digits=12, decimal_places=2,null=True,blank=True,default=0)
    nilai_denda_kendaraan = models.DecimalField(max_digits=12, decimal_places=2,null=True,blank=True,default=0)
    terlambat = models.DecimalField(max_digits=12, decimal_places=2,default=0)
    terlambat_kendaraan =models.DecimalField(max_digits=12, decimal_places=2,default=0)
    gerai = models.CharField(max_length=50)    
    norek = models.CharField(max_length=50)    
    tanggal = models.DateField(help_text="Tgl-Bl-Tahun", null=True)
    jenis = models.CharField(max_length=50)
    jenis_barang = models.CharField(max_length=50)
    cu = models.ForeignKey(User, related_name='+', editable=False, null=True, blank=True)
    mu = models.ForeignKey(User, related_name='+', editable=False, null=True, blank=True)
    cdate = models.DateTimeField(auto_now_add=True)
    mdate = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'logakadgadai'
        verbose_name = 'LogAkadGadai'
        verbose_name_plural = verbose_name


class AkadGadaiManager(models.Manager):
    def jangka_waktu(self):
        pass
    
    def for_user(self, user):
        try:
            gerai = user.get_profile().gerai
            gg_list = [gerai.id] + [k.id for k in gerai.tbl_cabang_set.all()]
            return self.filter(gerai__id__in=gg_list)
        except:
            return None
            
class AkadGadai(models.Model):
    agnasabah = models.ForeignKey(Nasabah)
    barang = models.ForeignKey(Barang)
    tanggal = models.DateField(help_text="tahun-bl-tg", null=True)
    gerai = models.ForeignKey('Tbl_Cabang',null=True,blank=True)
    nilai = models.FloatField()
    jangka_waktu= models.CharField(max_length=4 ,choices=JANGKA_WAKTU, null=True)
    jangka_waktu_kendaraan= models.CharField(max_length=4 ,choices=JANGKA_WAKTU_KENDARAAN, null=True)
    jenis = models.CharField(max_length=20 , null=True, blank=True)
    lunas = models.DateField()
    lelang = models.DateField(null=True, default=None, editable=False)
    pilih_jasa = models.CharField(max_length=4 ,choices= JASABARU, null=True,blank = True)
    '''bea materai dirubah menjadi data inputan di akadgadai(editor hasan tgl 04102012)'''
    bea_materai = models.FloatField(default=0, null=True, blank=True, help_text="(Untuk biaya materai, jika tidak ada isi 0)")
    
    cu = models.ForeignKey(User, related_name='c_akadgadai', editable=False, null=True, blank=True)
    mu = models.ForeignKey(User, related_name='m_akadgadai', editable=False, null=True, blank=True)
    cdate = models.DateTimeField(auto_now_add=True)
    mdate = models.DateTimeField(auto_now=True)
    lunas = models.DateField(null=True, default=None, blank=True)
    status_transaksi = models.CharField(max_length=20 ,choices=CHOICES_TRANSAKSI, null=True, blank=True)
    taksir=models.ForeignKey('Taksir')
    objects = AkadGadaiManager()
    jenis_transaksi = models.CharField(max_length=20 ,choices=CHOICES_JENIS_TRANSAKSI, null=True, blank=True)
    tanggal_permintaan =models.DateField(null=True, blank=True, editable=False)
    tanggal_pengiriman =models.DateField(null=True, blank=True, editable=False)
    status_permintaan= models.CharField(max_length=4 ,choices=STATUS_PERMINTAAN, null=True, blank=True, editable=False)
    status_taksir= models.CharField(max_length=4 ,choices=STATUS_TAKSIR, null=True, blank=True)
    jatuhtempo = models.DateField(null=True, blank=True)
    nilai_jasa = models.DecimalField(max_digits=12, decimal_places=2,null=True,blank=True,default=0)
    nilai_jasa_kendaraan = models.DecimalField(max_digits=12,decimal_places=2,default=0,null=True,blank=True)
    nilai_biayasimpan = models.DecimalField(max_digits=12,decimal_places=2,default=0,null=True,blank=True)
    nilai_beasimpan_kendaraan = models.DecimalField(max_digits=12,decimal_places =2,default=0,null=True,blank=True)
    nilai_adm = models.DecimalField(max_digits=12,decimal_places=2,default=0,null=True,blank=True)
    nilai_adm_kendaraan = models.DecimalField(max_digits=12,decimal_places=2,default=0,null=True,blank=True)
    nocoa_titipan = models.CharField(max_length=15,blank=True,null=True)
    nocoa_kas = models.CharField(max_length=15,blank=True,null=True)
    os_pokok = models.DecimalField(max_digits=12, decimal_places=2,null=True,default=0)
    asumsi_jasa = models.DecimalField(max_digits=12, decimal_places=2,null=True,blank=True)
    nilai_asuransi = models.DecimalField(max_digits=12, decimal_places=2,null=True,default=0)    
    nilai_provisi = models.DecimalField(max_digits=12, decimal_places=2,null=True,default=0)
    status_kw = models.CharField(max_length=20 ,null=True, blank=True)
    status_kwlunas = models.CharField(max_length=20 ,null=True, blank=True )####untuk tombol simpan di adm auto hide
    status_mcc = models.CharField(max_length=20 ,null=True, blank=True)
    status_label  = models.IntegerField(null=True, blank=True)
    selisih_pelunasan = models.DecimalField(max_digits=12, decimal_places=2,null=True,blank=True,default=0)
    kewajiban_pelunasan = models.DecimalField(max_digits=12, decimal_places=2,null=True,blank=True,default=0)####nilai pelunasan sebelumnya
    nilai_gu = models.DecimalField(max_digits=12, decimal_places=2,null=True,blank=True,default=0)####nilai pelunasan sebelumnya
    denda_gu = models.DecimalField(max_digits=12, decimal_places=2,null=True,blank=True,default=0)####nilai pelunasan sebelumnya
    jasa_gu = models.DecimalField(max_digits=12, decimal_places=2,null=True,blank=True,default=0)####nilai pelunasan sebelumnya  
    jns_gu = models.CharField(max_length=20 ,choices=STATUS_PENCAIRAN_NASABAH, null=True, blank=True)

    ## Tambahan Dari Server Exist
    sts_tdr = models.CharField(max_length=4 ,choices=STATUS_TANDATERIMA, null=True, blank=True)
    status_teguran = models.IntegerField(null=True, blank=True)
    klik_permintaan = models.DateTimeField(null=True, blank=True)
    no_teguran = models.IntegerField(null=True, blank=True)
    status_kondisi_barang = models.IntegerField(null=True, blank=True)
    ###menu pelunasan tambahan
    jasa_lunas = models.DecimalField(max_digits=12, decimal_places=2,null=True,blank=True,default=0)
    denda_lunas = models.DecimalField(max_digits=12, decimal_places=2,null=True,blank=True,default=0)
    jasa_kendaraan_lunas = models.DecimalField(max_digits=12, decimal_places=2,null=True,blank=True,default=0)
    denda_kendaraan_lunas = models.DecimalField(max_digits=12, decimal_places=2,null=True,blank=True,default=0)
    terlambat = models.DecimalField(max_digits=12, decimal_places=2,null=True,blank=True,default=0)
    terlambat_kendaraan = models.DecimalField(max_digits=12, decimal_places=2,null=True,blank=True,default=0)
    status_oto_plns = models.CharField(max_length=4 , null=True, blank=True) ## Untuk Otorisasi Pelunasan Manop
    nilai_lunas = models.DecimalField(max_digits=12, decimal_places=2,null=True,blank=True,default=0)####nilai pelunasan Oto Manop
    status_oto_akad_gu = models.CharField(max_length=4 , null=True, blank=True) ## Untuk Otorisasi Pelunasan GADAI ULANG Manop
    norek_lunas_sblm = models.CharField(max_length=20 , null=True, blank=True) ## Untuk Otorisasi Pelunasan GADAI ULANG Manop
    total_plns_gu =  models.DecimalField(max_digits=12, decimal_places=2,null=True,blank=True,default=0)#####NILIA PENGURANGAN
    status_permintaan= models.CharField(max_length=4 ,choices=STATUS_PERMINTAAN, null=True, blank=True)

    tgl_barang_masuk = models.DateField(null=True, blank=True)
    tgl_barang_keluar = models.DateField(null=True, blank=True)
    ruang_barang = models.CharField(null=True, blank = True,max_length=200,choices=RUANGAN_CHOICES)
    lemari_barang = models.CharField(null=True, blank = True,max_length=200,choices=LEMARI_CHOICES)
    kolom_barang = models.CharField(null=True, blank = True,max_length=200)
    rak_barang = models.CharField(null=True, blank = True,max_length=200,choices=RAK_CHOICES)
    row_barang = models.CharField(null=True, blank = True,max_length=200,choices=ROW_CHOICES)

    class Meta:
        db_table = 'akadgadai'
        ordering = ['-tanggal']
        verbose_name = 'AkadGadai'
        verbose_name_plural = verbose_name
        get_latest_by = 'tanggal'

    def tot_denda_lns(self):
        return self.denda_lunas + self.denda_kendaraan_lunas
    
    def tot_jasa_lns(self):
        return self.jasa_lunas + self.jasa_kendaraan_lunas

    def date_date_cuy(self):
        if self.tanggal == self.agnasabah.mdate.date():
            return True
        else:
            return False

    def param_tombol(self):
        if self.jenis_transaksi == '1':
            param = ParameterAkadUlang.objects.get(aktif=2,jangka_waktu = self.jangka_waktu)
            return int(param.jml_akad)
        else:
            param = ParameterAkadUlang.objects.get(aktif=2,jangka_waktu = self.jangka_waktu_kendaraan)
            return int(param.jml_akad)

    ### TEGURAN
    def blokir_teguran(self):
        sekarang = datetime.date.today()
        #batas = timedelta(days=2)
        #batas = timedelta(days=7)
        batas = timedelta(days=20)
        block = self.jatuhtempo - batas 
        if block > sekarang :
            return 'tutup' 
        else:
            return 'tampil'

    def nomor_teguran(self):
        for a in AkadGadai.objects.all():
            if a.id :
                b = AkadGadai.objects.filter(no_teguran__isnull = False).order_by('-no_teguran')
                aa= b[0]
                c = aa.no_teguran
                return c + 1

    def merk_all(self):
        if self.jenis_transaksi == '1':
            return self.barang.merk
        else:
            return self.barang.get_merk_kendaraan_display()

    def taksiran_kwitansi(self):
        if self.jenis_transaksi == '1':
            merk = "%s|%s|" % (self.barang.merk,self.barang.sn)
            return merk
        else:
            merk = "%s|%s|%s|"% (self.barang.get_jenis_kendaraan_display(),self.barang.get_merk_kendaraan_display() ,self.barang.type_kendaraan)
            return merk

    ### AKHIR TEGURAN


    def cekkasirgeraipelunasan(self):
        try:
            s = self.kasirgeraipelunasan
            ret = s.status == u'1'
        except KasirGerai.DoesNotExist:
            ret = False
        return ret
    cekkasirgeraipelunasan = property(cekkasirgeraipelunasan)

    def sts_trans_excel(self):
        if self.status_transaksi == None:
            return 'Aktif'
        else:
            return self.get_status_transaksi_display()

    def harga_lelang_filter(self, start_date,end_date):
        rs_pk = self.baranglelang_set.filter(tgl_lelang__range=(start_date,end_date))
        nilai= 0
        for p in rs_pk:
            nilai += p.harga_jual
        return nilai

    def nilai_pncr_filter(self, start_date,end_date):
        rs_pk = self.baranglelang_set.filter(tgl_lelang__range=(start_date,end_date))
        nilai= 0
        for p in rs_pk:
            nilai += p.aglelang.nilai
        return nilai
    
    def selisih_penjualan(self,start_date,end_date):
        selisih = self.harga_lelang_filter( start_date,end_date) - self.nilai_pncr_filter( start_date,end_date)
        if selisih > 0 :
            return selisih
        else:
            return 0 

    def total_terlambat(self):
        return self.terlambat + self.terlambat_kendaraan

    def jenis_barang_all(self):
        if self.jenis_transaksi == '1':
            return self.barang.get_jenis_barang_display()
        else:
            return self.barang.get_jenis_kendaraan_display()

    def kode_barang_all(self, ):
        if self.jenis_transaksi == '1':
            return self.barang.__unicode__()
        else:
            #return self.barang.__unic__kendaraan__()
            return "%s-%s" %(self.barang.id,self.taksir.type)

    def get_absolute_url_adm(self):
        return "/admgudang/data_retur_gaktif/" 

    def get_absolute_url_delete(self):
        return "/nasabah/%s/show/" % self.agnasabah.id

    def barang_history_akad_ulang(self ):
        if self.barang.jenis_barang == u'1':
            return '1'
        elif self.barang.jenis_barang == u'2':
            return '2'
        elif self.barang.jenis_barang == u'3':
            return '3'
        elif self.barang.jenis_barang == u'4':
            return '4'
        elif self.barang.jenis_barang == u'5':
            return '5'
        elif self.barang.jenis_kendaraan == u'1':
            return '6'  
        elif self.barang.jenis_kendaraan == u'2':
            return '7'     

    def total_pelunasan_gu(self):
        D = decimal.Decimal 
        return  D(self.kewajiban_pelunasan) + self.nilai_jasa + self.nilai_jasa_kendaraan + self.nilai_beasimpan_kendaraan\
            + self.nilai_biayasimpan + self.nilai_adm + self.nilai_adm_kendaraan + D(self.bea_materai) - D(self.nilai)

    def note_kwitansi(self):
        tiga_play = [self.id,self.id,self.id]
        a = tiga_play[0]
        if a == tiga_play[0]:
            return 'Asli'
        elif a == tiga_play[1]:
            return 'Copy'
        elif a == tiga_play[2]:
            return 'Copy Dua'
        else:
            return 'Copy Tiga'
    
    def total_pelunasan_otorisasi(self):
        return self.nilai_lunas + self.jasa_lunas + self.jasa_kendaraan_lunas + self.denda_lunas + self.denda_kendaraan_lunas

    def get_nasabah_url(self):
        return "/nasabah/%s/show/" % self.agnasabah.id

    def coba_pelunasan_terakhir(self):
        a = self.pelunasan_set.all().latest()
        return a.id

    def sms(self):    
        return 'Terima kasih Bpk/Ibu %s tlh menjadi nasabah KSU RIZKY ABADI,pinjaman sebesar %s, jatuh tempo pd tgl %s (Simulasi SMS PJB)' % (self.agnasabah.nama,number_format(self.nilai),self.jatuhtempo.strftime('%d-%m-%Y,'))
        #return 'Terima kasih Bpk/Ibu %s anda tlh menjadi nasabah KSU RIZKY ABADI,pinjaman sebesar %s & jangka waktu %s Hari, jatuh tempo pd tgl %s dgn jaminan %s' % (self.agnasabah.nama,number_format(self.nilai),self.jangka_waktu,self.jatuhtempo.strftime('%d-%m-%Y,'),self.barang.merk)

    def smslunas(self):    
        return 'Terima kasih Bpk/Ibu %s pinjaman anda telah lunas (KSU RIZKY ABADI)'% (self.agnasabah.nama)
                                                                                                                                        
    def pelunasan_terakhir(self):
        return self.pelunasan_set.all().latest()

    def coba_jw(self):
        if self.jenis_transaksi == u'1':
            return self.tanggal + datetime.timedelta(int(self.jangka_waktu))
        else:
            return self.jatuh_tempo_kendaraan_hitung()
        
    def kepala_gerai(self):
        try:
            s = self.kepalagerai
            ret = s.status=='1'
        except KepalaGerai.DoesNotExist:
            ret = False
        return ret
    
    def kepala_gerai_tolak(self):
        try:
            s = self.kepalagerai
            ret = s.status=='1'
        except KepalaGerai.DoesNotExist:
            ret = False
        return ret

    def next_kg(self):
    
        ret = ''
        #if self.manopkupeg and (self.manopkupeg.status == '1'):
            #ret = 'top'
        if self.kepala_gerai() and (self.kepalagerai.status == '1'):
            ret = 'KG'
        else:
            ret = ''
        return ret


    def get_jw_all(self):
        if self.jenis_transaksi == u'1':
            return self.jangka_waktu
        else:
            return self.jangka_waktu_kendaraan
    jw_all = property(get_jw_all)

    def jw_all(self):
        if self.jenis_transaksi == '1':
            return self.jangka_waktu
        else:
            return self.jangka_waktu_kendaraan
    
    def get_absolute_url(self):
        return "/akadgadai/%s/show/" % self.id

    def get_absolute_url_manop(self):
        return "/manop/%s/show/" % self.id
    
    def tanggal_akhir_bulan(self):
        tgl= self.tanggal + relativedelta(day=31)
        return tgl.day
    
    def asumsi_pendapatan_jasa(self):
        tanggal_r = (self.tanggal_akhir_bulan() - self.tanggal.day) + 1
        hitung_r = (tanggal_r  * self.nilai_jasa) /self.tanggal_akhir_bulan()
        hitung_kend = (tanggal_r  * self.nilai_jasa_kendaraan) /self.tanggal_akhir_bulan()
        if self.jenis_transaksi == '1':
            return hitung_r
        else:
            return hitung_kend
        
    def hari_terlambat(self):
        sekarang = datetime.date.today()
        selisih =  sekarang - self.jatuhtempo 
        if selisih.days < 0 :
            return 0
        else:
            return selisih.days  
    
    def denda_all_transaksi(self):
        if self.jenis_transaksi == '1':
            return self.denda_elektronik()
        else:
            return self.denda_kendaraan()

    def denda_elektronik(self):
        if self.jenis_transaksi == u'1':
            return int(self.nilai*0.05/30)*int(self.hari_terlambat())
        else:
            return 0
    def denda_kendaraan(self):
        if self.jenis_transaksi == u'1':
            return 0
        else:
            return int(self.nilai*0.05/30)*int(self.hari_terlambat())

    def hitung_jasa_pelunasan_elektronik(self):
        if self.jenis_transaksi == u'1':
            return int(round((self.nilai*0.02/7)*(self.hari_terlambat())))
            #return ((self.nilai*0.02)/7)*int(self.jangka_waktu)
        else:
            return 0

    def hitung_jasa_pelunasan_kendaraan(self):
        if self.jenis_transaksi == u'1':
            return 0
        else:
            return int(round((self.nilai*0.04/30)*(self.hari_terlambat())))

    def hitung_jasa_ayda(self):
        if self.jenis_transaksi == u'1':
            return int(round((self.nilai*0.02/7)*(self.hari_terlambat())))
        else:
            return int(round((self.nilai*0.04/30)*(self.hari_terlambat())))

    def norek_lapur_ayda(self):
        pn=0
        for p in self.lapur_set.all():
            try:
                pn = p.norek_lapur()
            except:
                pass
            return pn
    def norek_jual_lunas_ayda(self):
        pn=0
        for p in self.lunasterjual_set.all():
            try:
                pn = p.norek_jual_lunas()
            except:
                pass
            return pn

    def nilai_ayda(self):
        pn = 0
        for p in self.lapur_set.all():
            try:
                pn = p.nilai
            except:
                pass
            return pn

    def jasa_ayda(self):
        pn = 0
        for p in self.lapur_set.all():
            try:
                pn = p.jasa
            except:
                pass
            return pn

    def denda_ayda(self):
        pn = 0
        for p in self.lapur_set.all():
            try:
                pn = p.denda
            except:
                pass
            return pn

    def tanggal_lunas_ayda(self):
        pn = 0
        for p in self.lapur_set.all():
            try:
                pn = p.tanggal
            except:
                pass
            return pn

    def total_akad_ayda(self):
        return self.nilai_ayda() #+ self.jasa_ayda() + self.denda_ayda()


    def untung_rugi_ayda(self):
        return self.hargalelang() - float(self.total_akad_ayda())

    def untung_lelang_ayda(self):
        nilaix = self.hargalelang() - float(self.total_akad_ayda())
        if nilaix > 0:
           return nilaix
        else:
           return 0
   
    def rugi_lelang_ayda(self):
        nilaix = self.hargalelang() - float(self.total_akad_ayda())
        if nilaix < 0:
           return nilaix * -1
        else:
           return 0

    def hitung_denda_pelunasan(self):
        return int(round(((self.nilai*0.05/30))*(self.hari_terlambat())))
    
    def hitung_jasa_pelunasan(self):
        if self.jenis_transaksi == u'1':
            return self.hitung_jasa_pelunasan_elektronik()  
        else:
            return self.hitung_jasa_pelunasan_kendaraan() 

    ## Perubahan Hitungan Denda di Pelunasan
    def denda_plns_baru(self):
        if self.jenis_transaksi == u'1':
            if self.hari_terlambat() >= 1 and self.hari_terlambat() < 7:
                return int(round(self.nilai*0.05/30) *self.hari_terlambat())
                #sebelum dirubah
                #return int(round(self.nilai*0.02))
            if self.hari_terlambat() >= 7:
                return int(round(self.nilai*0.05/30) *self.hari_terlambat())
                #sebelum dirubah
                #return int(round(self.nilai*0.04))
            else:
                return int(0)
        elif self.jenis_transaksi != u'1':
            if self.hari_terlambat() >= 1 and self.hari_terlambat() < 7:
                #perubahan 16-09-2019
                return int(round(self.nilai*0.05/30) *self.hari_terlambat())
                #sblm Dirubah 
                #return int(round(self.nilai*0.04))
            if self.hari_terlambat() >= 7:
                #perubahan 16-09-2019
                return int(round(self.nilai*0.05/30) *self.hari_terlambat())
                #sblm Dirubah
                #return int(round(self.nilai*0.08))
            else:
                return int(0)
        else:
            return int(0)

    def denda_plns_baru_kendaraan(self):
        if self.hari_terlambat() >= 1 and self.hari_terlambat() < 7:
            return int(round(self.nilai*0.04))
        if self.hari_terlambat() >= 7:
            return int(round(self.nilai*0.08))
        else:
            return int(0)
    ### Akhir Perubahan Hitungan Denda di pelunasan
    @property
    def next_group(self):
        ret = ''
        if self.cekkasirgerai and (self.kasirgerai.status == '1'):
            ret = 'KASIRGERAI'
        else:
            ret = 'CABANG'
        

    def cekkasirgerai(self):
        try:
            s = self.kasirgerai
            ret = s.status == u'1'
        except KasirGerai.DoesNotExist:
            ret = False
        return ret
    cekkasir = property(cekkasirgerai)
    
    def notrans_jurnal(self):
        self.id = 0
        for a in self.agnasabah.akadgadai_set.all().order_by('tanggal'):
            if a.id == self.id:
                return self.id
            self.id += 1
    
    
    def _get_usia(self):
        skr = datetime.date.today()
        if not self.agnasabah.tgl_lahir:
            self.agnasabah.tgl_lahir = skr
        usia = skr - self.agnasabah.tgl_lahir
        return usia.days / 365
    usia = property(_get_usia)
    
    
    def kw_validasi(self):
        return "KT %s %s %s %s %s WIB|%s" % ((self.norek()),self.nocoa_titipan,self.nilai,self.nocoa_kas,self.mdate,(str(self.gerai.init_cabang)) )

    def __unicode__(self):
        return "%s-%s" %(self.agnasabah.nama,self.id)

####NOMOR ACCOUNT####
    def norek(self):
        return "%s.%s.%s.%s" % (str(self.gerai.kode_cabang).zfill(1),(self.tanggal.year),str(self.jenis_transaksi).zfill(1),str(self.id).zfill(6))
    
    def norek_import(self):
        return "%s.%s.%s.%s" % (str(self.gerai.kode_cabang).zfill(1),(self.tanggal),str(self.jenis_transaksi).zfill(1),str(self.id).zfill(6))

    def nonas(self):
        return "%s.%s.%s" % (str(self.gerai.kode_cabang).zfill(1),str(self.gerai.kode_cabang).zfill(2),str(self.agnasabah.id).zfill(6))
 
    def norek_id(self):
        return "%s" % (str(self.id).zfill(6))
####NOMOR ACCOUNT####
    
#### HITUNGAN ADM ####    
    def _get_jasa(self):
        tgl_1_12_18 = datetime.date(2018,12,1)

        if self.jangka_waktu == u'15':
	    return (self.nilai * (4.3/100))
        #---Perubahan Perhitungan Jasa Pertanggal 
        elif self.jangka_waktu != u'15' and self.tanggal >= tgl_1_12_18:
            if self.barang.jenis_barang == '6':
                return (self.nilai * 0.04/30) * float(self.jangka_waktu)
            if self.barang.jenis_barang == '7':
                return (self.nilai * 0.04/30) / float(self.jangka_waktu)
            else:
                return (self.nilai * (7.8/100)) ## Hitungan Baru
        else:
            if self.barang.jenis_barang == '1' and self.tanggal < tgl_1_12_18:
                return (self.nilai * (0.02/7)) * float(self.jangka_waktu)
            if self.barang.jenis_barang == '2':
                return (self.nilai * 0.02/7) * float(self.jangka_waktu)
            if self.barang.jenis_barang == '3':
                return (self.nilai * 0.02/7) * float(self.jangka_waktu)
            if self.barang.jenis_barang == '4':
                return (self.nilai * 0.02/7) * float(self.jangka_waktu)
            if self.barang.jenis_barang == '5':
                return (self.nilai * 0.02/7) * float(self.jangka_waktu)
            if self.barang.jenis_barang == '6':
                return (self.nilai * 0.04/30) * float(self.jangka_waktu)
            if self.barang.jenis_barang == '7':
                return (self.nilai * 0.04/30) / float(self.jangka_waktu)
            else:
                return 0
    jasa = property(_get_jasa)

    def persen_jasa(self):
        if self.jangka_waktu == u'15':
            return 4.3
        else:
            if self.barang.jenis_barang == '1':
                return 2
            if self.barang.jenis_barang == '2':
                return 2
            if self.barang.jenis_barang == '3':
                return 2
            if self.barang.jenis_barang == '4':
                return 2
            if self.barang.jenis_barang == '5':
                return 2
            if self.barang.jenis_barang == '6':
                return 4
            if self.barang.jenis_barang == '7':
                return 4
            else:
                return 0
    persentase_jasa = property(persen_jasa)

    def persen_jasa_kendaraan(self):
        if self.pilih_jasa == 2 or self.pilih_jasa == u'2':
            return 7
        else:
            return 4
        #return 4
    persentase_jasa_kendaraan = property (persen_jasa_kendaraan)

    def persentase_jasa_all(self):
        if self.jenis_transaksi == '1':
            return self.persentase_jasa
        else:
            return self.persentase_jasa_kendaraan
    
    ###tgl 1 april revisi jasa acc manop gadai    
    def _get_jasa_kendaraan(self):
        if self.pilih_jasa == 2 or self.pilih_jasa == u'2': #Yang baru
		    return (self.nilai * 7/100)
        else:
            if self.barang.jenis_kendaraan =='1' and self.jenis_transaksi == 2:
                return (self.nilai * 0.04)* float(self.jangka_waktu_kendaraan)
            if self.barang.jenis_kendaraan =='2' and self.jenis_transaksi == 2:
                return (self.nilai * 0.04)* float(self.jangka_waktu_kendaraan)
            else:
                return (self.nilai * 0.04)* float(self.jangka_waktu_kendaraan)
    jasa_kendaraan = property (_get_jasa_kendaraan)        

    def jasa_kwitansi(self):
        if self.jenis_transaksi == u'1':
            return round(self.jasa)
        else:
            return round(self.jasa_kendaraan)

    def _get_totjasa(self):
        return self.nilai_jasa + (self.nilai_jasa_kendaraan)            
    tot_jasa_kend_elek = property(_get_totjasa) 

    def _get_adm(self):
        mulai = datetime.date(2015,8,21) 
        akhir = datetime.date(2015,9,30)
        startdate = datetime.date(2016,6,27)
        tgl_baru = datetime.date(2018,01,25)

        if self.tanggal >= tgl_baru and self.jangka_waktu == u'15':
            return 15000
        if self.tanggal >= startdate and self.tanggal < datetime.date(2016,9,22) and self.gerai.kode_cabang != '303' and self.gerai.kode_cabang != '333':
            if self.barang.jenis_barang == u'1':
                return 10000
            if self.barang.jenis_barang == u'2':
                return 10000
            if self.barang.jenis_barang ==u'3':
                return 10000
            if self.barang.jenis_barang ==u'4':
                return 10000
            if self.barang.jenis_barang ==u'5':
                return 10000
            if self.barang.jenis_barang ==u'6':
                return 25000
            if self.barang.jenis_barang ==u'7':
                return 50000
            else:
                return 0
        
        #elif self.tanggal >= startdate and self.gerai.kode_cabang != '303' and self.gerai.kode_cabang != '333':
        if self.tanggal >= datetime.date(2016,9,24)  and self.gerai.kode_cabang != '303' and self.gerai.kode_cabang != '333':
            if self.barang.jenis_barang ==u'1':
                return 15000
            if self.barang.jenis_barang ==u'2':
                return 15000
            if self.barang.jenis_barang ==u'3':
                return 15000
            if self.barang.jenis_barang ==u'4':
                return 15000
            if self.barang.jenis_barang ==u'5':
                return 15000
            if self.barang.jenis_barang ==u'6':
                return 50000
            if self.barang.jenis_barang ==u'7':
                return 150000
            else:
                return 0
        if self.tanggal >= datetime.date(2016,9,22) and self.gerai.kode_cabang != '303' and self.gerai.kode_cabang != '333':
        #elif self.tanggal >= datetime.date(2016,9,22) and self.gerai.kode_cabang != '303' and self.gerai.kode_cabang != '333':
            if self.barang.jenis_barang ==u'1':
                return 15000
            if self.barang.jenis_barang ==u'2':
                return 15000
            if self.barang.jenis_barang ==u'3':
                return 15000
            if self.barang.jenis_barang ==u'4':
                return 15000
            if self.barang.jenis_barang ==u'5':
                return 15000
            if self.barang.jenis_barang ==u'6':
                return 50000
            if self.barang.jenis_barang ==u'7':
                return 150000
            else:
                return 0
        
        elif self.tanggal >= datetime.date(2016,9,22) and self.gerai.kode_cabang == '303' and self.gerai.kode_cabang == '333':
            return 0
        elif self.tanggal >= datetime.date(2016,9,22) and self.gerai.kode_cabang == '303' or self.gerai.kode_cabang == '333':
            return 0.00
    adm =property(_get_adm)    
    
    
    def _get_adm_kendaraan(self):
        mulai = datetime.date(2015,8,21) 
        akhir = datetime.date(2015,8,30)
        startdate = datetime.date(2016,6,27)
        #tgl_aturanbaru = datetime.date(2017,11,1)
        if self.pilih_jasa == 2 or self.pilih_jasa == u'2': #Yang baru
	        if self.barang.jenis_kendaraan =='1' and self.jenis_transaksi == '2':
	            return 0
	        elif self.barang.jenis_kendaraan =='2' and self.jenis_transaksi == '2':
	            return 0
	        elif self.barang.jenis_kendaraan =='2' and self.jenis_transaksi == '3':
	            return 0
	        else:
	            return 0
        else:
            if self.tanggal < startdate :
                if self.tanggal >= mulai and self.tanggal <= akhir :
                    return 0
                if self.barang.jenis_kendaraan =='1' and self.jenis_transaksi == '2':
                    return 25000
                elif self.barang.jenis_kendaraan =='2' and self.jenis_transaksi == '2':
                    return 50000
                elif self.barang.jenis_kendaraan =='2' and self.jenis_transaksi == '3':
                    return 150000
                else:
                    return 0
            elif self.tanggal >= startdate :#and self.tanggal < tgl_aturanbaru :
                if self.tanggal >= mulai and self.tanggal <= akhir :
                    return 0
                if self.barang.jenis_kendaraan =='1' and self.jenis_transaksi == '2':
                    return 50000
                elif self.barang.jenis_kendaraan =='2' and self.jenis_transaksi == '2':
                    return 50000
                elif self.barang.jenis_kendaraan =='2' and self.jenis_transaksi == '3':
                    return 150000
                else:
                    return 0
        #elif self.tanggal >= tgl_aturanbaru :
            #if self.tanggal >= mulai and self.tanggal <= akhir :
                #return 0
            #if self.barang.jenis_kendaraan =='1' and self.jenis_transaksi == '2':
                #return 0
            #elif self.barang.jenis_kendaraan =='2' and self.jenis_transaksi == '2':
                #return 0
            #elif self.barang.jenis_kendaraan =='2' and self.jenis_transaksi == '3':
                #return 0
            #else:
                #return 0
    adm_kendaraan = property (_get_adm_kendaraan)
 
    def _get_totadm(self):
        try:
            ret= self.adm + self.adm_kendaraan
            return ret
        except:
            return 0
    tot_adm_kend_elek = property(_get_totadm) 

    def _get_biayasimpan(self):
        startdate = datetime.date(2016,6,27)
        tgl_baru = datetime.date(2018,02,25)
        tgl_1_12_18 = datetime.date(2018,12,1)
        if self.jangka_waktu == u'15' and self.tanggal >= tgl_baru:
            return 15000

        if self.jangka_waktu == 14:
            if self.tanggal >= startdate and self.tanggal < datetime.date(2016,9,22) :
                if self.barang.jenis_barang == u'1' and self.jenis_transaksi == u'1':
                    return 15000
                if self.barang.jenis_barang == u'2' and self.jenis_transaksi == u'1':
                    return 20000
                if self.barang.jenis_barang == u'3' and self.jenis_transaksi == u'1':
                    return 20000
                if self.barang.jenis_barang == u'4' and self.jenis_transaksi == u'1':
                    return 20000
                if self.barang.jenis_barang == u'5' and self.jenis_transaksi == u'1':
                    return 30000
                if self.barang.jenis_barang == u'6' and self.jenis_transaksi == u'1':
                    return 75000
                if self.barang.jenis_barang == u'7' and self.jenis_transaksi == u'1':
                    return 450000
                else:
                    return 0
            if self.tanggal >= datetime.date(2016,9,24)  and self.gerai.kode_cabang != '303' or self.gerai.kode_cabang != '333':
                if self.barang.jenis_barang == u'1' and self.jenis_transaksi == u'1':
                    return 15000
                if self.barang.jenis_barang == u'2' and self.jenis_transaksi == u'1':
                    return 20000
                if self.barang.jenis_barang == u'3' and self.jenis_transaksi == u'1':
                    return 20000
                if self.barang.jenis_barang == u'4' and self.jenis_transaksi == u'1':
                    return 20000
                if self.barang.jenis_barang == u'5' and self.jenis_transaksi == u'1':
                    return 30000
                if self.barang.jenis_barang == u'6' and self.jenis_transaksi == u'1':
                    return 75000
                if self.barang.jenis_barang == u'7' and self.jenis_transaksi == u'1':
                    return 450000
                else:
                    return 0                    
            elif self.tanggal < startdate :
                if self.barang.jenis_barang == u'1' and self.jenis_transaksi == u'1':
                    return 5000
                if self.barang.jenis_barang == u'2' and self.jenis_transaksi == u'1':
                    return 10000
                if self.barang.jenis_barang == u'3' and self.jenis_transaksi == u'1':
                    return 10000
                if self.barang.jenis_barang == u'4' and self.jenis_transaksi == u'1':
                    return 10000
                if self.barang.jenis_barang == u'5' and self.jenis_transaksi == u'1':
                    return 15000
                if self.barang.jenis_barang == u'6' and self.jenis_transaksi == u'1':
                    return 50000
                if self.barang.jenis_barang == u'7' and self.jenis_transaksi == u'1':
                    return 100000
                else:
                    return 0
            elif self.tanggal >= datetime.date(2016,9,22) and self.gerai.kode_cabang == '303' or self.gerai.kode_cabang == '333':
                return 0                   

        else:
            ##BARU tgl_1_12_18
            if self.tanggal >= tgl_1_12_18  and self.gerai.kode_cabang != '303' or self.gerai.kode_cabang != '333':
                if self.barang.jenis_barang == u'1' and self.jenis_transaksi == u'1':
                    return 30000
                if self.barang.jenis_barang == u'2' and self.jenis_transaksi == u'1':
                    return 30000
                if self.barang.jenis_barang == u'3' and self.jenis_transaksi == u'1':
                    return 30000
                if self.barang.jenis_barang == u'4' and self.jenis_transaksi == u'1':
                    return 30000
                if self.barang.jenis_barang == u'5' and self.jenis_transaksi == u'1':
                    return 30000
                if self.barang.jenis_barang == u'6' and self.jenis_transaksi == u'1':
                    return 75000
                if self.barang.jenis_barang == u'7' and self.jenis_transaksi == u'1':
                    return 450000
                else:
                    return 0
            ##Akhir BARU tgl_1_12_18
            if self.tanggal >= datetime.date(2016,9,22) and self.tanggal < tgl_1_12_18 and self.gerai.kode_cabang != '303' and self.gerai.kode_cabang != '333':
                if self.barang.jenis_barang == u'1' and self.jenis_transaksi == u'1' :
                    return 20000
                if self.barang.jenis_barang == u'2' and self.jenis_transaksi == u'1' :
                    return 30000
                if self.barang.jenis_barang == u'3' and self.jenis_transaksi == u'1' :
                    return 30000
                if self.barang.jenis_barang == u'4' and self.jenis_transaksi == u'1' :
                    return 30000
                if self.barang.jenis_barang == u'5' and self.jenis_transaksi == u'1' :
                    return 40000
                if self.barang.jenis_barang == u'6' and self.jenis_transaksi == u'1' :
                    return 75000
                if self.barang.jenis_barang == u'7' and self.jenis_transaksi == u'1' :
                    return 450000
                else:
                    return 0
            elif self.tanggal >= datetime.date(2016,9,22) and self.tanggal < tgl_1_12_18 and self.gerai.kode_cabang == '303' or self.gerai.kode_cabang == '333':
                return 0
            elif self.tanggal >= datetime.date(2016,9,22) and self.tanggal < tgl_1_12_18 and self.gerai.kode_cabang == '303' or self.gerai.kode_cabang == '333':
                return 0
    biayasimpan =property(_get_biayasimpan)

    def _get_beasimpan_kendaraan(self):
        startdate = datetime.date(2016,6,27)
        #tgl_aturanbaru = datetime.date(2017,11,1)

        if self.pilih_jasa == 2 or self.pilih_jasa == u'2': #Yang baru
                if self.barang.jenis_kendaraan =='1' and self.jenis_transaksi == '2':
                    return 0
                elif self.barang.jenis_kendaraan =='2' and self.jenis_transaksi == '2':
                    return 0
                elif self.barang.jenis_kendaraan =='2' and self.jenis_transaksi == '3':
                    return 0
                else:
                    return 0
        else:
            if self.tanggal < startdate :
                if self.barang.jenis_kendaraan =='1' and self.jenis_transaksi == '2':
                    return 50000
                elif self.barang.jenis_kendaraan =='2' and self.jenis_transaksi == '2':
                    return 100000
                elif self.barang.jenis_kendaraan =='2' and self.jenis_transaksi == '3':
                    return 350000
                else:
                    return 0
            elif self.tanggal >= startdate :#and self.tanggal < tgl_aturanbaru:
                if self.barang.jenis_kendaraan =='1' and self.jenis_transaksi == '2':
                    return 75000
                elif self.barang.jenis_kendaraan =='2' and self.jenis_transaksi == '2':
                    return 100000
                elif self.barang.jenis_kendaraan =='2' and self.jenis_transaksi == '3':
                    return 450000
                else:
                    return 0
        #elif self.tanggal >= tgl_aturanbaru :
            #if self.barang.jenis_kendaraan =='1' and self.jenis_transaksi == '2':
                #return 0
            #elif self.barang.jenis_kendaraan =='2' and self.jenis_transaksi == '2':
                #return 0
            #elif self.barang.jenis_kendaraan =='2' and self.jenis_transaksi == '3':
                #return 0
            #else:
                #return 0
    beasimpan_kendaraan = property (_get_beasimpan_kendaraan)
    
    ###teddy jurnal(hitung totalberdasarkan filter jenis barang)
    def adm_all(self):
        if self.jenis_transaksi == u'1':
            return self.nilai_adm
        else:
            return self.nilai_adm_kendaraan
    
    def jasa_all(self):
        if self.jenis_transaksi == u'1':
            return self.nilai_jasa
        else:
            return self.nilai_jasa_kendaraan 
        
    def beasimpan_all(self):
        if self.jenis_transaksi == '1':
            return self.nilai_biayasimpan
        else:
            return self.nilai_beasimpan_kendaraan

    def terima_bersih_all(self):
        if self.jenis_transaksi == '1':
            return self.terima_bersih_kwitansi
        else:
            return self.terima_bersih_kendaraan

    def kewajiban_pembayaran_kasir(self):
        return (int(self.kewajiban_pelunasan) - int(self.nilai)) + int(self.jasa_kwitansi()) + (int(self.beasimpan_all())) + int(self.bea_materai)+ int(self.adm_all())
    def kewajiban_pembayaran_kasir_minus(self):
        return ((int(self.kewajiban_pelunasan) - int(self.nilai)) + int(self.jasa_kwitansi()) + (int(self.beasimpan_all())) + int(self.bea_materai)+ int(self.adm_all())) * -1
 
    def jurnal_titipan_all(self):
        d = decimal.Decimal
        return  d(self.nilai) - d(self.adm_all()) - d(round(self.jasa_all())) - d(self.beasimpan_all())
    jurnal_titipan = property(jurnal_titipan_all)
    
    ####teddy jurnal

    def _get_totbeasimpan(self):
        try:
            ret= self.biayasimpan + self.beasimpan_kendaraan
            return ret
        except:
            return 0
    tot_simpan_kend_elek = property(_get_totbeasimpan)

    def _get_jumlahbiaya_kwitansi(self):
        try:
            ret= round(self.adm + self.jasa_kwitansi() + self.biayasimpan + self.bea_materai)
            return ret
        except:
            return 0
    jumlahbiaya_kwitansi = property(_get_jumlahbiaya_kwitansi)

    def _get_jumlahbiaya(self):
        try:
            ret= self.jasa + self.adm + self.biayasimpan + self.bea_materai 
            return ret
        except:
            return 0
    jumlahbiaya = property(_get_jumlahbiaya)

    def _get_jumlahbiaya_kendaraan(self):
        try:
            ret= self.jasa_kendaraan + self.adm_kendaraan + self.beasimpan_kendaraan + self.bea_materai 
            return ret
        except:
            return 0

    jumlahbiaya_kendaraan = property(_get_jumlahbiaya_kendaraan)
    def jumlah_biaya_pk(self):
        if self.jenis_transaksi == '1':
            return round(self.jumlahbiaya)
        else:    
            return round(self.jumlahbiaya_kendaraan)

    def _get_jumlah_biaya(self):
        try:
            ret = self.jasa +self.adm + self.biayasimpan + self.jasa_kendaraan + self.adm_kendaraan + self.beasimpan_kendaraan + self.bea_materai
            return ret
        except:
            return 0
    jumlah_biaya = property(_get_jumlah_biaya)### jumlah biaya tanpa materai

    ####JUMLAH PERPANJANG 1 & 2####
    def _get_jumlahperpanjang(self):
        try:
            ret = self.jasa + self.denda + self.biayasimpan
            return ret
        except:
            return 0
    jumlahperpanjang = property(_get_jumlahperpanjang)
    ####JUMLAH PERPANJANG 1 & 2####
    
    def _get_terima(self):
        try:
            terima= self.nilai - self.jumlahbiaya
            return terima
        except:
            return 0
    terima_bersih = property(_get_terima)

    def _get_terima_kwitansi(self):
        try:
            terima= round(self.nilai - self.jumlahbiaya_kwitansi)# - self.bea_materai)
            return terima
        except:
            return 0
    terima_bersih_kwitansi = property(_get_terima_kwitansi)

    def _get_terima_kendaraan(self):
        try:
            terima= round(self.nilai - self.jumlahbiaya_kendaraan)# - self.bea_materai)
            return terima
        except:
            return 0
    terima_bersih_kendaraan = property(_get_terima_kendaraan)
    
    def _get_terimalunas(self):
        try:
            terima= self.nilai + self.denda
            return terima
        except:
            return 0
    terima_bersih = property(_get_terimalunas)
 #### HITUNGAN ADM ####  

    def jatuhtempo_hitung(self):
        return self.tanggal + datetime.timedelta(int(self.jangka_waktu))

    def jatuh_tempo_kendaraan_hitung(self):
        return add_months(self.tanggal, (int(self.jangka_waktu_kendaraan)))

    def menu_hitung_jt(self):####teddy new
        if self.jenis_transaksi == u'1':
            return self.tanggal + datetime.timedelta(int(self.jangka_waktu))
        else:
            return self.jatuh_tempo_kendaraan_hitung()

    def tgl_jatuhtempo(self):
        now = datetime.date.today()
        if self.barang.jenis_barang == '1':
            return self.jatuhtempo + datetime.timedelta(8)
        else:
            return self.jatuhtempo + datetime.timedelta(8)

    def terlambat_tajuhtempo(self):
        sekarang = datetime.date.today()
        hitung = sekarang - self.jatuhtempo
        return hitung.days

###jatuh tempo
    def _hari_jt(self):
        """Return banyaknya hari sejak jatuh tempo """
        hari_ini = datetime.date.today()
        selisih = hari_ini - self.jatuhtempo()
        return selisih.days
    hari_jangkawaktu = property(_hari_jt)

    @property    
    def hari_jw_kendaraan(self):
        """Return banyaknya hari sejak jatuh tempo kendaraan """
        hari_ini = datetime.date.today()
        selisih = hari_ini - self.jatuh_tempo_kendaraan()
        return selisih.days

    @property    
    def status_gadai(self):
        if self.barang.jenis_barang == "1" and self.hari_jangkawaktu >= 0 and self.hari_jangkawaktu <= 3 :
            return 'Jatuh Tempo elektronik'
        if self.barang.jenis_kendaraan == "2" and self.hari_jw_kendaraan >=0 and self.hari_jw_kendaraan <=3:
            return 'Jatuh Tempo Kendaraan'
        return

###jatuh tempo


    def jt_status(self):
        if self.jenis_transaksi == u'1':
            return  self.prpj_jatuhtempo()
        else:
            return self.prpj_jatuhtempo_kendaraan()      

    ###Pelunasan#####
    def lunas_identitas(self):
        tgl = 0
        for p in self.pelunasan_set.all():
            try:
                tgl = p.id
            except:
                pass
        return tgl

    def lunas_tanggal(self):
        tgl = 0
        for p in self.pelunasan_set.all():
            try:
                tgl = p.tanggal
            except:
                pass
        return tgl
    
    def status_manop_pelunasan(self):
        sts = 1
        for p in self.pelunasan_set.all():
            try:
                sts = p.status
            except:
                pass
        return sts

    def lunas_denda_all(self):
        if self.jenis_transaksi == u'1':
            return  self.lunas_denda()
        else:
            return self.lunas_denda_kendaraan()  

    def lunas_jasa_all(self):
        if self.jenis_transaksi == u'1':
            return  self.lunas_jasa()
        else:
            return self.lunas_bea_jasa_kendaraan()  

    def lunas_denda(self):
        dp = 0
        for p in self.pelunasan_set.all():
            try:
                dp = p.denda
            except:
                pass
        return dp

    def lunas_jasa(self):
        bsp = 0
        for p in self.pelunasan_set.all():
            try:
                bsp = p.bea_jasa
            except:
                pass
        return bsp

    def lunas_denda_kendaraan(self):
        dp = 0
        for p in self.pelunasan_set.all():
            try:
                dp = p.denda_kendaraan
            except:
                pass
        return dp

    def lunas_bea_jasa_kendaraan(self):
        bsp = 0
        for p in self.pelunasan_set.all():
            try:
                bsp = p.bea_jasa_kendaraan
            except:
                pass
        return bsp
        
    def nilai_pelunasan(self):
        bsp = 0
        for p in self.pelunasan_set.all():
            try:
                bsp = p.nilai
            except:
                pass
        return bsp  

    #def kondisi_pelunasan(self):
        #nsb = self.agnasabah.id
          
####barang lelang
    def tgllelang(self):
        for p in self.baranglelang_set.all():
            try:
                pn = p.tgl_lelang
            except:
                pass
            return pn

    def hargalelang(self):
        for p in self.baranglelang_set.all():
            try:
                pn = p.harga_jual
            except:
                pass
            return pn

    def namalelang(self):
        for p in self.baranglelang_set.all():
            try:
                pn = p.nama_pembeli
            except:
                pass
            return pn

    def nilai_lelang(self):
        nilaix = self.hargalelang() - self.nilai
        if nilaix > 0:
           return nilaix
        else:
           return 0
   
    def rugi_lelang(self):
        nilaix = self.hargalelang() - self.nilai
        if nilaix < 0:
           return nilaix
        else:
           return 0
    ###piutang
    def piutang(self):
        return self.nilai

KELOMPOK_BARANG = (
    ('1','HP'),
    ('2','LAPTOP/NB'),
    ('3','KAMERA'),
    ('4','PS'),
    ('5','TV LCD'),
    ('6','MOTOR'),
    ('7','MOBIL'),
)

class UploadPk(models.Model):
    upload = models.OneToOneField('AkadGadai',null=True, blank=True)
    berkas_pk = models.FileField(upload_to="media/pk/")
    
    def filename(self):
        return os.path.basename(self.berkas_pk.name)

    def get_absolute_url(self):
        return "/"

    class Meta:
        db_table = "uploadpk"
        verbose_name = ' UploadPk'
        ordering = ['-id']

class BerkasGadai(models.Model):
    upload = models.ForeignKey('AkadGadai')
    tanda_tangan = models.FileField(upload_to="media/berkasttd/")
    foto_nasabah = models.FileField(upload_to="media/berkasfoto/")
    berkas_barang = models.FileField(upload_to="media/barang/")
    
    def filename(self):
        return os.path.basename(self.tanda_tangan.name)

    def get_absolute_url(self):
        return "/"

    class Meta:
        db_table = "berkasgadai"
        verbose_name = 'BerkasGadai'
        ordering = ['-id']

class Teguran(models.Model):
    agteguran = models.ForeignKey(AkadGadai)
    tanggal = models.DateField(null=True)    
    no_teg = models.IntegerField(editable=True)
    nilai = models.FloatField()
    cu = models.ForeignKey(User, related_name='c_teguran', editable=False, null=True, blank=True)
    mu = models.ForeignKey(User, related_name='m_teguran', editable=False, null=True, blank=True)
    cdate = models.DateTimeField(auto_now_add=True)
    mdate = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'teguran'
        verbose_name = 'Teguran'
        verbose_name_plural = verbose_name

STATUS_HILANG = (
    ('1','LAPUR'),
)

class Hilang(models.Model):
    aghilang = models.ForeignKey(AkadGadai)
    tanggal = models.DateField(null=True)    
    status = models.CharField(max_length=7,choices=STATUS_HILANG)
    cu = models.ForeignKey(User, related_name='c_hilang', editable=False, null=True, blank=True)
    mu = models.ForeignKey(User, related_name='m_hilang', editable=False, null=True, blank=True)
    cdate = models.DateTimeField(auto_now_add=True)
    mdate = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'hilang'
        verbose_name = 'Hilang'

STATUS_LAIN_LAIN = (
    ('1','LAIN LAIN'),
)

class Lainlain(models.Model):
    aglain = models.ForeignKey(AkadGadai)
    tanggal = models.DateField(null=True)    
    status = models.CharField(max_length=7,choices=STATUS_LAIN_LAIN)
    cu = models.ForeignKey(User, related_name='c_lain_lain', editable=False, null=True, blank=True)
    mu = models.ForeignKey(User, related_name='m_lain_lain', editable=False, null=True, blank=True)
    cdate = models.DateTimeField(auto_now_add=True)
    mdate = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'lainlain'
        verbose_name = 'Lainlain'
        verbose_name_plural = verbose_name


STATUS_LUNAS = (
    ('1','LUNAS TERJUAL'),
)

class LunasTerjual(models.Model):
    aglunas = models.ForeignKey(AkadGadai)
    tanggal = models.DateField(null=True)    
    status = models.CharField(max_length=7,choices=STATUS_LUNAS)
    cu = models.ForeignKey(User, related_name='c_lunasterjual', editable=False, null=True, blank=True)
    mu = models.ForeignKey(User, related_name='m_lunasterjual', editable=False, null=True, blank=True)
    cdate = models.DateTimeField(auto_now_add=True)
    mdate = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'lunasterjual'
        verbose_name = 'LunasTerjual'
        verbose_name_plural = verbose_name
        
    #def __unicode__(self):
        #return self.aglunas

    def norek_jual_lunas(self):
        return "%s.%s.%s.%s" % (str(self.aglunas.gerai.kode_cabang).zfill(1),(self.tanggal.year),str(self.aglunas.jenis_transaksi).zfill(1),str(self.id).zfill(6))

           
STATUS_LAPUR = (
    ('1','AYDA'),
    ('2','TERJUAL')
)

class Lapur(models.Model):
    aglapur = models.ForeignKey(AkadGadai)
    gerai = models.CharField(max_length =30)
    tanggal = models.DateField(null=True)    
    status = models.CharField(max_length=7,choices=STATUS_LAPUR)
    nilai = models.DecimalField(max_digits=12, decimal_places=2,null=True,blank=True,default=0)
    jasa = models.DecimalField(max_digits=12,decimal_places=2,default=0,null=True,blank=True)
    denda = models.DecimalField(max_digits=12,decimal_places=2,default=0,null=True,blank=True)
    terlambat = models.IntegerField(max_length=4,default=0,null=True,blank=True)
    cu = models.ForeignKey(User, related_name='c_lapur', editable=False, null=True, blank=True)
    mu = models.ForeignKey(User, related_name='m_lapur', editable=False, null=True, blank=True)
    cdate = models.DateTimeField(auto_now_add=True)
    mdate = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'lapur'
        verbose_name = 'Lapur'

    def __unicode__(self):
        return self.aglapur.agnasabah.nama

    def total_ayda(self):
        return self.nilai + self.jasa + self.denda

    def norek_lapur(self): 
        return "%s.%s.%s.%s" % (str(self.aglapur.gerai.kode_cabang).zfill(1),(self.tanggal.year),str(self.aglapur.jenis_transaksi).zfill(1),str(self.id).zfill(6))

class HistoryLapur(models.Model):
    aglapur = models.ForeignKey(AkadGadai)
    gerai = models.CharField(max_length =30)
    tanggal = models.DateField(null=True)    
    status = models.CharField(max_length=7,choices=STATUS_LAPUR)
    nilai = models.DecimalField(max_digits=12, decimal_places=2,null=True,blank=True,default=0)
    jasa = models.DecimalField(max_digits=12,decimal_places=2,default=0,null=True,blank=True)
    denda = models.DecimalField(max_digits=12,decimal_places=2,default=0,null=True,blank=True)
    terlambat = models.IntegerField(max_length=4,default=0,null=True,blank=True)
    cu = models.ForeignKey(User, related_name='c_history_lapur', editable=False, null=True, blank=True)
    mu = models.ForeignKey(User, related_name='m_history_lapur', editable=False, null=True, blank=True)
    cdate = models.DateTimeField(auto_now_add=True)
    mdate = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'historylapur'
        verbose_name = 'HistoryLapur'


STATUS_WRITEOFF = (
    ('1','WRITE OFF'),
)

class Writeoff(models.Model):
    agwo = models.ForeignKey(AkadGadai)
    tanggal = models.DateField(null=True)    
    status = models.CharField(max_length=7,choices=STATUS_WRITEOFF)
    cu = models.ForeignKey(User, related_name='c_writeoff', editable=False, null=True, blank=True)
    mu = models.ForeignKey(User, related_name='m_writeoff', editable=False, null=True, blank=True)
    cdate = models.DateTimeField(auto_now_add=True)
    mdate = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'writeoff'
        verbose_name = 'writeoff'

ITEM_JURNAL_AYDA=(
    ('1','AYDA PUSAT'),
    ('2','AYDA GERAI ANGGOTA'),
    ('3','AYDA GERAI NON ANGGOTA'),
    ('4','PENJUALAN AYDA BANK'),
    ('5','PENJUALAN AYDA KAS'),
)

class AydaMapper(models.Model):
    item = models.CharField(max_length=50,null=True,blank=True,choices=ITEM_JURNAL_AYDA)
    cabang = models.ForeignKey('Tbl_Cabang',blank=True,null=True)
    debet = models.ForeignKey('Tbl_Akun',related_name="+",blank=True,null=True)
    kredit = models.ForeignKey('Tbl_Akun',related_name="+",blank=True,null=True)
    debet_lawan = models.ForeignKey('Tbl_Akun',related_name="+",blank=True,null=True)
    kredit_lawan = models.ForeignKey('Tbl_Akun',related_name="+",blank=True,null=True)
    kredit_lawan1 = models.ForeignKey('Tbl_Akun',related_name="+",blank=True,null=True)
    kredit_lawan2 = models.ForeignKey('Tbl_Akun',related_name="+",blank=True,null=True)
    debet_penjualan = models.ForeignKey('Tbl_Akun',related_name="+",blank=True,null=True)
    debet_penjualan_untung = models.ForeignKey('Tbl_Akun',related_name="+",blank=True,null=True)
    debet_penjualan_rugi = models.ForeignKey('Tbl_Akun',related_name="+",blank=True,null=True)
    kredit_penjualan = models.ForeignKey('Tbl_Akun',related_name="+",blank=True,null=True)
    kredit_penjualan_ayda = models.ForeignKey('Tbl_Akun',related_name="+",blank=True,null=True)
    
    class Meta:
       db_table = 'aydamapper'


class Biaya_Materai(models.Model):####BIAYA MATERAI PUSAT
    gerai = models.ForeignKey('Tbl_Cabang',null=True)
    tanggal = models.DateField(help_text="Tahun-bl-tg", null=True)
    saldo_awal = models.FloatField(default=0)
    saldo_akhir =  models.FloatField(default=0)
    antar_gerai= models.CharField(max_length=20 , null=True, blank=True)
    nilai = models.FloatField(default=0)
    keterangan = models.CharField(max_length=50 , null=True, blank=True)
    
    class Meta:
        db_table ='biaya_materai'
        verbose_name = 'Biaya_Materai'

class Biaya_Materai_Cab(models.Model):####BIAYA MATERAI CABANG
    gerai = models.ForeignKey('Tbl_Cabang',null=True)
    tanggal = models.DateField(help_text="Tahun-bl-tg", null=True)
    saldo_awal = models.FloatField(default=0)
    saldo_akhir =  models.FloatField(default=0)
    antar_gerai= models.CharField(max_length=20 , null=True, blank=True)
    nilai = models.FloatField(default=0)
    keterangan = models.CharField(max_length=50 , null=True, blank=True)
    norek = models.CharField(max_length=50 , null=True, blank=True)
    status = models.CharField(max_length=10 , null=True, blank=True)


    class Meta:
        db_table ='biaya_materai_cab'
        verbose_name = 'Biaya_Materai_Cab'


class BiayaManager(models.Manager):
    pass

    def for_user(self, user):
        try:
            biaya = user.get_profile().gerai
            geraigadai_list = self.all().filter(id__exact=gerai.id) | gerai.geraigadai_set.all()
        except:
            geraigadai_list = None
        return geraigadai_list

class Biaya(models.Model):
    gerai = models.ForeignKey('Tbl_Cabang',null=True,blank=True)
    tanggal = models.DateField(help_text="Tahun-bl-tg", null=True)
    saldo_awal = models.FloatField(default=0)
    saldo_akhir =  models.FloatField(default=0)
    antar_gerai_kembali= models.ForeignKey('Tbl_Cabang', null=True, blank=True,related_name="antar_gerai_kmb")
    antar_gerai= models.ForeignKey('Tbl_Cabang',null=True, blank=True,related_name="antar_gerai")
    penerimaan_saldo = models.FloatField(default=0)
    
    listrik = models.FloatField(default=0)
    ket_listrik= models.CharField(max_length=50 , null=True, blank=True)
    jenis_transaksi_listrik = models.CharField(max_length=2 , null=True, blank=True)
    
    pdam = models.FloatField(default=0)
    ket_pdam= models.CharField(max_length=50 , null=True, blank=True)
    jenis_transaksi_pdam = models.CharField(max_length=2 , null=True, blank=True)
    
    telpon = models.FloatField(default=0)
    ket_telpon= models.CharField(max_length=50 , null=True, blank=True)
    jenis_transaksi_telepon = models.CharField(max_length=2 , null=True, blank=True)
    
    foto_copy = models.FloatField(null=True,blank=True,default=0)
    ket_foto_copy= models.CharField(max_length=50 , null=True, blank=True)
    jenis_transaksi_foto_copy = models.CharField(max_length=2 , null=True, blank=True)
    
    majalah = models.FloatField(default=0)
    ket_majalah= models.CharField(max_length=50 , null=True, blank=True)
    jenis_transaksi_majalah = models.CharField(max_length=2 , null=True, blank=True)
    
    
    palkir = models.FloatField(default=0)
    ket_palkir= models.CharField(max_length=50 , null=True, blank=True)
    jenis_transaksi_palkir = models.CharField(max_length=2 , null=True, blank=True)
    
    bbm = models.FloatField(default=0)   
    ket_bbm= models.CharField(max_length=50 , null=True, blank=True)
    jenis_transaksi_bbm = models.CharField(max_length=2 , null=True, blank=True)
    
    #pulsa = models.FloatField(default=0)
    #ket_pulsa= models.CharField(max_length=50 , null=True, blank=True)
    jenis_transaksi_materai = models.CharField(max_length=2 , null=True, blank=True)
    
    materai = models.FloatField(default=0)
    ket_materai= models.CharField(max_length=50 , null=True, blank=True)
    jenis_transaksi_materai = models.CharField(max_length=2 , null=True, blank=True)
    
    pemb_lingkungan = models.FloatField(default=0)
    ket_pemb_lingkungan = models.CharField(max_length=50 , null=True, blank=True)
    jenis_transaksi_pemb_lingkungan = models.CharField(max_length=2 , null=True, blank=True)
    
    sumbangan= models.FloatField(default=0)
    ket_sumbangan = models.CharField(max_length=50 , null=True, blank=True)
    jenis_transaksi_sumbangan = models.CharField(max_length=2 , null=True, blank=True)
    
    perlengkapan = models.FloatField(default=0)
    ket_perlengkapan = models.CharField(max_length=50 , null=True, blank=True)
    jenis_transaksi_perlengkapan = models.CharField(max_length=2 , null=True, blank=True)
    
    konsumsi = models.FloatField(default=0)
    ket_konsumsi = models.CharField(max_length=50 , null=True, blank=True)
    jenis_transaksi_konsumsi = models.CharField(max_length=2 , null=True, blank=True)

    
    ket_penambahan_uk= models.CharField(max_length=50 , null=True, blank=True)
    ket_penambahan_saldo= models.CharField(max_length=50 , null=True, blank=True)

    pengembalian_uk = models.FloatField(default=0)
    ket_pengembalian_uk = models.CharField(max_length=50 , null=True, blank=True)
    penambahan_uk = models.FloatField(default=0)
    pengembalian_saldo = models.FloatField(default=0)
    penambahan_saldo = models.FloatField(default=0)
    ket_pengembalian_saldo= models.CharField(max_length=50 , null=True, blank=True)
    
    js_trans = models.CharField(max_length=20 , null=True, blank=True,default=None)
    js_trans_kembali = models.CharField(max_length=20 , null=True, blank=True,default=None)

    ###TAMBAHAN
    jenis_transaksi_biaya_bank = models.CharField(max_length=2 , null=True, blank=True)
    biaya_bank = models.FloatField(default=0)
    ket_biaya_bank = models.CharField(max_length=50 , null=True, blank=True)

    jenis_transaksi_pengiriman = models.CharField(max_length=2 , null=True, blank=True)
    pengiriman = models.FloatField(default=0)
    ket_pengiriman = models.CharField(max_length=50 , null=True, blank=True)
    class Meta:
        db_table="biaya"
        verbose_name="Biaya"
        verbose_name_plural = verbose_name
        ordering = ['-tanggal']        

    def get_absolute_url(self):
        return "/biaya/"


    def _get_totalbiaya(self):
        try:
            ret= self.listrik+ self.pdam+ self.telpon+self.foto_copy+self.majalah+self.iuran_keamanan+self.iuran_kebersihan+self.promosi+self.air_minum+self.sewa_gedung_gerai
            return ret
        except:
            return 0
    jumlahbiaya = property(_get_totalbiaya)

    def _get_totalpos(self):
        try:
            ret= self.prangko+ self.surat_kilat_khusus+ self.paket_pos_standar+self.paket_kilat_khusus+self.pos_express+self.ems+self.materai
            return ret
        except:
            return 0
    jumlahpospay = property(_get_totalpos)

    def _get_totalkas_gerai(self):
        try:
            ret= self.tunai + self.dari_gerai + self.bank
            return ret
        except:
            return 0
    jumlahkasgerai = property(_get_totalkas_gerai)

    def _get_totalkas_setoran(self):
        try:
            ret= self.setoran_bank + self.ke_gerai + self.tunai_pickup
            return ret
        except:
            return 0
    jumlahkassetoran = property(_get_totalkas_setoran)

class BiayaPusat(models.Model):
    gerai = models.ForeignKey('Tbl_Cabang',null=True,blank=True)
    tanggal = models.DateField(help_text="Tahun-bl-tg", null=True)
    saldo_awal = models.FloatField(default=0)
    saldo_akhir =  models.FloatField(default=0,null=True,blank=True)
    antar_gerai= models.CharField(max_length=20 , null=True, blank=True,default=None)
    #antar_gerai_kembali= models.CharField(max_length=20 , null=True, blank=True,default=None)
    antar_gerai_kembali= models.ForeignKey('Tbl_Cabang', null=True, blank=True,related_name="antar_pusat_kmbl")
    antar_gerai= models.ForeignKey('Tbl_Cabang',null=True, blank=True,related_name="antar_pusat")
 
    penerimaan_saldo = models.FloatField(default=0,null=True,blank=True)
    pendapatan_lain =  models.FloatField(default=0,null=True,blank=True)
    ket_pendapatan_lain= models.CharField(max_length=500 , null=True, blank=True)
    ###TAMBAHAN SEPUR
    bbm = models.FloatField(default=0,null=True,blank=True)
    ket_bbm = models.CharField(max_length=500 , null=True, blank=True)
    jenis_transaksi_bbm = models.CharField(max_length=6 , null=True, blank=True)
    bbm_gerai= models.ForeignKey('Tbl_Cabang', null=True, blank=True,related_name="+")

    tol = models.FloatField(default=0,null=True,blank=True)
    ket_tol= models.CharField(max_length=500 , null=True, blank=True)
    jenis_transaksi_tol = models.CharField(max_length=6 , null=True, blank=True)
    tol_gerai= models.ForeignKey('Tbl_Cabang', null=True, blank=True,related_name="+")

    transport = models.FloatField(default=0,null=True,blank=True)
    ket_transport = models.CharField(max_length=500 , null=True, blank=True)
    jenis_transaksi_transport = models.CharField(max_length=6 , null=True, blank=True)
    transport_gerai= models.ForeignKey('Tbl_Cabang', null=True, blank=True,related_name="+")

    peralkantor = models.FloatField(default=0,null=True,blank=True)
    ket_peralkantor = models.CharField(max_length=500 , null=True, blank=True)
    jenis_transaksi_peralkantor = models.CharField(max_length=6 , null=True, blank=True)
    peralkantor_gerai= models.ForeignKey('Tbl_Cabang', null=True, blank=True,related_name="+")
    ##AKHIR TAMBAHAN SEPUR    
    gaji = models.FloatField(default=0,null=True,blank=True)
    ket_gaji= models.CharField(max_length=500 , null=True, blank=True)
    jenis_transaksi_gaji = models.CharField(max_length=6 , null=True, blank=True)
    gaji_gerai= models.ForeignKey('Tbl_Cabang', null=True, blank=True,related_name="+")

    sewa = models.FloatField(default=0,null=True,blank=True)
    ket_sewa= models.CharField(max_length=500 , null=True, blank=True)
    jenis_transaksi_sewa = models.CharField(max_length=6 , null=True, blank=True)
    sewa_gerai= models.ForeignKey('Tbl_Cabang', null=True, blank=True,related_name="+")
    
    listrik = models.FloatField(default=0,null=True,blank=True)
    ket_listrik= models.CharField(max_length=500 , null=True, blank=True)
    jenis_transaksi_listrik = models.CharField(max_length=6 , null=True, blank=True)
    listrik_gerai= models.ForeignKey('Tbl_Cabang', null=True, blank=True,related_name="+")
    
    pdam = models.FloatField(default=0,null=True,blank=True)
    ket_pdam= models.CharField(max_length=500 , null=True, blank=True)
    jenis_transaksi_pdam = models.CharField(max_length=6 , null=True, blank=True)
    pdam_gerai= models.ForeignKey('Tbl_Cabang', null=True, blank=True,related_name="+")
    
    telpon = models.FloatField(default=0,null=True,blank=True)
    ket_telpon= models.CharField(max_length=500 , null=True, blank=True)
    jenis_transaksi_telepon = models.CharField(max_length=6 , null=True, blank=True)
    telpon_gerai= models.ForeignKey('Tbl_Cabang', null=True, blank=True,related_name="+")
    
    foto_copy = models.FloatField(null=True,blank=True,default=0)
    ket_foto_copy= models.CharField(max_length=500 , null=True, blank=True)
    jenis_transaksi_foto_copy = models.CharField(max_length=6 , null=True, blank=True)
    fotocopy_gerai= models.ForeignKey('Tbl_Cabang', null=True, blank=True,related_name="+")
    
    majalah = models.FloatField(default=0,null=True,blank=True)
    ket_majalah= models.CharField(max_length=500 , null=True, blank=True)
    jenis_transaksi_majalah = models.CharField(max_length=6 , null=True, blank=True)
    majalah_gerai= models.ForeignKey('Tbl_Cabang', null=True, blank=True,related_name="+")


    ##untuk transaksi pusat
    nilai_materai = models.FloatField(default=0,null=True,blank=True)
    keterangan_materai = models.CharField(max_length=500 , null=True, blank=True)
    
    ## AKhir untuk transaksi pusat
    
    pemb_lingkungan = models.FloatField(default=0,null=True,blank=True)
    ket_pemb_lingkungan = models.CharField(max_length=500 , null=True, blank=True)
    jenis_transaksi_pemb_lingkungan = models.CharField(max_length=6 , null=True, blank=True)
    lingkungan_gerai= models.ForeignKey('Tbl_Cabang', null=True, blank=True,related_name="+")
    
    sumbangan= models.FloatField(default=0,null=True,blank=True)
    ket_sumbangan = models.CharField(max_length=500 , null=True, blank=True)
    jenis_transaksi_sumbangan = models.CharField(max_length=6 , null=True, blank=True)
    sumbangan_gerai= models.ForeignKey('Tbl_Cabang', null=True, blank=True,related_name="+")
    
    perlengkapan = models.FloatField(default=0,null=True,blank=True)
    ket_perlengkapan = models.CharField(max_length=500 , null=True, blank=True)
    jenis_transaksi_perlengkapan = models.CharField(max_length=6 , null=True, blank=True)
    perlengkapan_gerai= models.ForeignKey('Tbl_Cabang', null=True, blank=True,related_name="+")
    
    konsumsi = models.FloatField(default=0,null=True,blank=True)
    ket_konsumsi = models.CharField(max_length=500 , null=True, blank=True)
    jenis_transaksi_konsumsi = models.CharField(max_length=6 , null=True, blank=True)
    js_trans = models.CharField(max_length=20 , null=True, blank=True,default=None)
    js_trans_kembali = models.CharField(max_length=20 , null=True, blank=True,default=None)
    konsumsi_gerai= models.ForeignKey('Tbl_Cabang', null=True, blank=True,related_name="+")
 
    ## TAMBAHAN UANG MUKA
    pengembalian_uk = models.FloatField(default=0)
    ket_pengembalian_uk = models.CharField(max_length=500 , null=True, blank=True)
    penambahan_uk = models.FloatField(default=0)
    ket_penambahan_uk= models.CharField(max_length=500 , null=True, blank=True)

    pembelian_materai = models.FloatField(default=0)
    ket_pmb_materai= models.CharField(max_length=500 , null=True, blank=True)
    jenis_pmb_materai = models.CharField(max_length=6 , null=True, blank=True)

    jual_materai = models.FloatField(default=0)
    ket_jual_materai= models.CharField(max_length=500 , null=True, blank=True)
    jenis_jual_materai = models.CharField(max_length=6 , null=True, blank=True)

    class Meta:
        db_table="biayapusat"
        verbose_name="BiayaPusat"
        verbose_name_plural = verbose_name
        ordering = ['-tanggal']        


STATUS_AKTIFASI = (
    ('1','NON AKTIF'),
    ('2','AKTIF')
)
class Taksir(models.Model):
    type = models.CharField(max_length=500)
    spesifikasi = models.CharField(max_length=350, null=True, blank=True)
    harga_baru = models.FloatField()
    harga_pasar = models.FloatField()
    maxpinjaman = models.FloatField()
    tglupdate = models.DateField()
    status = models.CharField(max_length=4 ,choices=STATUS_AKTIFASI, null=True, blank=True)    
    class Meta:
        db_table="taksir"
        verbose_name="Taksir"
        verbose_name_plural = verbose_name
        ordering = ['-type']

    def __unicode__(self):
        return "%s- Rp. %s - %s" %(self.type,number_format(self.maxpinjaman), self.id)

    def get_absolute_url(self):
        return "/taksir/%s/show/" % self.id

    def kobar(self):
        return "%s" % (str(self.id).zfill(4))


STATUS_TAKSIR =(
    ('1','Non Aktif'),
    ('2','Aktif'),    
)

class TaksirHistory(models.Model):
    history= models.ForeignKey('Taksir')
    type = models.CharField(max_length=500)
    spesifikasi = models.CharField(max_length=350, null=True, blank=True)
    harga_baru = models.FloatField()
    harga_pasar = models.FloatField()
    maxpinjaman = models.FloatField()
    tglupdate = models.DateTimeField()
    tgl = models.DateTimeField()
    status = models.CharField(max_length=35,choices=STATUS_TAKSIR, null=True, blank=True)
    cu = models.ForeignKey(User, related_name='+', null=True, blank=True)
    mu = models.ForeignKey(User, related_name='+', null=True, blank=True)
    
    class Meta:
        db_table="taksirhistory"
        verbose_name="TaksirHistory"
        verbose_name_plural = verbose_name
        ordering = ['-type']

STATUS_MANOP = (
    ('1','CAIR'),
    ('2','TOLAK'),
)
class ManopGadai(models.Model):
    manop = models.OneToOneField('AkadGadai',null=True, blank=True)
    pelunasan = models.OneToOneField('Pelunasan',null=True, blank=True)
    status = models.CharField(max_length=1, choices=STATUS_MANOP)
    tanggal = models.DateField()
    cu = models.ForeignKey(User, related_name='c_manopgadai', editable=False, null=True, blank=True)
    mu = models.ForeignKey(User, related_name='m_manopgadai', editable=False, null=True, blank=True)
    note = models.CharField(max_length=200, null=True, blank=True)
    
    class Meta:
        db_table = 'manopGadai'
        verbose_name = 'ManopGadai'
        verbose_name_plural = verbose_name

JENIS_PNC = (
    ('1','KAS'),('2','BANK')
)
STATUS_ADMGUDANG = (
    ('1','TERIMA GUDANG'),
    ('2','BLM DITERIMA'),
)

class AdmGudang(models.Model):
    adm = models.ForeignKey(AkadGadai)
    status = models.CharField(max_length=1, choices=STATUS_ADMGUDANG)
    tanggal = models.DateField()
    cu = models.ForeignKey(User, related_name='c_admgudang', editable=False, null=True, blank=True)
    mu = models.ForeignKey(User, related_name='m_admgudang', editable=False, null=True, blank=True)
    note = models.CharField(max_length=200, null=True, blank=True)
    
    class Meta:
        db_table = 'admgudang'
        verbose_name = 'AdmGudang'
        verbose_name_plural = verbose_name
        get_latest_by = 'status'

##firman##
class BarangLelang(models.Model):
    aglelang =models.ForeignKey(AkadGadai)
    tgl_lelang = models.DateField(null = True)
    harga_jual = models.FloatField()
    nama_pembeli = models.CharField(max_length=70, blank = True, null=True)
    no_identitas = models. CharField( max_length= 20, null=True)
    alamat_pembeli = models.CharField(max_length=120,null=True, blank=True)
    no_telp = models.CharField(max_length=70, blank = True, null=True)   
    jenis = models.CharField(max_length=1, choices=JENIS_PNC,blank=True,null=True) 
    class Meta:
        db_table="lelang"
        verbose_name="Lelang"
        verbose_name_plural = verbose_name

    def laba(self):
       return self.aglelang.nilai - self.harga_jual 

    def tt_jual(self):
        selisih = self.harga_jual - self.aglelang.nilai
        if selisih > 0 :
            return selisih
        else:
            return 0        
STATUS_AKUN =(
    ('0','Tidak Aktif'),
    ('1','Aktif'),
)

JENIS_AKUN =(
    ('A','AKTIFA'),
    ('P','PASSIVA'),
    ('L','RUGI DAN LABA')
)

VIEW_UNIT_AKUN =(
    ('0','SEMUA'),
    ('000','PASSIVA'),
    ('L','RUGI DAN LABA')
)

## NEraca neraca 
AKTIVA_AA = ('10.00.00','11.00.00','11.01.00','11.01.01','11.01.02','11.01.03','11.01.04','11.01.05','11.01.06','11.01.07','11.01.08','11.01.09',
'11.01.10','11.01.11','11.01.12','11.01.13','11.01.14','11.01.15','11.01.16','11.01.17','11.01.18','11.01.19','11.01.20','11.01.21',
'11.01.22','11.01.23','11.01.24','11.01.25','11.01.35','11.05.00','11.05.01','11.05.02','11.05.03','11.05.04','11.05.05','11.05.06',
'11.05.07','11.05.08','11.05.09','11.05.10','11.05.11','11.05.12','11.05.13','11.05.14','11.05.15','11.05.16','11.05.17','11.05.18',
'11.05.19','11.05.20','11.05.21','11.05.22','11.05.23','11.06.00','11.06.01','11.06.02','11.06.99','11.07.00','11.07.01','11.08.00',
'11.08.01','11.09.00','11.09.01','11.10.00','11.10.01','11.10.02','11.10.03','11.10.04','11.10.06','11.10.07','11.10.08','11.10.12',
'11.11.00','11.11.01','11.11.02','11.11.03','11.11.04','11.12.00','11.12.02','11.13.00','11.13.01','11.13.02','11.13.03','11.13.04',
'11.13.05','11.13.06','11.13.07','11.13.08','11.13.09','11.13.10','11.13.11','12.00.00','12.01.00','12.01.01','12.01.02','12.01.03',
'12.01.04','12.01.05','12.01.06','12.02.00','12.02.01','12.02.02','12.02.03','12.02.04','12.02.05','12.03.00','12.03.01','12.03.02',
'12.03.03','12.03.04','12.03.05','13.00.00','13.01.00','13.01.01','13.01.02','13.01.03','13.01.04','13.02.00','13.02.01','13.02.02',
'13.02.03','13.02.04','13.02.05','13.02.06','13.02.07','13.02.99','13.03.00','13.03.01','13.03.02','13.03.03','13.03.04','13.03.99',
'13.04.00','13.04.01','13.04.02','13.04.03','13.04.99','13.05.00','13.05.01','13.05.02','13.05.10','13.06.00','13.06.01','13.06.02',
'13.06.03','13.06.04','13.06.05','13.06.06','13.06.07','13.06.08','13.06.09','13.06.10','13.06.14','13.06.15','13.06.16','13.06.22',
'13.06.99','13.06.23','12.03.08',
'11.05.24','11.05.25','11.05.26','11.05.27','11.05.28','11.05.29','11.05.30','11.05.31',
###Tambahan
'12.03.23','12.03.22','12.03.21','12.03.20','12.03.19','12.03.18','12.03.17','12.03.16','12.03.15','12.03.14','12.03.13','12.03.12',
'12.03.11','12.03.10','12.03.09','12.03.08','12.03.07','12.03.06',)

PASIVA_BB = ('20.00.00','21.00.00','21.01.00','21.01.01','21.01.02','21.01.03','21.01.04','21.02.00','21.02.01','21.03.00','21.03.01','21.03.02',
'21.04.00','21.04.01','21.04.02','21.05.00','21.05.01','21.05.10','21.06.00','21.06.03','21.06.04','21.06.05','21.06.06','21.06.07',
'21.06.08','21.06.09','21.06.10','21.06.11','21.06.12','21.06.13','21.06.14','21.06.15','21.06.16','21.06.17','21.06.18','21.06.99',
'21.07.00','21.07.01','21.07.02','21.08.00','21.08.01','21.08.02','21.09.00','21.09.01','21.09.02','21.10.00','21.10.01','22.00.00',
'22.03.00','22.03.01','22.03.02','22.03.03','22.03.04','22.04.00','22.04.01','22.04.02','22.04.03','22.04.04','22.04.05','22.04.06',
'22.04.07','22.04.08','22.04.09','22.04.10','22.04.11','22.04.12','22.05.00','22.05.01','22.05.02','22.05.03','22.05.04','22.05.05',
'22.06.00','22.06.01','23.00.00','23.01.00','23.01.01','23.01.02','23.02.00','23.02.01','23.02.02','23.02.03','22.05.08',
##Tambahan
'22.05.99','22.05.23','22.05.22','22.05.21','22.05.20','22.05.19','22.05.18','22.05.17','22.05.16','22.05.15','22.05.14','22.05.13',
'22.05.12','22.05.11','22.05.10','22.05.09','22.05.08','22.05.07','22.05.06')

EKUITAS_CC = ('30.00.00','31.00.00','31.01.01','31.01.02','31.01.03','32.00.00','32.01.01','32.01.02','32.01.03','33.00.00',
'33.01.01','34.00.00','34.01.01','34.01.02','35.00.00','35.01.01','35.01.02','35.01.03','35.01.04')
## Akhir NEraca neraca 

### Untuk Laba Rugi
AA =('41.00.00','41.01.00','41.01.01','41.01.02','41.01.03','41.01.04','41.01.05','41.01.07','41.01.08','41.02.00','41.02.01','41.02.02',
'41.02.03','41.02.12','41.03.00','41.03.01','41.03.02','41.03.09','41.03.10','41.04.00','41.04.01','41.04.02','41.04.03','41.04.04',
'41.04.05','41.04.06','41.04.99')

BB = ('60.00.00','61.00.00','61.01.01','61.01.02','61.01.03','61.01.04','61.01.99','61.01.05','61.01.06','61.01.07')

CC =('50.00.00','51.00.00','51.01.00','51.01.01','51.01.02','51.01.03','51.01.04','51.01.05','51.01.06','51.01.07',
'51.01.08','51.02.00','51.02.01','51.02.02','51.02.03','51.03.00','51.03.01','51.03.02','51.03.03','51.03.04',
'51.03.05','51.03.06','51.03.07','51.03.08','51.03.09','51.04.00','51.04.01','51.04.02','51.04.03','51.05.00',
'51.05.01','51.06.00','51.06.01','51.06.02','51.06.03','51.06.04','51.06.05','51.07.00','51.07.01','51.07.02',
'51.07.03','51.07.04','51.08.00','51.08.01','51.08.02','51.08.03','51.08.04','51.09.00','51.09.01','51.09.02',
'51.09.03','51.09.04','51.09.05','51.09.06','51.09.07','51.09.08','51.09.09','51.09.10','51.09.11','51.09.99',
'51.10.00','51.10.01','51.10.02','51.10.03','51.10.04','51.10.99','51.11.00','51.11.01','51.11.02','51.11.03',
'51.11.04','51.11.05','51.11.06','51.11.07','51.11.08','51.11.09','51.11.10','51.11.11','51.11.12','51.11.13',
'51.11.14','51.11.15','51.11.16','51.11.17','51.11.18','51.11.19','51.11.20','51.11.21','51.11.22','51.11.23',
'51.11.24','51.11.99')

DD =('70.00.00','71.01.00','71.01.01','71.01.02','71.01.03','71.01.04','71.01.05',
'71.01.99','51.11.25','51.04.04','51.10.05','51.11.26','51.11.27')
### Akhir Laba Rugi

#class Tbl_AkunManager(models.Manager):     
LAPORAN_AKUN =( 
                ('A','AKTIFA'),('P','PASSIVA'),('E','EKUITAS'),('PO','PENDAPATAN OPS'),
				('BO','BEBAN OPS'),('PNO','PENDAPATAN NON OPS'),('BNO','BEBAN NON OPS'),
                ('K','KONTIGEN'),('KS','KONTIGENSI'),
)
class Tbl_Akun(models.Model):
    no_urut = models.IntegerField(null=True, blank=True, editable=False)
    kode_guna = models.CharField(max_length=15)
    header_parent = models.ForeignKey('self', null=True, blank=True)
    coa = models.CharField(max_length=15, unique=True)
    deskripsi = models.CharField(max_length=500)
    saldo_mf = models.DecimalField(null=True, blank=True, max_digits =11,decimal_places = 2)
    saldo_krs = models.DecimalField(null=True, blank=True,max_digits =11,decimal_places = 2)
    saldo_pjb = models.DecimalField(null=True, blank=True,max_digits =18,decimal_places = 2)
    

    status = models.CharField(max_length=10, choices=STATUS_AKUN)
    jenis = models.CharField(max_length=10, choices=JENIS_AKUN)
    view_unit = models.CharField(max_length=10)
    kode_cabang = models.CharField(max_length=3,null=True,blank=True)
    view_cabang = models.CharField(max_length=10)
    tanggal = models.DateField(null=True, blank=True)
    saldo_akhir_pjb = models.DecimalField(null=True, blank=True,max_digits =11,decimal_places = 2)
    layer = models.CharField(max_length=5,null=True,blank=True)
    jenis_laporan = models.CharField(max_length=30, choices=LAPORAN_AKUN)
    #objects = Tbl_AkunManager()        

    class Meta:
        db_table = "tbl_akun"


    def total_debet_count(self):
        sekarang = datetime.date.today()
        return sum([a.debet for a in Tbl_Transaksi.objects.filter(id_cabang = 300).filter(id_coa__id = self.id).filter(tgl_trans = sekarang)])
 
    def total_kredit_count(self):
        sekarang = datetime.date.today()
        return sum([a.kredit for a in Tbl_Transaksi.objects.filter(id_cabang = 300).filter(id_coa__id = self.id).filter(tgl_trans = sekarang)])

### Untuk Neraca
    def neraca_saldo_count(self, id_cabang, start_date):
        if id_cabang == '500':
            return sum([a.saldo for a in Tbl_TransaksiKeu.objects.filter(id_coa__coa__in = AKTIVA_AA).filter(tgl_trans=start_date).filter(jenis ='SALDOKASGERAI') ])
        else:
            return sum([a.saldo for a in Tbl_TransaksiKeu.objects.filter(id_coa__coa__in = AKTIVA_AA).filter(id_cabang = id_cabang).filter(tgl_trans=start_date).filter(jenis ='SALDOKASGERAI') ])
  
    def neraca_debet_count(self, id_cabang, start_date,end_date):
        if id_cabang == '500':
            return sum([a.debet for a in Tbl_Transaksi.objects.filter(id_coa__coa__in = AKTIVA_AA).filter(tgl_trans__range=(start_date,end_date))])
        else:
            return sum([a.debet for a in Tbl_Transaksi.objects.filter(id_coa__coa__in = AKTIVA_AA).filter(id_cabang = id_cabang).filter(tgl_trans__range=(start_date,end_date))])

    def neraca_kredit_count(self, id_cabang, start_date,end_date):
        if id_cabang == '500':
            return sum([a.kredit for a in Tbl_Transaksi.objects.filter(id_coa__coa__in = AKTIVA_AA).filter(tgl_trans__range=(start_date,end_date))])
        else:
            return sum([a.kredit for a in Tbl_Transaksi.objects.filter(id_coa__coa__in = AKTIVA_AA).filter(id_cabang = id_cabang).filter(tgl_trans__range=(start_date,end_date))])


    def neraca_pasiva_saldo_count(self, id_cabang, start_date):
        return sum([a.saldo for a in Tbl_TransaksiKeu.objects.filter(id_coa__coa__startswith="2").filter(id_cabang = id_cabang).filter(tgl_trans=start_date).filter(jenis ='SALDOKASGERAI') ])

    def neraca_pasiva_saldo_count_gabungan(self, start_date):
        return sum([a.saldo for a in Tbl_TransaksiKeu.objects.filter(id_coa__coa__startswith="2").filter(tgl_trans=start_date).filter(jenis ='SALDOKASGERAI') ])

    def neraca_pasiva_debet_count(self, id_cabang, start_date,end_date):
        return sum([a.debet for a in Tbl_Transaksi.objects.filter(id_coa__coa__in = PASIVA_BB).filter(id_cabang = id_cabang).filter(tgl_trans__range=(start_date,end_date))])

    def neraca_pasiva_debet_count_gabungan(self, start_date, end_date):
        return sum([a.debet for a in Tbl_Transaksi.objects.filter(id_coa__coa__in = PASIVA_BB).filter(tgl_trans__range=(start_date,end_date))])

    def neraca_pasiva_kredit_count(self, id_cabang, start_date,end_date):
        return sum([a.kredit for a in Tbl_Transaksi.objects.filter(id_coa__coa__in = PASIVA_BB).filter(id_cabang = id_cabang).filter(tgl_trans__range=(start_date,end_date))])

    def neraca_pasiva_kredit_count_gabungan(self, start_date,end_date):
        return sum([a.kredit for a in Tbl_Transaksi.objects.filter(id_coa__coa__in = PASIVA_BB).filter(tgl_trans__range=(start_date,end_date))])

    def neraca_ekuitas_saldo_count(self, id_cabang, start_date):
        return sum([a.saldo for a in Tbl_TransaksiKeu.objects.filter(id_coa__coa__in = EKUITAS_CC).filter(id_cabang = id_cabang).filter(tgl_trans=start_date).filter(jenis ='SALDOKASGERAI') ])

    def neraca_ekuitas_saldo_count_gabungan(self, start_date):
        return sum([a.saldo for a in Tbl_TransaksiKeu.objects.filter(id_coa__coa__in = EKUITAS_CC).filter(tgl_trans=start_date).filter(jenis ='SALDOKASGERAI') ])


    def neraca_ekuitas_debet_count(self, id_cabang, start_date,end_date):
        return sum([a.debet for a in Tbl_Transaksi.objects.filter(id_coa__coa__in = EKUITAS_CC).filter(id_cabang = id_cabang).filter(tgl_trans__range=(start_date,end_date))])       

    def neraca_ekuitas_debet_count_gabungan(self, start_date,end_date):
        return sum([a.debet for a in Tbl_Transaksi.objects.filter(id_coa__coa__in = EKUITAS_CC).filter(tgl_trans__range=(start_date,end_date))])

    def neraca_ekuitas_kredit_count(self, id_cabang, start_date,end_date):
        return sum([a.kredit for a in Tbl_Transaksi.objects.filter(id_coa__coa__in = EKUITAS_CC).filter(id_cabang = id_cabang).filter(tgl_trans__range=(start_date,end_date))])

    def neraca_ekuitas_kredit_count_gabungan(self, start_date,end_date):
        return sum([a.kredit for a in Tbl_Transaksi.objects.filter(id_coa__coa__in = EKUITAS_CC).filter(tgl_trans__range=(start_date,end_date))])

    ### Akhir Untuk Neraca


    #### Untuk Posting Saldo Masuk Ke SHU
    def pdp_lb_rugi_saldo_gabungan_posting(self, start_date, id_cabang):
        return sum([a.saldo for a in Tbl_TransaksiKeu.objects.filter(id_coa__coa__in = AA,id_cabang =
            id_cabang,tgl_trans=start_date,jenis ='SALDOKASGERAI') ])

    def pdp_non_lb_rugi_saldo_gabungan_posting(self, start_date,end_date, id_cabang):
        return sum([a.debet for a in Tbl_Transaksi.objects.filter(id_coa__coa__in = BB).filter(id_cabang = id_cabang).filter(tgl_trans__range=(start_date,end_date)).filter(jenis ='SALDOKASGERAI') ])

    def pdp_non_lb_rugi_kredit_gabungan_posting(self, start_date, end_date, id_cabang):
        return sum([a.kredit for a in Tbl_Transaksi.objects.filter(id_coa__coa__in = BB).filter(id_cabang = id_cabang).filter(tgl_trans__range=(start_date,end_date)) ])

    def pdp_lb_rugi_debet_gabungan_posting(self, start_date,end_date, id_cabang):
        return sum([a.debet for a in Tbl_Transaksi.objects.filter(id_coa__coa__in = AA).filter(id_cabang = id_cabang).filter(tgl_trans__range= (start_date,end_date))])

    def pdp_lb_rugi_kredit_gabungan_posting(self, start_date,end_date, id_cabang):
        return sum([a.kredit for a in Tbl_Transaksi.objects.filter(id_coa__coa__in = AA).filter(id_cabang = id_cabang).filter(tgl_trans__range=(start_date,end_date))]) 

    def pdp_non_lb_rugi_debet_gabungan_posting(self, start_date,end_date,id_cabang):
        return sum([a.debet for a in Tbl_Transaksi.objects.filter(id_coa__coa__in = BB).filter(id_cabang = id_cabang).filter(tgl_trans__range= (start_date,end_date))])

    def beban_lb_rugi_saldo_gabungan_posting(self, start_date,id_cabang):
        return sum([a.saldo for a in Tbl_TransaksiKeu.objects.filter(id_coa__coa__in = CC).filter(id_cabang = id_cabang).filter(tgl_trans=start_date).filter(jenis ='SALDOKASGERAI') ])

    def beban_lb_rugi_kredit_gabungan_posting(self, start_date,end_date,id_cabang):
        return sum([a.kredit for a in Tbl_Transaksi.objects.filter(id_coa__coa__in = CC).filter(id_cabang = id_cabang).filter(tgl_trans__range=(start_date,end_date))])

    def beban_non_lb_rugi_kredit_gabungan_posting(self, start_date,end_date,id_cabang):
        return sum([a.kredit for a in Tbl_Transaksi.objects.filter(id_coa__coa__in = DD).filter(id_cabang = id_cabang).filter(tgl_trans__range= (start_date,end_date))])

    def beban_lb_rugi_debet_gabungan_posting(self, start_date,end_date,id_cabang):
        return sum([a.debet for a in Tbl_Transaksi.objects.filter(id_coa__coa__in = CC).filter(id_cabang = id_cabang).filter(tgl_trans__range= (start_date,end_date))])

    def beban_non_lb_rugi_debet_gabungan_posting(self, start_date,end_date,id_cabang):
        return sum([a.debet for a in Tbl_Transaksi.objects.filter(id_coa__coa__in = DD).filter(id_cabang = id_cabang).filter(tgl_trans__range= (start_date,end_date)) ])

    ### Akhir Untuk Posting Saldo Masuk Ke SHU


    ### Untuk Laba Rugi
    def pdp_lb_rugi_saldo(self, id_cabang, start_date):
        return sum([a.saldo for a in Tbl_TransaksiKeu.objects.filter(id_coa__coa__in = AA).filter(id_cabang = id_cabang).filter(tgl_trans=start_date).filter(jenis ='SALDOKASGERAI') ])

    def pdp_lb_rugi_saldo_gabungan(self, start_date):
        return sum([a.saldo for a in Tbl_Transaksi.objects.filter(id_coa__coa__in = AA).filter(tgl_trans=start_date).filter(jenis ='SALDOKASGERAI') ])

    def pdp_lb_rugi_debet_gabungan(self, start_date,end_date):
        return sum([a.debet for a in Tbl_Transaksi.objects.filter(id_coa__coa__in = AA).filter(tgl_trans__range= (start_date,end_date))])

    def pdp_lb_rugi_debet(self, id_cabang, start_date, end_date):
        return sum([a.debet for a in Tbl_Transaksi.objects.filter(id_coa__coa__in = AA).filter(id_cabang = id_cabang).filter(tgl_trans__range=(start_date, end_date)) ])
    
    def pdp_lb_rugi_kredit(self, id_cabang, start_date, end_date):
        return sum([a.kredit for a in Tbl_Transaksi.objects.filter(id_coa__coa__in = AA).filter(id_cabang = id_cabang).filter(tgl_trans__range=(start_date, end_date)) ])

    def pdp_non_lb_rugi_saldo(self, id_cabang, start_date, end_date):
        return sum([a.debet for a in Tbl_Transaksi.objects.filter(id_coa__coa__in = BB).filter(id_cabang = id_cabang).filter(tgl_trans__range=(start_date, end_date)).filter(jenis ='SALDOKASGERAI') ])

    def pdp_lb_rugi_kredit_gabungan(self, start_date,end_date):
        return sum([a.kredit for a in Tbl_Transaksi.objects.filter(id_coa__coa__in = AA).filter(tgl_trans__range=(start_date,end_date))]) 

    def pdp_non_lb_rugi_saldo_gabungan(self, start_date,end_date):
        return sum([a.debet for a in Tbl_Transaksi.objects.filter(id_coa__coa__in = BB).filter(tgl_trans__range=(start_date,end_date)).filter(jenis ='SALDOKASGERAI') ])

    def pdp_non_lb_rugi_kredit_gabungan(self, start_date, end_date):
        return sum([a.kredit for a in Tbl_Transaksi.objects.filter(id_coa__coa__in = BB).filter(tgl_trans__range=(start_date,end_date)) ])

    def pdp_non_lb_rugi_debet_gabungan(self, start_date,end_date):
        return sum([a.debet for a in Tbl_Transaksi.objects.filter(id_coa__coa__in = BB).filter(tgl_trans__range= (start_date,end_date))])

    def beban_lb_rugi_debet_gabungna(self, start_date):
        return sum([a.debet for a in Tbl_Transaksi.objects.filter(id_coa__coa__in = CC).filter(tgl_trans=start_date) ])

    def beban_lb_rugi_kredit_gabungan(self, start_date,end_date):
        return sum([a.kredit for a in Tbl_Transaksi.objects.filter(id_coa__coa__in = CC).filter(tgl_trans__range=(start_date,end_date))])

    def beban_non_lb_rugi_kredit_gabungan(self, start_date,end_date):
        return sum([a.kredit for a in Tbl_Transaksi.objects.filter(id_coa__coa__in = DD).filter(tgl_trans__range= (start_date,end_date))])

    def beban_lb_rugi_saldo_gabungan(self, start_date):
        return sum([a.saldo for a in Tbl_Transaksi.objects.filter(id_coa__coa__in = CC).filter(tgl_trans=start_date).filter(jenis ='SALDOKASGERAI') ])

    def beban_lb_rugi_debet_gabungan(self, start_date,end_date):
        return sum([a.debet for a in Tbl_Transaksi.objects.filter(id_coa__coa__in = CC).filter(tgl_trans__range= (start_date,end_date))])

    def beban_lb_rugi_kredit_gabungan(self, start_date,end_date):
        return sum([a.kredit for a in Tbl_Transaksi.objects.filter(id_coa__coa__in = CC).filter(tgl_trans__range = (start_date,end_date))])

    def beban_non_lb_rugi_saldo_gabungan(self,start_date):
        return sum([a.saldo for a in Tbl_Transaksi.objects.filter(id_coa__coa__in = DD).filter(tgl_trans=start_date).filter(jenis ='SALDOKASGERAI') ])

    def beban_non_lb_rugi_debet_gabungan(self, start_date,end_date):
        return sum([a.debet for a in Tbl_Transaksi.objects.filter(id_coa__coa__in = DD).filter(tgl_trans__range= (start_date,end_date)) ])

    def pdp_non_lb_rugi_debet(self, id_cabang, start_date, end_date):
        return sum([a.debet for a in Tbl_Transaksi.objects.filter(id_coa__coa__in = BB).filter(id_cabang = id_cabang).filter(tgl_trans__range=(start_date, end_date)) ])

    def pdp_non_lb_rugi_kredit(self, id_cabang, start_date, end_date):
        return sum([a.kredit for a in Tbl_Transaksi.objects.filter(id_coa__coa__in = BB).filter(id_cabang = id_cabang).filter(tgl_trans__range=(start_date, end_date)) ])

    def beban_lb_rugi_saldo(self, id_cabang, start_date):
        return sum([a.saldo for a in Tbl_TransaksiKeu.objects.filter(id_coa__coa__in = CC).filter(id_cabang = id_cabang).filter(tgl_trans=start_date).filter(jenis ='SALDOKASGERAI') ])   

    def beban_lb_rugi_debet(self, id_cabang, start_date, end_date):
        return sum([a.debet for a in Tbl_Transaksi.objects.filter(id_coa__coa__in = CC).filter(id_cabang = id_cabang).filter(tgl_trans__range=(start_date, end_date)) ])

    def beban_lb_rugi_kredit(self, id_cabang, start_date, end_date):
        return sum([a.kredit for a in Tbl_Transaksi.objects.filter(id_coa__coa__in = CC).filter(id_cabang = id_cabang).filter(tgl_trans__range=(start_date, end_date)) ])

    def beban_non_lb_rugi_saldo(self, id_cabang, start_date):
        return sum([a.saldo for a in Tbl_Transaksi.objects.filter(id_coa__coa__in = DD).filter(id_cabang = id_cabang).filter(tgl_trans=start_date).filter(jenis ='SALDOKASGERAI') ])

    def beban_non_lb_rugi_debet(self, id_cabang, start_date, end_date):
        return sum([a.debet for a in Tbl_Transaksi.objects.filter(id_coa__coa__in = DD).filter(id_cabang = id_cabang).filter(tgl_trans__range=(start_date, end_date)) ])

    def beban_non_lb_rugi_kredit(self, id_cabang, start_date, end_date):
        return sum([a.kredit for a in Tbl_Transaksi.objects.filter(id_coa__coa__in = DD).filter(id_cabang = id_cabang).filter(tgl_trans__range=(start_date,end_date)) ])

 
    def total_shu_cabang(self,id_cabang,start_date,end_date):
        gr_pendapatan1 = Tbl_TransaksiKeu.objects.filter(tgl_trans__range = (start_date,end_date)).filter(id_unit__in = (0,1,300)).\
            filter(id_cabang = id_cabang).filter(id_coa__jenis_laporan ='PO')
        gr_pendapatan_non1 = Tbl_TransaksiKeu.objects.filter(tgl_trans__range = (start_date,end_date)).filter(id_unit__in = (0,1,300)).\
            filter(id_cabang = id_cabang).filter(id_coa__jenis_laporan ='PNO')
        gr_beban1 = Tbl_TransaksiKeu.objects.filter(tgl_trans__range = (start_date,end_date)).filter(id_unit__in = (0,1,300)).\
            filter(id_cabang = id_cabang).filter(id_coa__jenis_laporan ='BO')
        gr_beban_non1 = Tbl_TransaksiKeu.objects.filter(tgl_trans__range = (start_date,end_date)).filter(id_unit__in = (0,1,300)).\
            filter(id_cabang = id_cabang).filter(id_coa__jenis_laporan ='BNO')
        s_pend = sum([c.saldo for c in gr_pendapatan1]) + sum([c.saldo for c in gr_pendapatan_non1])
        s_beban = (sum([c.saldo for c in gr_beban1]) + sum([c.saldo for c in gr_beban_non1]))
        jumlah = s_pend  - s_beban
        return jumlah        

    def shu_dibagikan(sef,posisi_tgl):
        return sum([a.saldo for a in Tbl_TransaksiKeu.objects.filter(id_coa__jenis_laporan =('E')).filter(tgl_trans =(posisi_tgl)).\
            filter(id_coa__id = 404)])

    def hitung_modal_penyerta(sef,posisi_tgl):
        return sum([a.saldo for a in Tbl_TransaksiKeu.objects.filter(id_coa__jenis_laporan =('E')).filter(tgl_trans =(posisi_tgl)).\
            filter(id_coa__id = 393)])

    def total_shu_cabang_laporan_gerai(self,id_cabang,posisi_tgl):
        gr_pendapatan1 = Tbl_TransaksiKeu.objects.filter(tgl_trans= (posisi_tgl)).filter(id_unit__in = (0,1,300)).\
            filter(id_cabang = id_cabang).filter(id_coa__jenis_laporan ='PO')
        gr_pendapatan_non1 = Tbl_TransaksiKeu.objects.filter(tgl_trans = (posisi_tgl)).filter(id_unit__in = (0,1,300)).\
            filter(id_cabang = id_cabang).filter(id_coa__jenis_laporan ='PNO')
        gr_beban1 = Tbl_TransaksiKeu.objects.filter(tgl_trans = (posisi_tgl)).filter(id_unit__in = (0,1,300)).\
            filter(id_cabang = id_cabang).filter(id_coa__jenis_laporan ='BO')
        gr_beban_non1 = Tbl_TransaksiKeu.objects.filter(tgl_trans= (posisi_tgl)).filter(id_unit__in = (0,1,300)).\
            filter(id_cabang = id_cabang).filter(id_coa__jenis_laporan ='BNO')
        s_pend = sum([c.saldo for c in gr_pendapatan1]) + sum([c.saldo for c in gr_pendapatan_non1])
        s_beban = (sum([c.saldo for c in gr_beban1]) + sum([c.saldo for c in gr_beban_non1]))
        jumlah = s_pend  - s_beban
        return jumlah

    def total_shu_cabang_laporan_gabungan(self,posisi_tgl):
        gr_pendapatan1 = Tbl_TransaksiKeu.objects.filter(tgl_trans = (posisi_tgl)).filter(id_unit__in = (0,1,300)).\
            filter(id_coa__jenis_laporan ='PO')
        gr_pendapatan_non1 = Tbl_TransaksiKeu.objects.filter(tgl_trans = (posisi_tgl)).filter(id_unit__in = (0,1,300)).\
            filter(id_coa__jenis_laporan ='PNO')
        gr_beban1 = Tbl_TransaksiKeu.objects.filter(tgl_trans = (posisi_tgl)).filter(id_unit__in = (0,1,300)).\
            filter(id_coa__jenis_laporan ='BO')
        gr_beban_non1 = Tbl_TransaksiKeu.objects.filter(tgl_trans = (posisi_tgl)).filter(id_unit__in = (0,1,300)).\
            filter(id_coa__jenis_laporan ='BNO')
        s_pend = sum([c.saldo for c in gr_pendapatan1]) + sum([c.saldo for c in gr_pendapatan_non1])
        s_beban = (sum([c.saldo for c in gr_beban1]) + sum([c.saldo for c in gr_beban_non1]))
        jumlah = s_pend  - s_beban
        return jumlah   
 
    def total_shu_gerai(self,start_date,end_date):
        jumlah = ((self.pdp_lb_rugi_saldo_gabungan(start_date=start_date) +\
                ###Rubah Sementara
                self.pdp_non_lb_rugi_saldo_gabungan(start_date=start_date,end_date = end_date)) +\
                self.pdp_non_lb_rugi_kredit_gabungan(start_date=start_date, end_date=end_date) + \
                self.pdp_lb_rugi_debet_gabungan(start_date=start_date, end_date=end_date) +\
                (self.pdp_lb_rugi_kredit_gabungan(start_date=start_date,end_date = end_date) +\
                self.pdp_non_lb_rugi_debet_gabungan(start_date=start_date,end_date = end_date))) -\
                ((self.beban_lb_rugi_saldo_gabungan(start_date=start_date)  )) +\
                self.pdp_non_lb_rugi_saldo_gabungan(start_date=start_date,end_date = end_date) -\
                (self.beban_lb_rugi_kredit_gabungan(start_date=start_date,end_date = end_date) +\
                self.beban_non_lb_rugi_kredit_gabungan(start_date=start_date,end_date= end_date)) +\
                (self.beban_lb_rugi_debet_gabungan(start_date=start_date,end_date = end_date) +\
                self.beban_non_lb_rugi_debet_gabungan(start_date=start_date,end_date=end_date))
        return jumlah

    ### Akhir Laba Rugi


    ####### SALDO AKHIR POSTING,Khusus untuk menu possting akhir hari
    def saldo_debet_total_posting(self,kode_cabang):
        sekarang = datetime.date.today()
        return sum([p.debet for p in self.tbl_transaksi_set.filter(id_unit=300).filter(tgl_trans=sekarang).filter(jurnal__kode_cabang=kode_cabang).\
            exclude(jenis='SALDOKASGERAI')])
    
    
    def saldo_kredit_total_posting(self,kode_cabang,tanggal):
        sekarang = datetime.date.today()
        return sum([p.kredit for p in self.tbl_transaksi_set.filter(id_unit=300).filter(tgl_trans=(tanggal)).\
            filter(id_cabang =kode_cabang).exclude(jenis='SALDOKASGERAI')])
    
    def saldo_kas_posting_jadi(self,kode_cabang,tanggal):
        sekarang = datetime.date.today()
        total = 0
        for k in self.tbl_transaksi_set.filter(jenis='SALDOKASGERAI').filter(tgl_trans = tanggal).filter(jurnal__kode_cabang =kode_cabang):
            if k.saldo == None:
                return total
            else:
                total += k.saldo
        return total
    '''
    def saldo_kas_posting_jadi(self,kode_cabang,tanggal):
        sekarang = datetime.date.today()
        total = 0
        akumulasi_debet = 0
        akumulasi_kredit = 0
        for k in self.tbl_transaksi_set.filter(jenis='SALDOKASGERAI').filter(tgl_trans = tanggal).filter(jurnal__kode_cabang =kode_cabang):
            if k.id_coa.coa[0:1] == str(2) or k.id_coa.coa[0:1] == str(3) or k.id_coa.coa[0:1] == str(4) or k.id_coa.coa[0:1] == str(6):
                akumulasi_debet += k.debet
                akumulasi_kredit += k.kredit
                total =(k.id_coa.saldo_kas(tanggal) + akumulasi_kredit - akumulasi_debet)
                return total
    '''
    ####### SALDO AKHIR POSTING,Khusus untuk menu possting akhir hari

    def saldo_debet_total(self):
        sekarang = datetime.date.today()
        return sum([p.debet for p in self.tbl_transaksi_set.filter(id_unit=300).filter(tgl_trans=sekarang).exclude(jenis='SALDOKASGERAI')])
    saldo_debet_total = property(saldo_debet_total)
    
    def saldo_kredit_total(self):
        sekarang = datetime.date.today()
        return sum([p.kredit for p in self.tbl_transaksi_set.filter(id_unit=300).filter(tgl_trans=(sekarang)).exclude(jenis='SALDOKASGERAI')])
    saldo_kredit_total = property(saldo_kredit_total)

    def saldo_kas_posting(self):
        total = 0
        for k in self.tbl_transaksi_set.filter(jenis='SALDOKASGERAI').filter(status_jurnal='3'):
            if k.saldo == None:
                return total
            else:
                total += k.saldo
        return total
    saldo_kas_posting = property(saldo_kas_posting)
    
    def saldo_kas(self,start_date):
        total = 0
        for k in self.tbl_transaksi_set.filter(jenis='SALDOKASGERAI').filter(status_jurnal__in=('2','3')).filter(tgl_trans = start_date):
            if k.saldo == None:
                return total
            else:
                total += int(k.saldo)
        return total
    #saldo_kas = property(saldo_kas)

    def saldo_kas_pusat_besar(self,start_date):
        total = 0
        saldo_keu = Tbl_TransaksiKeu.objects.filter(tgl_trans=start_date).filter(id_coa__coa = '11.01.05').\
            filter(id_cabang = 300).filter(jenis = 'SALDOKASGERAI')
        for k in saldo_keu:
            if k.saldo == None:
                return total
            else:
                total += int(k.saldo)
        return total

    def saldo_uang_muka_pusat(self,start_date):
        total = 0
        saldo_keu = Tbl_TransaksiKeu.objects.filter(tgl_trans=start_date).filter(id_coa__coa = '13.06.03').\
            filter(id_cabang = 300).filter(jenis = 'SALDOKASGERAI')
        for k in saldo_keu:
            if k.saldo == None:
                return total
            else:
                total += int(k.saldo)
        return total

    '''
    def saldo_kas(self,start_date):
        total = 0
        for k in self.tbl_transaksi_set.filter(jenis='SALDOKASGERAI').filter(status_jurnal='2').filter(tgl_trans = start_date):
            total += int(k.saldo)
            return total    
    '''
    def saldo_kas_ref(self,start_date,id_cabang):
        total = 0
        for k in self.tbl_transaksi_set.filter(jenis='SALDOKASGERAI').filter(status_jurnal__in=('2','3')).filter(tgl_trans = start_date):
            if k.saldo == None:
                return total
            else:
                total += int(k.saldo)
        return total
    ### Saldo Laporan Buku Besar
    def saldo_kas_ref_laporan(self,start_date,id_cabang):
        total = 0
        for k in self.tbl_transaksikeu_set.filter(jenis='SALDOKASGERAI').filter(status_jurnal__in=('2','3')).filter(tgl_trans = start_date):
            if k.saldo == None:
                return total
            else:
                total += int(k.saldo)
        return total

    def saldo_kas_laporan(self,start_date):
        total = 0
        ayeuna = datetime.date.today()
        #aa = timedelta(days=1)
        #besok = ayeuna - aa
        for k in self.tbl_transaksikeu_set.filter(jenis__in=('SALDOKASGERAI','SALDOBANKGERAI')).filter(status_jurnal__in=('2','3')).filter(tgl_trans = start_date):
            if k.saldo == None:
                return total
            else:
                total += int(k.saldo)
        return total

    ####saldo per gerai untuk buku besar 2 nov 2016
    def saldo_kas_laporan_gerai(self,start_date,id_cabang):
        total = 0
        ayeuna = datetime.date.today()
        #aa = timedelta(days=1)
        #besok = ayeuna - aa
        for k in self.tbl_transaksikeu_set.filter(jenis__in=('SALDOKASGERAI','SALDOBANKGERAI')).filter(status_jurnal__in=('2','3')).\
            filter(tgl_trans = start_date,id_cabang =id_cabang):
            if k.saldo == None:
                return total
            else:
                total += int(k.saldo)
        return total

    def saldo_kas_ref_laporan_gerai(self,start_date,id_cabang):
        total = 0
        for k in self.tbl_transaksikeu_set.filter(jenis='SALDOKASGERAI').filter(status_jurnal__in=('2','3')).\
            filter(tgl_trans = start_date,id_cabang = id_cabang):
            if k.saldo == None:
                return total
            else:
                total += int(k.saldo)
        return total
    ####saldo per gerai untuk buku besar 2 nov 2016

    def saldo_kas_rj(self,start_date):#####saldo di rekap jurnal tgl 29-jan-2016
        total = 0
        for k in self.tbl_transaksi_set.filter(jenis__in=('SALDOKASGERAI','SALDOBANKGERAI')).filter(status_jurnal='2').filter(tgl_trans = start_date):
            if k.saldo == None:
                return total
            else:
                total += int(k.saldo)
        return total    

    def saldo_kas_bb(self,start_date):### saldo buku besar non Posting
        total = 0
        for k in self.tbl_transaksi_set.filter(jenis__in=('SALDOKASGERAI','SALDOBANKGERAI')).filter(tgl_trans = start_date).filter(status_jurnal='2'):
            if k.saldo == None:
                return total
            else:
                total += k.saldo
        return total
 
    def saldo_kas_bb_laporan(self,start_date):### saldo buku besar non Posting
        total = 0
        for k in self.tbl_transaksikeu_set.filter(jenis__in=('SALDOKASGERAI','SALDOBANKGERAI')).filter(tgl_trans = start_date).filter(status_jurnal__in=('2','3')):
            if k.saldo == None:
                return total
            else:
                total += k.saldo
        return total
    def saldo_awalhari(self,id_cabang,start_date):
        total = 0
        for k in self.tbl_transaksi_set.filter(tgl_trans = start_date).filter(jurnal__kode_cabang = id_cabang).filter(jenis=('SALDOKASGERAI')):
            if k.saldo == None:
                return total
            else:
                total += k.saldo
        return total
    #saldo_awalhari = property(saldo_awalhari)

    def saldo_awalhari_gabungan(self,start_date):
        total = 0
        for k in self.tbl_transaksi_set.filter(tgl_trans = start_date):
            if k.saldo == None:
                return total
            else:
                total += k.saldo
        return total
    #saldo_awalhari = property(saldo_awalhari)
    
    def view_saldo_awal_gbg_posting(self,id_cabang, start_date):
        ret = 0
        if self.header_parent == None:
            for anak in self.children():
                ret += sum([p.saldo for p in anak.tbl_transaksikeu_set.filter(id_unit=300).filter(tgl_trans=(start_date)).\
                    filter(jurnal__kode_cabang = id_cabang).filter(status_jurnal= '2').filter(jenis='SALDOKASGERAI')])
                for cucu in anak.children():
                    ret +=  sum([p.saldo for p in cucu.tbl_transaksikeu_set.filter(id_unit=300).filter(jurnal__kode_cabang = id_cabang).\
                       filter(tgl_trans=(start_date)).filter(status_jurnal= '2').filter(jenis='SALDOKASGERAI')])
                    for cicit in cucu.children():
                        ret += sum([p.saldo for p in cicit.tbl_transaksikeu_set.filter(id_unit=300).filter(jurnal__kode_cabang = id_cabang).\
                            filter(tgl_trans=(start_date)).filter(status_jurnal= '2').filter(jenis='SALDOKASGERAI')])
            return ret
        elif self.coa == '11.00.00' or self.coa == '12.00.00' or self.coa == '13.00.00' or self.coa == '21.00.00' or self.coa == '22.00.00' or\
            self.coa == '23.00.00' or self.coa == '31.00.00' or self.coa == '32.00.00' or self.coa == '33.00.00' or self.coa == '34.00.00' or \
            self.coa == '35.00.00' or  self.coa == '41.00.00' or self.coa == '51.00.00'or self.coa == '61.00.00':
            for anak in self.children():
                ret += sum([p.saldo for p in anak.tbl_transaksikeu_set.filter(id_unit=300).filter(tgl_trans=(start_date)).\
                    filter(jurnal__kode_cabang = id_cabang).filter(status_jurnal= '2').filter(jenis='SALDOKASGERAI')])
                for cucu in anak.children():
                    ret += sum([p.saldo for p in cucu.tbl_transaksikeu_set.filter(id_unit=300).filter(tgl_trans=(start_date)).\
                        filter(jurnal__kode_cabang = id_cabang).filter(status_jurnal= '2').filter(jenis='SALDOKASGERAI')])
            return ret
        elif self.coa == '11.01.00' or self.coa == '11.05.00' or self.coa == '11.06.00' or self.coa == '11.07.00' or self.coa == '11.08.00' or\
            self.coa == '11.09.00' or self.coa == '11.10.00' or self.coa == '11.11.00' or self.coa == '11.12.00' or self.coa == '11.13.00' or \
            self.coa == '12.01.00' or self.coa == '12.02.00' or self.coa == '12.03.00' or self.coa == '13.01.00' or self.coa == '13.02.00' or \
            self.coa == '13.03.00' or self.coa == '13.04.00' or self.coa == '13.05.00' or self.coa == '13.06.00' or self.coa == '21.01.00' or \
            self.coa == '21.02.00' or self.coa == '21.03.00' or self.coa == '21.04.00' or self.coa == '21.05.00' or self.coa == '21.06.00' or \
            self.coa == '21.07.00' or self.coa == '21.08.00' or self.coa == '21.09.00' or self.coa == '21.10.00' or self.coa == '22.03.00' or \
            self.coa == '22.04.00' or self.coa == '22.05.00' or self.coa == '22.06.00' or self.coa == '23.01.00' or self.coa == '23.02.00' or \
            self.coa == '41.01.00' or self.coa == '41.02.00' or self.coa == '41.03.00' or self.coa == '51.01.00' or self.coa == '51.02.00' or \
            self.coa == '51.03.00' or self.coa == '51.04.00' or self.coa == '51.05.00' or self.coa == '51.06.00' or self.coa == '51.07.00' or \
            self.coa == '51.08.00' or self.coa == '51.09.00' or self.coa == '51.10.00' or self.coa == '51.11.00' or self.coa == '41.04.00' or \
            self.coa == '12.04.00' or self.coa == '22.07.00' :
            for anak in self.children():
                ret += sum([p.saldo for p in anak.tbl_transaksikeu_set.filter(id_unit=300).filter(tgl_trans=(start_date)).\
                    filter(jurnal__kode_cabang = id_cabang).filter(status_jurnal= '2').filter(jenis='SALDOKASGERAI')])
            return ret
        else:
            return  sum([p.saldo for p in self.tbl_transaksikeu_set.filter(id_unit=300).filter(tgl_trans=(start_date)).\
                filter(status_jurnal= '2').filter(jurnal__kode_cabang=id_cabang).filter(jenis='SALDOKASGERAI')])

    ###non posting
    def saldo_shu_neraca_gabungan(self, start_date,end_date):
        ret = 0
        if self.coa == '35.04.00':
           return ((self.pdp_lb_rugi_saldo_gabungan(start_date=start_date) +\
                self.pdp_non_lb_rugi_saldo_gabungan(start_date=start_date,end_date = end_date)) +\
                (self.pdp_lb_rugi_kredit_gabungan(start_date=start_date,end_date = end_date) +\
                self.pdp_non_lb_rugi_kredit_gabungan(start_date=start_date,end_date = end_date)) -\
                (self.pdp_lb_rugi_debet_gabungan(start_date=start_date,end_date = end_date) +\
                self.pdp_non_lb_rugi_debet_gabungan(start_date=start_date,end_date = end_date)))\
                - ((self.beban_lb_rugi_saldo_gabungan(start_date=start_date)\
                + self.pdp_non_lb_rugi_saldo_gabungan(start_date=start_date,end_date = end_date))\
                - (self.beban_lb_rugi_kredit_gabungan(start_date=start_date,end_date = end_date)\
                + self.beban_non_lb_rugi_kredit_gabungan(start_date=start_date,end_date = end_date))\
                + (self.beban_lb_rugi_debet_gabungan(start_date=start_date,end_date = end_date)\
                + self.beban_non_lb_rugi_debet_gabungan(start_date=start_date,end_date = end_date)))
        else:
            return ret 

    def saldo_shu_neraca(self,id_cabang, start_date,end_date):
        ret = 0
        if self.coa == '35.04.00':
            return ((self.pdp_lb_rugi_saldo(id_cabang = id_cabang, start_date=start_date) +\
                self.pdp_non_lb_rugi_saldo(id_cabang = id_cabang, start_date=start_date,end_date=end_date)) +\
                (self.pdp_lb_rugi_kredit(id_cabang = id_cabang, start_date=start_date,end_date=end_date) +\
                self.pdp_non_lb_rugi_kredit(id_cabang = id_cabang, start_date=start_date,end_date=end_date)) -\
                (self.pdp_lb_rugi_debet(id_cabang = id_cabang,start_date=start_date,end_date = end_date) +\
                self.pdp_non_lb_rugi_debet(id_cabang = id_cabang, start_date=start_date,end_date = end_date)))\
                - ((self.beban_lb_rugi_saldo(id_cabang = id_cabang, start_date=start_date)\
                + self.pdp_non_lb_rugi_saldo(id_cabang = id_cabang,start_date=start_date,end_date = end_date))\
                - (self.beban_lb_rugi_kredit(id_cabang = id_cabang, start_date=start_date,end_date=end_date)
                + self.beban_non_lb_rugi_kredit(id_cabang = id_cabang, start_date=start_date,end_date = end_date))\
                + (self.beban_lb_rugi_debet(id_cabang = id_cabang,start_date=start_date,end_date = end_date)\
                + self.beban_non_lb_rugi_debet(id_cabang = id_cabang, start_date=start_date,end_date = end_date)))
        else:
            return ret


    def view_saldo_awal_gbg_neraca(self,id_cabang, start_date):
        ret = 0
        if self.coa == '35.04.00':
            return ((self.pdp_lb_rugi_saldo(id_cabang = id_cabang, start_date=start_date) +\
                self.pdp_non_lb_rugi_saldo(id_cabang = id_cabang, start_date=start_date)) +\
                (self.pdp_lb_rugi_kredit(id_cabang = id_cabang, start_date=start_date) +\
                self.pdp_non_lb_rugi_kredit(id_cabang = id_cabang, start_date=start_date)) -\
                (self.pdp_lb_rugi_debet(id_cabang = id_cabang,start_date=start_date) +\
                self.pdp_non_lb_rugi_debet(id_cabang = id_cabang, start_date=start_date)))\
                - ((self.beban_lb_rugi_saldo(id_cabang = id_cabang, start_date=start_date) + self.pdp_non_lb_rugi_saldo(id_cabang = id_cabang,\
                start_date=start_date)) - (self.beban_lb_rugi_kredit(id_cabang = id_cabang, start_date=start_date) +\
                self.beban_non_lb_rugi_kredit(id_cabang = id_cabang, start_date=start_date)) + (self.beban_lb_rugi_debet(id_cabang = id_cabang,\
                start_date=start_date) + self.beban_non_lb_rugi_debet(id_cabang = id_cabang, start_date=start_date)))

        elif self.header_parent == None:
            for anak in self.children():
                ret += sum([p.saldo for p in anak.tbl_transaksi_set.filter(id_unit=300).filter(tgl_trans=(start_date)).\
                    filter(jurnal__kode_cabang = id_cabang).filter(status_jurnal= '2').filter(jenis__in=('SALDOKASGERAI','SALDOBANKGERAI'))])
                for cucu in anak.children():
                    ret +=  sum([p.saldo for p in cucu.tbl_transaksi_set.filter(id_unit=300).filter(jurnal__kode_cabang = id_cabang).\
                       filter(tgl_trans=(start_date)).filter(status_jurnal= '2').filter(jenis__in=('SALDOKASGERAI','SALDOBANKGERAI'))])
                    for cicit in cucu.children():
                        ret += sum([p.saldo for p in cicit.tbl_transaksi_set.filter(id_unit=300).filter(jurnal__kode_cabang = id_cabang).\
                            filter(tgl_trans=(start_date)).filter(status_jurnal= '2').filter(jenis__in=('SALDOKASGERAI','SALDOBANKGERAI'))])
            return ret
        elif self.coa == '11.00.00' or self.coa == '12.00.00' or self.coa == '13.00.00' or self.coa == '21.00.00' or self.coa == '22.00.00' or\
            self.coa == '23.00.00' or self.coa == '31.00.00' or self.coa == '32.00.00' or self.coa == '33.00.00' or self.coa == '34.00.00' or \
            self.coa == '35.00.00' or  self.coa == '41.00.00' or self.coa == '51.00.00'or self.coa == '61.00.00':
            for anak in self.children():
                ret += sum([p.saldo for p in anak.tbl_transaksi_set.filter(id_unit=300).filter(tgl_trans=(start_date)).\
                    filter(jurnal__kode_cabang = id_cabang).filter(status_jurnal= '2').filter(jenis__in=('SALDOKASGERAI','SALDOBANKGERAI'))])
                for cucu in anak.children():
                    ret += sum([p.saldo for p in cucu.tbl_transaksi_set.filter(id_unit=300).filter(tgl_trans=(start_date)).\
                        filter(jurnal__kode_cabang = id_cabang).filter(status_jurnal= '2').filter(jenis__in=('SALDOKASGERAI','SALDOBANKGERAI'))])
            return ret
        elif self.coa == '11.01.00' or self.coa == '11.05.00' or self.coa == '11.06.00' or self.coa == '11.07.00' or self.coa == '11.08.00' or\
            self.coa == '11.09.00' or self.coa == '11.10.00' or self.coa == '11.11.00' or self.coa == '11.12.00' or self.coa == '11.13.00' or \
            self.coa == '12.01.00' or self.coa == '12.02.00' or self.coa == '12.03.00' or self.coa == '13.01.00' or self.coa == '13.02.00' or \
            self.coa == '13.03.00' or self.coa == '13.04.00' or self.coa == '13.05.00' or self.coa == '13.06.00' or self.coa == '21.01.00' or \
            self.coa == '21.02.00' or self.coa == '21.03.00' or self.coa == '21.04.00' or self.coa == '21.05.00' or self.coa == '21.06.00' or \
            self.coa == '21.07.00' or self.coa == '21.08.00' or self.coa == '21.09.00' or self.coa == '21.10.00' or self.coa == '22.03.00' or \
            self.coa == '22.04.00' or self.coa == '22.05.00' or self.coa == '22.06.00' or self.coa == '23.01.00' or self.coa == '23.02.00' or \
            self.coa == '41.01.00' or self.coa == '41.02.00' or self.coa == '41.03.00' or self.coa == '51.01.00' or self.coa == '51.02.00' or \
            self.coa == '51.03.00' or self.coa == '51.04.00' or self.coa == '51.05.00' or self.coa == '51.06.00' or self.coa == '51.07.00' or \
            self.coa == '51.08.00' or self.coa == '51.09.00' or self.coa == '51.10.00' or self.coa == '51.11.00' or self.coa == '41.04.00':
            for anak in self.children():
                ret += sum([p.saldo for p in anak.tbl_transaksi_set.filter(id_unit=300).filter(tgl_trans=(start_date)).\
                    filter(jurnal__kode_cabang = id_cabang).filter(status_jurnal= '2').filter(jenis__in=('SALDOKASGERAI','SALDOBANKGERAI'))])
            return ret
        else:
            return  sum([p.saldo for p in self.tbl_transaksi_set.filter(id_unit=300).filter(tgl_trans=(start_date)).\
                filter(jurnal__kode_cabang = id_cabang).filter(status_jurnal= '2').filter(jenis__in=('SALDOKASGERAI','SALDOBANKGERAI'))])

    def view_saldo_awal_gbg(self,id_cabang, start_date):
        ret = 0
        if self.header_parent == None:
            for anak in self.children():
                ret += sum([p.saldo for p in anak.tbl_transaksikeu_set.filter(id_unit=300).filter(tgl_trans=(start_date)).\
                    filter(jurnal__kode_cabang = id_cabang).filter(status_jurnal__in = ('2','3')).filter(jenis__in=('SALDOKASGERAI','SALDOBANKGERAI'))])
                for cucu in anak.children():
                    ret +=  sum([p.saldo for p in cucu.tbl_transaksikeu_set.filter(id_unit=300).filter(jurnal__kode_cabang = id_cabang).\
                       filter(tgl_trans=(start_date)).filter(status_jurnal__in= ('2','3')).filter(jenis__in=('SALDOKASGERAI','SALDOBANKGERAI'))])
                    for cicit in cucu.children():
                        ret += sum([p.saldo for p in cicit.tbl_transaksikeu_set.filter(id_unit=300).filter(jurnal__kode_cabang = id_cabang).\
                            filter(tgl_trans=(start_date)).filter(status_jurnal__in= ('2','3')).filter(jenis__in=('SALDOKASGERAI','SALDOBANKGERAI'))])
            return ret
        elif self.coa == '11.00.00' or self.coa == '12.00.00' or self.coa == '13.00.00' or self.coa == '21.00.00' or self.coa == '22.00.00' or\
            self.coa == '23.00.00' or self.coa == '31.00.00' or self.coa == '32.00.00' or self.coa == '33.00.00' or self.coa == '34.00.00' or \
            self.coa == '35.00.00' or  self.coa == '41.00.00' or self.coa == '51.00.00'or self.coa == '61.00.00':
            for anak in self.children():
                ret += sum([p.saldo for p in anak.tbl_transaksikeu_set.filter(id_unit=300).filter(tgl_trans=(start_date)).\
                    filter(jurnal__kode_cabang = id_cabang).filter(status_jurnal__in= ('2','3')).filter(jenis__in=('SALDOKASGERAI','SALDOBANKGERAI'))])
                for cucu in anak.children():
                    ret += sum([p.saldo for p in cucu.tbl_transaksikeu_set.filter(id_unit=300).filter(tgl_trans=(start_date)).\
                        filter(jurnal__kode_cabang = id_cabang).filter(status_jurnal__in= ('2','3')).filter(jenis__in=('SALDOKASGERAI','SALDOBANKGERAI'))])
            return ret
        elif self.coa == '11.01.00' or self.coa == '11.05.00' or self.coa == '11.06.00' or self.coa == '11.07.00' or self.coa == '11.08.00' or\
            self.coa == '11.09.00' or self.coa == '11.10.00' or self.coa == '11.11.00' or self.coa == '11.12.00' or self.coa == '11.13.00' or \
            self.coa == '12.01.00' or self.coa == '12.02.00' or self.coa == '12.03.00' or self.coa == '13.01.00' or self.coa == '13.02.00' or \
            self.coa == '13.03.00' or self.coa == '13.04.00' or self.coa == '13.05.00' or self.coa == '13.06.00' or self.coa == '21.01.00' or \
            self.coa == '21.02.00' or self.coa == '21.03.00' or self.coa == '21.04.00' or self.coa == '21.05.00' or self.coa == '21.06.00' or \
            self.coa == '21.07.00' or self.coa == '21.08.00' or self.coa == '21.09.00' or self.coa == '21.10.00' or self.coa == '22.03.00' or \
            self.coa == '22.04.00' or self.coa == '22.05.00' or self.coa == '22.06.00' or self.coa == '23.01.00' or self.coa == '23.02.00' or \
            self.coa == '41.01.00' or self.coa == '41.02.00' or self.coa == '41.03.00' or self.coa == '51.01.00' or self.coa == '51.02.00' or \
            self.coa == '51.03.00' or self.coa == '51.04.00' or self.coa == '51.05.00' or self.coa == '51.06.00' or self.coa == '51.07.00' or \
            self.coa == '51.08.00' or self.coa == '51.09.00' or self.coa == '51.10.00' or self.coa == '51.11.00' or self.coa == '41.04.00':
            for anak in self.children():
                ret += sum([p.saldo for p in anak.tbl_transaksikeu_set.filter(id_unit=300).filter(tgl_trans=(start_date)).\
                    filter(jurnal__kode_cabang = id_cabang).filter(status_jurnal__in= ('2','3')).filter(jenis__in=('SALDOKASGERAI','SALDOBANKGERAI'))])
            return ret
        else:
            return  sum([p.saldo for p in self.tbl_transaksikeu_set.filter(id_unit=300).filter(tgl_trans=(start_date)).\
                filter(jurnal__kode_cabang = id_cabang).filter(status_jurnal__in= ('2','3')).filter(jenis__in=('SALDOKASGERAI','SALDOBANKGERAI'))])

    
    def view_saldo_awal_gabungan_neraca(self, start_date):
        ret = 0
        if self.header_parent == None:
            for anak in self.children():
                ret += sum([p.saldo for p in anak.tbl_transaksikeu_set.filter(id_unit=300).filter(tgl_trans=(start_date)).\
                    filter(status_jurnal__in= ('2','3')).filter(jenis='SALDOKASGERAI')])
                for cucu in anak.children():
                    ret +=  sum([p.saldo for p in cucu.tbl_transaksikeu_set.filter(id_unit=300).\
                       filter(tgl_trans=(start_date)).filter(status_jurnal__in= ('2','3')).filter(jenis='SALDOKASGERAI')])
                    for cicit in cucu.children():
                        ret += sum([p.saldo for p in cicit.tbl_transaksikeu_set.filter(id_unit=300).\
                            filter(tgl_trans=(start_date)).filter(status_jurnal__in= ('2','3')).filter(jenis='SALDOKASGERAI')])
            return ret
        elif self.coa == '11.00.00' or self.coa == '12.00.00' or self.coa == '13.00.00' or self.coa == '21.00.00' or self.coa == '22.00.00' or\
            self.coa == '23.00.00' or self.coa == '31.00.00' or self.coa == '32.00.00' or self.coa == '33.00.00' or self.coa == '34.00.00' or \
            self.coa == '35.00.00' or  self.coa == '41.00.00' or self.coa == '51.00.00'or self.coa == '61.00.00':
            for anak in self.children():
                ret += sum([p.saldo for p in anak.tbl_transaksikeu_set.filter(id_unit=300).filter(tgl_trans=(start_date)).\
                    filter(status_jurnal__in= ('2','3')).filter(jenis='SALDOKASGERAI')])
                for cucu in anak.children():
                    ret += sum([p.saldo for p in cucu.tbl_transaksikeu_set.filter(id_unit=300).filter(tgl_trans=(start_date)).\
                        filter(status_jurnal__in= ('2',3)).filter(jenis='SALDOKASGERAI')])
            return ret
        elif self.coa == '11.01.00' or self.coa == '11.05.00' or self.coa == '11.06.00' or self.coa == '11.07.00' or self.coa == '11.08.00' or\
            self.coa == '11.09.00' or self.coa == '11.10.00' or self.coa == '11.11.00' or self.coa == '11.12.00' or self.coa == '11.13.00' or \
            self.coa == '12.01.00' or self.coa == '12.02.00' or self.coa == '12.03.00' or self.coa == '13.01.00' or self.coa == '13.02.00' or \
            self.coa == '13.03.00' or self.coa == '13.04.00' or self.coa == '13.05.00' or self.coa == '13.06.00' or self.coa == '21.01.00' or \
            self.coa == '21.02.00' or self.coa == '21.03.00' or self.coa == '21.04.00' or self.coa == '21.05.00' or self.coa == '21.06.00' or \
            self.coa == '21.07.00' or self.coa == '21.08.00' or self.coa == '21.09.00' or self.coa == '21.10.00' or self.coa == '22.03.00' or \
            self.coa == '22.04.00' or self.coa == '22.05.00' or self.coa == '22.06.00' or self.coa == '23.01.00' or self.coa == '23.02.00' or \
            self.coa == '41.01.00' or self.coa == '41.02.00' or self.coa == '41.03.00' or self.coa == '51.01.00' or self.coa == '51.02.00' or \
            self.coa == '51.03.00' or self.coa == '51.04.00' or self.coa == '51.05.00' or self.coa == '51.06.00' or self.coa == '51.07.00' or \
            self.coa == '51.08.00' or self.coa == '51.09.00' or self.coa == '51.10.00' or self.coa == '51.11.00' or self.coa == '41.04.00' or self.coa == '12.04.00' or self.coa == '22.07.00':
            for anak in self.children():
                ret += sum([p.saldo for p in anak.tbl_transaksikeu_set.filter(id_unit=300).filter(tgl_trans=(start_date)).\
                    filter(status_jurnal__in= ('2','3')).filter(jenis='SALDOKASGERAI')])
            return ret
        else:
            return  sum([p.saldo for p in self.tbl_transaksikeu_set.filter(id_unit=300).filter(tgl_trans=(start_date)).\
                    filter(status_jurnal__in= ('2','3')).filter(jenis='SALDOKASGERAI')])

    def kredit_hari(self, id_cabang, start_date):
        ret = 0
        if self.header_parent == None:
            for anak in self.children():
                ret += sum([p.kredit for p in anak.tbl_transaksi_set.filter(id_unit=300).filter(tgl_trans=(start_date))])
                for cucu in anak.children():
                    ret += sum([p.kredit for p in cucu.tbl_transaksi_set.filter(id_unit=300).filter(tgl_trans=(start_date))])
                    for cicit in cucu.children():
                        ret += sum([p.kredit for p in cicit.tbl_transaksi_set.filter(id_unit=300).filter(tgl_trans=(start_date))])
            return ret    
        #elif self.coa[2:] == '.00.00' :
        elif self.coa == '11.00.00' or self.coa == '12.00.00' or self.coa == '13.00.00' or self.coa == '21.00.00' or self.coa == '22.00.00' or\
            self.coa == '23.00.00' or self.coa == '31.00.00' or self.coa == '32.00.00' or self.coa == '33.00.00' or self.coa == '34.00.00' or \
            self.coa == '35.00.00' or  self.coa == '41.00.00' or self.coa == '51.00.00'or self.coa == '61.00.00':
            for anak in self.children():
                ret += sum([p.kredit for p in anak.tbl_transaksi_set.filter(id_cabang=id_cabang).filter(id_unit=300).filter(tgl_trans=(start_date))])
                for cucu in anak.children():
                    ret += sum([p.kredit for p in cucu.tbl_transaksi_set.filter(id_cabang=id_cabang).filter(id_unit=300).\
                       filter(tgl_trans=(start_date))])
            return ret
        #elif self.coa[5:] == '.00' and self.view_unit == u'300':
        elif self.coa == '11.01.00' or self.coa == '11.05.00' or self.coa == '11.06.00' or self.coa == '11.07.00' or self.coa == '11.08.00' or\
            self.coa == '11.09.00' or self.coa == '11.10.00' or self.coa == '11.11.00' or self.coa == '11.12.00' or self.coa == '11.13.00' or \
            self.coa == '12.01.00' or self.coa == '12.02.00' or self.coa == '12.03.00' or self.coa == '13.01.00' or self.coa == '13.02.00' or \
            self.coa == '13.03.00' or self.coa == '13.04.00' or self.coa == '13.05.00' or self.coa == '13.06.00' or self.coa == '21.01.00' or \
            self.coa == '21.02.00' or self.coa == '21.03.00' or self.coa == '21.04.00' or self.coa == '21.05.00' or self.coa == '21.06.00' or \
            self.coa == '21.07.00' or self.coa == '21.08.00' or self.coa == '21.09.00' or self.coa == '21.10.00' or self.coa == '22.03.00' or \
            self.coa == '22.04.00' or self.coa == '22.05.00' or self.coa == '22.06.00' or self.coa == '23.01.00' or self.coa == '23.02.00' or \
            self.coa == '41.01.00' or self.coa == '41.02.00' or self.coa == '41.03.00' or self.coa == '51.01.00' or self.coa == '51.02.00' or \
            self.coa == '51.03.00' or self.coa == '51.04.00' or self.coa == '51.05.00' or self.coa == '51.06.00' or self.coa == '51.07.00' or \
            self.coa == '51.08.00' or self.coa == '51.09.00' or self.coa == '51.10.00' or self.coa == '51.11.00':
            for anak in self.children():
                ret += sum([p.kredit for p in anak.tbl_transaksi_set.filter(id_cabang=id_cabang).filter(id_unit=300).filter(tgl_trans=(start_date))])
            return ret        
        else:            
            return sum([p.kredit for p in self.tbl_transaksi_set.filter(id_cabang=id_cabang).filter(id_unit=300).filter(tgl_trans=(start_date))])
        
    def debet_hari(self, id_cabang, start_date):
        ret = 0
        if self.header_parent == None:
            for anak in self.children():
                ret += sum([p.debet for p in anak.tbl_transaksi_set.filter(id_unit=300).filter(tgl_trans=(start_date))])
                for cucu in anak.children():
                    ret += sum([p.debet for p in cucu.tbl_transaksi_set.filter(id_unit=300).filter(tgl_trans=(start_date))])
                    for cicit in cucu.children():
                        ret += sum([p.debet for p in cicit.tbl_transaksi_set.filter(id_unit=300).filter(tgl_trans=(start_date))])
            return ret    
        #elif self.coa[2:] == '.00.00':
        elif self.coa == '11.00.00' or self.coa == '12.00.00' or self.coa == '13.00.00' or self.coa == '21.00.00' or self.coa == '22.00.00' or \
            self.coa == '23.00.00' or self.coa == '31.00.00' or self.coa == '32.00.00' or self.coa == '33.00.00' or self.coa == '34.00.00' or \
            self.coa == '35.00.00' or  self.coa == '41.00.00' or self.coa == '51.00.00'or self.coa == '61.00.00':
            for anak in self.children():
                ret += sum([p.debet for p in anak.tbl_transaksi_set.filter(id_unit=300).filter(tgl_trans=(start_date))])
                for cucu in anak.children():
                    ret += sum([p.debet for p in cucu.tbl_transaksi_set.filter(id_unit=300).filter(tgl_trans=(start_date))])
            return ret
        #elif self.coa[5:] == '.00' and self.view_unit==u'300':
        elif self.coa == '11.01.00' or self.coa == '11.05.00' or self.coa == '11.06.00' or self.coa == '11.07.00' or self.coa == '11.08.00' or \
            self.coa == '11.09.00' or self.coa == '11.10.00' or self.coa == '11.11.00' or self.coa == '11.12.00' or self.coa == '11.13.00' or \
            self.coa == '12.01.00' or self.coa == '12.02.00' or self.coa == '12.03.00' or self.coa == '13.01.00' or self.coa == '13.02.00' or \
            self.coa == '13.03.00' or self.coa == '13.04.00' or self.coa == '13.05.00' or self.coa == '13.06.00' or self.coa == '21.01.00' or \
            self.coa == '21.02.00' or self.coa == '21.03.00' or self.coa == '21.04.00' or self.coa == '21.05.00' or self.coa == '21.06.00' or \
            self.coa == '21.07.00' or self.coa == '21.08.00' or self.coa == '21.09.00' or self.coa == '21.10.00' or self.coa == '22.03.00' or \
            self.coa == '22.04.00' or self.coa == '22.05.00' or self.coa == '22.06.00' or self.coa == '23.01.00' or self.coa == '23.02.00' or \
            self.coa == '41.01.00' or self.coa == '41.02.00' or self.coa == '41.03.00' or self.coa == '51.01.00' or self.coa == '51.02.00' or \
            self.coa == '51.03.00' or self.coa == '51.04.00' or self.coa == '51.05.00' or self.coa == '51.06.00' or self.coa == '51.07.00' or \
            self.coa == '51.08.00' or self.coa == '51.09.00' or self.coa == '51.10.00' or self.coa == '51.11.00':
            for anak in self.children():
                ret += sum([p.debet for p in anak.tbl_transaksi_set.filter(id_cabang=id_cabang).filter(id_unit=300).filter(tgl_trans=(start_date))])
            return ret
        else:
            return sum([p.debet for p in self.tbl_transaksi_set.filter(id_cabang=id_cabang).filter(id_unit=300).filter(tgl_trans=(start_date))])
        
    ######GABUNGAN    
    def debet_gabung_hari(self, id_cabang, start_date):
        ret = 0
        if self.header_parent == None:
            for anak in self.children():
                ret += sum([p.debet for p in anak.tbl_transaksi_set.filter(id_unit=300).filter(tgl_trans=(start_date))])
                for cucu in anak.children():
                    ret += sum([p.debet for p in cucu.tbl_transaksi_set.filter(id_unit=300).filter(tgl_trans=(start_date))])
                    for cicit in cucu.children():
                        ret += sum([p.debet for p in cicit.tbl_transaksi_set.filter(id_unit=300).filter(tgl_trans=(start_date))])
            return ret    
        #elif self.coa[2:] == '.00.00':
        elif self.coa == '11.00.00' or self.coa == '12.00.00' or self.coa == '13.00.00' or self.coa == '21.00.00' or self.coa == '22.00.00' or \
            self.coa == '23.00.00' or self.coa == '31.00.00' or self.coa == '32.00.00' or self.coa == '33.00.00' or self.coa == '34.00.00' or \
            self.coa == '35.00.00' or  self.coa == '41.00.00' or self.coa == '51.00.00'or self.coa == '61.00.00':
            for anak in self.children():
                ret += sum([p.debet for p in anak.tbl_transaksi_set.filter(id_unit=300).filter(tgl_trans=(start_date))])
                for cucu in anak.children():
                    ret += sum([p.debet for p in cucu.tbl_transaksi_set.filter(id_unit=300).filter(tgl_trans=(start_date))])
            return ret
        #elif self.coa[5:] == '.00':
        elif self.coa == '11.01.00' or self.coa == '11.05.00' or self.coa == '11.06.00' or self.coa == '11.07.00' or self.coa == '11.08.00' or \
            self.coa == '11.09.00' or self.coa == '11.10.00' or self.coa == '11.11.00' or self.coa == '11.12.00' or self.coa == '11.13.00' or \
            self.coa == '12.01.00' or self.coa == '12.02.00' or self.coa == '12.03.00' or self.coa == '13.01.00' or self.coa == '13.02.00' or \
            self.coa == '13.03.00' or self.coa == '13.04.00' or self.coa == '13.05.00' or self.coa == '13.06.00' or self.coa == '21.01.00' or \
            self.coa == '21.02.00' or self.coa == '21.03.00' or self.coa == '21.04.00' or self.coa == '21.05.00' or\
            self.coa == '21.06.00' or self.coa == '21.07.00' or self.coa == '21.08.00' or self.coa == '21.09.00' or self.coa == '21.10.00' or\
            self.coa == '22.03.00' or self.coa == '22.04.00' or self.coa == '22.05.00' or self.coa == '22.06.00' or self.coa == '23.01.00' or \
            self.coa == '23.02.00' or self.coa == '41.01.00' or self.coa == '41.02.00' or self.coa == '41.03.00' or self.coa == '51.01.00' or \
            self.coa == '51.02.00' or self.coa == '51.03.00' or self.coa == '51.04.00' or self.coa == '51.05.00' or self.coa == '51.06.00' or \
            self.coa == '51.07.00' or self.coa == '51.08.00' or self.coa == '51.09.00' or self.coa == '51.10.00' or self.coa == '51.11.00':
            for anak in self.children():
                ret += sum([p.debet for p in anak.tbl_transaksi_set.filter(id_unit=300).filter(tgl_trans=(start_date))])
            return ret
        else:
            return sum([p.debet for p in self.tbl_transaksi_set.filter(id_unit=300).filter(tgl_trans=(start_date))])

      
    def kredit_gabung_hari(self, id_cabang, start_date):
        ret = 0
        #if self.coa[1:] == '0.00.00':
        if self.header_parent == None:
            for anak in self.children():
                ret += sum([p.kredit for p in anak.tbl_transaksi_set.filter(id_unit=300).filter(tgl_trans=(start_date))])
                for cucu in anak.children():
                    ret += sum([p.kredit for p in cucu.tbl_transaksi_set.filter(id_unit=300).filter(tgl_trans=(start_date))])
                    for cicit in cucu.children():
                        ret += sum([p.kredit for p in cicit.tbl_transaksi_set.filter(id_unit=300).filter(tgl_trans=(start_date))])
            return ret    
        #elif self.coa[2:] == '.00.00':
        elif self.coa == '11.00.00' or self.coa == '12.00.00' or self.coa == '13.00.00' or self.coa == '21.00.00' or self.coa == '22.00.00' \
            or self.coa == '23.00.00' or self.coa == '31.00.00' or self.coa == '32.00.00' or self.coa == '33.00.00' or self.coa == '34.00.00' \
            or self.coa == '35.00.00' or  self.coa == '41.00.00' or self.coa == '51.00.00'or self.coa == '61.00.00':
            for anak in self.children():
                ret += sum([p.kredit for p in anak.tbl_transaksi_set.filter(id_unit=300).filter(tgl_trans=(start_date))])
                for cucu in anak.children():
                    ret += sum([p.kredit for p in cucu.tbl_transaksi_set.filter(id_unit=300).filter(tgl_trans=(start_date))])
            return ret
        #elif self.coa[5:] == '.00':
        elif self.coa == '11.01.00' or self.coa == '11.05.00' or self.coa == '11.06.00' or self.coa == '11.07.00' or self.coa == '11.08.00' \
            or self.coa == '11.09.00' or self.coa == '11.10.00' or self.coa == '11.11.00' or self.coa == '11.12.00' or self.coa == '11.13.00'\
            or self.coa == '12.01.00' or self.coa == '12.02.00' or self.coa == '12.03.00' or self.coa == '13.01.00' or self.coa == '13.02.00'\
            or self.coa == '13.03.00' or self.coa == '13.04.00' or self.coa == '13.05.00' or self.coa == '13.06.00' or self.coa == '21.01.00'\
            or self.coa == '21.02.00' or self.coa == '21.03.00' or self.coa == '21.04.00' or self.coa == '21.05.00' or self.coa == '21.06.00'\
            or self.coa == '21.07.00' or self.coa == '21.08.00' or self.coa == '21.09.00' or self.coa == '21.10.00' or self.coa == '22.03.00'\
            or self.coa == '22.04.00' or self.coa == '22.05.00' or self.coa == '22.06.00' or self.coa == '23.01.00' or self.coa == '23.02.00'\
            or self.coa == '41.01.00' or self.coa == '41.02.00' or self.coa == '41.03.00' or self.coa == '51.01.00' or self.coa == '51.02.00'\
            or self.coa == '51.03.00' or self.coa == '51.04.00' or self.coa == '51.05.00' or self.coa == '51.06.00' or self.coa == '51.07.00'\
            or self.coa == '51.08.00' or self.coa == '51.09.00' or self.coa == '51.10.00' or self.coa == '51.11.00':
            for anak in self.children():
                ret += sum([p.kredit for p in anak.tbl_transaksi_set.filter(id_unit=300).filter(tgl_trans=(start_date))])
            return ret        
        else:            
            return sum([p.kredit for p in self.tbl_transaksi_set.filter(id_unit=300).filter(tgl_trans=(start_date))])        
    ######GABUNGAN HARI

    ######GABUNGAN    
    def my_debet_gabung(self, id_cabang, start_date, end_date):
        ret = 0
        #if self.coa[1:] == '0.00.00':
        if self.header_parent == None:
            for anak in self.children():
                ret += sum([p.debet for p in anak.tbl_transaksi_set.filter(status_jurnal= '2').filter(id_unit=300).\
                    filter(tgl_trans__range=(start_date,end_date))])
                for cucu in anak.children():
                    ret += sum([p.debet for p in cucu.tbl_transaksi_set.filter(status_jurnal= '2').filter(id_unit=300).\
                        filter(tgl_trans__range=(start_date,end_date))])
                    for cicit in cucu.children():
                        ret += sum([p.debet for p in cicit.tbl_transaksi_set.filter(status_jurnal= '2').filter(id_unit=300).\
                            filter(tgl_trans__range=(start_date,end_date))])
            return ret    
        #elif self.coa[2:] == '.00.00':
        elif self.coa == '11.00.00' or self.coa == '12.00.00' or self.coa == '13.00.00' or self.coa == '21.00.00' or self.coa == '22.00.00'\
            or self.coa == '23.00.00' or self.coa == '31.00.00' or self.coa == '32.00.00' or self.coa == '33.00.00' or self.coa == '34.00.00'\
            or self.coa == '35.00.00' or  self.coa == '41.00.00' or self.coa == '51.00.00'or self.coa == '61.00.00':
            for anak in self.children():
                ret += sum([p.debet for p in anak.tbl_transaksi_set.filter(status_jurnal= '2').filter(id_unit=300).\
                    filter(tgl_trans__range=(start_date,end_date))])
                for cucu in anak.children():
                    ret += sum([p.debet for p in cucu.tbl_transaksi_set.filter(id_unit=300).filter(status_jurnal= '2').\
                        filter(tgl_trans__range=(start_date,end_date))])
            return ret
        #elif self.coa[5:] == '.00':
        elif self.coa == '11.01.00' or self.coa == '11.05.00' or self.coa == '11.06.00' or self.coa == '11.07.00' or self.coa == '11.08.00'\
            or self.coa == '11.09.00' or self.coa == '11.10.00' or self.coa == '11.11.00' or self.coa == '11.12.00' or self.coa == '11.13.00'\
            or self.coa == '12.01.00' or self.coa == '12.02.00' or self.coa == '12.03.00' or self.coa == '13.01.00' or self.coa == '13.02.00'\
            or self.coa == '13.03.00' or self.coa == '13.04.00' or self.coa == '13.05.00' or self.coa == '13.06.00' or self.coa == '21.01.00'\
            or self.coa == '21.02.00' or self.coa == '21.03.00' or self.coa == '21.04.00' or self.coa == '21.05.00' or self.coa == '21.06.00'\
            or self.coa == '21.07.00' or self.coa == '21.08.00' or self.coa == '21.09.00' or self.coa == '21.10.00' or self.coa == '22.03.00'\
            or self.coa == '22.04.00' or self.coa == '22.05.00' or self.coa == '22.06.00' or self.coa == '23.01.00' or self.coa == '23.02.00'\
            or self.coa == '41.01.00' or self.coa == '41.02.00' or self.coa == '41.03.00' or self.coa == '51.01.00' or self.coa == '51.02.00'\
            or self.coa == '51.03.00' or self.coa == '51.04.00' or self.coa == '51.05.00' or self.coa == '51.06.00' or self.coa == '51.07.00'\
            or self.coa == '51.08.00' or self.coa == '51.09.00' or self.coa == '51.10.00' or self.coa == '51.11.00':
            for anak in self.children():
                ret += sum([p.debet for p in anak.tbl_transaksi_set.filter(status_jurnal= '2').filter(id_unit=300).\
                    filter(tgl_trans__range=(start_date,end_date))])
            return ret
        else:
            return sum([p.debet for p in self.tbl_transaksi_set.filter(status_jurnal= '2').filter(id_unit=300).\
                filter(tgl_trans__range=(start_date,end_date))])

      
    def my_kredit_gabung(self, id_cabang, start_date, end_date):
        ret = 0
        #if self.coa[1:] == '0.00.00':
        if self.header_parent == None:
            for anak in self.children():
                ret += sum([p.kredit for p in anak.tbl_transaksi_set.filter(status_jurnal= '2').filter(id_unit=300).\
                    filter(tgl_trans__range=(start_date,end_date))])
                for cucu in anak.children():
                    ret += sum([p.kredit for p in cucu.tbl_transaksi_set.filter(status_jurnal= '2').filter(id_unit=300).\
                        filter(tgl_trans__range=(start_date,end_date))])
                    for cicit in cucu.children():
                        ret += sum([p.kredit for p in cicit.tbl_transaksi_set.filter(status_jurnal= '2').filter(id_unit=300).\
                            filter(tgl_trans__range=(start_date,end_date))])
            return ret    
        #elif self.coa[2:] == '.00.00':
        elif self.coa == '11.00.00' or self.coa == '12.00.00' or self.coa == '13.00.00' or self.coa == '21.00.00' or self.coa == '22.00.00'\
            or self.coa == '23.00.00' or self.coa == '31.00.00' or self.coa == '32.00.00' or self.coa == '33.00.00' or self.coa == '34.00.00'\
            or self.coa == '35.00.00' or  self.coa == '41.00.00' or self.coa == '51.00.00'or self.coa == '61.00.00':
            for anak in self.children():
                ret += sum([p.kredit for p in anak.tbl_transaksi_set.filter(status_jurnal= '2').filter(id_unit=300).\
                    filter(tgl_trans__range=(start_date,end_date))])
                for cucu in anak.children():
                    ret += sum([p.kredit for p in cucu.tbl_transaksi_set.filter(status_jurnal= '2').filter(id_unit=300).\
                        filter(tgl_trans__range=(start_date,end_date))])
            return ret
        #elif self.coa[5:] == '.00':
        elif self.coa == '11.01.00' or self.coa == '11.05.00' or self.coa == '11.06.00' or self.coa == '11.07.00' or self.coa == '11.08.00'\
            or self.coa == '11.09.00' or self.coa == '11.10.00' or self.coa == '11.11.00' or self.coa == '11.12.00' or self.coa == '11.13.00'\
            or self.coa == '12.01.00' or self.coa == '12.02.00' or self.coa == '12.03.00' or self.coa == '13.01.00' or self.coa == '13.02.00'\
            or self.coa == '13.03.00' or self.coa == '13.04.00' or self.coa == '13.05.00' or self.coa == '13.06.00' or self.coa == '21.01.00'\
            or self.coa == '21.02.00' or self.coa == '21.03.00' or self.coa == '21.04.00' or self.coa == '21.05.00' or self.coa == '21.06.00'\
            or self.coa == '21.07.00' or self.coa == '21.08.00' or self.coa == '21.09.00' or self.coa == '21.10.00' or self.coa == '22.03.00' \
            or self.coa == '22.04.00' or self.coa == '22.05.00' or self.coa == '22.06.00' or self.coa == '23.01.00' or self.coa == '23.02.00'\
            or self.coa == '41.01.00' or self.coa == '41.02.00' or self.coa == '41.03.00' or self.coa == '51.01.00' or self.coa == '51.02.00'\
            or self.coa == '51.03.00' or self.coa == '51.04.00' or self.coa == '51.05.00' or self.coa == '51.06.00' or self.coa == '51.07.00'\
            or self.coa == '51.08.00' or self.coa == '51.09.00' or self.coa == '51.10.00' or self.coa == '51.11.00':
            for anak in self.children():
                ret += sum([p.kredit for p in anak.tbl_transaksi_set.filter(status_jurnal= '2').filter(id_unit=300).\
                    filter(tgl_trans__range=(start_date,end_date))])
            return ret        
        else:            
            return sum([p.kredit for p in self.tbl_transaksi_set.filter(status_jurnal= '2').filter(id_unit=300).\
                filter(tgl_trans__range=(start_date,end_date))])
    
    def view_saldo_akhir_gabung(self,id_cabang, start_date, end_date):
        if self.coa[0:2] == str(20) or self.coa[0:2] == str(21) or self.coa[0:2] == str(22) or self.coa[0:2] == str(23) or\
            self.coa[0:2] == str(30) or self.coa[0:2] == str(31) or self.coa[0:2] == str(32) or self.coa[0:2] == str(33) or\
            self.coa[0:2] == str(34) or self.coa[0:2] == str(35) or self.coa[0:2] == str(40) or self.coa[0:2] == str(41) or\
            self.coa[0:2] == str(60) or self.coa[0:2] == str(61):
            return (self.saldo_pjb + (self.my_kredit_gabung(id_cabang,start_date,end_date)) - \
                self.my_debet_gabung(id_cabang,start_date,end_date))
        else:
            return (self.saldo_pjb + self.my_debet_gabung(id_cabang,start_date,end_date)) - \
                (self.my_kredit_gabung(id_cabang,start_date,end_date))
    
    ######GABUNGAN  
    ### NERACA DI REPORT BARU SEBELUM POSTING
    def my_debet_gabung_neraca(self, start_date, end_date):
        ret = 0
        #if self.coa[1:] == '0.00.00':
        if self.header_parent == None:
            for anak in self.children():
                ret += sum([p.debet for p in anak.tbl_transaksi_set.filter(status_jurnal= '2').filter(id_unit=300).\
                    filter(tgl_trans__range=(start_date,end_date))])
                for cucu in anak.children():
                    ret += sum([p.debet for p in cucu.tbl_transaksi_set.filter(status_jurnal= '2').filter(id_unit=300).\
                        filter(tgl_trans__range=(start_date,end_date))])
                    for cicit in cucu.children():
                        ret += sum([p.debet for p in cicit.tbl_transaksi_set.filter(status_jurnal= '2').filter(id_unit=300).\
                            filter(tgl_trans__range=(start_date,end_date))])
            return ret    
        #elif self.coa[2:] == '.00.00':
        elif self.coa == '11.00.00' or self.coa == '12.00.00' or self.coa == '13.00.00' or self.coa == '21.00.00' or self.coa == '22.00.00'\
            or self.coa == '23.00.00' or self.coa == '31.00.00' or self.coa == '32.00.00' or self.coa == '33.00.00' or self.coa == '34.00.00'\
            or self.coa == '35.00.00' or  self.coa == '41.00.00' or self.coa == '51.00.00'or self.coa == '61.00.00':
            for anak in self.children():
                ret += sum([p.debet for p in anak.tbl_transaksi_set.filter(status_jurnal= '2').filter(id_unit=300).\
                    filter(tgl_trans__range=(start_date,end_date))])
                for cucu in anak.children():
                    ret += sum([p.debet for p in cucu.tbl_transaksi_set.filter(id_unit=300).filter(status_jurnal= '2').\
                        filter(tgl_trans__range=(start_date,end_date))])
            return ret
        #elif self.coa[5:] == '.00':
        elif self.coa == '11.01.00' or self.coa == '11.05.00' or self.coa == '11.06.00' or self.coa == '11.07.00' or self.coa == '11.08.00'\
            or self.coa == '11.09.00' or self.coa == '11.10.00' or self.coa == '11.11.00' or self.coa == '11.12.00' or self.coa == '11.13.00'\
            or self.coa == '12.01.00' or self.coa == '12.02.00' or self.coa == '12.03.00' or self.coa == '13.01.00' or self.coa == '13.02.00'\
            or self.coa == '13.03.00' or self.coa == '13.04.00' or self.coa == '13.05.00' or self.coa == '13.06.00' or self.coa == '21.01.00'\
            or self.coa == '21.02.00' or self.coa == '21.03.00' or self.coa == '21.04.00' or self.coa == '21.05.00' or self.coa == '21.06.00'\
            or self.coa == '21.07.00' or self.coa == '21.08.00' or self.coa == '21.09.00' or self.coa == '21.10.00' or self.coa == '22.03.00'\
            or self.coa == '22.04.00' or self.coa == '22.05.00' or self.coa == '22.06.00' or self.coa == '23.01.00' or self.coa == '23.02.00'\
            or self.coa == '41.01.00' or self.coa == '41.02.00' or self.coa == '41.03.00' or self.coa == '51.01.00' or self.coa == '51.02.00'\
            or self.coa == '51.03.00' or self.coa == '51.04.00' or self.coa == '51.05.00' or self.coa == '51.06.00' or self.coa == '51.07.00'\
            or self.coa == '51.08.00' or self.coa == '51.09.00' or self.coa == '51.10.00' or self.coa == '51.11.00' or self.coa == '12.04.00' or self.coa == '22.07.00':
            for anak in self.children():
                ret += sum([p.debet for p in anak.tbl_transaksi_set.filter(status_jurnal= '2').filter(id_unit=300).\
                    filter(tgl_trans__range=(start_date,end_date))])
            return ret
        else:
            return sum([p.debet for p in self.tbl_transaksi_set.filter(status_jurnal= '2').filter(id_unit=300).\
                filter(tgl_trans__range=(start_date,end_date))])

    def my_kredit_gabung_neraca(self, start_date, end_date):
        ret = 0
        #if self.coa[1:] == '0.00.00':
        if self.header_parent == None:
            for anak in self.children():
                ret += sum([p.kredit for p in anak.tbl_transaksi_set.filter(status_jurnal= '2').filter(id_unit=300).\
                    filter(tgl_trans__range=(start_date,end_date))])
                for cucu in anak.children():
                    ret += sum([p.kredit for p in cucu.tbl_transaksi_set.filter(status_jurnal= '2').filter(id_unit=300).\
                        filter(tgl_trans__range=(start_date,end_date))])
                    for cicit in cucu.children():
                        ret += sum([p.kredit for p in cicit.tbl_transaksi_set.filter(status_jurnal= '2').filter(id_unit=300).\
                            filter(tgl_trans__range=(start_date,end_date))])
            return ret    
        #elif self.coa[2:] == '.00.00':
        elif self.coa == '11.00.00' or self.coa == '12.00.00' or self.coa == '13.00.00' or self.coa == '21.00.00' or self.coa == '22.00.00'\
            or self.coa == '23.00.00' or self.coa == '31.00.00' or self.coa == '32.00.00' or self.coa == '33.00.00' or self.coa == '34.00.00'\
            or self.coa == '35.00.00' or  self.coa == '41.00.00' or self.coa == '51.00.00'or self.coa == '61.00.00':
            for anak in self.children():
                ret += sum([p.kredit for p in anak.tbl_transaksi_set.filter(status_jurnal= '2').filter(id_unit=300).\
                    filter(tgl_trans__range=(start_date,end_date))])
                for cucu in anak.children():
                    ret += sum([p.kredit for p in cucu.tbl_transaksi_set.filter(status_jurnal= '2').filter(id_unit=300).\
                        filter(tgl_trans__range=(start_date,end_date))])
            return ret
        #elif self.coa[5:] == '.00':
        elif self.coa == '11.01.00' or self.coa == '11.05.00' or self.coa == '11.06.00' or self.coa == '11.07.00' or self.coa == '11.08.00'\
            or self.coa == '11.09.00' or self.coa == '11.10.00' or self.coa == '11.11.00' or self.coa == '11.12.00' or self.coa == '11.13.00'\
            or self.coa == '12.01.00' or self.coa == '12.02.00' or self.coa == '12.03.00' or self.coa == '13.01.00' or self.coa == '13.02.00'\
            or self.coa == '13.03.00' or self.coa == '13.04.00' or self.coa == '13.05.00' or self.coa == '13.06.00' or self.coa == '21.01.00'\
            or self.coa == '21.02.00' or self.coa == '21.03.00' or self.coa == '21.04.00' or self.coa == '21.05.00' or self.coa == '21.06.00'\
            or self.coa == '21.07.00' or self.coa == '21.08.00' or self.coa == '21.09.00' or self.coa == '21.10.00' or self.coa == '22.03.00' \
            or self.coa == '22.04.00' or self.coa == '22.05.00' or self.coa == '22.06.00' or self.coa == '23.01.00' or self.coa == '23.02.00'\
            or self.coa == '41.01.00' or self.coa == '41.02.00' or self.coa == '41.03.00' or self.coa == '51.01.00' or self.coa == '51.02.00'\
            or self.coa == '51.03.00' or self.coa == '51.04.00' or self.coa == '51.05.00' or self.coa == '51.06.00' or self.coa == '51.07.00'\
            or self.coa == '51.08.00' or self.coa == '51.09.00' or self.coa == '51.10.00' or self.coa == '51.11.00' or self.coa == '12.04.00' or self.coa == '22.07.00':
            for anak in self.children():
                ret += sum([p.kredit for p in anak.tbl_transaksi_set.filter(status_jurnal= '2').filter(id_unit=300).\
                    filter(tgl_trans__range=(start_date,end_date))])
            return ret        
        else:            
            return sum([p.kredit for p in self.tbl_transaksi_set.filter(status_jurnal= '2').filter(id_unit=300).\
                filter(tgl_trans__range=(start_date,end_date))])


    def my_debet_gabung_neraca_posting(self, id_cabang, start_date):
        ret = 0
        #if self.coa[1:] == '0.00.00':
        if self.header_parent == None:
            for anak in self.children():
                ret += sum([p.debet for p in anak.tbl_transaksi_set.filter(status_jurnal= '3').filter(id_unit=300).\
                    filter(tgl_trans=(start_date))])
                for cucu in anak.children():
                    ret += sum([p.debet for p in cucu.tbl_transaksi_set.filter(status_jurnal= '3').filter(id_unit=300).\
                        filter(tgl_trans=(start_date))])
                    for cicit in cucu.children():
                        ret += sum([p.debet for p in cicit.tbl_transaksi_set.filter(status_jurnal= '3').filter(id_unit=300).\
                            filter(tgl_trans=(start_date))])
            return ret
        #elif self.coa[2:] == '.00.00':
        elif self.coa == '11.00.00' or self.coa == '12.00.00' or self.coa == '13.00.00' or self.coa == '21.00.00' or self.coa == '22.00.00'\
            or self.coa == '23.00.00' or self.coa == '31.00.00' or self.coa == '32.00.00' or self.coa == '33.00.00' or self.coa == '34.00.00'\
            or self.coa == '35.00.00' or  self.coa == '41.00.00' or self.coa == '51.00.00'or self.coa == '61.00.00':
            for anak in self.children():
                ret += sum([p.debet for p in anak.tbl_transaksi_set.filter(status_jurnal= '3').filter(id_unit=300).\
                    filter(tgl_trans=(start_date))])
                for cucu in anak.children():
                    ret += sum([p.debet for p in cucu.tbl_transaksi_set.filter(id_unit=300).filter(status_jurnal= '3').\
                        filter(tgl_trans=(start_date))])
            return ret
        #elif self.coa[5:] == '.00':
        elif self.coa == '11.01.00' or self.coa == '11.05.00' or self.coa == '11.06.00' or self.coa == '11.07.00' or self.coa == '11.08.00'\
            or self.coa == '11.09.00' or self.coa == '11.10.00' or self.coa == '11.11.00' or self.coa == '11.12.00' or self.coa == '11.13.00'\
            or self.coa == '12.01.00' or self.coa == '12.02.00' or self.coa == '12.03.00' or self.coa == '13.01.00' or self.coa == '13.02.00'\
            or self.coa == '13.03.00' or self.coa == '13.04.00' or self.coa == '13.05.00' or self.coa == '13.06.00' or self.coa == '21.01.00'\
            or self.coa == '21.02.00' or self.coa == '21.03.00' or self.coa == '21.04.00' or self.coa == '21.05.00' or self.coa == '21.06.00'\
            or self.coa == '21.07.00' or self.coa == '21.08.00' or self.coa == '21.09.00' or self.coa == '21.10.00' or self.coa == '22.03.00'\
            or self.coa == '22.04.00' or self.coa == '22.05.00' or self.coa == '22.06.00' or self.coa == '23.01.00' or self.coa == '23.02.00'\
            or self.coa == '41.01.00' or self.coa == '41.02.00' or self.coa == '41.03.00' or self.coa == '51.01.00' or self.coa == '51.02.00'\
            or self.coa == '51.03.00' or self.coa == '51.04.00' or self.coa == '51.05.00' or self.coa == '51.06.00' or self.coa == '51.07.00'\
            or self.coa == '51.08.00' or self.coa == '51.09.00' or self.coa == '51.10.00' or self.coa == '51.11.00':
            for anak in self.children():
                ret += sum([p.debet for p in anak.tbl_transaksi_set.filter(status_jurnal= '3').filter(id_unit=300).\
                    filter(tgl_trans=(start_date))])
            return ret
        else:
            return sum([p.debet for p in self.tbl_transaksi_set.filter(status_jurnal= '3').filter(id_unit=300).\
                filter(tgl_trans=(start_date))])


    def my_kredit_gabung_neraca_posting(self, id_cabang, start_date):
        ret = 0
        #if self.coa[1:] == '0.00.00':
        if self.header_parent == None:
            for anak in self.children():
                ret += sum([p.kredit for p in anak.tbl_transaksi_set.filter(status_jurnal= '3').filter(id_unit=300).\
                    filter(tgl_trans=(start_date))])
                for cucu in anak.children():
                    ret += sum([p.kredit for p in cucu.tbl_transaksi_set.filter(status_jurnal= '3').filter(id_unit=300).\
                        filter(tgl_trans=(start_date))])
                    for cicit in cucu.children():
                        ret += sum([p.kredit for p in cicit.tbl_transaksi_set.filter(status_jurnal= '3').filter(id_unit=300).\
                            filter(tgl_trans=(start_date))])
            return ret
        #elif self.coa[2:] == '.00.00':
        elif self.coa == '11.00.00' or self.coa == '12.00.00' or self.coa == '13.00.00' or self.coa == '21.00.00' or self.coa == '22.00.00'\
            or self.coa == '23.00.00' or self.coa == '31.00.00' or self.coa == '32.00.00' or self.coa == '33.00.00' or self.coa == '34.00.00'\
            or self.coa == '35.00.00' or  self.coa == '41.00.00' or self.coa == '51.00.00'or self.coa == '61.00.00':
            for anak in self.children():
                ret += sum([p.kredit for p in anak.tbl_transaksi_set.filter(status_jurnal= '3').filter(id_unit=300).\
                    filter(tgl_trans=(start_date))])
                for cucu in anak.children():
                    ret += sum([p.kredit for p in cucu.tbl_transaksi_set.filter(status_jurnal= '3').filter(id_unit=300).\
                        filter(tgl_trans=(start_date))])
            return ret
        #elif self.coa[5:] == '.00':
        elif self.coa == '11.01.00' or self.coa == '11.05.00' or self.coa == '11.06.00' or self.coa == '11.07.00' or self.coa == '11.08.00'\
            or self.coa == '11.09.00' or self.coa == '11.10.00' or self.coa == '11.11.00' or self.coa == '11.12.00' or self.coa == '11.13.00'\
            or self.coa == '12.01.00' or self.coa == '12.02.00' or self.coa == '12.03.00' or self.coa == '13.01.00' or self.coa == '13.02.00'\
            or self.coa == '13.03.00' or self.coa == '13.04.00' or self.coa == '13.05.00' or self.coa == '13.06.00' or self.coa == '21.01.00'\
            or self.coa == '21.02.00' or self.coa == '21.03.00' or self.coa == '21.04.00' or self.coa == '21.05.00' or self.coa == '21.06.00'\
            or self.coa == '21.07.00' or self.coa == '21.08.00' or self.coa == '21.09.00' or self.coa == '21.10.00' or self.coa == '22.03.00' \
            or self.coa == '22.04.00' or self.coa == '22.05.00' or self.coa == '22.06.00' or self.coa == '23.01.00' or self.coa == '23.02.00'\
            or self.coa == '41.01.00' or self.coa == '41.02.00' or self.coa == '41.03.00' or self.coa == '51.01.00' or self.coa == '51.02.00'\
            or self.coa == '51.03.00' or self.coa == '51.04.00' or self.coa == '51.05.00' or self.coa == '51.06.00' or self.coa == '51.07.00'\
            or self.coa == '51.08.00' or self.coa == '51.09.00' or self.coa == '51.10.00' or self.coa == '51.11.00':
            for anak in self.children():
                ret += sum([p.kredit for p in anak.tbl_transaksi_set.filter(status_jurnal= '3').filter(id_unit=300).\
                    filter(tgl_trans=(start_date))])
            return ret
        else:
            return sum([p.kredit for p in self.tbl_transaksi_set.filter(status_jurnal= '3').filter(id_unit=300).\
                filter(tgl_trans=(start_date))])
   
    def view_saldo_akhir_gabung_neraca(self, start_date,end_date):
        if self.coa[0:2] == str(20) or self.coa[0:2] == str(21) or self.coa[0:2] == str(22) or self.coa[0:2] == str(23) or self.coa[0:2] == str(30) \
            or self.coa[0:2] == str(31) or self.coa[0:2] == str(32) or self.coa[0:2] == str(33) or self.coa[0:2] == str(34)\
            or self.coa[0:2] == str(35) or self.coa[0:2] == str(40) or self.coa[0:2] == str(41) or self.coa[0:2] == str(60)\
            or self.coa[0:2] == str(61):
            ###Rubah Sementara
            return (self.view_saldo_awal_gabungan_neraca(start_date)) + (self.my_kredit_gabung_neraca(start_date,end_date)\
                - self.my_debet_gabung_neraca(start_date,end_date))

            return (self.view_saldo_awal_gabungan_neraca(start_date) + (self.my_kredit_gabung_neraca(start_date))\
                - self.my_debet_gabung_neraca(start_date))
        else:
            return (self.view_saldo_awal_gabungan_neraca(start_date)  - (self.my_kredit_gabung_neraca(start_date,end_date)) +\
                self.my_debet_gabung_neraca(start_date,end_date))

    def total_debet_nenek_neraca_gabungan(self,  start_date, end_date):
        ret = 0
        #if self.coa[1:] == '0.00.00':
        if self.header_parent == None:
            for anak in self.children():
                ret += sum([p.debet for p in anak.tbl_transaksi_set.filter(id_unit=300).filter(tgl_trans__range=(start_date,end_date))])
                for cucu in anak.children():
                    ret += sum([p.debet for p in cucu.tbl_transaksi_set.filter(id_unit=300).filter(tgl_trans__range=(start_date,end_date))])
                    for cicit in cucu.children():
                        ret += sum([p.debet for p in cicit.tbl_transaksi_set.filter(id_unit=300).filter(tgl_trans__range=(start_date,end_date))])
            return ret
        else:
            return ret

    def total_kredit_nenek_neraca_gabungan(self, start_date, end_date):
        ret = 0
        #if self.coa[1:] == '0.00.00':
        if self.header_parent == None:
            for anak in self.children():
                ret += sum([p.kredit for p in anak.tbl_transaksi_set.filter(tgl_trans__range=(start_date,end_date))])
                for cucu in anak.children():
                    ret += sum([p.kredit for p in cucu.tbl_transaksi_set.filter(tgl_trans__range=(start_date,end_date))])
                    for cicit in cucu.children():
                        ret += sum([p.kredit for p in cicit.tbl_transaksi_set.filter(tgl_trans__range=(start_date,end_date))])
            return ret
        else:
            return ret


    def total_debet_nenek_neraca(self, id_cabang, start_date):
        ret = 0
        #if self.coa[1:] == '0.00.00':
        if self.header_parent == None:
            for anak in self.children():
                ret += sum([p.debet for p in anak.tbl_transaksi_set.filter(id_cabang=id_cabang).filter(id_unit=300).filter(tgl_trans=(start_date))])
                for cucu in anak.children():
                    ret += sum([p.debet for p in cucu.tbl_transaksi_set.filter(id_cabang=id_cabang).filter(id_unit=300).filter(tgl_trans=(start_date))])
                    for cicit in cucu.children():
                        ret += sum([p.debet for p in cicit.tbl_transaksi_set.filter(id_cabang=id_cabang).filter(id_unit=300).filter(tgl_trans=(start_date))])
            return ret    
        else:            
            return ret

    def total_kredit_nenek_neraca(self, id_cabang, start_date):
        ret = 0
        #if self.coa[1:] == '0.00.00':
        if self.header_parent == None:
            for anak in self.children():
                ret += sum([p.kredit for p in anak.tbl_transaksi_set.filter(id_cabang=id_cabang).filter(tgl_trans=(start_date))])
                for cucu in anak.children():
                    ret += sum([p.kredit for p in cucu.tbl_transaksi_set.filter(id_cabang=id_cabang).filter(tgl_trans=(start_date))])
                    for cicit in cucu.children():
                        ret += sum([p.kredit for p in cicit.tbl_transaksi_set.filter(id_cabang=id_cabang).filter(tgl_trans=(start_date))])
            return ret
        else:            
            return ret

    def my_kredit_neraca(self, id_cabang, start_date, end_date):
        ret = 0
        #if self.coa[1:] == '0.00.00':
        if self.header_parent == None:
            for anak in self.children():
                ret += sum([p.kredit for p in anak.tbl_transaksi_set.filter(id_cabang=id_cabang).filter(status_jurnal= '2').filter(id_unit=300).filter(tgl_trans__range=(start_date,end_date))])
                for cucu in anak.children():
                    ret += sum([p.kredit for p in cucu.tbl_transaksi_set.filter(id_cabang=id_cabang).filter(status_jurnal= '2').filter(id_unit=300).filter(tgl_trans__range=(start_date,end_date))])
                    for cicit in cucu.children():
                        ret += sum([p.kredit for p in cicit.tbl_transaksi_set.filter(id_cabang=id_cabang).filter(status_jurnal= '2').filter(id_unit=300).filter(tgl_trans__range=(start_date,end_date))])
            return ret    
        #elif self.coa[2:] == '.00.00':
        elif self.coa == '11.00.00' or self.coa == '12.00.00' or self.coa == '13.00.00' or self.coa == '21.00.00' or self.coa == '22.00.00' or self.coa == '23.00.00' or\
            self.coa == '31.00.00' or self.coa == '32.00.00' or self.coa == '33.00.00' or self.coa == '34.00.00' or self.coa == '35.00.00' or  self.coa == '41.00.00' or \
            self.coa == '51.00.00'or self.coa == '61.00.00':
            for anak in self.children():
                ret += sum([p.kredit for p in anak.tbl_transaksi_set.filter(id_cabang=id_cabang).filter(status_jurnal= '2').filter(id_unit=300).filter(tgl_trans__range=(start_date,end_date))])
                for cucu in anak.children():
                    ret += sum([p.kredit for p in cucu.tbl_transaksi_set.filter(id_cabang=id_cabang).filter(status_jurnal= '2').filter(id_unit=300).filter(tgl_trans__range=(start_date,end_date))])
            return ret
        #elif self.coa[5:] == '.00':
        elif self.coa == '11.01.00' or self.coa == '11.05.00' or self.coa == '11.06.00' or self.coa == '11.07.00' or self.coa == '11.08.00' or self.coa == '11.09.00' or \
            self.coa == '11.10.00' or self.coa == '11.11.00' or self.coa == '11.12.00' or self.coa == '11.13.00' or self.coa == '12.01.00' or self.coa == '12.02.00' or \
            self.coa == '12.03.00' or self.coa == '13.01.00' or self.coa == '13.02.00' or self.coa == '13.03.00' or self.coa == '13.04.00' or self.coa == '13.05.00' or \
            self.coa == '13.06.00' or self.coa == '21.01.00' or self.coa == '21.02.00' or self.coa == '21.03.00' or self.coa == '21.04.00' or self.coa == '21.05.00' or\
            self.coa == '21.06.00' or self.coa == '21.07.00' or self.coa == '21.08.00' or self.coa == '21.09.00' or self.coa == '21.10.00' or self.coa == '22.03.00' or \
            self.coa == '22.04.00' or self.coa == '22.05.00' or self.coa == '22.06.00' or self.coa == '23.01.00' or self.coa == '23.02.00' or self.coa == '41.01.00' or \
            self.coa == '41.02.00' or self.coa == '41.03.00' or self.coa == '51.01.00' or self.coa == '51.02.00' or self.coa == '51.03.00' or self.coa == '51.04.00' or \
            self.coa == '51.05.00' or self.coa == '51.06.00' or self.coa == '51.07.00' or self.coa == '51.08.00' or self.coa == '51.09.00' or self.coa == '51.10.00' or \
            self.coa == '51.11.00' or self.coa == '41.04.00' or self.coa == '12.04.00' or self.coa == '22.07.00':
            for anak in self.children():
                ret += sum([p.kredit for p in anak.tbl_transaksi_set.filter(id_cabang=id_cabang).filter(status_jurnal= '2').filter(id_unit=300).filter(tgl_trans__range=(start_date,end_date))])
            return ret        
        else:            
            return sum([p.kredit for p in self.tbl_transaksi_set.filter(id_cabang=id_cabang).filter(status_jurnal= '2').filter(id_unit=300).filter(tgl_trans__range=(start_date,end_date))])

    def my_debet_neraca(self, id_cabang, start_date,end_date):
        ret = 0
        #if self.coa[1:] == '0.00.00':
        if self.header_parent == None:
            for anak in self.children():
                ret += sum([p.debet for p in anak.tbl_transaksi_set.filter(id_cabang=id_cabang).filter(status_jurnal= '2').filter(id_unit=300).filter(tgl_trans__range=(start_date,end_date))])
                for cucu in anak.children():
                    ret += sum([p.debet for p in cucu.tbl_transaksi_set.filter(id_cabang=id_cabang).filter(status_jurnal= '2').filter(id_unit=300).filter(tgl_trans__range=(start_date,end_date))])
                    for cicit in cucu.children():
                        ret += sum([p.debet for p in cicit.tbl_transaksi_set.filter(id_cabang=id_cabang).filter(status_jurnal= '2').filter(id_unit=300).filter(tgl_trans__range=(start_date,end_date))])
            return ret    
        #elif self.coa[2:] == '.00.00':
        elif self.coa == '11.00.00' or self.coa == '12.00.00' or self.coa == '13.00.00' or self.coa == '21.00.00' or self.coa == '22.00.00' or self.coa == '23.00.00' or\
            self.coa == '31.00.00' or self.coa == '32.00.00' or self.coa == '33.00.00' or self.coa == '34.00.00' or self.coa == '35.00.00' or  self.coa == '41.00.00' or \
            self.coa == '51.00.00'or self.coa == '61.00.00':
            for anak in self.children():
                ret += sum([p.debet for p in anak.tbl_transaksi_set.filter(id_cabang=id_cabang).filter(status_jurnal= '2').filter(id_unit=300).filter(tgl_trans__range=(start_date,end_date))])
                for cucu in anak.children():
                    ret += sum([p.debet for p in cucu.tbl_transaksi_set.filter(id_cabang=id_cabang).filter(id_unit=300).filter(status_jurnal= '2').filter(tgl_trans__range=(start_date,end_date))])
            return ret
        #elif self.coa[5:] == '.00':
        elif self.coa == '11.01.00' or self.coa == '11.05.00' or self.coa == '11.06.00' or self.coa == '11.07.00' or self.coa == '11.08.00' or self.coa == '11.09.00' or \
            self.coa == '11.10.00' or self.coa == '11.11.00' or self.coa == '11.12.00' or self.coa == '11.13.00' or self.coa == '12.01.00' or self.coa == '12.02.00' or \
            self.coa == '12.03.00' or self.coa == '13.01.00' or self.coa == '13.02.00' or self.coa == '13.03.00' or self.coa == '13.04.00' or self.coa == '13.05.00' or \
            self.coa == '13.06.00' or self.coa == '21.01.00' or self.coa == '21.02.00' or self.coa == '21.03.00' or self.coa == '21.04.00' or self.coa == '21.05.00' or\
            self.coa == '21.06.00' or self.coa == '21.07.00' or self.coa == '21.08.00' or self.coa == '21.09.00' or self.coa == '21.10.00' or self.coa == '22.03.00' or \
            self.coa == '22.04.00' or self.coa == '22.05.00' or self.coa == '22.06.00' or self.coa == '23.01.00' or self.coa == '23.02.00' or self.coa == '41.01.00' or \
            self.coa == '41.02.00' or self.coa == '41.03.00' or self.coa == '51.01.00' or self.coa == '51.02.00' or self.coa == '51.03.00' or self.coa == '51.04.00' or \
            self.coa == '51.05.00' or self.coa == '51.06.00' or self.coa == '51.07.00' or self.coa == '51.08.00' or self.coa == '51.09.00' or self.coa == '51.10.00' or \
            self.coa == '51.11.00' or self.coa == '41.04.00' or self.coa == '12.04.00' or self.coa == '22.07.00':
            for anak in self.children():
                ret += sum([p.debet for p in anak.tbl_transaksi_set.filter(id_cabang=id_cabang).filter(status_jurnal= '2').filter(id_unit=300).filter(tgl_trans__range=(start_date,end_date))])
            return ret
        else:
            return sum([p.debet for p in self.tbl_transaksi_set.filter(id_cabang=id_cabang).filter(status_jurnal= '2').filter(id_unit=300).filter(tgl_trans__range=(start_date,end_date))])


    def view_saldo_akhir_neraca(self,id_cabang, start_date):
        if self.coa[0:2] == str(20) or self.coa[0:2] == str(21) or self.coa[0:2] == str(22) or self.coa[0:2] == str(23) or self.coa[0:2] == str(30) or \
            self.coa[0:2] == str(31) or self.coa[0:2] == str(32) or self.coa[0:2] == str(33) or self.coa[0:2] == str(34) or self.coa[0:2] == str(35) or \
            self.coa[0:2] == str(40) or self.coa[0:2] == str(41) or self.coa[0:2] == str(60) or self.coa[0:2] == str(61):
            return (self.saldo_pjb + (self.my_kredit_neraca(id_cabang,start_date)) - self.my_debet_neraca(id_cabang,start_date))
        else:
            return (self.saldo_pjb + self.my_debet_neraca(id_cabang,start_date)) - (self.my_kredit_neraca(id_cabang,start_date))

    ## AKHIR NERACA DI REPORT BARU SEBELUM POSTING

    ### NERACA DI REPORT BARU SETELAH POSTING
    def my_debet_gabung_posting(self, start_date, end_date):
        ret = 0
        #if self.coa[1:] == '0.00.00':
        if self.header_parent == None:
            for anak in self.children():
                ret += sum([p.debet for p in anak.tbl_transaksi_set.filter(status_jurnal= '2').filter(id_unit=300).\
                    filter(tgl_trans__range=(start_date,end_date))])
                for cucu in anak.children():
                    ret += sum([p.debet for p in cucu.tbl_transaksi_set.filter(status_jurnal= '2').filter(id_unit=300).\
                        filter(tgl_trans__range=(start_date,end_date))])
                    for cicit in cucu.children():
                        ret += sum([p.debet for p in cicit.tbl_transaksi_set.filter(status_jurnal= '2').filter(id_unit=300).\
                            filter(tgl_trans__range=(start_date,end_date))])
            return ret    
        #elif self.coa[2:] == '.00.00':
        elif self.coa == '11.00.00' or self.coa == '12.00.00' or self.coa == '13.00.00' or self.coa == '21.00.00' or self.coa == '22.00.00'\
            or self.coa == '23.00.00' or self.coa == '31.00.00' or self.coa == '32.00.00' or self.coa == '33.00.00' or self.coa == '34.00.00'\
            or self.coa == '35.00.00' or  self.coa == '41.00.00' or self.coa == '51.00.00'or self.coa == '61.00.00':
            for anak in self.children():
                ret += sum([p.debet for p in anak.tbl_transaksi_set.filter(status_jurnal= '2').filter(id_unit=300).\
                    filter(tgl_trans__range=(start_date,end_date))])
                for cucu in anak.children():
                    ret += sum([p.debet for p in cucu.tbl_transaksi_set.filter(id_unit=300).filter(status_jurnal= '2').\
                        filter(tgl_trans__range=(start_date,end_date))])
            return ret
        #elif self.coa[5:] == '.00':
        elif self.coa == '11.01.00' or self.coa == '11.05.00' or self.coa == '11.06.00' or self.coa == '11.07.00' or self.coa == '11.08.00'\
            or self.coa == '11.09.00' or self.coa == '11.10.00' or self.coa == '11.11.00' or self.coa == '11.12.00' or self.coa == '11.13.00'\
            or self.coa == '12.01.00' or self.coa == '12.02.00' or self.coa == '12.03.00' or self.coa == '13.01.00' or self.coa == '13.02.00'\
            or self.coa == '13.03.00' or self.coa == '13.04.00' or self.coa == '13.05.00' or self.coa == '13.06.00' or self.coa == '21.01.00'\
            or self.coa == '21.02.00' or self.coa == '21.03.00' or self.coa == '21.04.00' or self.coa == '21.05.00' or self.coa == '21.06.00'\
            or self.coa == '21.07.00' or self.coa == '21.08.00' or self.coa == '21.09.00' or self.coa == '21.10.00' or self.coa == '22.03.00'\
            or self.coa == '22.04.00' or self.coa == '22.05.00' or self.coa == '22.06.00' or self.coa == '23.01.00' or self.coa == '23.02.00'\
            or self.coa == '41.01.00' or self.coa == '41.02.00' or self.coa == '41.03.00' or self.coa == '51.01.00' or self.coa == '51.02.00'\
            or self.coa == '51.03.00' or self.coa == '51.04.00' or self.coa == '51.05.00' or self.coa == '51.06.00' or self.coa == '51.07.00'\
            or self.coa == '51.08.00' or self.coa == '51.09.00' or self.coa == '51.10.00' or self.coa == '51.11.00':
            for anak in self.children():
                ret += sum([p.debet for p in anak.tbl_transaksi_set.filter(status_jurnal= '2').filter(id_unit=300).\
                    filter(tgl_trans__range=(start_date,end_date))])
            return ret
        else:
            return sum([p.debet for p in self.tbl_transaksi_set.filter(status_jurnal= '2').filter(id_unit=300).\
                filter(tgl_trans__range=(start_date,end_date))])

    def my_kredit_gabung_posting(self,start_date,end_date):
        ret = 0
        #if self.coa[1:] == '0.00.00':
        if self.header_parent == None:
            for anak in self.children():
                ret += sum([p.kredit for p in anak.tbl_transaksi_set.filter(status_jurnal= '2').filter(id_unit=300).\
                    filter(tgl_trans__range=(start_date,end_date))])
                for cucu in anak.children():
                    ret += sum([p.kredit for p in cucu.tbl_transaksi_set.filter(status_jurnal= '2').filter(id_unit=300).\
                        filter(tgl_trans__range=(start_date,end_date))])
                    for cicit in cucu.children():
                        ret += sum([p.kredit for p in cicit.tbl_transaksi_set.filter(status_jurnal= '2').filter(id_unit=300).\
                            filter(tgl_trans__range=(start_date,end_date))])
            return ret    
        #elif self.coa[2:] == '.00.00':
        elif self.coa == '11.00.00' or self.coa == '12.00.00' or self.coa == '13.00.00' or self.coa == '21.00.00' or self.coa == '22.00.00'\
            or self.coa == '23.00.00' or self.coa == '31.00.00' or self.coa == '32.00.00' or self.coa == '33.00.00' or self.coa == '34.00.00'\
            or self.coa == '35.00.00' or  self.coa == '41.00.00' or self.coa == '51.00.00'or self.coa == '61.00.00':
            for anak in self.children():
                ret += sum([p.kredit for p in anak.tbl_transaksi_set.filter(status_jurnal= '3').filter(id_unit=300).\
                    filter(tgl_trans__range=(start_date,end_date))])
                for cucu in anak.children():
                    ret += sum([p.kredit for p in cucu.tbl_transaksi_set.filter(status_jurnal= '3').filter(id_unit=300).\
                        filter(tgl_trans__range=(start_date,end_date))])
            return ret
        #elif self.coa[5:] == '.00':
        elif self.coa == '11.01.00' or self.coa == '11.05.00' or self.coa == '11.06.00' or self.coa == '11.07.00' or self.coa == '11.08.00'\
            or self.coa == '11.09.00' or self.coa == '11.10.00' or self.coa == '11.11.00' or self.coa == '11.12.00' or self.coa == '11.13.00'\
            or self.coa == '12.01.00' or self.coa == '12.02.00' or self.coa == '12.03.00' or self.coa == '13.01.00' or self.coa == '13.02.00'\
            or self.coa == '13.03.00' or self.coa == '13.04.00' or self.coa == '13.05.00' or self.coa == '13.06.00' or self.coa == '21.01.00'\
            or self.coa == '21.02.00' or self.coa == '21.03.00' or self.coa == '21.04.00' or self.coa == '21.05.00' or self.coa == '21.06.00'\
            or self.coa == '21.07.00' or self.coa == '21.08.00' or self.coa == '21.09.00' or self.coa == '21.10.00' or self.coa == '22.03.00' \
            or self.coa == '22.04.00' or self.coa == '22.05.00' or self.coa == '22.06.00' or self.coa == '23.01.00' or self.coa == '23.02.00'\
            or self.coa == '41.01.00' or self.coa == '41.02.00' or self.coa == '41.03.00' or self.coa == '51.01.00' or self.coa == '51.02.00'\
            or self.coa == '51.03.00' or self.coa == '51.04.00' or self.coa == '51.05.00' or self.coa == '51.06.00' or self.coa == '51.07.00'\
            or self.coa == '51.08.00' or self.coa == '51.09.00' or self.coa == '51.10.00' or self.coa == '51.11.00':
            for anak in self.children():
                ret += sum([p.kredit for p in anak.tbl_transaksi_set.filter(status_jurnal= '3').filter(id_unit=300).\
                    filter(tgl_trans__range=(start_date,end_date))])
            return ret        
        else:            
            return sum([p.kredit for p in self.tbl_transaksi_set.filter(status_jurnal= '3').filter(id_unit=300).\
                filter(tgl_trans__range=(start_date,end_date))])
    
    def view_saldo_akhir_gabung_posting(self, start_date,end_date):
        if self.coa[0:2] == str(20) or self.coa[0:2] == str(21) or self.coa[0:2] == str(22) or self.coa[0:2] == str(23) or\
            self.coa[0:2] == str(30) or self.coa[0:2] == str(31) or self.coa[0:2] == str(32) or self.coa[0:2] == str(33) or\
            self.coa[0:2] == str(34) or self.coa[0:2] == str(35) or self.coa[0:2] == str(40) or self.coa[0:2] == str(41) or\
            self.coa[0:2] == str(60) or self.coa[0:2] == str(61):
            return (self.view_saldo_awal_gabungan_posting(start_date) + (self.my_kredit_gabung_posting(start_date,end_date)) - self.my_debet_gabung_posting(start_date,end_date))
        else:
            return (self.view_saldo_awal_gabungan_posting(start_date) + self.my_debet_gabung_posting(start_date,end_date)) - (self.my_kredit_gabung_posting(start_date,end_date))

    def total_debet_nenek_posting(self, start_date, end_date):
        ret = 0
        #if self.coa[1:] == '0.00.00':
        if self.header_parent == None:
            for anak in self.children():
                ret += sum([p.debet for p in anak.tbl_transaksi_set.filter(id_unit=300).filter(tgl_trans__range=(start_date,end_date))])
                for cucu in anak.children():
                    ret += sum([p.debet for p in cucu.tbl_transaksi_set.filter(id_unit=300).filter(tgl_trans__range=(start_date,end_date))])
                    for cicit in cucu.children():
                        ret += sum([p.debet for p in cicit.tbl_transaksi_set.filter(id_unit=300).filter(tgl_trans__range=(start_date,end_date))])
            return ret    
        else:            
            return ret

    def total_kredit_nenek_posting(self, start_date,end_date):
        ret = 0
        #if self.coa[1:] == '0.00.00':
        if self.header_parent == None:
            for anak in self.children():
                ret += sum([p.kredit for p in anak.tbl_transaksi_set.filter(tgl_trans__range=(start_date,end_date))])
                for cucu in anak.children():
                    ret += sum([p.kredit for p in cucu.tbl_transaksi_set.filter(tgl_trans__range=(start_date,end_date))])
                    for cicit in cucu.children():
                        ret += sum([p.kredit for p in cicit.tbl_transaksi_set.filter(tgl_trans__range=(start_date,end_date))])
            return ret
        else:            
            return ret

    def my_kredit_posting(self, id_cabang, start_date, end_date):
        ret = 0
        #if self.coa[1:] == '0.00.00':
        if self.header_parent == None:
            for anak in self.children():
                ret += sum([p.kredit for p in anak.tbl_transaksi_set.filter(id_cabang=id_cabang).filter(status_jurnal= '2').filter(id_unit=300).filter(tgl_trans__range=(start_date,end_date))])
                for cucu in anak.children():
                    ret += sum([p.kredit for p in cucu.tbl_transaksi_set.filter(id_cabang=id_cabang).filter(status_jurnal= '2').filter(id_unit=300).filter(tgl_trans__range=(start_date,end_date))])
                    for cicit in cucu.children():
                        ret += sum([p.kredit for p in cicit.tbl_transaksi_set.filter(id_cabang=id_cabang).filter(status_jurnal= '2').filter(id_unit=300).filter(tgl_trans__range=(start_date,end_date))])
            return ret    
        #elif self.coa[2:] == '.00.00':
        elif self.coa == '11.00.00' or self.coa == '12.00.00' or self.coa == '13.00.00' or self.coa == '21.00.00' or self.coa == '22.00.00' or self.coa == '23.00.00' or\
            self.coa == '31.00.00' or self.coa == '32.00.00' or self.coa == '33.00.00' or self.coa == '34.00.00' or self.coa == '35.00.00' or  self.coa == '41.00.00' or \
            self.coa == '51.00.00'or self.coa == '61.00.00':
            for anak in self.children():
                ret += sum([p.kredit for p in anak.tbl_transaksi_set.filter(id_cabang=id_cabang).filter(status_jurnal= '2').filter(id_unit=300).filter(tgl_trans__range=(start_date,end_date))])
                for cucu in anak.children():
                    ret += sum([p.kredit for p in cucu.tbl_transaksi_set.filter(id_cabang=id_cabang).filter(status_jurnal= '2').filter(id_unit=300).filter(tgl_trans__range=(start_date,end_date))])
            return ret
        #elif self.coa[5:] == '.00':
        elif self.coa == '11.01.00' or self.coa == '11.05.00' or self.coa == '11.06.00' or self.coa == '11.07.00' or self.coa == '11.08.00' or self.coa == '11.09.00' or \
            self.coa == '11.10.00' or self.coa == '11.11.00' or self.coa == '11.12.00' or self.coa == '11.13.00' or self.coa == '12.01.00' or self.coa == '12.02.00' or \
            self.coa == '12.03.00' or self.coa == '13.01.00' or self.coa == '13.02.00' or self.coa == '13.03.00' or self.coa == '13.04.00' or self.coa == '13.05.00' or \
            self.coa == '13.06.00' or self.coa == '21.01.00' or self.coa == '21.02.00' or self.coa == '21.03.00' or self.coa == '21.04.00' or self.coa == '21.05.00' or\
            self.coa == '21.06.00' or self.coa == '21.07.00' or self.coa == '21.08.00' or self.coa == '21.09.00' or self.coa == '21.10.00' or self.coa == '22.03.00' or \
            self.coa == '22.04.00' or self.coa == '22.05.00' or self.coa == '22.06.00' or self.coa == '23.01.00' or self.coa == '23.02.00' or self.coa == '41.01.00' or \
            self.coa == '41.02.00' or self.coa == '41.03.00' or self.coa == '51.01.00' or self.coa == '51.02.00' or self.coa == '51.03.00' or self.coa == '51.04.00' or \
            self.coa == '51.05.00' or self.coa == '51.06.00' or self.coa == '51.07.00' or self.coa == '51.08.00' or self.coa == '51.09.00' or self.coa == '51.10.00' or \
            self.coa == '51.11.00' or self.coa == '41.04.00':
            for anak in self.children():
                ret += sum([p.kredit for p in anak.tbl_transaksi_set.filter(id_cabang=id_cabang).filter(status_jurnal= '2').filter(id_unit=300).filter(tgl_trans__range=(start_date,end_date))])
            return ret        
        else:            
            return sum([p.kredit for p in self.tbl_transaksi_set.filter(id_cabang=id_cabang).filter(status_jurnal= '2').filter(id_unit=300).filter(tgl_trans__range=(start_date,end_date))])

    def my_debet_posting(self, id_cabang, start_date, end_date):
        ret = 0
        #if self.coa[1:] == '0.00.00':
        if self.header_parent == None:
            for anak in self.children():
                ret += sum([p.debet for p in anak.tbl_transaksi_set.filter(id_cabang=id_cabang).filter(status_jurnal= '2').filter(id_unit=300).filter(tgl_trans__range=(start_date,end_date))])
                for cucu in anak.children():
                    ret += sum([p.debet for p in cucu.tbl_transaksi_set.filter(id_cabang=id_cabang).filter(status_jurnal= '2').filter(id_unit=300).filter(tgl_trans__range=(start_date,end_date))])
                    for cicit in cucu.children():
                        ret += sum([p.debet for p in cicit.tbl_transaksi_set.filter(id_cabang=id_cabang).filter(status_jurnal= '2').filter(id_unit=300).filter(tgl_trans__range=(start_date,end_date))])
            return ret    
        #elif self.coa[2:] == '.00.00':
        elif self.coa == '11.00.00' or self.coa == '12.00.00' or self.coa == '13.00.00' or self.coa == '21.00.00' or self.coa == '22.00.00' or self.coa == '23.00.00' or\
            self.coa == '31.00.00' or self.coa == '32.00.00' or self.coa == '33.00.00' or self.coa == '34.00.00' or self.coa == '35.00.00' or  self.coa == '41.00.00' or \
            self.coa == '51.00.00'or self.coa == '61.00.00':
            for anak in self.children():
                ret += sum([p.debet for p in anak.tbl_transaksi_set.filter(id_cabang=id_cabang).filter(status_jurnal= '2').filter(id_unit=300).filter(tgl_trans__range=(start_date,end_date))])
                for cucu in anak.children():
                    ret += sum([p.debet for p in cucu.tbl_transaksi_set.filter(id_cabang=id_cabang).filter(id_unit=300).filter(status_jurnal= '2').filter(tgl_trans__range=(start_date,end_date))])
            return ret
        #elif self.coa[5:] == '.00':
        elif self.coa == '11.01.00' or self.coa == '11.05.00' or self.coa == '11.06.00' or self.coa == '11.07.00' or self.coa == '11.08.00' or self.coa == '11.09.00' or \
            self.coa == '11.10.00' or self.coa == '11.11.00' or self.coa == '11.12.00' or self.coa == '11.13.00' or self.coa == '12.01.00' or self.coa == '12.02.00' or \
            self.coa == '12.03.00' or self.coa == '13.01.00' or self.coa == '13.02.00' or self.coa == '13.03.00' or self.coa == '13.04.00' or self.coa == '13.05.00' or \
            self.coa == '13.06.00' or self.coa == '21.01.00' or self.coa == '21.02.00' or self.coa == '21.03.00' or self.coa == '21.04.00' or self.coa == '21.05.00' or\
            self.coa == '21.06.00' or self.coa == '21.07.00' or self.coa == '21.08.00' or self.coa == '21.09.00' or self.coa == '21.10.00' or self.coa == '22.03.00' or \
            self.coa == '22.04.00' or self.coa == '22.05.00' or self.coa == '22.06.00' or self.coa == '23.01.00' or self.coa == '23.02.00' or self.coa == '41.01.00' or \
            self.coa == '41.02.00' or self.coa == '41.03.00' or self.coa == '51.01.00' or self.coa == '51.02.00' or self.coa == '51.03.00' or self.coa == '51.04.00' or \
            self.coa == '51.05.00' or self.coa == '51.06.00' or self.coa == '51.07.00' or self.coa == '51.08.00' or self.coa == '51.09.00' or self.coa == '51.10.00' or \
            self.coa == '51.11.00' or self.coa == '41.04.00':
            for anak in self.children():
                ret += sum([p.debet for p in anak.tbl_transaksi_set.filter(id_cabang=id_cabang).filter(status_jurnal= '2').filter(id_unit=300).filter(tgl_trans__range=(start_date,end_date))])
            return ret
        else:
            return sum([p.debet for p in self.tbl_transaksikeu_set.filter(id_cabang=id_cabang).filter(status_jurnal= '2').filter(id_unit=300).filter(tgl_trans=(start_date))])

    def view_saldo_akhir_posting(self,id_cabang, start_date):
        if self.coa[0:2] == str(20) or self.coa[0:2] == str(21) or self.coa[0:2] == str(22) or self.coa[0:2] == str(23) or self.coa[0:2] == str(30) or \
            self.coa[0:2] == str(31) or self.coa[0:2] == str(32) or self.coa[0:2] == str(33) or self.coa[0:2] == str(34) or self.coa[0:2] == str(35) or \
            self.coa[0:2] == str(40) or self.coa[0:2] == str(41) or self.coa[0:2] == str(60) or self.coa[0:2] == str(61):
            return (self.saldo_pjb + (self.my_kredit_posting(id_cabang,start_date)) - self.my_debet_posting(id_cabang,start_date))
        else:
            return (self.saldo_pjb + self.my_debet_posting(id_cabang,start_date)) - (self.my_kredit_posting(id_cabang,start_date))

    def view_saldo_awal_gabungan_posting(self, start_date):
        ret = 0
        if self.header_parent == None:
            for anak in self.children():
                ret += sum([p.saldo for p in anak.tbl_transaksikeu_set.filter(id_unit=300).filter(tgl_trans=(start_date)).\
                    filter(status_jurnal__in=('2','3')).filter(jenis='SALDOKASGERAI')])
                for cucu in anak.children():
                    ret +=  sum([p.saldo for p in cucu.tbl_transaksikeu_set.filter(id_unit=300).\
                       filter(tgl_trans=(start_date)).filter(status_jurnal__in= ('2','3')).filter(jenis='SALDOKASGERAI')])
                    for cicit in cucu.children():
                        ret += sum([p.saldo for p in cicit.tbl_transaksikeu_set.filter(id_unit=300).\
                            filter(tgl_trans=(start_date)).filter(status_jurnal__in= ('2','3')).filter(jenis='SALDOKASGERAI')])
            return ret
        elif self.coa == '11.00.00' or self.coa == '12.00.00' or self.coa == '13.00.00' or self.coa == '21.00.00' or self.coa == '22.00.00' or\
            self.coa == '23.00.00' or self.coa == '31.00.00' or self.coa == '32.00.00' or self.coa == '33.00.00' or self.coa == '34.00.00' or \
            self.coa == '35.00.00' or  self.coa == '41.00.00' or self.coa == '51.00.00'or self.coa == '61.00.00':
            for anak in self.children():
                ret += sum([p.saldo for p in anak.tbl_transaksikeu_set.filter(id_unit=300).filter(tgl_trans=(start_date)).\
                    filter(status_jurnal__in= ('2','3')).filter(jenis='SALDOKASGERAI')])
                for cucu in anak.children():
                    ret += sum([p.saldo for p in cucu.tbl_transaksikeu_set.filter(id_unit=300).filter(tgl_trans=(start_date)).\
                        filter(status_jurnal__in= ('2','3')).filter(jenis='SALDOKASGERAI')])
            return ret
        elif self.coa == '11.01.00' or self.coa == '11.05.00' or self.coa == '11.06.00' or self.coa == '11.07.00' or self.coa == '11.08.00' or\
            self.coa == '11.09.00' or self.coa == '11.10.00' or self.coa == '11.11.00' or self.coa == '11.12.00' or self.coa == '11.13.00' or \
            self.coa == '12.01.00' or self.coa == '12.02.00' or self.coa == '12.03.00' or self.coa == '13.01.00' or self.coa == '13.02.00' or \
            self.coa == '13.03.00' or self.coa == '13.04.00' or self.coa == '13.05.00' or self.coa == '13.06.00' or self.coa == '21.01.00' or \
            self.coa == '21.02.00' or self.coa == '21.03.00' or self.coa == '21.04.00' or self.coa == '21.05.00' or self.coa == '21.06.00' or \
            self.coa == '21.07.00' or self.coa == '21.08.00' or self.coa == '21.09.00' or self.coa == '21.10.00' or self.coa == '22.03.00' or \
            self.coa == '22.04.00' or self.coa == '22.05.00' or self.coa == '22.06.00' or self.coa == '23.01.00' or self.coa == '23.02.00' or \
            self.coa == '41.01.00' or self.coa == '41.02.00' or self.coa == '41.03.00' or self.coa == '51.01.00' or self.coa == '51.02.00' or \
            self.coa == '51.03.00' or self.coa == '51.04.00' or self.coa == '51.05.00' or self.coa == '51.06.00' or self.coa == '51.07.00' or \
            self.coa == '51.08.00' or self.coa == '51.09.00' or self.coa == '51.10.00' or self.coa == '51.11.00' or self.coa == '41.04.00':
            for anak in self.children():
                ret += sum([p.saldo for p in anak.tbl_transaksikeu_set.filter(id_unit=300).filter(tgl_trans=(start_date)).\
                    filter(status_jurnal__in= ('2','3')).filter(jenis='SALDOKASGERAI')])
            return ret
        else:
            return  sum([p.saldo for p in self.tbl_transaksikeu_set.filter(id_unit=300).filter(tgl_trans=(start_date)).\
                    filter(status_jurnal__in= ('2','3')).filter(jenis='SALDOKASGERAI')])
    ## AKHIR NERACA DI REPORT BARU SETELAH POSTING

    def __unicode__(self):
        return "%s-%s" % (self.coa,self.deskripsi)
    
    def tes_coa(self):
        tes = self.coa[-2:]
        return tes
    
    def children(self):
        #return self.tbl_akun_set.filter(view_unit__in=( '0','1','300'))
        return self.tbl_akun_set.all()
    
    def is_child(self):
        #return self.tbl_akun_set.filter(view_unit__in=( '0','1','300')).count()
        return self.tbl_akun_set.all().count() == 0 
    
    def is_akun(self):
        return self.tbl_akun_set.all().count() >= 0
    
    def my_debet_all(self):
        ret = 0
        if self.coa[5:] == '.00':
            for anak in self.children():
                ret += sum([p.debet for p in anak.tbl_transaksi_set.filter(id_unit = 300)])
            return ret
        else:
            return sum([p.debet for p in self.tbl_transaksi_set.filter(id_unit = 300)])
        
    def my_kredit_all(self):
        ret = 0
        if self.coa[5:] == '.00':
            for anak in self.children():
                ret += sum([p.kredit for p in anak.tbl_transaksi_set.filter(id_unit = 300)])
            return ret        
        else:            
            return sum([p.kredit for p in self.tbl_transaksi_set.filter(id_unit = 300)])


    
    def my_debet_month(self, id_cabang, month, year):
        ret = 0
        if self.coa[1:] == '0.00.00':
            for anak in self.children():
                ret += sum([p.debet for p in anak.tbl_transaksi_set.filter(id_cabang=id_cabang).filter(status_jurnal= '2').filter(tgl_trans__month=month).filter(tgl_trans__year=year)])
                for cucu in anak.children():
                    ret += sum([p.debet for p in cucu.tbl_transaksi_set.filter(id_cabang=id_cabang).filter(status_jurnal= '2').filter(tgl_trans__month=month).filter(tgl_trans__year=year)])
                    for cicit in cucu.children():
                        ret += sum([p.debet for p in cicit.tbl_transaksi_set.filter(id_cabang=id_cabang).filter(status_jurnal= '2').filter(tgl_trans__month=month).filter(tgl_trans__year=year)])
            return ret    
        elif self.coa[2:] == '.00.00':
            for anak in self.children():
                ret += sum([p.debet for p in anak.tbl_transaksi_set.filter(id_cabang=id_cabang).filter(status_jurnal= '2').filter(tgl_trans__month=month).filter(tgl_trans__year=year)])
                for cucu in anak.children():
                    ret += sum([p.debet for p in cucu.tbl_transaksi_set.filter(id_cabang=id_cabang).filter(status_jurnal= '2').filter(tgl_trans__month=month).filter(tgl_trans__year=year)])
            return ret
        elif self.coa[5:] == '.00':
            for anak in self.children():
                ret += sum([p.debet for p in anak.tbl_transaksi_set.filter(id_cabang=id_cabang).filter(status_jurnal= '2').filter(tgl_trans__month=month).filter(tgl_trans__year=year)])
            return ret
        else:
            return ret
        
    def my_kredit_month(self, id_cabang, month, year):
        ret = 0
        if self.coa[1:] == '0.00.00':
            for anak in self.children():
                ret += sum([p.kredit for p in anak.tbl_transaksi_set.filter(id_cabang=id_cabang).filter(status_jurnal= '2').filter(tgl_trans__month=month).filter(tgl_trans__year=year)])
                for cucu in anak.children():
                    ret += sum([p.kredit for p in cucu.tbl_transaksi_set.filter(id_cabang=id_cabang).filter(status_jurnal= '2').filter(tgl_trans__month=month).filter(tgl_trans__year=year)])
                    for cicit in cucu.children():
                        ret += sum([p.kredit for p in cicit.tbl_transaksi_set.filter(id_cabang=id_cabang).filter(status_jurnal= '2').filter(tgl_trans__month=month).filter(tgl_trans__year=year)])
            return ret    
        elif self.coa[2:] == '.00.00':
            for anak in self.children():
                ret += sum([p.kredit for p in anak.tbl_transaksi_set.filter(id_cabang=id_cabang).filter(status_jurnal= '2').filter(tgl_trans__month=month).filter(tgl_trans__year=year)])
                for cucu in anak.children():
                    ret += sum([p.kredit for p in cucu.tbl_transaksi_set.filter(id_cabang=id_cabang).filter(status_jurnal= '2').filter(tgl_trans__month=month).filter(tgl_trans__year=year)])
            return ret
        elif self.coa[5:] == '.00':
            for anak in self.children():
                ret += sum([p.kredit for p in anak.tbl_transaksi_set.filter(id_cabang=id_cabang).filter(status_jurnal= '2').filter(tgl_trans__month=month).filter(tgl_trans__year=year)])
            return ret        
        else:            
            return ret

    
    def my_debet(self, id_cabang, start_date, end_date):
        ret = 0
        #if self.coa[1:] == '0.00.00':
        if self.header_parent == None:
            for anak in self.children():
                ret += sum([p.debet for p in anak.tbl_transaksi_set.filter(id_cabang=id_cabang).filter(status_jurnal= '2').filter(id_unit=300).filter(tgl_trans__range=(start_date,end_date))])
                for cucu in anak.children():
                    ret += sum([p.debet for p in cucu.tbl_transaksi_set.filter(id_cabang=id_cabang).filter(status_jurnal= '2').filter(id_unit=300).filter(tgl_trans__range=(start_date,end_date))])
                    for cicit in cucu.children():
                        ret += sum([p.debet for p in cicit.tbl_transaksi_set.filter(id_cabang=id_cabang).filter(status_jurnal= '2').filter(id_unit=300).filter(tgl_trans__range=(start_date,end_date))])
            return ret    
        #elif self.coa[2:] == '.00.00':
        elif self.coa == '11.00.00' or self.coa == '12.00.00' or self.coa == '13.00.00' or self.coa == '21.00.00' or self.coa == '22.00.00' or self.coa == '23.00.00' or\
            self.coa == '31.00.00' or self.coa == '32.00.00' or self.coa == '33.00.00' or self.coa == '34.00.00' or self.coa == '35.00.00' or  self.coa == '41.00.00' or \
            self.coa == '51.00.00'or self.coa == '61.00.00':
            for anak in self.children():
                ret += sum([p.debet for p in anak.tbl_transaksi_set.filter(id_cabang=id_cabang).filter(status_jurnal= '2').filter(id_unit=300).filter(tgl_trans__range=(start_date,end_date))])
                for cucu in anak.children():
                    ret += sum([p.debet for p in cucu.tbl_transaksi_set.filter(id_cabang=id_cabang).filter(id_unit=300).filter(status_jurnal= '2').filter(tgl_trans__range=(start_date,end_date))])
            return ret
        #elif self.coa[5:] == '.00':
        elif self.coa == '11.01.00' or self.coa == '11.05.00' or self.coa == '11.06.00' or self.coa == '11.07.00' or self.coa == '11.08.00' or self.coa == '11.09.00' or \
            self.coa == '11.10.00' or self.coa == '11.11.00' or self.coa == '11.12.00' or self.coa == '11.13.00' or self.coa == '12.01.00' or self.coa == '12.02.00' or \
            self.coa == '12.03.00' or self.coa == '13.01.00' or self.coa == '13.02.00' or self.coa == '13.03.00' or self.coa == '13.04.00' or self.coa == '13.05.00' or \
            self.coa == '13.06.00' or self.coa == '21.01.00' or self.coa == '21.02.00' or self.coa == '21.03.00' or self.coa == '21.04.00' or self.coa == '21.05.00' or\
            self.coa == '21.06.00' or self.coa == '21.07.00' or self.coa == '21.08.00' or self.coa == '21.09.00' or self.coa == '21.10.00' or self.coa == '22.03.00' or \
            self.coa == '22.04.00' or self.coa == '22.05.00' or self.coa == '22.06.00' or self.coa == '23.01.00' or self.coa == '23.02.00' or self.coa == '41.01.00' or \
            self.coa == '41.02.00' or self.coa == '41.03.00' or self.coa == '51.01.00' or self.coa == '51.02.00' or self.coa == '51.03.00' or self.coa == '51.04.00' or \
            self.coa == '51.05.00' or self.coa == '51.06.00' or self.coa == '51.07.00' or self.coa == '51.08.00' or self.coa == '51.09.00' or self.coa == '51.10.00' or \
            self.coa == '51.11.00' or self.coa == '41.04.00':
            for anak in self.children():
                ret += sum([p.debet for p in anak.tbl_transaksi_set.filter(id_cabang=id_cabang).filter(status_jurnal= '2').filter(id_unit=300).filter(tgl_trans__range=(start_date,end_date))])
            return ret
        else:
            return sum([p.debet for p in self.tbl_transaksi_set.filter(id_cabang=id_cabang).filter(status_jurnal= '2').filter(id_unit=300).filter(tgl_trans__range=(start_date,end_date))])

      
    def my_kredit(self, id_cabang, start_date, end_date):
        ret = 0
        #if self.coa[1:] == '0.00.00':
        if self.header_parent == None:
            for anak in self.children():
                ret += sum([p.kredit for p in anak.tbl_transaksi_set.filter(id_cabang=id_cabang).filter(status_jurnal= '2').filter(id_unit=300).filter(tgl_trans__range=(start_date,end_date))])
                for cucu in anak.children():
                    ret += sum([p.kredit for p in cucu.tbl_transaksi_set.filter(id_cabang=id_cabang).filter(status_jurnal= '2').filter(id_unit=300).filter(tgl_trans__range=(start_date,end_date))])
                    for cicit in cucu.children():
                        ret += sum([p.kredit for p in cicit.tbl_transaksi_set.filter(id_cabang=id_cabang).filter(status_jurnal= '2').filter(id_unit=300).filter(tgl_trans__range=(start_date,end_date))])
            return ret    
        #elif self.coa[2:] == '.00.00':
        elif self.coa == '11.00.00' or self.coa == '12.00.00' or self.coa == '13.00.00' or self.coa == '21.00.00' or self.coa == '22.00.00' or self.coa == '23.00.00' or\
            self.coa == '31.00.00' or self.coa == '32.00.00' or self.coa == '33.00.00' or self.coa == '34.00.00' or self.coa == '35.00.00' or  self.coa == '41.00.00' or \
            self.coa == '51.00.00'or self.coa == '61.00.00':
            for anak in self.children():
                ret += sum([p.kredit for p in anak.tbl_transaksi_set.filter(id_cabang=id_cabang).filter(status_jurnal= '2').filter(id_unit=300).filter(tgl_trans__range=(start_date,end_date))])
                for cucu in anak.children():
                    ret += sum([p.kredit for p in cucu.tbl_transaksi_set.filter(id_cabang=id_cabang).filter(status_jurnal= '2').filter(id_unit=300).filter(tgl_trans__range=(start_date,end_date))])
            return ret
        #elif self.coa[5:] == '.00':
        elif self.coa == '11.01.00' or self.coa == '11.05.00' or self.coa == '11.06.00' or self.coa == '11.07.00' or self.coa == '11.08.00' or self.coa == '11.09.00' or \
            self.coa == '11.10.00' or self.coa == '11.11.00' or self.coa == '11.12.00' or self.coa == '11.13.00' or self.coa == '12.01.00' or self.coa == '12.02.00' or \
            self.coa == '12.03.00' or self.coa == '13.01.00' or self.coa == '13.02.00' or self.coa == '13.03.00' or self.coa == '13.04.00' or self.coa == '13.05.00' or \
            self.coa == '13.06.00' or self.coa == '21.01.00' or self.coa == '21.02.00' or self.coa == '21.03.00' or self.coa == '21.04.00' or self.coa == '21.05.00' or\
            self.coa == '21.06.00' or self.coa == '21.07.00' or self.coa == '21.08.00' or self.coa == '21.09.00' or self.coa == '21.10.00' or self.coa == '22.03.00' or \
            self.coa == '22.04.00' or self.coa == '22.05.00' or self.coa == '22.06.00' or self.coa == '23.01.00' or self.coa == '23.02.00' or self.coa == '41.01.00' or \
            self.coa == '41.02.00' or self.coa == '41.03.00' or self.coa == '51.01.00' or self.coa == '51.02.00' or self.coa == '51.03.00' or self.coa == '51.04.00' or \
            self.coa == '51.05.00' or self.coa == '51.06.00' or self.coa == '51.07.00' or self.coa == '51.08.00' or self.coa == '51.09.00' or self.coa == '51.10.00' or \
            self.coa == '51.11.00' or self.coa == '41.04.00':
            for anak in self.children():
                ret += sum([p.kredit for p in anak.tbl_transaksi_set.filter(id_cabang=id_cabang).filter(status_jurnal= '2').filter(id_unit=300).filter(tgl_trans__range=(start_date,end_date))])
            return ret        
        else:            
            return sum([p.kredit for p in self.tbl_transaksi_set.filter(id_cabang=id_cabang).filter(status_jurnal= '2').filter(id_unit=300).filter(tgl_trans__range=(start_date,end_date))])

    def hitung_saldo_akhir_cc(self, id_cabang, start_date, end_date):
        nilai_debet = sum([p.debet for p in self.tbl_transaksi_set.filter(id_cabang=id_cabang).filter(id_unit=300).filter(status_jurnal= '2').filter(tgl_trans__range=(start_date,end_date))])
        nilai_kredit = sum([p.kredit for p in self.tbl_transaksi_set.filter(id_cabang=id_cabang).filter(id_unit=300).filter(status_jurnal= '2').filter(tgl_trans__range=(start_date,end_date))])
        total_nilai = nilai_debet -nilai_kredit 
        return total_nilai

    def hitung_saldo_akhir(self, id_cabang, start_date, end_date):
        ret = 0        
        #if self.coa[1:] == '0.00.00':
        if self.header_parent == None:
            for anak in self.children():
                nilai_debet = sum([p.debet for p in anak.tbl_transaksi_set.filter(id_cabang=id_cabang).filter(id_unit=300).filter(status_jurnal= '2').filter(tgl_trans__range=(start_date,end_date))])
                nilai_kredit = sum([p.kredit for p in anak.tbl_transaksi_set.filter(id_cabang=id_cabang).filter(id_unit=300).filter(status_jurnal= '2').filter(tgl_trans__range=(start_date,end_date))])
                total_nilai = nilai_debet - nilai_kredit
                ret += total_nilai
                for cucu in anak.children():
                    nilai_debet = sum([p.debet for p in anak.tbl_transaksi_set.filter(id_cabang=id_cabang).filter(id_unit=300).filter(status_jurnal= '2').filter(tgl_trans__range=(start_date,end_date))])
                    nilai_kredit = sum([p.kredit for p in anak.tbl_transaksi_set.filter(id_cabang=id_cabang).filter(id_unit=300).filter(status_jurnal= '2').filter(tgl_trans__range=(start_date,end_date))])
                    total_nilai = nilai_debet -nilai_kredit
                    ret += total_nilai
                    for cicit in cucu.children():
                        ret += total_nilai
            return ret    
        elif self.coa[2:] == '.00.00':
            for anak in self.children():
                nilai_debet = sum([p.debet for p in anak.tbl_transaksi_set.filter(id_cabang=id_cabang).filter(id_unit=300).filter(status_jurnal= '2').filter(tgl_trans__range=(start_date,end_date))])
                nilai_kredit = sum([p.kredit for p in anak.tbl_transaksi_set.filter(id_cabang=id_cabang).filter(id_unit=300).filter(status_jurnal= '2').filter(tgl_trans__range=(start_date,end_date))])
                total_nilai = nilai_debet -nilai_kredit
                ret += total_nilai
                for cucu in anak.children():
                    nilai_debet = sum([p.debet for p in anak.tbl_transaksi_set.filter(id_cabang=id_cabang).filter(id_unit=300).filter(status_jurnal= '2').filter(tgl_trans__range=(start_date,end_date))])
                    nilai_kredit = sum([p.kredit for p in anak.tbl_transaksi_set.filter(id_cabang=id_cabang).filter(id_unit=300).filter(status_jurnal= '2').filter(tgl_trans__range=(start_date,end_date))])
                    total_nilai = nilai_debet -nilai_kredit
                    ret += total_nilai
            return ret
        elif self.coa[5:] == '.00':
            for anak in self.children():
                nilai_debet = sum([p.debet for p in anak.tbl_transaksi_set.filter(id_cabang=id_cabang).filter(id_unit=300).filter(status_jurnal= '2').filter(tgl_trans__range=(start_date,end_date))])
                nilai_kredit = sum([p.kredit for p in anak.tbl_transaksi_set.filter(id_cabang=id_cabang).filter(id_unit=300).filter(status_jurnal= '2').filter(tgl_trans__range=(start_date,end_date))])
                total_nilai = nilai_debet -nilai_kredit
                ret += total_nilai
            return ret
        else:
            nilai_debet = sum([p.debet for p in self.tbl_transaksi_set.filter(id_cabang=id_cabang).filter(id_unit=300).filter(status_jurnal= '2').filter(tgl_trans__range=(start_date,end_date))])
            nilai_kredit = sum([p.kredit for p in self.tbl_transaksi_set.filter(id_cabang=id_cabang).filter(id_unit=300).filter(status_jurnal= '2').filter(tgl_trans__range=(start_date,end_date))])
            total_nilai = nilai_debet -nilai_kredit            
            return total_nilai
        
    def hitung_saldo_akhir_bln(self, id_cabang, month, year):
        ret = 0        
        #if self.coa[1:] == '0.00.00':
        if self.header_parent == None:
            for anak in self.children():
                nilai_debet = sum([p.debet for p in anak.tbl_transaksi_set.filter(id_cabang=id_cabang).filter(status_jurnal= '2').filter(tgl_trans__range=(start_date,end_date))])
                nilai_kredit = sum([p.kredit for p in anak.tbl_transaksi_set.filter(id_cabang=id_cabang).filter(status_jurnal= '2').filter(tgl_trans__range=(start_date,end_date))])
                total_nilai = nilai_debet - nilai_kredit
                ret += total_nilai
                for cucu in anak.children():
                    nilai_debet = sum([p.debet for p in anak.tbl_transaksi_set.filter(id_cabang=id_cabang).filter(status_jurnal= '2').filter(tgl_trans__range=(start_date,end_date))])
                    nilai_kredit = sum([p.kredit for p in anak.tbl_transaksi_set.filter(id_cabang=id_cabang).filter(status_jurnal= '2').filter(tgl_trans__range=(start_date,end_date))])
                    total_nilai = nilai_debet -nilai_kredit
                    ret += total_nilai
                    for cicit in cucu.children():
                        ret += total_nilai
            return ret    
        elif self.coa[2:] == '.00.00':
            for anak in self.children():
                nilai_debet = sum([p.debet for p in anak.tbl_transaksi_set.filter(id_cabang=id_cabang).filter(status_jurnal= '2').filter(tgl_trans__range=(start_date,end_date))])
                nilai_kredit = sum([p.kredit for p in anak.tbl_transaksi_set.filter(id_cabang=id_cabang).filter(status_jurnal= '2').filter(tgl_trans__range=(start_date,end_date))])
                total_nilai = nilai_debet -nilai_kredit
                ret += total_nilai
                for cucu in anak.children():
                    nilai_debet = sum([p.debet for p in anak.tbl_transaksi_set.filter(id_cabang=id_cabang).filter(status_jurnal= '2').filter(tgl_trans__range=(start_date,end_date))])
                    nilai_kredit = sum([p.kredit for p in anak.tbl_transaksi_set.filter(id_cabang=id_cabang).filter(status_jurnal= '2').filter(tgl_trans__range=(start_date,end_date))])
                    total_nilai = nilai_debet -nilai_kredit
                    ret += total_nilai
            return ret
        elif self.coa[5:] == '.00':
            for anak in self.children():
                nilai_debet = sum([p.debet for p in anak.tbl_transaksi_set.filter(id_cabang=id_cabang).filter(status_jurnal= '2').filter(tgl_trans__range=(start_date,end_date))])
                nilai_kredit = sum([p.kredit for p in anak.tbl_transaksi_set.filter(id_cabang=id_cabang).filter(status_jurnal= '2').filter(tgl_trans__range=(start_date,end_date))])
                total_nilai = nilai_debet -nilai_kredit
                ret += total_nilai
            return ret
        else:
            nilai_debet = sum([p.debet for p in self.tbl_transaksi_set.filter(id_cabang=id_cabang).filter(status_jurnal= '2').filter(tgl_trans__range=(start_date,end_date))])
            nilai_kredit = sum([p.kredit for p in self.tbl_transaksi_set.filter(id_cabang=id_cabang).filter(status_jurnal= '2').filter(tgl_trans__range=(start_date,end_date))])
            total_nilai = nilai_debet -nilai_kredit            
            return total_nilai

    def total_kredit_nenek(self, id_cabang, start_date, end_date):
        ret = 0
        #if self.coa[1:] == '0.00.00':
        if self.header_parent == None:
            for anak in self.children():
                ret += sum([p.kredit for p in anak.tbl_transaksi_set.filter(id_cabang=id_cabang).filter(tgl_trans__range=(start_date,end_date))])
                for cucu in anak.children():
                    ret += sum([p.kredit for p in cucu.tbl_transaksi_set.filter(id_cabang=id_cabang).filter(tgl_trans__range=(start_date,end_date))])
                    for cicit in cucu.children():
                        ret += sum([p.kredit for p in cicit.tbl_transaksi_set.filter(id_cabang=id_cabang).filter(tgl_trans__range=(start_date,end_date))])
            return ret
        else:            
            return ret
        
    def total_debet_nenek(self, id_cabang, start_date, end_date):
        ret = 0
        #if self.coa[1:] == '0.00.00':
        if self.header_parent == None:
            for anak in self.children():
                ret += sum([p.debet for p in anak.tbl_transaksi_set.filter(id_cabang=id_cabang).filter(id_unit=300).filter(tgl_trans__range=(start_date,end_date))])
                for cucu in anak.children():
                    ret += sum([p.debet for p in cucu.tbl_transaksi_set.filter(id_cabang=id_cabang).filter(id_unit=300).filter(tgl_trans__range=(start_date,end_date))])
                    for cicit in cucu.children():
                        ret += sum([p.debet for p in cicit.tbl_transaksi_set.filter(id_cabang=id_cabang).filter(id_unit=300).filter(tgl_trans__range=(start_date,end_date))])
            return ret    
        else:            
            return ret
        
    def selisih_kredit_nenek(self, id_cabang, start_date, end_date):
        ret = 0
        #if self.coa[1:] == '0.00.00':
        if self.header_parent == None:
            for anak in self.children():
                ret += sum([p.kredit for p in anak.tbl_transaksi_set.filter(id_cabang=id_cabang).filter(status_jurnal= '1').filter(tgl_trans__range=(start_date,end_date))])
                for cucu in anak.children():
                    ret += sum([p.kredit for p in cucu.tbl_transaksi_set.filter(id_cabang=id_cabang).filter(status_jurnal= '1').filter(tgl_trans__range=(start_date,end_date))])
                    for cicit in cucu.children():
                        ret += sum([p.kredit for p in cicit.tbl_transaksi_set.filter(id_cabang=id_cabang).filter(status_jurnal= '1').filter(tgl_trans__range=(start_date,end_date))])
            return ret
        else:            
            return ret
    ######LABA RUGI GABUNGAN 21-07-2016
    def kredit_shu_nonpos_lr_gabungan(self, id_cabang, start_date,end_date):##### SHU KREDIT NONPOS
        ret = 0
        #if self.coa[1:] == '0.00.00':
        if self.header_parent == None:
            for anak in self.children():
                ret += sum([p.kredit for p in anak.tbl_transaksi_set.filter(status_jurnal= '2').filter(id_unit=300).filter(tgl_trans__range=(start_date,end_date))])
                for cucu in anak.children():
                    ret += sum([p.kredit for p in cucu.tbl_transaksi_set.filter(status_jurnal= '2').filter(id_unit=300).filter(tgl_trans__range=(start_date,end_date))])
                    for cicit in cucu.children():
                        ret += sum([p.kredit for p in cicit.tbl_transaksi_set.filter(status_jurnal= '2').filter(id_unit=300).filter(tgl_trans__range=(start_date,end_date))])
            return ret    
        #elif self.coa[2:] == '.00.00':
        elif self.coa == '41.00.00' or self.coa == '51.00.00'or self.coa == '61.00.00':
            for anak in self.children():
                ret += sum([p.kredit for p in anak.tbl_transaksi_set.filter(status_jurnal= '2').filter(id_unit=300).filter(tgl_trans__range=(start_date,end_date))])
                for cucu in anak.children():
                    ret += sum([p.kredit for p in cucu.tbl_transaksi_set.filter(status_jurnal= '2').filter(id_unit=300).filter(tgl_trans__range=(start_date,end_date))])
            return ret
        #elif self.coa[5:] == '.00':
        elif self.coa == '41.01.00' or self.coa == '41.02.00' or self.coa == '41.03.00' or self.coa == '51.01.00' or self.coa == '51.02.00' or self.coa == '51.03.00' or self.coa == '51.04.00' or \
            self.coa == '51.05.00' or self.coa == '51.06.00' or self.coa == '51.07.00' or self.coa == '51.08.00' or self.coa == '51.09.00' or self.coa == '51.10.00' or \
            self.coa == '51.11.00' or self.coa == '41.04.00':
            for anak in self.children():
                ret += sum([p.kredit for p in anak.tbl_transaksi_set.filter(status_jurnal= '2').filter(id_unit=300).filter(tgl_trans__range=(start_date,end_date))])
            return ret        
        else:            
            return sum([p.kredit for p in self.tbl_transaksi_set.filter(status_jurnal= '2').filter(id_unit=300).filter(tgl_trans__range=(start_date,end_date))])


    def debet_shu_nonpos_lr_gabungan(self, id_cabang, start_date,end_date):
        ret = 0
        #if self.coa[1:] == '0.00.00':
        if self.header_parent == None:
            for anak in self.children():
                ret += sum([p.debet for p in anak.tbl_transaksi_set.filter(status_jurnal= '2').filter(id_unit=300).filter(tgl_trans__range=(start_date,end_date))])
                for cucu in anak.children():
                    ret += sum([p.debet for p in cucu.tbl_transaksi_set.filter(status_jurnal= '2').filter(id_unit=300).filter(tgl_trans__range=(start_date,end_date))])
                    for cicit in cucu.children():
                        ret += sum([p.debet for p in cicit.tbl_transaksi_set.filter(status_jurnal= '2').filter(id_unit=300).filter(tgl_trans__range=(start_date,end_date))])
            return ret    
        #elif self.coa[2:] == '.00.00':
        elif self.coa == '41.00.00' or self.coa == '51.00.00'or self.coa == '61.00.00':
            for anak in self.children():
                ret += sum([p.debet for p in anak.tbl_transaksi_set.filter(status_jurnal= '2').filter(id_unit=300).filter(tgl_trans__range=(start_date,end_date))])
                for cucu in anak.children():
                    ret += sum([p.debet for p in cucu.tbl_transaksi_set.filter(id_unit=300).filter(status_jurnal= '2').filter(tgl_trans__range=(start_date,end_date))])
            return ret
        #elif self.coa[5:] == '.00':
        elif self.coa == '41.01.00' or self.coa == '41.02.00' or self.coa == '41.03.00' or self.coa == '51.01.00' or self.coa == '51.02.00' or self.coa == '51.03.00' or \
            self.coa == '51.04.00' or self.coa == '51.05.00' or self.coa == '51.06.00' or self.coa == '51.07.00' or self.coa == '51.08.00' or \
            self.coa == '51.09.00' or self.coa == '51.10.00' or self.coa == '51.11.00' or self.coa == '41.04.00':
            for anak in self.children():
                ret += sum([p.debet for p in anak.tbl_transaksi_set.filter(status_jurnal= '2').filter(id_unit=300).filter(tgl_trans__range=(start_date,end_date))])
            return ret
        else:
            return sum([p.debet for p in self.tbl_transaksi_set.filter(status_jurnal= '2').filter(id_unit=300).filter(tgl_trans__range=(start_date,end_date))])

    def saldo_awal_nonposting_shu_lr_gabungan(self,id_cabang, start_date):#####SHU SALDO AWAL NONPOSTING
        ret = 0
        if self.header_parent == None:
            for anak in self.children():
                ret += sum([p.saldo for p in anak.tbl_transaksikeu_set.filter(id_unit=300).filter(tgl_trans=(start_date)).\
                    filter(status_jurnal__in= ('2','3')).filter(jenis__in=('SALDOKASGERAI','SALDOBANKGERAI'))])
                for cucu in anak.children():
                    ret +=  sum([p.saldo for p in cucu.tbl_transaksikeu_set.filter(id_unit=300).filter(tgl_trans=(start_date)).\
                        filter(status_jurnal__in= ('2','3')).filter(jenis__in=('SALDOKASGERAI','SALDOBANKGERAI'))])
                    for cicit in cucu.children():
                        ret += sum([p.saldo for p in cicit.tbl_transaksikeu_set.filter(id_unit=300).filter(tgl_trans=(start_date)).\
                            filter(status_jurnal__in= ('2','3')).filter(jenis__in=('SALDOKASGERAI','SALDOBANKGERAI'))])
            return ret
        elif self.coa == '41.00.00' or self.coa == '51.00.00'or self.coa == '61.00.00':
            for anak in self.children():
                ret += sum([p.saldo for p in anak.tbl_transaksikeu_set.filter(id_unit=300).filter(tgl_trans=(start_date)).\
                    filter(status_jurnal__in= ('2','3')).filter(jenis__in=('SALDOKASGERAI','SALDOBANKGERAI'))])
                for cucu in anak.children():
                    ret += sum([p.saldo for p in cucu.tbl_transaksikeu_set.filter(id_unit=300).filter(tgl_trans=(start_date)).\
                        filter(status_jurnal__in= ('2','3')).filter(jenis__in=('SALDOKASGERAI','SALDOBANKGERAI'))])
            return ret
        elif self.coa == '41.01.00' or self.coa == '41.02.00' or self.coa == '41.03.00' or self.coa == '51.01.00' or self.coa == '51.02.00' or \
            self.coa == '51.03.00' or self.coa == '51.04.00' or self.coa == '51.05.00' or self.coa == '51.06.00' or self.coa == '51.07.00' or \
            self.coa == '51.08.00' or self.coa == '51.09.00' or self.coa == '51.10.00' or self.coa == '51.11.00' or self.coa == '41.04.00':
            for anak in self.children():
                ret += sum([p.saldo for p in anak.tbl_transaksikeu_set.filter(id_unit=300).filter(tgl_trans=(start_date)).\
                    filter(status_jurnal__in= ('2','3')).filter(jenis__in=('SALDOKASGERAI','SALDOBANKGERAI'))])
            return ret
        else:
            return  sum([p.saldo for p in self.tbl_transaksikeu_set.filter(id_unit=300).filter(tgl_trans=(start_date)).\
                filter(status_jurnal__in= ('2','3')).filter(jenis__in=('SALDOKASGERAI','SALDOBANKGERAI'))])
    ######AKHIR LABA RUGI GABUNGAN 21-07-2016

    ### UNTUK ALL  TOTAL Di LABA RUGI
    def pendapatan_total_debet_laba_rugi(self, id_cabang, start_date):
        ret = 0
        #if self.coa[1:] == '0.00.00':
        if self.coa == '40.00.00':
            for anak in self.children():
                ret += sum([p.debet for p in anak.tbl_transaksi_set.filter(id_cabang=id_cabang).filter(status_jurnal= '3').filter(tgl_trans=(start_date))])
                for cucu in anak.children():
                    ret += sum([p.debet for p in cucu.tbl_transaksi_set.filter(id_cabang=id_cabang).filter(status_jurnal= '3').filter(tgl_trans=(start_date))])
                    for cicit in cucu.children():
                        ret += sum([p.debet for p in cicit.tbl_transaksi_set.filter(id_cabang=id_cabang).filter(status_jurnal= '3').filter(tgl_trans=(start_date))])
            return ret    
        else:
            return  sum([p.saldo for p in self.tbl_transaksi_set.filter(id_cabang=id_cabang).filter(status_jurnal= '3').filter(tgl_trans=(start_date))])

    def beban_total_debet_laba_rugi(self, id_cabang, start_date):
        ret = 0
        #if self.coa[1:] == '0.00.00':
        if self.coa == '50.00.00':
            for anak in self.children():
                ret += sum([p.debet for p in anak.tbl_transaksi_set.filter(id_cabang=id_cabang).filter(status_jurnal= '3').filter(tgl_trans=(start_date))])
                for cucu in anak.children(): 
                    ret += sum([p.debet for p in cucu.tbl_transaksi_set.filter(id_cabang=id_cabang).filter(status_jurnal= '3').filter(tgl_trans=(start_date))])
                    for cicit in cucu.children():
                        ret += sum([p.debet for p in cicit.tbl_transaksi_set.filter(id_cabang=id_cabang).filter(status_jurnal= '3').filter(tgl_trans=(start_date))])
            return ret    
        else:            
            return ret

    def pendapatan_total_kredit_laba_rugi(self, id_cabang, start_date):
        ret = 0
        #if self.coa[1:] == '0.00.00':
        if self.coa == '40.00.00':
            for anak in self.children():
                ret += sum([p.kredit for p in anak.tbl_transaksi_set.filter(id_cabang=id_cabang).filter(status_jurnal= '3').filter(tgl_trans=(start_date))])
                for cucu in anak.children():
                    ret += sum([p.kredit for p in cucu.tbl_transaksi_set.filter(id_cabang=id_cabang).filter(status_jurnal= '3').filter(tgl_trans=(start_date))])
                    for cicit in cucu.children():
                        ret += sum([p.kredit for p in cicit.tbl_transaksi_set.filter(id_cabang=id_cabang).filter(status_jurnal= '3').filter(tgl_trans=(start_date))])
            return ret
        else:
            return ret


    def beban_total_kredit_laba_rugi(self, id_cabang, start_date):
        ret = 0
        #if self.coa[1:] == '0.00.00':
        if self.coa == '50.00.00':
            for anak in self.children():
                ret += sum([p.kredit for p in anak.tbl_transaksi_set.filter(id_cabang=id_cabang).filter(status_jurnal= '3').filter(tgl_trans=(start_date))])
                for cucu in anak.children():
                    ret += sum([p.kredit for p in cucu.tbl_transaksi_set.filter(id_cabang=id_cabang).filter(status_jurnal= '3').filter(tgl_trans=(start_date))])
                    for cicit in cucu.children():
                        ret += sum([p.kredit for p in cicit.tbl_transaksi_set.filter(id_cabang=id_cabang).filter(status_jurnal= '3').filter(tgl_trans=(start_date))])
            return ret
        else:
            return ret
    ## Akhir all Total Laba Rugi
    #def view_saldo_akhir(self,id_cabang, start_date, end_date):
        #return (self.saldo_pjb + self.my_debet(id_cabang,start_date,end_date)) - (self.my_kredit(id_cabang,start_date,end_date)) 

    def view_saldo_akhir(self,id_cabang, start_date, end_date):
        if self.coa[0:2] == str(20) or self.coa[0:2] == str(21) or self.coa[0:2] == str(22) or self.coa[0:2] == str(23) or self.coa[0:2] == str(30) or \
            self.coa[0:2] == str(31) or self.coa[0:2] == str(32) or self.coa[0:2] == str(33) or self.coa[0:2] == str(34) or self.coa[0:2] == str(35) or \
            self.coa[0:2] == str(40) or self.coa[0:2] == str(41) or self.coa[0:2] == str(60) or self.coa[0:2] == str(61):
            return (self.saldo_pjb + (self.my_kredit(id_cabang,start_date,end_date)) - self.my_debet(id_cabang,start_date,end_date))
        else:
            return (self.saldo_pjb + self.my_debet(id_cabang,start_date,end_date)) - (self.my_kredit(id_cabang,start_date,end_date))
   
    def get_jumlah_debet(self):        
        pk = self.tbl_transaksi_set.all()
        return sum([ a.debet for a in pk ])
    
    def get_jumlah_kredit(self):
        pk = self.tbl_transaksi_set.all() 
        return sum([ a.kredit for a in pk ])
    
    
    def kpl_coa(self):
        for p in self.tbl_transaksi_set.all():
            try:
                pn = p.id_unit 
            except:
                pass
            return pn
        
    def debet_satu(self):
        for p in self.tbl_transaksi_set.all():
            try:
                pn = p.debet
            except:
                pass
            return pn
        
    def kredit_dua(self):
        for p in self.tbl_transaksi_set.all():
            try:
                pn = p.kredit
            except:
                pass
            return pn


    #####SHU KREDIT DEBET SALDO  UNTUK LAPORAN SHU POSTING,GABUNGAN,NON
    def kredit_shu_nonpos_cabang(self, id_cabang, start_date,end_date):##### SHU KREDIT NONPOS
        ret = 0
        #if self.coa[1:] == '0.00.00':
        if self.header_parent == None:
            for anak in self.children():
                ret += sum([p.kredit for p in anak.tbl_transaksi_set.filter(id_cabang=id_cabang).filter(status_jurnal= '2').filter(id_unit=300).filter(tgl_trans__range=(start_date,end_date))])
                for cucu in anak.children():
                    ret += sum([p.kredit for p in cucu.tbl_transaksi_set.filter(id_cabang=id_cabang).filter(status_jurnal= '2').filter(id_unit=300).filter(tgl_trans__range=(start_date,end_date))])
                    for cicit in cucu.children():
                        ret += sum([p.kredit for p in cicit.tbl_transaksi_set.filter(id_cabang=id_cabang).filter(status_jurnal= '2').filter(id_unit=300).filter(tgl_trans__range=(start_date,end_date))])
            return ret    
        #elif self.coa[2:] == '.00.00':
        elif self.coa == '41.00.00' or self.coa == '51.00.00'or self.coa == '61.00.00':
            for anak in self.children():
                ret += sum([p.kredit for p in anak.tbl_transaksi_set.filter(id_cabang=id_cabang).filter(status_jurnal= '2').filter(id_unit=300).filter(tgl_trans__range=(start_date,end_date))])
                for cucu in anak.children():
                    ret += sum([p.kredit for p in cucu.tbl_transaksi_set.filter(id_cabang=id_cabang).filter(status_jurnal= '2').filter(id_unit=300).filter(tgl_trans__range=(start_date,end_date))])
            return ret
        #elif self.coa[5:] == '.00':
        elif self.coa == '41.01.00' or self.coa == '41.02.00' or self.coa == '41.03.00' or self.coa == '51.01.00' or self.coa == '51.02.00' or self.coa == '51.03.00' or self.coa == '51.04.00' or \
            self.coa == '51.05.00' or self.coa == '51.06.00' or self.coa == '51.07.00' or self.coa == '51.08.00' or self.coa == '51.09.00' or self.coa == '51.10.00' or \
            self.coa == '51.11.00' or self.coa == '41.04.00':
            for anak in self.children():
                ret += sum([p.kredit for p in anak.tbl_transaksi_set.filter(id_cabang=id_cabang).filter(status_jurnal= '2').filter(id_unit=300).filter(tgl_trans__range=(start_date,end_date))])
            return ret        
        else:            
            return sum([p.kredit for p in self.tbl_transaksi_set.filter(id_cabang=id_cabang).filter(status_jurnal= '2').filter(id_unit=300).filter(tgl_trans__range=(start_date,end_date))])

    def debet_shu_nonpos_cabang(self, id_cabang, start_date,end_date):
        ret = 0
        #if self.coa[1:] == '0.00.00':
        if self.header_parent == None:
            for anak in self.children():
                ret += sum([p.debet for p in anak.tbl_transaksi_set.filter(id_cabang=id_cabang).filter(status_jurnal= '2').filter(id_unit=300).filter(tgl_trans__range=(start_date,end_date))])
                for cucu in anak.children():
                    ret += sum([p.debet for p in cucu.tbl_transaksi_set.filter(id_cabang=id_cabang).filter(status_jurnal= '2').filter(id_unit=300).filter(tgl_trans__range=(start_date,end_date))])
                    for cicit in cucu.children():
                        ret += sum([p.debet for p in cicit.tbl_transaksi_set.filter(id_cabang=id_cabang).filter(status_jurnal= '2').filter(id_unit=300).filter(tgl_trans__range=(start_date,end_date))])
            return ret    
        #elif self.coa[2:] == '.00.00':
        elif self.coa == '41.00.00' or self.coa == '51.00.00'or self.coa == '61.00.00':
            for anak in self.children():
                ret += sum([p.debet for p in anak.tbl_transaksi_set.filter(id_cabang=id_cabang).filter(status_jurnal= '2').filter(id_unit=300).filter(tgl_trans__range=(start_date,end_date))])
                for cucu in anak.children():
                    ret += sum([p.debet for p in cucu.tbl_transaksi_set.filter(id_cabang=id_cabang).filter(id_unit=300).filter(status_jurnal= '2').filter(tgl_trans__range=(start_date,end_date))])
            return ret
        #elif self.coa[5:] == '.00':
        elif self.coa == '41.01.00' or self.coa == '41.02.00' or self.coa == '41.03.00' or self.coa == '51.01.00' or self.coa == '51.02.00' or self.coa == '51.03.00' or \
            self.coa == '51.04.00' or self.coa == '51.05.00' or self.coa == '51.06.00' or self.coa == '51.07.00' or self.coa == '51.08.00' or \
            self.coa == '51.09.00' or self.coa == '51.10.00' or self.coa == '51.11.00' or self.coa == '41.04.00':
            for anak in self.children():
                ret += sum([p.debet for p in anak.tbl_transaksi_set.filter(id_cabang=id_cabang).filter(status_jurnal= '2').filter(id_unit=300).filter(tgl_trans__range=(start_date,end_date))])
            return ret
        else:
            return sum([p.debet for p in self.tbl_transaksi_set.filter(id_cabang=id_cabang).filter(status_jurnal= '2').filter(id_unit=300).filter(tgl_trans__range=(start_date,end_date))])

    def kredit_shu_pos_gb(self, start_date, end_date):#####KREDIT GABUNG NONPOS
        ret = 0
        #if self.coa[1:] == '0.00.00':
        if self.header_parent == None:
            for anak in self.children():
                ret += sum([p.kredit for p in anak.tbl_transaksi_set.filter(status_jurnal= '2').filter(id_unit=300).filter(tgl_trans__range=(start_date, end_date))])
                for cucu in anak.children():
                    ret += sum([p.kredit for p in cucu.tbl_transaksi_set.filter(status_jurnal= '2').filter(id_unit=300).filter(tgl_trans__range=(start_date, end_date))])
                    for cicit in cucu.children():
                        ret += sum([p.kredit for p in cicit.tbl_transaksi_set.filter(status_jurnal= '2').filter(id_unit=300).filter(tgl_trans__range=(start_date, end_date))])
            return ret    
        #elif self.coa[2:] == '.00.00':
        elif self.coa == '41.00.00' or self.coa == '51.00.00'or self.coa == '61.00.00':
            for anak in self.children():
                ret += sum([p.kredit for p in anak.tbl_transaksi_set.filter(status_jurnal= '2').filter(id_unit=300).filter(tgl_trans__range=(start_date, end_date))])
                for cucu in anak.children():
                    ret += sum([p.kredit for p in cucu.tbl_transaksi_set.filter(status_jurnal= '2').filter(id_unit=300).filter(tgl_trans__range=(start_date, end_date))])
            return ret
        #elif self.coa[5:] == '.00':
        elif self.coa == '41.01.00' or self.coa == '41.02.00' or self.coa == '41.03.00' or self.coa == '51.01.00' or self.coa == '51.02.00' or self.coa == '51.03.00' or self.coa == '51.04.00' or \
            self.coa == '51.05.00' or self.coa == '51.06.00' or self.coa == '51.07.00' or self.coa == '51.08.00' or self.coa == '51.09.00' or self.coa == '51.10.00' or \
            self.coa == '51.11.00' or self.coa == '41.04.00':
            for anak in self.children():
                ret += sum([p.kredit for p in anak.tbl_transaksi_set.filter(status_jurnal= '2').filter(id_unit=300).filter(tgl_trans__range=(start_date, end_date))])
            return ret        
        else:            
            return sum([p.kredit for p in self.tbl_transaksi_set.filter(status_jurnal= '2').filter(id_unit=300).filter(tgl_trans__range=(start_date, end_date))])

    def debet_shu_pos_gb(self,start_date, end_date):####debet GABUNG
        ret = 0
        #if self.coa[1:] == '0.00.00':
        if self.header_parent == None:
            for anak in self.children():
                ret += sum([p.debet for p in anak.tbl_transaksi_set.filter(status_jurnal= '2').filter(id_unit=300).filter(tgl_trans__range=(start_date, end_date))])
                for cucu in anak.children():
                    ret += sum([p.debet for p in cucu.tbl_transaksi_set.filter(status_jurnal= '2').filter(id_unit=300).filter(tgl_trans__range=(start_date, end_date))])
                    for cicit in cucu.children():
                        ret += sum([p.debet for p in cicit.tbl_transaksi_set.filter(status_jurnal= '2').filter(id_unit=300).filter(tgl_trans__range=(start_date, end_date))])
            return ret    
        #elif self.coa[2:] == '.00.00':
        elif self.coa == '41.00.00' or self.coa == '51.00.00'or self.coa == '61.00.00':
            for anak in self.children():
                ret += sum([p.debet for p in anak.tbl_transaksi_set.filter(status_jurnal= '2').filter(id_unit=300).filter(tgl_trans__range=(start_date, end_date))])
                for cucu in anak.children():
                    ret += sum([p.debet for p in cucu.tbl_transaksi_set.filter(id_unit=300).filter(status_jurnal= '2').filter(tgl_trans__range=(start_date, end_date))])
            return ret
        #elif self.coa[5:] == '.00':
        elif self.coa == '41.01.00' or self.coa == '41.02.00' or self.coa == '41.03.00' or self.coa == '51.01.00' or self.coa == '51.02.00' or self.coa == '51.03.00' or \
            self.coa == '51.04.00' or self.coa == '51.05.00' or self.coa == '51.06.00' or self.coa == '51.07.00' or self.coa == '51.08.00' or \
            self.coa == '51.09.00' or self.coa == '51.10.00' or self.coa == '51.11.00' or self.coa == '41.04.00':
            for anak in self.children():
                ret += sum([p.debet for p in anak.tbl_transaksi_set.filter(status_jurnal= '2').filter(id_unit=300).filter(tgl_trans__range=(start_date, end_date))])
            return ret
        else:
            return sum([p.debet for p in self.tbl_transaksi_set.filter(status_jurnal= '2').filter(id_unit=300).filter(tgl_trans__range=(start_date, end_date))])

    def saldo_awal_nonposting_shu(self,id_cabang, start_date):#####SHU SALDO AWAL NONPOSTING
        ret = 0
        if self.header_parent == None:
            for anak in self.children():
                ret += sum([p.saldo for p in anak.tbl_transaksikeu_set.filter(id_unit=300).filter(tgl_trans=(start_date)).\
                    filter(jurnal__kode_cabang = id_cabang).filter(status_jurnal__in= ('2','3')).filter(jenis__in=('SALDOKASGERAI','SALDOBANKGERAI'))])
                for cucu in anak.children():
                    ret +=  sum([p.saldo for p in cucu.tbl_transaksikeu_set.filter(id_unit=300).filter(jurnal__kode_cabang = id_cabang).\
                       filter(tgl_trans=(start_date)).filter(status_jurnal__in= ('2','3')).filter(jenis__in=('SALDOKASGERAI','SALDOBANKGERAI'))])
                    for cicit in cucu.children():
                        ret += sum([p.saldo for p in cicit.tbl_transaksikeu_set.filter(id_unit=300).filter(jurnal__kode_cabang = id_cabang).\
                            filter(tgl_trans=(start_date)).filter(status_jurnal__in= ('2','3')).filter(jenis__in=('SALDOKASGERAI','SALDOBANKGERAI'))])
            return ret
        elif self.coa == '41.00.00' or self.coa == '51.00.00'or self.coa == '61.00.00':
            for anak in self.children():
                ret += sum([p.saldo for p in anak.tbl_transaksikeu_set.filter(id_unit=300).filter(tgl_trans=(start_date)).\
                    filter(jurnal__kode_cabang = id_cabang).filter(status_jurnal__in= ('2','3')).filter(jenis__in=('SALDOKASGERAI','SALDOBANKGERAI'))])
                for cucu in anak.children():
                    ret += sum([p.saldo for p in cucu.tbl_transaksikeu_set.filter(id_unit=300).filter(tgl_trans=(start_date)).\
                        filter(jurnal__kode_cabang = id_cabang).filter(status_jurnal__in= ('2','3')).filter(jenis__in=('SALDOKASGERAI','SALDOBANKGERAI'))])
            return ret
        elif self.coa == '41.01.00' or self.coa == '41.02.00' or self.coa == '41.03.00' or self.coa == '51.01.00' or self.coa == '51.02.00' or \
            self.coa == '51.03.00' or self.coa == '51.04.00' or self.coa == '51.05.00' or self.coa == '51.06.00' or self.coa == '51.07.00' or \
            self.coa == '51.08.00' or self.coa == '51.09.00' or self.coa == '51.10.00' or self.coa == '51.11.00' or self.coa == '41.04.00':
            for anak in self.children():
                ret += sum([p.saldo for p in anak.tbl_transaksikeu_set.filter(id_unit=300).filter(tgl_trans=(start_date)).\
                    filter(jurnal__kode_cabang = id_cabang).filter(status_jurnal__in= ('2','3')).filter(jenis__in=('SALDOKASGERAI','SALDOBANKGERAI'))])
            return ret
        else:
            return  sum([p.saldo for p in self.tbl_transaksikeu_set.filter(id_unit=300).filter(tgl_trans=(start_date)).\
                filter(status_jurnal__in= ('2','3')).filter(jurnal__kode_cabang=id_cabang).filter(jenis__in=('SALDOKASGERAI','SALDOBANKGERAI'))])

    

    ###### KREDIT UNTUK LAPORAN SHU POSTING,GABUNGAN,NON
JENIS_JURNAL = (
   ('1','GL-GL'),
   ('2','SALDO AWAL'),
   ('3','SALDO YANG DI KIRIM'),
)

J_STATUS = (
    ('0','NON BANK'),
    ('1','BANK'),
    ('2','J.Pendapatan'),
)

class Jurnal_History(models.Model):
    def number():
        kode = 100000000
        no = Jurnal_History.objects.all().count()
        if no == None:
            return 1
        else:
            return no + 1 + kode
        
    diskripsi = models.CharField(max_length=200, blank=True, null=True)
    no_akad = models.IntegerField(default=number,blank=True, null=True)
    tgl_trans = models.DateField(blank=True, null=True)
    j_status = models.CharField(max_length=1, choices=J_STATUS,default= 0)
    object_id = models.IntegerField(max_length=11,blank =True,null=True)
    kode_cabang = models.CharField(max_length=5,blank=True,null=True)
    cdate = models.DateTimeField(auto_now_add=True)
    mdate = models.DateTimeField(auto_now=True)
    cu = models.ForeignKey(User, related_name='+', null=True)
    mu = models.ForeignKey(User, related_name='+', null=True)
    
    def __unicode__(self):
        return '%s' % (self.id)
    
    class Meta:
        db_table = "jurnal_history"
        
    def nobukti_sama(self):
        sama = Jurnal.objects.values('nobukti').order_by()
        return sama
    
    def coa_rak_pusat(self):
        coa = 0
        for p in self.ordered_items.filter(kredit = 0).filter(tgl_trans= datetime.date.today()):
            try:
                coa = p.id_coa
            except:
                pass
        return coa
    coa_rak_pusat = property(coa_rak_pusat)
            
class Tbl_Transaksi_History(models.Model):
    deskripsi = models.CharField(max_length=500, blank=True, null=True)
    id_coa = models.ForeignKey(Tbl_Akun,null =True,blank=True,related_name='orders')
    jurnal_h = models.ForeignKey(Jurnal_History, related_name='ordered_items')
    no_trans = models.IntegerField(max_length=6, null=True, blank=True)
    jenis = models.CharField(max_length=500)
    debet = models.IntegerField(max_length=11)
    kredit = models.IntegerField(max_length=11)
    id_cabang = models.IntegerField(max_length=3)
    id_cabang_tuju = models.IntegerField(max_length=3,blank=True,null=True)
    id_unit = models.IntegerField(max_length=3)
    id_product  = models.IntegerField(max_length=1)
    status_jurnal = models.IntegerField(max_length=1)
    user = models.ForeignKey(User, related_name='c_tbl_transaksi_h', editable=False, null=True, blank=True)
    tgl_trans = models.DateField()
    status_posting = models.IntegerField(max_length=1,blank=True,null=True)
    
    
    class Meta:
        db_table = "tbl_transaksi_history"        

    def get_absolute_url(self):
        return "/jurnal/add_baru_h/" 

    
        
class Jurnal(models.Model):
    def number():
        kode = 1000000
        no = Jurnal.objects.all().count()
        if no == None:
            return 1
        else:
            return no + 1 + kode
    nobukti= models.CharField(max_length=350,blank=True, null=True)
    no_akad = models.IntegerField(default=number,blank=True, null=True) 
    object_id = models.IntegerField(max_length=11,blank =True,null=True)        
    diskripsi = models.CharField(max_length=200, blank=True, null=True)
    kode_cabang = models.CharField(max_length=5,blank=True,null=True)
    tgl_trans = models.DateField()
    cdate = models.DateTimeField(auto_now_add=True)
    mdate = models.DateTimeField(auto_now=True)
    cu = models.ForeignKey(User, related_name='jurnal_creator', null=True)
    mu = models.ForeignKey(User, related_name='jurnal_modifier', null=True)

    def __unicode__(self):
        return '%s' % (self.id)
    
    class Meta:
        db_table = "jurnal"

    def saldo_sekarang(self):#### DIPAKE DI REPORT POSISIKAS,POSTING TANGGAL
        sekarang = datetime.date.today()
        total = 0
        for k in self.tbl_transaksi_set.filter(tgl_trans= sekarang).filter(status_jurnal = 2).filter(id_coa__coa__contains= '11.01').\
            filter(debet=0).filter(kredit=0):
            if k.saldo == None:
                return total
            else:
                total += k.saldo
        return total
    saldo_sekarang = property(saldo_sekarang)

    def saldo_awalhari(self):
        total = 0
        for k in self.tbl_transaksi_set.filter(jenis = 'SALDOAWALGERAI'):
            if k.saldo == None:
                return total
            else:
                total += k.saldo
        return total
    saldo_awalhari = property(saldo_awalhari)

    def tot_trans_jurnal(self):
        sekarang = datetime.date.today()
        return self.tbl_transaksi_set.filter(tgl_trans=sekarang).filter(status_jurnal=2).count()
    tot_trans_jurnal = property(tot_trans_jurnal)

    def status_posting(self):
        sekarang = datetime.date.today()
        return self.tbl_transaksi_set.filter(tgl_trans=sekarang).filter(status_posting__isnull=False).count()        
    status_posting = property(status_posting)

    def postingon(self):
        sekarang = datetime.date.today()
        return self.tbl_transaksi_set.filter(tgl_trans=sekarang).filter(posting=1).count()        
    postingon = property(postingon)

    def postingoff(self):
        sekarang = datetime.date.today()
        return self.tbl_transaksi_set.filter(tgl_trans=sekarang).filter(posting=2).count()        
    postingoff = property(postingoff)           

    def postingonoff(self):
        sekarang = datetime.date.today()
        return self.tbl_transaksi_set.filter(tgl_trans=sekarang).filter(posting__isnull=True).count()        
    postingonoff = property(postingonoff)  

    ####PENDAPATAN
    def pendapatan_kredit_filter(self):####PENdapatan POSISI KREDIT KREDIT
        sekarang = datetime.date.today()
        jenispcr = dict([[k, 0] for k,v in JENIS_PENDAPATAN_KREDIT_FILTER])
        kb = self.tbl_transaksi_set.filter(tgl_trans = sekarang).filter(jenis__in=jenispcr).filter(status_jurnal=2).filter(id_coa__in= (448L,287L))
        return sum([p.kredit for p in kb]) 
    pendapatan_kredit_filter = property(pendapatan_kredit_filter)
    
    def pendapatan_kredit(self):####PEndapatan POSISI KREDIT
        sekarang = datetime.date.today()
        jenispcr = dict([[k, 0] for k,v in JENIS_PENDAPATAN_KREDIT])
        kb = self.tbl_transaksi_set.filter(tgl_trans = sekarang).filter(jenis__in=jenispcr).filter(status_jurnal=2)
        return sum([p.kredit for p in kb]) 
    pendapatan_kredit = property(pendapatan_kredit)
    ####PENDAPATAN
    
    ####PENGELUARAN
    def pengeluaran_debet(self):####PENGELUARAN POSISI DEBET
        sekarang = datetime.date.today()
        jenispcr = dict([[k, 0] for k,v in JENIS_PENGELUARAN_DEBET])
        kb = self.tbl_transaksi_set.filter(tgl_trans = sekarang).filter(jenis__in=jenispcr).filter(status_jurnal=2)
        return sum([p.debet for p in kb])
    pengeluaran_debet = property(pengeluaran_debet)

    def pengeluaran_kredit(self):####PENGELUARAN KREDIT
        sekarang = datetime.date.today()
        jenispcr = dict([[k, 0] for k,v in JENIS_PENGELUARAN_KREDIT])
        kb = self.tbl_transaksi_set.filter(tgl_trans = sekarang).filter(jenis__in=jenispcr).filter(status_jurnal=2)
        return sum([p.kredit for p in kb]) 
    pengeluaran_kredit = property(pengeluaran_kredit)

    def setoran_saldo(self):####PENGELUARAN KREDIT
        sekarang = datetime.date.today()
        jenispcr = dict([[k, 0] for k,v in JENIS_SALDO_YG_DISETORKAN])
        kb = self.tbl_transaksi_set.filter(tgl_trans = sekarang).filter(jenis__in=jenispcr).filter(status_jurnal=2)
        return sum([p.debet for p in kb])
    setoran_saldo = property(setoran_saldo)
    ####PENGELUARAN
    #####POSTING REPORT JURNAL
    def cari_pencairan(self):####PENCAIRAN KASIR PINJAMAN
        sekarang = datetime.date.today()
        jenispcr = dict([[k, 0] for k,v in JENIS_BANDING_PENCAIRAN])
        pencairan = self.tbl_transaksi_set.filter(tgl_trans = sekarang).filter(jenis__in=jenispcr).filter(status_jurnal=2).filter(id_coa=287L)
        return sum([p.kredit for p in pencairan]) 
    cari_pencairan = property(cari_pencairan)

    def cari_pencairan_nonfilter(self):####PENCAIRAN KASIR NON FILTER PINJAMAN
        sekarang = datetime.date.today()
        jenispcr = dict([[k, 0] for k,v in JENIS_PENCAIRAN_NON_FILTER])
        p_filter = self.tbl_transaksi_set.filter(tgl_trans = sekarang).filter(jenis__in=jenispcr).filter(status_jurnal=2)
        return sum([p.kredit for p in p_filter])
    cari_pencairan_nonfilter = property(cari_pencairan_nonfilter)

    def cari_pencairan_nonfilter_debet(self):####PENCAIRAN KASIR NON FILTER PINJAMAN
        sekarang = datetime.date.today()
        jenispcr = dict([[k, 0] for k,v in JENIS_PENCAIRAN_NON_FILTER_DEBET])
        p_filter = self.tbl_transaksi_set.filter(tgl_trans = sekarang).filter(jenis__in=jenispcr).filter(status_jurnal=2)
        return sum([p.debet for p in p_filter])
    cari_pencairan_nonfilter_debet = property(cari_pencairan_nonfilter_debet)

    def cari_biaya_debet(self):####BIAYA PINJAMAN
        sekarang = datetime.date.today()
        jenispcr = dict([[k, 0] for k,v in JENIS_BIAYA_GERAI])
        p_filter = self.tbl_transaksi_set.filter(tgl_trans = sekarang).filter(jenis__in=jenispcr).filter(status_jurnal=2)
        return sum([p.debet for p in p_filter])
    cari_biaya_debet = property(cari_biaya_debet)

    def transaksi_pdpt_geraifilter(self):####TRANSAKSI PENDAPATAN GERAI
        sekarang = datetime.date.today()
        jenispcr = dict([[k, 0] for k,v in JENIS_PENDAPATAN_GERAI_FILTER])
        pdpt = self.tbl_transaksi_set.filter(tgl_trans = sekarang).filter(jenis__in=jenispcr).filter(status_jurnal=2).filter(id_coa=448L)
        return sum([p.kredit for p in pdpt])
    transaksi_pdpt_geraifilter = property(transaksi_pdpt_geraifilter)

    def transaksi_penjualan_gerai(self):####TRANSAKSI PENDAPATAN PENJUALAN GERAI
        sekarang = datetime.date.today()
        jenispcr = dict([[k, 0] for k,v in JENIS_PENJUALAN])
        jual = self.tbl_transaksi_set.filter(tgl_trans = sekarang).filter(jenis__in=jenispcr).filter(status_jurnal=2)
        return sum([p.kredit for p in jual])
    transaksi_penjualan_gerai = property(transaksi_penjualan_gerai)
    ########POSTTING REPORT JURNAL

    def transaksi_kelebihan(self):####TRANSAKSI SISA/KELEBIHAN
        sekarang = datetime.date.today()
        jenispcr = dict([[k, 0] for k,v in JENIS_BANDING_SISA_TRANSAKSI])
        kelebihan = self.tbl_transaksi_set.filter(tgl_trans = sekarang).filter(jenis__in=jenispcr).filter(status_jurnal=2).filter(id_coa=448L)
        return sum([p.kredit for p in kelebihan])
    transaksi_kelebihan = property(transaksi_kelebihan)
        
    def nobukti_sama(self):
        sama = Jurnal.objects.values('nobukti').order_by()
        return sama
    
    def nilai_debet(self):
        return self.tbl_transaksi_set.filter(debet__gt=0).aggregate(Sum('debet'))['debet__sum']
    
    def nilai_kredit(self):
        return self.tbl_transaksi_set.filter(kredit__gt=0).aggregate(Sum('kredit'))['kredit__sum'] 
     
class Tbl_Transaksi(models.Model):
    id_coa = models.ForeignKey(Tbl_Akun,null =True,blank=True)
    jurnal = models.ForeignKey(Jurnal)
    no_trans = models.IntegerField(max_length=6, null=True, blank=True)
    jenis = models.CharField(max_length=100)
    debet = models.IntegerField(max_length=11)
    kredit = models.IntegerField(max_length=11)
    id_cabang = models.IntegerField(max_length=3)
    id_cabang_tuju = models.IntegerField(max_length=3,null=True,blank=True)
    id_unit = models.IntegerField(max_length=3)
    id_product  = models.IntegerField(max_length=1)
    status_jurnal = models.IntegerField(max_length=1)
    user = models.ForeignKey(User, related_name='c_tbl_transaksi', editable=False, null=True, blank=True)
    tgl_trans = models.DateField()
    status_posting = models.IntegerField(max_length=1,blank=True,null=True)
    deskripsi = models.CharField(max_length=500, blank=True, null=True)
    saldo = models.IntegerField(max_length=16, blank=True, null=True)
    posting = models.CharField(max_length=3, blank=True, null=True)
    
    class Meta:
        db_table = "tbl_transaksi"       

    def hitung_saldo_awal(self):###untuk report buku besar all
        if self.saldo == None:
            return self.saldo == 0
        else:
            return self.saldo 
    hitung_saldo_awal=property(hitung_saldo_awal)
    
    def __unicode__(self):
        return '%s-%s' % ((self.id),(self.jurnal))

    def saldo_awalhari(self):
        sekarang = datetime.date.today()
        total = 0
        for k in Tbl_Transaksi.objects.filter(tgl_trans = sekarang):
            if k.saldo == None:
                return total
            else:
                total += k.saldo
        return total
    saldo_awalhari = property(saldo_awalhari)

    def gl_validasi(self):
        return "KGL %s %s %s %s %s %s" % ((self.jurnal.nobukti),self.id_coa.coa,self.kredit,self.id_coa.coa,self.tgl_trans,self.id_cabang)

    def gabung_kode_coa(self):
        return "%s.%s" % ((self.kepala_coa()),(self.id_coa.coa))

    ### Transaksi Kasir
    def total_pencairan_kasir_pembulatan(self, ):
        tbl = Tbl_Transaksi.objects.filter(tgl_trans = datetime.date.today()).filter(jenis = u'Pencairan_kasir').filter(id_coa= 7L)
        return sum ([a.debet for a in tbl])
    
    def total_pelunasan_kasir(self, ):
        tbl = Tbl_Transaksi.objects.filter(tgl_trans = datetime.date.today()).filter(jenis = u'Pelunasan_kasir').filter(id_coa= 7L)
        return sum ([a.debet for a in tbl])
        
    def kepala_coa(self):
        kp_coa= self.id_unit + self.id_cabang
        return kp_coa
    
    ###hitungan saldo
    def hitung_saldo_akhir(self):
        return self.id_coa.saldo_pjb #+ (self.debet - self.kredit)    

    def get_jumlah_saldo_test(self):
        total =0
        for kp in self.jurnal.tbl_transaksi_set.all():
            total += kp.debet() 
        total = self.hitung_saldo_akhir() + (self.debet - self.kredit)
        return total
    ###hitungan saldo
    
    def get_jumlah_debet(self):
        return self.debet + self.kredit
    
    def __unicode__(self):
        return "%s" % (self.id_cabang)
 
    def get_absolute_url_batal_jurnal(self):
        return "/jurnal/%s/add_baru_h/" % self.id_cabang
    
    def get_absolute_url_batal_jurnal_glcabang(self):
        return "/jurnal/%s/gl_glcabang/" % self.id_cabang   

    def get_absolute_url(self):
        return "/jurnal/%s/add/" % self.id_cabang

    def get_absolute_url_staff(self):
        return "/jurnal/%s/add_staff/" % self.id_cabang

    def get_absolute_url_non(self):
        return "/jurnal/%s/add_non_kas/" % self.id_cabang

    def get_absolute_url_non_staff(self):
        return "/jurnal/%s/add_staff_non_kas/" % self.id_cabang
    
    def get_absolute_url_biaya(self):
        return "/biaya/%s/add/" % self.id_cabang

    def get_absolute_url_biaya_pusat(self):
        return "/keuangan/%s/add_pusat/" % self.id_cabang

    def get_absolute_url_biaya_keuangan(self):
        return "/keuangan/%s/add/" % self.id_cabang

    def keuangan_hapus(self):
        return "/keuangan/%s/add/" % self.id_cabang
    
    def number_tampil(self):
        return "%s.%s" % (self.kepala_coa(), self.id)
    
    def next_group(self):
        ret = 'MANKEU'
        if self.cekmankeu and (self.manopkeu.status == '1'):
            return ret
        #else:
            #ret = 'MANKEU'
        
    
    def cekmankeu(self):
        try:
            s = self.manopkeu
            ret = s.status == '1'
        except ManopKeu.DoesNotExist:
            ret = False
        return ret

class Saldonon_Posting(models.Model):
    tbl = models.ForeignKey(Tbl_Transaksi, blank=True, null=True)
    id_coa = models.ForeignKey(Tbl_Akun, blank=True, null=True)
    tanggal = models.DateField(null=True)    
    saldo = models.IntegerField(max_length=11, blank=True, null=True)
    kode_cabang = models.CharField(max_length=3,blank=True,null=True)
    jenis = models.CharField(max_length=60,blank=True,null=True)
    cu = models.ForeignKey(User, related_name='c_saldo', editable=False, null=True, blank=True)
    mu = models.ForeignKey(User, related_name='m_saldo', editable=False, null=True, blank=True)
        
    class Meta:
        db_table = 'saldonon_posting'
        verbose_name = 'Saldonon_Posting'


STATUS_KEUANGAN = (
    ('1','OK'),
    ('2','TOLAK'),
)    

class KeuanganPusat(models.Model):
    keuangan_pusat = models.ForeignKey(Jurnal,blank=True,null=True)
    tanggal = models.DateField()
    tanggal_sbl = models.DateField()
    kode_cabang = models.IntegerField(null = True,blank=True)
    saldo = models.DecimalField(null=True, blank=True, max_digits =11,decimal_places = 2)
    cu = models.ForeignKey(User, related_name='+', editable=False, null=True, blank=True)
    mu = models.ForeignKey(User, related_name='+', editable=False, null=True, blank=True)
    note = models.CharField(max_length=200, null=True, blank=True)
    
    class Meta:
        db_table = "keuanganpusat"

    
STATUS_MANKEU = (
    ('1','OK'),
    ('2','TOLAK'),
)       
        
class ManopKeu(models.Model):
    manop = models.OneToOneField('Tbl_Transaksi',blank=True,null=True)
    mankeu = models.OneToOneField('Tbl_Akun',blank=True,null=True)
    status = models.CharField(max_length=1, choices=STATUS_MANKEU)
    tanggal = models.DateField()
    cu = models.ForeignKey(User, related_name='c_mankeu', editable=False, null=True, blank=True)
    mu = models.ForeignKey(User, related_name='m_mankeu', editable=False, null=True, blank=True)
    note = models.CharField(max_length=200, null=True, blank=True)
    
    class Meta:
        db_table = 'manopkeu'
        verbose_name = 'ManopKeu'
        verbose_name_plural = verbose_name

STATUS_KPLGERAI = (
    ('1','OK'),
    ('2','TOLAK'),
)    
class KplGerai(models.Model):
    kpl_gerai = models.OneToOneField('Tbl_Transaksi',blank=True,null=True)
    akun_kpl = models.OneToOneField('Tbl_Akun',blank=True,null=True)
    status = models.CharField(max_length=1, choices=STATUS_KPLGERAI)
    tanggal = models.DateField()
    cu = models.ForeignKey(User, related_name='c_kplgerai', editable=False, null=True, blank=True)
    mu = models.ForeignKey(User, related_name='m_kplgerai', editable=False, null=True, blank=True)
    note = models.CharField(max_length=200, null=True, blank=True)
    
    class Meta:
        db_table = 'kplgerai'
        verbose_name = 'KplGerai'
        verbose_name_plural = verbose_name
        
class KepalaGerai(models.Model):
    kepala_gerai = models.OneToOneField('AkadGadai',blank=True,null=True)
    status = models.CharField(max_length=1, choices=STATUS_KPLGERAI)
    tanggal = models.DateField()
    cu = models.ForeignKey(User, related_name='c_kepalagerai', editable=False, null=True, blank=True)
    mu = models.ForeignKey(User, related_name='m_kepalagerai', editable=False, null=True, blank=True)
    note = models.CharField(max_length=200, null=True, blank=True)
    
    class Meta:
        db_table = 'kepalagerai'
        verbose_name = 'KepalaGerai'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return "%s-%s" % (self.kepala_gerai,self.id)        

class Wilayah(models.Model):
    nama_admin = models.CharField(max_length=50,null=True,blank=True)
    nama_kg = models.CharField(max_length=50,null=True,blank=True)
    nama_kasir = models.CharField(max_length=50,null=True,blank=True)
    alamat = models.CharField(max_length=255, blank=True, null=True)
    no_telp = models.CharField(max_length=35, blank=True, null=True)
    init_cabang = models.CharField(max_length=12,null=True)
    
    class Meta:
        abstract = True

STATUS_AKTIFASI_CABANG = (
    ('1','AKTIF'),
    ('2','TUTUP'),
)

class GeraiGadaiManager(models.Manager):
    pass

    def for_user(self, user):
        try:
            gerai = user.get_profile().gerai
            geraigadai_list = self.all().filter(id__exact=gerai.id) | gerai.tbl_cabang_set.all()
        except:
            geraigadai_list = None
        return geraigadai_list

class Tbl_Cabang(Wilayah):
    kode_cabang = models.CharField(max_length=3)    
    nama_cabang = models.CharField(max_length=30,null=True)
    objects = GeraiGadaiManager()
    parent = models.ForeignKey('self', blank=True, null=True)
    kode_unit = models.CharField(max_length=3)
    nama_unit = models.CharField(max_length=30)
    id_lama = models.IntegerField(max_length=11, blank=True, null=True)           
    status_aktif = models.CharField(max_length=50,null=True,blank=True,choices= STATUS_AKTIFASI_CABANG) 

    class Meta:
        db_table = 'tbl_cabang'
        verbose_name = 'Tabel Cabang'
        verbose_name_plural = verbose_name

    def get_jumlah_terlambat_filter(self, start_date,end_date):
        rs_pk = self.akadgadai_set.filter(tanggal__range=(start_date,end_date))
        nilai =0
        for p in rs_pk:
            nilai += p.total_terlambat()
        return nilai

    def total_terlambat_filter(self,start_date,end_date):
        return self.get_jumlah_terlambat_filter(start_date,end_date)


    def get_jumlah_terlambatplns_filter(self, start_date,end_date):
        rs_pk = self.pelunasan_set.filter(tanggal__range=(start_date,end_date))
        nilai =0
        for p in rs_pk:
            nilai += p.total_terlambat_plns()
        return nilai

    def total_terlambatplns_filter(self,start_date,end_date):
        return self.get_jumlah_terlambatplns_filter(start_date,end_date)

    ####MATERAI 
    def pembelian_materai_pusat(self):
        sekarang = datetime.date.today()
        pembelian = Tbl_Transaksi.objects.filter(id_cabang=self.kode_cabang).filter(jenis = 'PEMBELIAN MATERAI PUSAT').\
        filter(tgl_trans= sekarang).filter(debet__gt= 0).filter(status_jurnal = 2)
        return sum([a.debet for a in pembelian])

    def penjualan_materai_pusat(self):
        sekarang = datetime.date.today()
        penjualan = Tbl_Transaksi.objects.filter(id_cabang=self.kode_cabang).filter(jenis = 'PENJUALAN MATERAI PUSAT').\
        filter(tgl_trans= sekarang).filter(debet__gt= 0).filter(status_jurnal = 2)
        return sum([a.debet for a in penjualan])

    def saldo_materai(self):
        sekarang = datetime.date.today()
        saldo = Tbl_TransaksiKeu.objects.filter(id_cabang=self.kode_cabang).filter(id_coa__coa= '13.04.03').\
        filter(tgl_trans= sekarang).filter(status_jurnal = 2)
        return sum([a.saldo for a in saldo])

    def permintaan_materai(self):
        sekarang = datetime.date.today()
        permintaan = Tbl_Transaksi.objects.filter(id_cabang=self.kode_cabang).filter(jenis = 'Penerimaan Materai').\
        filter(tgl_trans= sekarang).filter(debet__gt= 0).filter(status_jurnal = 2)
        #return sum([a.debet for a in permintaan])
        if self.kode_cabang == '300' :
            return 0
        else:
            return sum([a.debet for a in permintaan])


    def pemakaian_materai(self):
        sekarang = datetime.date.today()
        pemakaian = Tbl_Transaksi.objects.filter(id_cabang=self.kode_cabang).filter(id_coa_id = 231).filter(tgl_trans= sekarang).\
        filter(kredit__gt= 0).filter(status_jurnal = 2).filter(jenis__in =('Pencairan','Pencairan_Barang_sama','Pemakaian Materai Pusat'))

        permintaan = Tbl_Transaksi.objects.filter(id_cabang=self.kode_cabang).filter(jenis = 'Penerimaan Materai').\
        filter(tgl_trans= sekarang).filter(debet__gt= 0).filter(status_jurnal = 2)

        #return sum([a.kredit for a in pemakaian])
        if self.kode_cabang == '300' :
            return sum([a.kredit for a in pemakaian]) + sum([a.debet for a in permintaan])
        else:
            return sum([a.kredit for a in pemakaian])

    def saldo_akhir_materai(self):
        if self.kode_cabang != '300' :
            return self.pembelian_materai_pusat() + self.saldo_materai() + self.permintaan_materai() - self.pemakaian_materai()
        else:
            return self.pembelian_materai_pusat() + self.saldo_materai() + self.permintaan_materai() - self.penjualan_materai_pusat() - self.pemakaian_materai()

    def pcs_materai_1(self):
        return self.saldo_akhir_materai() / 6000

    ### AKHIR MATERAI

    ### MATERAI RANGE TANGGAL
    def range_pembelian_materai_pusat(self,start_date,end_date):
        sekarang = datetime.date.today()
        pembelian = Tbl_Transaksi.objects.filter(id_cabang=self.kode_cabang).filter(jenis = 'PEMBELIAN MATERAI PUSAT').\
        filter(tgl_trans__range= (start_date,end_date)).filter(debet__gt= 0).filter(status_jurnal = 2)
        return sum([a.debet for a in pembelian])

    def range_penjualan_materai_pusat(self,start_date,end_date):
        sekarang = datetime.date.today()
        penjualan = Tbl_Transaksi.objects.filter(id_cabang=self.kode_cabang).filter(jenis = 'PENJUALAN MATERAI PUSAT').\
        filter(tgl_trans__range= (start_date,end_date)).filter(debet__gt= 0).filter(status_jurnal = 2)
        return sum([a.debet for a in penjualan])

    def range_saldo_materai(self,start_date):
        sekarang = datetime.date.today()
        saldo = Tbl_TransaksiKeu.objects.filter(id_cabang=self.kode_cabang).filter(id_coa__coa= '13.04.03').\
        filter(tgl_trans= start_date)#.filter(status_jurnal = 2)
        return sum([a.saldo for a in saldo])

    def range_permintaan_materai(self,start_date,end_date):
        sekarang = datetime.date.today()
        permintaan = Tbl_Transaksi.objects.filter(id_cabang=self.kode_cabang).filter(jenis = 'Penerimaan Materai').\
        filter(tgl_trans__range= (start_date,end_date)).filter(debet__gt= 0).filter(status_jurnal = 2)
        #return sum([a.debet for a in permintaan])
        if self.kode_cabang == '300' :
            return 0
        else:
            return sum([a.debet for a in permintaan])

    def range_pemakaian_materai(self,start_date,end_date):
        sekarang = datetime.date.today()
        pemakaian = Tbl_Transaksi.objects.filter(id_cabang=self.kode_cabang).filter(id_coa_id = 231).filter(tgl_trans__range= (start_date,end_date)).\
        filter(kredit__gt= 0).filter(status_jurnal = 2).filter(jenis__in =('Pencairan','Pencairan_Barang_sama','Pemakaian Materai Pusat'))

        permintaan = Tbl_Transaksi.objects.filter(id_cabang=self.kode_cabang).filter(jenis = 'Penerimaan Materai').\
        filter(tgl_trans__range= (start_date,end_date)).filter(debet__gt= 0).filter(status_jurnal = 2)
        
        if self.kode_cabang == '300' :
            return sum([a.kredit for a in pemakaian]) + sum([a.debet for a in permintaan])
        else:
            return sum([a.kredit for a in pemakaian]) 

    def range_saldo_akhir_materai(self,start_date,end_date):
        if self.kode_cabang != '300' :
            return self.range_pembelian_materai_pusat(start_date,end_date) + self.range_saldo_materai(start_date = start_date) + self.range_permintaan_materai(start_date = start_date, end_date = end_date) - self.range_pemakaian_materai(start_date = start_date, end_date = end_date)
        else:
            return self.range_pembelian_materai_pusat(start_date,end_date) + self.range_saldo_materai(start_date = start_date) + self.range_permintaan_materai(start_date = start_date, end_date = end_date) - self.range_penjualan_materai_pusat(start_date = start_date, end_date = end_date)- self.range_pemakaian_materai(start_date = start_date, end_date = end_date)

    def pcs_materai(self,start_date,end_date):
        return self.range_saldo_akhir_materai(start_date,end_date) / 6000
    ### AKHOR MATERAI TANGGAL

    ### report Aging Gudang Aktif  Pencairan NEW TEDDY START
    def jumlah_aging_hp_filter(self,start_date):        
        return self.akadgadai_set.filter(barang__jenis_barang=1).filter(tanggal=start_date).count()

    def total_pinjaman_aging_hp_filter(self,start_date):
        sekarang = datetime.date.today()
        rs_pk = self.akadgadai_set.filter(barang__jenis_barang=1).filter(tanggal=start_date)
        nilai= 0
        for p in rs_pk:
            nilai += p.nilai
        return nilai

    def jumlah_aging_laptop_filter(self,start_date):
        return self.akadgadai_set.filter(barang__jenis_barang=2).filter(tanggal=start_date).count()

    def total_pinjaman_aging_laptop_filter(self,start_date):
        rs_pk = self.akadgadai_set.filter(barang__jenis_barang=2).filter(tanggal=start_date)
        nilai= 0
        for p in rs_pk:
            nilai += p.nilai
        return nilai
    
    def jumlah_aging_kamera_filter(self,start_date):
        return self.akadgadai_set.filter(barang__jenis_barang=3).filter(tanggal=start_date).count()

    def total_pinjaman_aging_kamera_filter(self,start_date):
        rs_pk = self.akadgadai_set.filter(barang__jenis_barang=3).filter(tanggal=start_date)
        nilai= 0
        for p in rs_pk:
            nilai += p.nilai
        return nilai

    def jumlah_aging_ps_filter(self,start_date):
        return self.akadgadai_set.filter(barang__jenis_barang=4).filter(tanggal=start_date).count()
    
    def total_pinjaman_aging_ps_filter(self,start_date):
        rs_pk = self.akadgadai_set.filter(barang__jenis_barang=4).filter(tanggal=start_date)
        nilai= 0
        for p in rs_pk:
            nilai += p.nilai
        return nilai
            
    def jumlah_aging_tv_filter(self,start_date):
        return self.akadgadai_set.filter(barang__jenis_barang=5).filter(tanggal=start_date).count()        
    
    def total_pinjaman_aging_tv_filter(self,start_date):
        rs_pk = self.akadgadai_set.filter(barang__jenis_barang=5).filter(tanggal=start_date)
        nilai= 0
        for p in rs_pk:
            nilai += p.nilai
        return nilai    

    def jumlah_aging_motor_filter(self,start_date):
        return self.akadgadai_set.filter(barang__jenis_kendaraan=1).filter(tanggal=start_date).count()
    
    def total_pinjaman_aging_motor_filter(self,start_date):
        rs_pk = self.akadgadai_set.filter(barang__jenis_kendaraan=1).filter(tanggal=start_date)
        nilai= 0
        for p in rs_pk:
            nilai += p.nilai
        return nilai

    def jumlah_aging_mobil_filter(self,start_date):
        return self.akadgadai_set.filter(barang__jenis_kendaraan=2).filter(tanggal=start_date).count()
    
    def total_pinjaman_aging_mobil_filter(self,start_date):
        rs_pk = self.akadgadai_set.filter(barang__jenis_kendaraan=2).filter(tanggal=start_date)
        nilai= 0
        for p in rs_pk:
            nilai += p.nilai
        return nilai

    def total_aging_hari_filter(self,start_date):
        return self.total_pinjaman_aging_motor_filter(start_date) + self.total_pinjaman_aging_mobil_filter(start_date)\
            + self.total_pinjaman_aging_hp_filter(start_date) + self.total_pinjaman_aging_laptop_filter(start_date) + \
            self.total_pinjaman_aging_kamera_filter(start_date) + self.total_pinjaman_aging_ps_filter(start_date) + \
            self.total_pinjaman_aging_tv_filter(start_date)

    ### report Aging Gudang Aktif PENcairan New Teddy

    ### report Aging Gudang Aktif LELANG New Teddy
    def lelang_aging_hp_filter(self,start_date):
        return self.akadgadai_set.filter(barang__jenis_barang=1).filter(status_transaksi__in=('2','6')).\
            filter(baranglelang__tgl_lelang=start_date).count()

    def total_lelang_aging_hp_filter(self,start_date):
        rs_pk = self.akadgadai_set.filter(barang__jenis_barang=1).filter(status_transaksi__in=('2','6')).\
            filter(baranglelang__tgl_lelang=start_date)
        nilai= 0
        for p in rs_pk:
            nilai += p.nilai
        return nilai
    
    def lelang_aging_laptop_filter(self,start_date):
        return self.akadgadai_set.filter(barang__jenis_barang=2).filter(status_transaksi__in=('2','6')).\
            filter(baranglelang__tgl_lelang=start_date).count()

    def total_lelang_aging_laptop_filter(self,start_date):
        rs_pk = self.akadgadai_set.filter(barang__jenis_barang=2).filter(status_transaksi__in=('2','6')).\
            filter(baranglelang__tgl_lelang=start_date)
        nilai= 0
        for p in rs_pk:
            nilai += p.nilai
        return nilai

    def lelang_aging_kamera_filter(self,start_date):
        return self.akadgadai_set.filter(barang__jenis_barang=3).filter(status_transaksi__in=('2','6')).filter(baranglelang__tgl_lelang=start_date).count()
    
    def total_lelang_aging_kamera_filter(self,start_date):
        rs_pk = self.akadgadai_set.filter(barang__jenis_barang=3).filter(status_transaksi__in=('2','6')).filter(baranglelang__tgl_lelang=start_date)
        nilai= 0
        for p in rs_pk:
            nilai += p.nilai
        return nilai
                
    def lelang_aging_ps_filter(self,start_date):
        return self.akadgadai_set.filter(barang__jenis_barang=4).filter(status_transaksi__in=('2','6')).filter(baranglelang__tgl_lelang=start_date).count()
    
    def total_lelang_aging_ps_filter(self,start_date):
        rs_pk = self.akadgadai_set.filter(barang__jenis_barang=4).filter(status_transaksi__in=('2','6')).filter(baranglelang__tgl_lelang=start_date)
        nilai= 0
        for p in rs_pk:
            nilai += p.nilai
        return nilai
            
    def lelang_aging_tv_filter(self,start_date):
        return self.akadgadai_set.filter(barang__jenis_barang=5).filter(status_transaksi__in=('2','6')).filter(baranglelang__tgl_lelang=start_date).count()
    
    def total_lelang_aging_tv_filter(self,start_date):
        rs_pk = self.akadgadai_set.filter(barang__jenis_barang=5).filter(status_transaksi__in=('2','6')).filter(baranglelang__tgl_lelang=start_date)
        nilai= 0
        for p in rs_pk:
            nilai += p.nilai
        return nilai

    def lelang_aging_motor_filter(self,start_date):
        return self.akadgadai_set.filter(barang__jenis_kendaraan=1).filter(status_transaksi__in=('2','6')).filter(baranglelang__tgl_lelang=start_date).count()
    
    def total_lelang_aging_motor_filter(self,start_date):
        rs_pk = self.akadgadai_set.filter(barang__jenis_kendaraan=1).filter(status_transaksi__in=('2','6')).filter(baranglelang__tgl_lelang=start_date)
        nilai= 0
        for p in rs_pk:
            nilai += p.nilai
        return nilai
    
    def lelang_aging_mobil_filter(self,start_date):
        return self.akadgadai_set.filter(barang__jenis_kendaraan=2).filter(status_transaksi__in=('2','6')).filter(baranglelang__tgl_lelang=start_date).count()
    
    def total_lelang_aging_mobil_filter(self,start_date):
        rs_pk = self.akadgadai_set.filter(barang__jenis_kendaraan=2).filter(status_transaksi__in=('2','6')).filter(baranglelang__tgl_lelang=start_date)
        nilai= 0
        for p in rs_pk:
            nilai += p.nilai
        return nilai

    def total_lelangaging_hari_filter(self,start_date):
        return self.total_lelang_aging_motor_filter(start_date) + self.total_lelang_aging_mobil_filter(start_date) + \
            self.total_lelang_aging_hp_filter(start_date) + self.total_lelang_aging_laptop_filter(start_date) + \
            self.total_lelang_aging_kamera_filter(start_date) + self.total_lelang_aging_ps_filter(start_date) + \
            self.total_lelang_aging_tv_filter(start_date)
    ### report Aging Gudang Aktif LELANG New Teddy

    ### report Aging Gudang Aktif LUNAS New Teddy
    def pelunasan_aging_hp_filter(self,start_date):
        return self.akadgadai_set.filter(barang__jenis_barang=1).filter(status_transaksi='1').filter(pelunasan__tanggal=start_date).count()
    
    def total_pelunasan_aging_hp_filter(self,start_date):
        rs_pk = self.akadgadai_set.filter(barang__jenis_barang=1).filter(status_transaksi='1').filter(pelunasan__tanggal=start_date)
        nilai= 0
        for p in rs_pk:
            nilai += p.nilai
        return nilai
    
    def pelunasan_aging_laptop_filter(self,start_date):
        return self.akadgadai_set.filter(barang__jenis_barang=2).filter(status_transaksi='1').filter(pelunasan__tanggal=start_date).count()

    def total_pelunasan_aging_laptop_filter(self,start_date):
        rs_pk = self.akadgadai_set.filter(barang__jenis_barang=2).filter(status_transaksi='1').filter(pelunasan__tanggal=start_date)
        nilai= 0
        for p in rs_pk:
            nilai += p.nilai
        return nilai
        
    def pelunasan_aging_kamera_filter(self,start_date):
        return self.akadgadai_set.filter(barang__jenis_barang=3).filter(status_transaksi='1').filter(pelunasan__tanggal=start_date).count()
    
    def total_pelunasan_aging_kamera_filter(self,start_date):
        rs_pk = self.akadgadai_set.filter(barang__jenis_barang=3).filter(status_transaksi='1').filter(pelunasan__tanggal=start_date)
        nilai= 0
        for p in rs_pk:
            nilai += p.nilai
        return nilai
                
    def pelunasan_aging_ps_filter(self,start_date):
        return self.akadgadai_set.filter(barang__jenis_barang=4).filter(status_transaksi='1').filter(pelunasan__tanggal=start_date).count()
    
    def total_pelunasan_aging_ps_filter(self,start_date):
        rs_pk = self.akadgadai_set.filter(barang__jenis_barang=4).filter(status_transaksi='1').filter(pelunasan__tanggal=start_date)
        nilai= 0
        for p in rs_pk:
            nilai += p.nilai
        return nilai
            
    def pelunasan_aging_tv_filter(self,start_date):
        return self.akadgadai_set.filter(barang__jenis_barang=5).filter(status_transaksi='1').filter(pelunasan__tanggal=start_date).count()
    
    def total_pelunasan_aging_tv_filter(self,start_date):
        rs_pk = self.akadgadai_set.filter(barang__jenis_barang=5).filter(status_transaksi='1').filter(pelunasan__tanggal=start_date)
        nilai= 0
        for p in rs_pk:
            nilai += p.nilai
        return nilai

    def pelunasan_aging_motor_filter(self,start_date):
        return self.akadgadai_set.filter(barang__jenis_kendaraan=1).filter(status_transaksi='1').filter(pelunasan__tanggal=start_date).count()
    
    def total_pelunasan_aging_motor_filter(self,start_date):
        rs_pk = self.akadgadai_set.filter(barang__jenis_kendaraan=1).filter(status_transaksi='1').filter(pelunasan__tanggal=start_date)
        nilai= 0
        for p in rs_pk:
            nilai += p.nilai
        return nilai
    
    def pelunasan_aging_mobil_filter(self,start_date):
        return self.akadgadai_set.filter(barang__jenis_kendaraan=2).filter(status_transaksi='1').filter(pelunasan__tanggal=start_date).count()
    
    def total_pelunasan_aging_mobil_filter(self,start_date):
        rs_pk = self.akadgadai_set.filter(barang__jenis_kendaraan=2).filter(status_transaksi='1').filter(pelunasan__tanggal=start_date)
        nilai= 0
        for p in rs_pk:
            nilai += p.nilai
        return nilai

    def total_lunasaging_hari_filter(self,start_date):
        return self.total_pelunasan_aging_motor_filter(start_date) + self.total_pelunasan_aging_mobil_filter(start_date) + \
            self.total_pelunasan_aging_hp_filter(start_date) + self.total_pelunasan_aging_laptop_filter(start_date) + \
            self.total_pelunasan_aging_kamera_filter(start_date) + self.total_pelunasan_aging_ps_filter(start_date) + \
            self.total_pelunasan_aging_tv_filter(start_date)    

    ### report Aging Gudang Aktif LUNAS New Teddy

    ### report Aging Gudang Aktif RETUR New Teddy
    def retur_aging_hp_filter(self,start_date):
        return self.akadgadai_set.filter(barang__jenis_barang=1).filter(tanggal_permintaan=start_date).filter(status_permintaan="2").count()
    
    def total_retur_aging_hp_filter(self,start_date):
        rs_pk = self.akadgadai_set.filter(barang__jenis_barang=1).filter(tanggal_permintaan=start_date).filter(status_permintaan="2")
        nilai= 0
        for p in rs_pk:
            nilai += p.nilai
        return nilai    

    def retur_aging_laptop_filter(self,start_date):
        return self.akadgadai_set.filter(barang__jenis_barang=2).filter(tanggal_permintaan=start_date).filter(status_permintaan="2").count()

    def total_retur_aging_laptop_filter(self,start_date):
        rs_pk = self.akadgadai_set.filter(barang__jenis_barang=2).filter(tanggal_permintaan=start_date).filter(status_permintaan="2")
        nilai= 0
        for p in rs_pk:
            nilai += p.nilai
        return nilai
        
    def retur_aging_kamera_filter(self,start_date):
        return self.akadgadai_set.filter(barang__jenis_barang=3).filter(tanggal_permintaan=start_date).filter(status_permintaan="2").count()
    
    def total_retur_aging_kamera_filter(self,start_date):
        rs_pk = self.akadgadai_set.filter(barang__jenis_barang=3).filter(tanggal_permintaan=start_date).filter(status_permintaan="2")
        nilai= 0
        for p in rs_pk:
            nilai += p.nilai
        return nilai
                
    def retur_aging_ps_filter(self,start_date):
        return self.akadgadai_set.filter(barang__jenis_barang=4).filter(tanggal_permintaan=start_date).filter(status_permintaan="2").count()
    
    def total_retur_aging_ps_filter(self,start_date):
        rs_pk = self.akadgadai_set.filter(barang__jenis_barang=4).filter(tanggal_permintaan=start_date).filter(status_permintaan="2")
        nilai= 0
        for p in rs_pk:
            nilai += p.nilai
        return nilai
            
    def retur_aging_tv_filter(self,start_date):
        return self.akadgadai_set.filter(barang__jenis_barang=5).filter(tanggal_permintaan=start_date).filter(status_permintaan="2").count()        

    def total_retur_aging_tv_filter(self,start_date):
        rs_pk = self.akadgadai_set.filter(barang__jenis_barang=5).filter(tanggal_permintaan=start_date).filter(status_permintaan="2")
        nilai= 0
        for p in rs_pk:
            nilai += p.nilai
        return nilai

    def retur_aging_motor_filter(self,start_date):
        return self.akadgadai_set.filter(barang__jenis_kendaraan=1).filter(tanggal_permintaan=start_date).filter(status_permintaan="2").count()
    
    def total_retur_aging_motor_filter(self,start_date):
        rs_pk = self.akadgadai_set.filter(barang__jenis_kendaraan=1).filter(tanggal_permintaan=start_date).filter(status_permintaan="2")
        nilai= 0
        for p in rs_pk:
            nilai += p.nilai
        return nilai
    
    def retur_aging_mobil_filter(self,start_date):
        return self.akadgadai_set.filter(barang__jenis_kendaraan=2).filter(tanggal_permintaan=start_date).filter(status_permintaan="2").count()
    
    def total_retur_aging_mobil_filter(self,start_date):
        rs_pk = self.akadgadai_set.filter(barang__jenis_kendaraan=2).filter(tanggal_permintaan=start_date).filter(status_permintaan="2")
        nilai= 0
        for p in rs_pk:
            nilai += p.nilai
        return nilai

    def total_returaging_hari_filter(self,start_date):
        return self.total_retur_aging_motor_filter(start_date) + self.total_retur_aging_mobil_filter(start_date) + \
            self.total_retur_aging_hp_filter(start_date) + self.total_retur_aging_laptop_filter(start_date) + \
            self.total_retur_aging_kamera_filter(start_date) + self.total_retur_aging_ps_filter(start_date) + \
            self.total_retur_aging_tv_filter(start_date)   
   
    ### report Aging Gudang Aktif RETUR New Teddy finis

    def get_jumlah_adm_harian_filter(self, start_date,end_date):
        if not start_date:			
            rs_pk = self.akadgadai_set.filter(tanggal__range=(start_date,end_date)).filter(kepalagerai__status = 1)
        else:
            rs_pk = self.akadgadai_set.filter(tanggal__range=(start_date,end_date)).filter(kepalagerai__status = 1)
        nilai= 0
        for p in rs_pk:
            nilai += p.tot_adm_kend_elek
        return nilai

    def get_jumlah_beasimpan_harian_filter(self, start_date,end_date):
        now = datetime.date.today()
        if not start_date:			
            rs_pk = self.akadgadai_set.filter(tanggal__range=(start_date,end_date)).filter(kepalagerai__status = 1)
        else:
            rs_pk = self.akadgadai_set.filter(tanggal__range=(start_date,end_date)).filter(kepalagerai__status = 1)
        nilai= 0
        for p in rs_pk:
            nilai += p.tot_simpan_kend_elek
        return nilai

    def plns_denda_harian_filter(self, start_date,end_date):
        if not start_date:			
            rs_pk = self.pelunasan_set.filter(tanggal__range=(start_date,end_date))
        else:
            rs_pk = self.pelunasan_set.filter(tanggal__range=(start_date,end_date))
        nilai= 0
        for p in rs_pk:
            nilai += p.denda_total
        return nilai

    def total_harian_denda_filter(self,start_date,end_date):
        return float(self.plns_denda_harian_filter(start_date,end_date))

    def total_harian_beasimpan_filter(self,start_date,end_date):
        return self.get_jumlah_beasimpan_harian_filter(start_date,end_date)

    def adm_harian_filter(self,start_date,end_date):
        return self.get_jumlah_adm_harian_filter(start_date,end_date) 

    def ll_harga(self,start_date,end_date):
        rs_pk = self.akadgadai_set.filter(status_transaksi = 7)
        nilai= 0
        for p in rs_pk:
            nilai += p.selisih_penjualan(start_date,end_date)
        return nilai   
 
    def akumulasi_pendapatan_harian_filter(self,start_date,end_date):
        D = decimal.Decimal
        return (D(self.total_harian_jasa_filter(start_date,end_date))) + \
            (D(self.total_harian_denda_filter(start_date,end_date)))+ self.total_harian_beasimpan_filter(start_date,end_date)+\
            D(self.adm_harian_filter(start_date,end_date)) +  (D(self.ll_harga(start_date,end_date))) + D(self.nilai_jasa_terlambat_plns(start_date,end_date))
 
    def get_jumlah_jasa_harian_filter(self, start_date,end_date):
        now = datetime.date.today()
        if not start_date:			
            rs_pk = self.akadgadai_set.filter(tanggal__range=(start_date,end_date)).filter(kepalagerai__status = 1)
        else:
            rs_pk = self.akadgadai_set.filter(tanggal__range=(start_date,end_date)).filter(kepalagerai__status = 1)
        nilai= 0
        for p in rs_pk:
            nilai += p.tot_jasa_kend_elek
        return nilai

    def plns_jasa_harian_filter(self, start_date,end_date):        
        if not start_date:			
            rs_pk = self.pelunasan_set.filter(tanggal__range=(start_date,end_date))
        else:
            rs_pk = self.pelunasan_set.filter(tanggal__range=(start_date,end_date))
        nilai= 0
        for p in rs_pk:
            nilai += p.bea_jasa_total
        return nilai

    def total_harian_jasa_filter(self,start_date,end_date):########111111
        return (self.get_jumlah_jasa_harian_filter(start_date,end_date)) #(self.plns_jasa_harian_filter(start_date,end_date)) + (self.get_jumlah_jasa_harian_filter(start_date,end_date))

    def plns_nilai_harian_filter(self, start_date,end_date):
        if not start_date:			
            rs_pk = self.pelunasan_set.filter(tanggal__range=(start_date,end_date)).filter(pelunasan__status_transaksi = 1)
        else:
            rs_pk = self.pelunasan_set.filter(tanggal__range=(start_date,end_date)).filter(pelunasan__status_transaksi = 1)
        nilai= 0
        for p in rs_pk:
            nilai += p.nilai
        return nilai
    
    def nilai_pencairan_harian_filter(self,start_date,end_date):
        return self.get_jumlah_nilai_harian_filter(start_date,end_date)

    def aktif_harian_filter(self,start_date,end_date):
        return self.akadgadai_set.filter(tanggal__range=(start_date,end_date)).exclude(kepalagerai__status ='2').count()#.filter(lunas__isnull =True).count() firman tgl 4 april 2015

    def get_jumlah_nilai_harian_filter(self, start_date, end_date):
        nilai= 0
        if not start_date:
            rs_pk = self.akadgadai_set.filter(tanggal__range=(start_date,end_date)).filter(kepalagerai__status = 1)
        else:
            rs_pk = self.akadgadai_set.filter(tanggal__range=(start_date,end_date)).filter(kepalagerai__status = 1)
        for p in rs_pk:
            nilai += p.nilai
        return nilai

    def lpr_all_barang(self,start_date, end_date):
        return self.akadgadai_set.filter(lapur__tanggal__range=(start_date,end_date),lapur__status = '1').filter(status_transaksi= 6).count()

    def lpr_nominal_all_barang(self,start_date, end_date):
        return self.akadgadai_set.filter(lapur__tanggal__range=(start_date,end_date),lapur__status = '1').filter(status_transaksi= 6)
    
    def lpr_hp_filter(self,start_date, end_date):
        return self.akadgadai_set.filter(lapur__tanggal__range=(start_date,end_date),lapur__status = '1').filter(status_transaksi=6).filter(barang__jenis_barang=1).count()
    
    def lpr_nominal_hp_filter(self,start_date, end_date):
        return self.akadgadai_set.filter(lapur__tanggal__range=(start_date,end_date),lapur__status = '1').filter(status_transaksi="6").filter(barang__jenis_barang=1)
 
    def lpr_laptop_filter(self,start_date, end_date):
        return self.akadgadai_set.filter(lapur__tanggal__range=(start_date,end_date),lapur__status = '1').filter(status_transaksi="6").filter(barang__jenis_barang=2).count()
    
    def lpr_nominal_laptop_filter(self,start_date, end_date):
        return self.akadgadai_set.filter(lapur__tanggal__range=(start_date,end_date),lapur__status = '1').filter(status_transaksi="6").filter(barang__jenis_barang=2)
    
    def lpr_kamera_filter(self,start_date, end_date):
        return self.akadgadai_set.filter(lapur__tanggal__range=(start_date,end_date),lapur__status = '1').filter(status_transaksi="6").filter(barang__jenis_barang=3).count()
    
    def lpr_nominal_kamera_filter(self,start_date, end_date):
        return self.akadgadai_set.filter(lapur__tanggal__range=(start_date,end_date),lapur__status = '1').filter(status_transaksi="6").filter(barang__jenis_barang=3)
    
    def lpr_ps_filter(self,start_date, end_date):
        return self.akadgadai_set.filter(lapur__tanggal__range=(start_date,end_date),lapur__status = '1').filter(status_transaksi="6").filter(barang__jenis_barang=4).count()
    
    def lpr_nominal_ps_filter(self,start_date, end_date):
        return self.akadgadai_set.filter(lapur__tanggal__range=(start_date,end_date),lapur__status = '1').filter(status_transaksi="6").filter(barang__jenis_barang=4)
    
    def lpr_tv_filter(self,start_date, end_date):
        return self.akadgadai_set.filter(lapur__tanggal__range=(start_date,end_date),lapur__status = '1').filter(status_transaksi="6").filter(barang__jenis_barang=5).count()
    
    def lpr_nominal_tv_filter(self,start_date, end_date):
        return self.akadgadai_set.filter(lapur__tanggal__range=(start_date,end_date),lapur__status = '1').filter(status_transaksi="6").filter(barang__jenis_barang=5)
    
    def lpr_motor_filter(self,start_date, end_date):
        return self.akadgadai_set.filter(lapur__tanggal__range=(start_date,end_date),lapur__status = '1').filter(status_transaksi="6").filter(barang__jenis_kendaraan=1).count()
    
    def lpr_nominal_motor_filter(self,start_date, end_date):
        return self.akadgadai_set.filter(lapur__tanggal__range=(start_date,end_date),lapur__status = '1').filter(status_transaksi="6").filter(barang__jenis_kendaraan=1)
    
    def lpr_mobil_filter(self,start_date, end_date):
        return self.akadgadai_set.filter(lapur__tanggal__range=(start_date,end_date),lapur__status = '1').filter(status_transaksi="6").filter(barang__jenis_kendaraan=2).count()
    
    def lpr_nominal_mobil_filter(self,start_date, end_date):
        return self.akadgadai_set.filter(lapur__tanggal__range=(start_date,end_date),lapur__status = '1').filter(status_transaksi="6").filter(barang__jenis_kendaraan=2)

    ### LAPORAN KAS BESAR PUSAT
    def pendapatan_kas(self):
        sekarang = datetime.date.today()
        pendapatan = Tbl_Transaksi.objects.filter(id_unit = 300).filter(id_cabang_tuju = self.kode_cabang).filter(debet__gt =0).\
        filter(id_coa__id=4).filter(jenis = 'GL_GL_PENAMBAHAN_PUSAT_KAS_GERAI').filter(tgl_trans= sekarang)
        return sum([a.debet for a in pendapatan])

    def pengeluaran_kas(self):
        sekarang = datetime.date.today()
        pengeluaran = Tbl_Transaksi.objects.filter(id_unit = 300).filter(id_cabang_tuju=self.kode_cabang).filter(kredit__gt =0).\
        filter(id_coa__id=4).filter(jenis = 'GL_GL_PENGELUARAN_PUSAT_KAS_GERAI').filter(tgl_trans= sekarang)
        return sum([a.kredit for a in pengeluaran])

    ### AKHIR LAPORAN KAS BESAR PUSAT

    ### LAPORAN BANK BESAR PUSAT
    def pendapatan_bank(self):
        sekarang = datetime.date.today()
        pendapatan = Tbl_Transaksi.objects.filter(id_cabang= 300).filter(id_cabang_tuju= self.kode_cabang).filter(debet__gt =0).filter(id_coa_id__in =(4,132)).filter(jenis__in = ('GL_GL_PENAMBAHAN_PUSAT_BANK','GL_GL_RAK_PUSAT')).filter(tgl_trans= sekarang)
        return sum([a.debet for a in pendapatan])

    def pengeluaran_bank(self):
        sekarang = datetime.date.today()
        pengeluaran = Tbl_Transaksi.objects.filter(id_cabang= 300).filter(id_cabang_tuju= self.kode_cabang).filter(kredit__gt =0).filter(id_coa_id =(132)).\
        filter(jenis = 'GL_GL_PENGELUARAN_PUSAT_BANK').filter(tgl_trans= sekarang)
        return sum([a.kredit for a in pengeluaran])
    ### AKHIR LAPORAN BANK BESAR PUSAT
        
       
    def __unicode__(self):
        return "%s-%s" % (self.nama_cabang,self.kode_cabang)
    
    def is_gerai(self):
        return self.parent == None

    def aktif_nasabah_harian_filter(self,start_date, end_date):
        return self.aktif_plns_harian_filter(start_date, end_date) + self.aktif_harian_filter(start_date, end_date) + \
            self.aktif_prpj_harian_filter(start_date,end_date)
    
    def aktif_plns_harian_filter(self, start_date, end_date):
        return self.pelunasan_set.filter(tanggal__range=(start_date,end_date)).filter(pelunasan__status_transaksi = 1).count()     

    def aktif_nasabah_harian_filter(self,start_date, end_date):
        return self.aktif_plns_harian_filter(start_date, end_date) + self.aktif_harian_filter(start_date, end_date)
        
    #def aktif_prpj_harian_filter(self,start_date,end_date):
        #return self.perpanjang_set.filter(tanggal__range=(start_date,end_date)).count()

    #####LAPORAN PA DIRMAN
    def noa_ayda(self, start_date, end_date):
         return Lapur.objects.filter(tanggal__range=(start_date,end_date)).filter(gerai = self.kode_cabang).filter(status = 1).count()     

    def nilai_ayda(self, start_date, end_date):
         lap = Lapur.objects.filter(tanggal__range=(start_date,end_date)).filter(gerai = self.kode_cabang).filter(status = 1)
         return sum([a.nilai for a in lap])

    def noa_ayda_history(self, start_date, end_date):
         return HistoryLapur.objects.filter(tanggal__range=(start_date,end_date)).filter(gerai = self.kode_cabang).count()

    def nilai_ayda_history(self, start_date, end_date):
         lap = HistoryLapur.objects.filter(tanggal__range=(start_date,end_date)).filter(gerai = self.kode_cabang)
         return sum([a.nilai for a in lap])


    def total_noa_ayda_lunas(self, start_date, end_date):
         return self.aktif_plns_harian_filter(start_date, end_date) + self.noa_ayda_history(start_date, end_date)

    def total_nilai_ayda_lunas(self, start_date, end_date):
        return self.plns_nilai_harian_filter( start_date,end_date) + self.nilai_ayda_history(start_date, end_date)

    def nilai_jual_ayda(self, start_date, end_date):
         lap = Lapur.objects.filter(tanggal__range=(start_date,end_date)).filter(gerai = self.kode_cabang).filter(status = 2)
         return sum([a.nilai for a in lap])

    def nilai_jasa_terlambat_plns(self, start_date,end_date):        
        lap = self.pelunasan_set.filter(tanggal__range=(start_date,end_date)).filter(gerai = self.id)
        return sum([a.bea_jasa_kendaraan for a in lap]) + sum([a.bea_jasa for a in lap])

    def rekap_piutang(self ,end_date):
        piu = self.akadgadai_set.filter(tanggal__range=(datetime.date(2000,01,01),end_date)).filter(gerai__kode_cabang =self.kode_cabang).\
            exclude(status_transaksi__in=('1','2','4','5','6','7','8','9','10'))
        return sum([a.nilai for a in piu])
    #####Akhir LAPORAN PA DIRMAN

    def aktif_harian_filter(self,start_date,end_date):
        #return self.akadgadai_set.exclude(status_transaksi__in=('1','2','4','5','6','7','8','9','10')).filter(tanggal__range=(start_date,end_date)).count()# firman tgl 4 april 2015
        return self.akadgadai_set.filter(tanggal__range=(start_date,end_date)).count()# firman tgl 4 april 2015

    def all_barang(self,start_date, end_date):
        return self.akadgadai_set.exclude(status_transaksi__in=('1','2','4','5','6','7','8','9','10')).filter(tanggal__range=(start_date,end_date)).count()

    def nominal_all_barang(self,start_date, end_date):
        return self.akadgadai_set.exclude(status_transaksi__in=('1','2','4','5','6','7','8','9','10')).filter(tanggal__range=(start_date,end_date))

    def hp_filter(self,start_date, end_date):
        return self.akadgadai_set.exclude(status_transaksi__in=('1','2','4','5','6','7','8','9','10')).filter(tanggal__range=(start_date,end_date)).filter(barang__jenis_barang=1).count()

    def nominal_hp_filter(self,start_date, end_date):
        return self.akadgadai_set.exclude(status_transaksi__in=('1','2','4','5','6','7','8','9','10')).filter(tanggal__range=(start_date,end_date)).filter(barang__jenis_barang=1)

    def laptop_filter(self,start_date, end_date):
        return self.akadgadai_set.exclude(status_transaksi__in=('1','2','4','5','6','7','8','9','10')).filter(tanggal__range=(start_date,end_date)).filter(barang__jenis_barang=2).count()

    def nominal_laptop_filter(self,start_date, end_date):
        return self.akadgadai_set.exclude(status_transaksi__in=('1','2','4','5','6','7','8','9','10')).filter(tanggal__range=(start_date,end_date)).filter(barang__jenis_barang=2)

    def kamera_filter(self,start_date, end_date):
        return self.akadgadai_set.exclude(status_transaksi__in=('1','2','4','5','6','7','8','9','10')).filter(tanggal__range=(start_date,end_date)).filter(barang__jenis_barang=3).count() 

    def nominal_kamera_filter(self,start_date, end_date):
        return self.akadgadai_set.exclude(status_transaksi__in=('1','2','4','5','6','7','8','9','10')).filter(tanggal__range=(start_date,end_date)).filter(barang__jenis_barang=3)    

    def ps_filter(self,start_date, end_date):
        return self.akadgadai_set.exclude(status_transaksi__in=('1','2','4','5','6','7','8','9','10')).filter(tanggal__range=(start_date,end_date)).filter(barang__jenis_barang=4).count()
    
    def nominal_ps_filter(self,start_date, end_date):
        return self.akadgadai_set.exclude(status_transaksi__in=('1','2','4','5','6','7','8','9','10')).filter(tanggal__range=(start_date,end_date)).filter(barang__jenis_barang=4)
    
    def tv_filter(self,start_date, end_date):
        return self.akadgadai_set.exclude(status_transaksi__in=('1','2','4','5','6','7','8','9','10')).filter(tanggal__range=(start_date,end_date)).filter(barang__jenis_barang=5).count()
    
    def nominal_tv_filter(self,start_date, end_date):
        return self.akadgadai_set.exclude(status_transaksi__in=('1','2','4','5','6','7','8','9','10')).filter(tanggal__range=(start_date,end_date)).filter(barang__jenis_barang=5)

    def motor_filter(self,start_date, end_date):
        return self.akadgadai_set.exclude(status_transaksi__in=('1','2','4','5','6','7','8','9','10')).filter(tanggal__range=(start_date,end_date)).\
             filter(barang__jenis_kendaraan=1).count()

    def nominal_motor_filter(self,start_date, end_date):
        return self.akadgadai_set.exclude(status_transaksi__in=('1','2','4','5','6','7','8','9','10')).filter(tanggal__range=(start_date,end_date)).filter(barang__jenis_kendaraan=1)

    def mobil_filter(self,start_date, end_date):
        return self.akadgadai_set.exclude(status_transaksi__in=('1','2','4','5','6','7','8','9','10')).filter(tanggal__range=(start_date,end_date)).filter(barang__jenis_kendaraan=2).\
             count()

    def nominal_mobil_filter(self,start_date, end_date):
        return self.akadgadai_set.exclude(status_transaksi__in=('1','2','4','5','6','7','8','9','10')).filter(tanggal__range=(start_date,end_date)).filter(status_transaksi=None).\
            filter(barang__jenis_kendaraan=2)

    def is_cabang(self):
        return self.tbl_cabang_set.all().count() >= 0    

    def aktif (self):
        return self.akadgadai_set.filter(lunas__isnull =True).count()
    
    def get_jumlah_nilai(self, hari=None):
        if not hari:			
            rs_pk = self.akadgadai_set.filter(lunas__isnull=True)
        else:
            rs_pk = self.akadgadai_set.filter(tanggal=hari).filter(kode_unit=300)
        nilai= 0
        for p in rs_pk:
            nilai += p.nilai
        return nilai
    
    def piutang(self):
        ag = self.akadgadai_set.all() 
        return sum([p.piutang() for p in ag])
    
    def total_jatuhtempo(self):
        sekarang = datetime.date.today()
        return self.akadgadai_set.filter(pelunasan__isnull = True).filter(jatuhtempo__lte=sekarang).count()
    
    def get_jumlah_jatuhtempo(self, hari=None):
        sekarang = datetime.date.today()
        if not hari:			
            rs_pk = self.akadgadai_set.filter(pelunasan__isnull = True).filter(jatuhtempo__lte=sekarang)
        else:
            rs_pk = self.akadgadai_set.filter(tanggal=hari)
        nilai= 0
        for p in rs_pk:
            nilai += p.nilai
        return nilai
    
    def get_banyak_lunas(self):
        return self.akadgadai_set.filter(lunas__isnull=False).count()

    def get_banyak_lelang(self):
        return self.akadgadai_set.filter(status_transaksi = u'LELANG').count()
    
    def get_total_nilailelang(self):
        rs_pk = self.akadgadai_set.filter(status_transaksi=u'LELANG')
        nilai= 0
        for p in rs_pk:
            nilai = p.hargalelang()
        return nilai
    
    def total_barang(self):
        return self.aktif() + self.get_banyak_lunas() - self.get_banyak_lelang()

    ##TAMBAHAN ADM GUADANG AKTIF 25/02/2016
    def plns_nilai_bulanan(self, hari=None):
        now = datetime.date.today()
        bulan = now.month
        tahun = now.year
        if not hari:            
            rs_pk = self.pelunasan_set.filter(tanggal__month = bulan).filter(tanggal__year=tahun)
        else:
            rs_pk = self.pelunasan_set.filter(tanggal=hari)
        nilai= 0
        for p in rs_pk:
            nilai += p.nilai
        return nilai

        ### REPORT AGING ALL GERAI Penerimaan Barang Harian
    def jumlah_aging_motor(self):
        sekarang = datetime.date.today()
        return self.akadgadai_set.filter(barang__jenis_kendaraan=1).filter(tanggal=sekarang).count()
    
    def total_pinjaman_aging_motor(self,hari = None):
        sekarang = datetime.date.today()
        if not hari:            
            rs_pk = self.akadgadai_set.filter(barang__jenis_kendaraan=1).filter(tanggal=sekarang)
        else:
            rs_pk = self.akadgadai_set.filter(tanggal=hari)
        nilai= 0
        for p in rs_pk:
            nilai += p.nilai
        return nilai
    
    def jumlah_aging_mobil(self):
        sekarang = datetime.date.today()
        return self.akadgadai_set.filter(barang__jenis_kendaraan=2).filter(tanggal=sekarang).count()
    
    def total_pinjaman_aging_mobil(self,hari = None):
        sekarang = datetime.date.today()
        if not hari:            
            rs_pk = self.akadgadai_set.filter(barang__jenis_kendaraan=2).filter(tanggal=sekarang)
        else:
            rs_pk = self.akadgadai_set.filter(tanggal=hari)
        nilai= 0
        for p in rs_pk:
            nilai += p.nilai
        return nilai
    
    def jumlah_aging_hp(self):
        sekarang = datetime.date.today()
        return self.akadgadai_set.filter(barang__jenis_barang=1).filter(tanggal=sekarang).count()
    
    def total_pinjaman_aging_hp(self,hari = None):
        sekarang = datetime.date.today()
        if not hari:            
            rs_pk = self.akadgadai_set.filter(barang__jenis_barang=1).filter(tanggal=sekarang)
        else:
            rs_pk = self.akadgadai_set.filter(tanggal=hari)
        nilai= 0
        for p in rs_pk:
            nilai += p.nilai
        return nilai
    
    def jumlah_aging_laptop(self):
        sekarang = datetime.date.today()
        return self.akadgadai_set.filter(barang__jenis_barang=2).filter(tanggal=sekarang).count()

    def total_pinjaman_aging_laptop(self,hari = None):
        sekarang = datetime.date.today()
        if not hari:            
            rs_pk = self.akadgadai_set.filter(barang__jenis_barang=2).filter(tanggal=sekarang)
        else:
            rs_pk = self.akadgadai_set.filter(tanggal=hari)
        nilai= 0
        for p in rs_pk:
            nilai += p.nilai
        return nilai
        
    def jumlah_aging_kamera(self):
        sekarang = datetime.date.today()
        return self.akadgadai_set.filter(barang__jenis_barang=3).filter(tanggal=sekarang).count()
    
    def total_pinjaman_aging_kamera(self,hari = None):
        sekarang = datetime.date.today()
        if not hari:            
            rs_pk = self.akadgadai_set.filter(barang__jenis_barang=3).filter(tanggal=sekarang)
        else:
            rs_pk = self.akadgadai_set.filter(tanggal=hari)
        nilai= 0
        for p in rs_pk:
            nilai += p.nilai
        return nilai
                
    def jumlah_aging_ps(self):
        sekarang = datetime.date.today()
        return self.akadgadai_set.filter(barang__jenis_barang=4).filter(tanggal=sekarang).count()
    
    def total_pinjaman_aging_ps(self,hari = None):
        sekarang = datetime.date.today()
        if not hari:            
            rs_pk = self.akadgadai_set.filter(barang__jenis_barang=4).filter(tanggal=sekarang)
        else:
            rs_pk = self.akadgadai_set.filter(tanggal=hari)
        nilai= 0
        for p in rs_pk:
            nilai += p.nilai
        return nilai
            
    def jumlah_aging_tv(self):
        sekarang = datetime.date.today()
        return self.akadgadai_set.filter(barang__jenis_barang=5).filter(tanggal=sekarang).count()        
    
    def total_pinjaman_aging_tv(self,hari = None):
        sekarang = datetime.date.today()
        if not hari:            
            rs_pk = self.akadgadai_set.filter(barang__jenis_barang=5).filter(tanggal=sekarang)
        else:
            rs_pk = self.akadgadai_set.filter(tanggal=hari)
        nilai= 0
        for p in rs_pk:
            nilai += p.nilai
        return nilai

    def total_aging_hari(self):
        return self.total_pinjaman_aging_motor() + self.total_pinjaman_aging_mobil() + self.total_pinjaman_aging_hp() + self.total_pinjaman_aging_laptop() + self.total_pinjaman_aging_kamera() + self.total_pinjaman_aging_ps() + self.total_pinjaman_aging_tv()

    ### REPORT AGING ALL GERAI Penerimaan Barang Harian    
        ### REPORT AGING ALL GERAI Lelang Barang Harian

    def lelang_aging_motor(self):
        sekarang = datetime.date.today()
        return self.akadgadai_set.filter(barang__jenis_kendaraan=1).filter(status_transaksi='LELANG').filter(baranglelang__tgl_lelang=sekarang).count()
    
    def total_lelang_aging_motor(self,hari = None):
        sekarang = datetime.date.today()
        if not hari:            
            rs_pk = self.akadgadai_set.filter(barang__jenis_kendaraan=1).filter(status_transaksi='LELANG').filter(baranglelang__tgl_lelang=sekarang)
        else:
            rs_pk = self.akadgadai_set.filter(tanggal=hari)
        nilai= 0
        for p in rs_pk:
            nilai += p.nilai
        return nilai
    
    def lelang_aging_mobil(self):
        sekarang = datetime.date.today()
        return self.akadgadai_set.filter(barang__jenis_kendaraan=2).filter(status_transaksi='LELANG').filter(baranglelang__tgl_lelang=sekarang).count()
    
    def total_lelang_aging_mobil(self,hari = None):
        sekarang = datetime.date.today()
        if not hari:            
            rs_pk = self.akadgadai_set.filter(barang__jenis_kendaraan=2).filter(status_transaksi='LELANG').filter(baranglelang__tgl_lelang=sekarang)
        else:
            rs_pk = self.akadgadai_set.filter(tanggal=hari)
        nilai= 0
        for p in rs_pk:
            nilai += p.nilai
        return nilai

    def lelang_aging_hp(self):
        sekarang = datetime.date.today()
        return self.akadgadai_set.filter(barang__jenis_barang=1).filter(status_transaksi='LELANG').filter(baranglelang__tgl_lelang=sekarang).count()
    
    def total_lelang_aging_hp(self,hari = None):
        sekarang = datetime.date.today()
        if not hari:            
            rs_pk = self.akadgadai_set.filter(barang__jenis_barang=1).filter(status_transaksi='LELANG').filter(baranglelang__tgl_lelang=sekarang)
        else:
            rs_pk = self.akadgadai_set.filter(tanggal=hari)
        nilai= 0
        for p in rs_pk:
            nilai += p.nilai
        return nilai
    
    def lelang_aging_laptop(self):
        sekarang = datetime.date.today()
        return self.akadgadai_set.filter(barang__jenis_barang=2).filter(status_transaksi='LELANG').filter(baranglelang__tgl_lelang=sekarang).count()

    def total_lelang_aging_laptop(self,hari = None):
        sekarang = datetime.date.today()
        if not hari:            
            rs_pk = self.akadgadai_set.filter(barang__jenis_barang=2).filter(status_transaksi='LELANG').filter(baranglelang__tgl_lelang=sekarang)
        else:
            rs_pk = self.akadgadai_set.filter(tanggal=hari)
        nilai= 0
        for p in rs_pk:
            nilai += p.nilai
        return nilai
        
    def lelang_aging_kamera(self):
        sekarang = datetime.date.today()
        return self.akadgadai_set.filter(barang__jenis_barang=3).filter(status_transaksi='LELANG').filter(baranglelang__tgl_lelang=sekarang).count()
    
    def total_lelang_aging_kamera(self,hari = None):
        sekarang = datetime.date.today()
        if not hari:            
            rs_pk = self.akadgadai_set.filter(barang__jenis_barang=3).filter(status_transaksi='LELANG').filter(baranglelang__tgl_lelang=sekarang)
        else:
            rs_pk = self.akadgadai_set.filter(tanggal=hari)
        nilai= 0
        for p in rs_pk:
            nilai += p.nilai
        return nilai
                
    def lelang_aging_ps(self):
        sekarang = datetime.date.today()
        return self.akadgadai_set.filter(barang__jenis_barang=4).filter(status_transaksi='LELANG').filter(baranglelang__tgl_lelang=sekarang).count()
    
    def total_lelang_aging_ps(self,hari = None):
        sekarang = datetime.date.today()
        if not hari:            
            rs_pk = self.akadgadai_set.filter(barang__jenis_barang=4).filter(status_transaksi='LELANG').filter(baranglelang__tgl_lelang=sekarang)
        else:
            rs_pk = self.akadgadai_set.filter(tanggal=hari)
        nilai= 0
        for p in rs_pk:
            nilai += p.nilai
        return nilai
            
    def lelang_aging_tv(self):
        sekarang = datetime.date.today()
        return self.akadgadai_set.filter(barang__jenis_barang=5).filter(status_transaksi='LELANG').filter(baranglelang__tgl_lelang=sekarang).count()
    
    def total_lelang_aging_tv(self,hari = None):
        sekarang = datetime.date.today()
        if not hari:            
            rs_pk = self.akadgadai_set.filter(barang__jenis_barang=5).filter(status_transaksi='LELANG').filter(baranglelang__tgl_lelang=sekarang)
        else:
            rs_pk = self.akadgadai_set.filter(tanggal=hari)
        nilai= 0
        for p in rs_pk:
            nilai += p.nilai
        return nilai

    def total_lelangaging_hari(self):
        return self.total_lelang_aging_motor() + self.total_lelang_aging_mobil() + self.total_lelang_aging_hp() + self.total_lelang_aging_laptop() + self.total_lelang_aging_kamera() + self.total_lelang_aging_ps() + self.total_lelang_aging_tv()
    ### AKHIR REPORT AGING ALL GERAI Lelang Barang Harian

        ### REPORT AGING ALL GERAI Pelunasan Barang Harian

    def pelunasan_aging_motor(self):
        sekarang = datetime.date.today()
        return self.akadgadai_set.filter(barang__jenis_kendaraan=1).filter(status_transaksi='LUNAS').filter(pelunasan__tanggal=sekarang).count()
    
    def total_pelunasan_aging_motor(self,hari = None):
        sekarang = datetime.date.today()
        if not hari:            
            rs_pk = self.akadgadai_set.filter(barang__jenis_kendaraan=1).filter(status_transaksi='LUNAS').filter(pelunasan__tanggal=sekarang)
        else:
            rs_pk = self.akadgadai_set.filter(tanggal=hari)
        nilai= 0
        for p in rs_pk:
            nilai += p.nilai
        return nilai
    
    def pelunasan_aging_mobil(self):
        sekarang = datetime.date.today()
        return self.akadgadai_set.filter(barang__jenis_kendaraan=2).filter(status_transaksi='LUNAS').filter(pelunasan__tanggal=sekarang).count()
    
    def total_pelunasan_aging_mobil(self,hari = None):
        sekarang = datetime.date.today()
        if not hari:            
            rs_pk = self.akadgadai_set.filter(barang__jenis_kendaraan=2).filter(status_transaksi='LUNAS').filter(pelunasan__tanggal=sekarang)
        else:
            rs_pk = self.akadgadai_set.filter(tanggal=hari)
        nilai= 0
        for p in rs_pk:
            nilai += p.nilai
        return nilai

    def pelunasan_aging_hp(self):
        sekarang = datetime.date.today()
        return self.akadgadai_set.filter(barang__jenis_barang=1).filter(status_transaksi='LUNAS').filter(pelunasan__tanggal=sekarang).count()
    
    def total_pelunasan_aging_hp(self,hari = None):
        sekarang = datetime.date.today()
        if not hari:            
            rs_pk = self.akadgadai_set.filter(barang__jenis_barang=1).filter(status_transaksi='LUNAS').filter(pelunasan__tanggal=sekarang)
        else:
            rs_pk = self.akadgadai_set.filter(tanggal=hari)
        nilai= 0
        for p in rs_pk:
            nilai += p.nilai
        return nilai
    
    def pelunasan_aging_laptop(self):
        sekarang = datetime.date.today()
        return self.akadgadai_set.filter(barang__jenis_barang=2).filter(status_transaksi='LUNAS').filter(pelunasan__tanggal=sekarang).count()

    def total_pelunasan_aging_laptop(self,hari = None):
        sekarang = datetime.date.today()
        if not hari:            
            rs_pk = self.akadgadai_set.filter(barang__jenis_barang=2).filter(status_transaksi='LUNAS').filter(pelunasan__tanggal=sekarang)
        else:
            rs_pk = self.akadgadai_set.filter(tanggal=hari)
        nilai= 0
        for p in rs_pk:
            nilai += p.nilai
        return nilai
        
    def pelunasan_aging_kamera(self):
        sekarang = datetime.date.today()
        return self.akadgadai_set.filter(barang__jenis_barang=3).filter(status_transaksi='LUNAS').filter(pelunasan__tanggal=sekarang).count()
    
    def total_pelunasan_aging_kamera(self,hari = None):
        sekarang = datetime.date.today()
        if not hari:            
            rs_pk = self.akadgadai_set.filter(barang__jenis_barang=3).filter(status_transaksi='LUNAS').filter(pelunasan__tanggal=sekarang)
        else:
            rs_pk = self.akadgadai_set.filter(tanggal=hari)
        nilai= 0
        for p in rs_pk:
            nilai += p.nilai
        return nilai
                
    def pelunasan_aging_ps(self):
        sekarang = datetime.date.today()
        return self.akadgadai_set.filter(barang__jenis_barang=4).filter(status_transaksi='LUNAS').filter(pelunasan__tanggal=sekarang).count()
    
    def total_pelunasan_aging_ps(self,hari = None):
        sekarang = datetime.date.today()
        if not hari:            
            rs_pk = self.akadgadai_set.filter(barang__jenis_barang=4).filter(status_transaksi='LUNAS').filter(pelunasan__tanggal=sekarang)
        else:
            rs_pk = self.akadgadai_set.filter(tanggal=hari)
        nilai= 0
        for p in rs_pk:
            nilai += p.nilai
        return nilai
            
    def pelunasan_aging_tv(self):
        sekarang = datetime.date.today()
        return self.akadgadai_set.filter(barang__jenis_barang=5).filter(status_transaksi='LUNAS').filter(pelunasan__tanggal=sekarang).count()
    
    def total_pelunasan_aging_tv(self,hari = None):
        sekarang = datetime.date.today()
        if not hari:            
            rs_pk = self.akadgadai_set.filter(barang__jenis_barang=5).filter(status_transaksi='LUNAS').filter(pelunasan__tanggal=sekarang)
        else:
            rs_pk = self.akadgadai_set.filter(tanggal=hari)
        nilai= 0
        for p in rs_pk:
            nilai += p.nilai
        return nilai

    def total_lunasaging_hari(self):
        return self.total_pelunasan_aging_motor() + self.total_pelunasan_aging_mobil() + self.total_pelunasan_aging_hp() + self.total_pelunasan_aging_laptop() + self.total_pelunasan_aging_kamera() + self.total_pelunasan_aging_ps() + self.total_pelunasan_aging_tv()
    ### AKHIR REPORT AGING ALL GERAI Pelunasan Barang Harian

    ### REPORT AGING ALL GERAI Retur Barang Harian
    def retur_aging_motor(self):
        sekarang = datetime.date.today()
        return self.akadgadai_set.filter(barang__jenis_kendaraan=1).filter(tanggal_permintaan=sekarang).filter(status_permintaan="2").count()
    
    def total_retur_aging_motor(self,hari = None):
        sekarang = datetime.date.today()
        if not hari:            
            rs_pk = self.akadgadai_set.filter(barang__jenis_kendaraan=1).filter(tanggal_permintaan=sekarang).filter(status_permintaan="2")
        else:
            rs_pk = self.akadgadai_set.filter(tanggal=hari)
        nilai= 0
        for p in rs_pk:
            nilai += p.nilai
        return nilai
    
    def retur_aging_mobil(self):
        sekarang = datetime.date.today()
        return self.akadgadai_set.filter(barang__jenis_kendaraan=2).filter(tanggal_permintaan=sekarang).filter(status_permintaan="2").count()
    
    def total_retur_aging_mobil(self,hari = None):
        sekarang = datetime.date.today()
        if not hari:            
            rs_pk = self.akadgadai_set.filter(barang__jenis_kendaraan=2).filter(tanggal_permintaan=sekarang).filter(status_permintaan="2")
        else:
            rs_pk = self.akadgadai_set.filter(tanggal=hari)
        nilai= 0
        for p in rs_pk:
            nilai += p.nilai
        return nilai

    def retur_aging_hp(self):
        sekarang = datetime.date.today()
        return self.akadgadai_set.filter(barang__jenis_barang=1).filter(tanggal_permintaan=sekarang).filter(status_permintaan="2").count()
    
    def total_retur_aging_hp(self,hari = None):
        sekarang = datetime.date.today()
        if not hari:            
            rs_pk = self.akadgadai_set.filter(barang__jenis_barang=1).filter(tanggal_permintaan=sekarang).filter(status_permintaan="2")
        else:
            rs_pk = self.akadgadai_set.filter(tanggal=hari)
        nilai= 0
        for p in rs_pk:
            nilai += p.nilai
        return nilai    

    def retur_aging_laptop(self):
        sekarang = datetime.date.today()
        return self.akadgadai_set.filter(barang__jenis_barang=2).filter(tanggal_permintaan=sekarang).filter(status_permintaan="2").count()

    def total_retur_aging_laptop(self,hari = None):
        sekarang = datetime.date.today()
        if not hari:            
            rs_pk = self.akadgadai_set.filter(barang__jenis_barang=2).filter(tanggal_permintaan=sekarang).filter(status_permintaan="2")
        else:
            rs_pk = self.akadgadai_set.filter(tanggal=hari)
        nilai= 0
        for p in rs_pk:
            nilai += p.nilai
        return nilai
        
    def retur_aging_kamera(self):
        sekarang = datetime.date.today()
        return self.akadgadai_set.filter(barang__jenis_barang=3).filter(tanggal_permintaan=sekarang).filter(status_permintaan="2").count()
    
    def total_retur_aging_kamera(self,hari = None):
        sekarang = datetime.date.today()
        if not hari:            
            rs_pk = self.akadgadai_set.filter(barang__jenis_barang=3).filter(tanggal_permintaan=sekarang).filter(status_permintaan="2")
        else:
            rs_pk = self.akadgadai_set.filter(tanggal=hari)
        nilai= 0
        for p in rs_pk:
            nilai += p.nilai
        return nilai
                
    def retur_aging_ps(self):
        sekarang = datetime.date.today()
        return self.akadgadai_set.filter(barang__jenis_barang=4).filter(tanggal_permintaan=sekarang).filter(status_permintaan="2").count()
    
    def total_retur_aging_ps(self,hari = None):
        sekarang = datetime.date.today()
        if not hari:            
            rs_pk = self.akadgadai_set.filter(barang__jenis_barang=4).filter(tanggal_permintaan=sekarang).filter(status_permintaan="2")
        else:
            rs_pk = self.akadgadai_set.filter(tanggal=hari)
        nilai= 0
        for p in rs_pk:
            nilai += p.nilai
        return nilai
            
    def retur_aging_tv(self):
        sekarang = datetime.date.today()
        return self.akadgadai_set.filter(barang__jenis_barang=5).filter(tanggal_permintaan=sekarang).filter(status_permintaan="2").count()        
    def total_retur_aging_tv(self,hari = None):
        sekarang = datetime.date.today()
        if not hari:            
            rs_pk = self.akadgadai_set.filter(barang__jenis_barang=5).filter(tanggal_permintaan=sekarang).filter(status_permintaan="2")
        else:
            rs_pk = self.akadgadai_set.filter(tanggal=hari)
        nilai= 0
        for p in rs_pk:
            nilai += p.nilai
        return nilai

    def total_returaging_hari(self):
        return self.total_retur_aging_motor() + self.total_retur_aging_mobil() + self.total_retur_aging_hp() + self.total_retur_aging_laptop() + self.total_retur_aging_kamera() + self.total_retur_aging_ps() + self.total_retur_aging_tv()        
    ### AKHIR REPORT AGING ALL GERAI Retur Barang Harian

    ##AKHIR TAMBAHAN ADM GUADANG AKTIF        
class Tbl_Product(models.Model):
    kode_produk= models.IntegerField(max_length=1)
    nama_produk = models.CharField(max_length=30,null=True)

    class Meta:
        db_table ="tbl_product"
    
class Tbl_Unit(models.Model):
    kode_unit = models.CharField(max_length=3)
    nama_unit = models.CharField(max_length=30)
    
    class Meta:
        db_table ="tbl_unit"

STATUS_LIMIT=(
    ('1','Aktif'),
    ('2','Non AKtif'),    
)

class Limit_PetyCash(models.Model):
    nilai =  models.DecimalField(max_digits=12, decimal_places=2)
    tanggal=models.DateField()
    status = models.CharField(max_length=4 ,choices=STATUS_LIMIT, null=True, blank=True)
    cu = models.ForeignKey(User, related_name='+', editable=False, null=True, blank=True)
    mu = models.ForeignKey(User, related_name='+', editable=False, null=True, blank=True)
    class Meta:
        db_table ="limit_petycash"

STATUS_LUNAS=(
    ('1','LUNAS'),
    ('2','BLM LUNAS'),    
)

STATUS_OTORISASI=(
    ('1','---------'),
    ('2','DEVIASI'),
)

class LogPelunasan(models.Model):
    norek = models.CharField(max_length =50)
    status = models.CharField(max_length =50)
    tanggal=models.DateField()
    nilai = models.DecimalField(max_digits=12, decimal_places=2)
    terlambat = models.DecimalField(max_digits=12, decimal_places=2,default=0)
    gerai = models.CharField(max_length=50)

    nilai_jasa = models.DecimalField(max_digits=12, decimal_places=2,null=True,blank=True,default=0)
    nilai_jasa_kendaraan = models.DecimalField(max_digits=12, decimal_places=2,null=True,blank=True,default=0)
    nilai_denda = models.DecimalField(max_digits=12, decimal_places=2,null=True,blank=True,default=0)
    nilai_denda_kendaraan = models.DecimalField(max_digits=12, decimal_places=2,null=True,blank=True,default=0)
    jenis_barang = models.CharField(max_length =50)

    cu = models.ForeignKey(User, related_name='+', editable=False, null=True, blank=True)
    mu = models.ForeignKey(User, related_name='+', editable=False, null=True, blank=True)
    cdate = models.DateTimeField(auto_now_add=True)
    mdate = models.DateTimeField(auto_now=True)
         
    def __unicode__(self):
        return '%s %s' % (self.id, self.tanggal)
        
    class Meta:
        db_table ="logpelunasan"
        verbose_name= "LogPelunasan"
        verbose_name_plural = verbose_name
        get_latest_by = 'tanggal'
        ordering = ['-tanggal']

STS_PLNS =(
    ('1','Lepas'),
    ('2','Lunas GU'),
    ('3','Lunas Terjual')
)

class Pelunasan(models.Model):
    pelunasan = models.ForeignKey(AkadGadai)
    status_pelunasan= models.CharField(max_length=4 ,choices=STATUS_LUNAS, null=True, blank=True)
    tanggal=models.DateField()
    
    nilai = models.DecimalField(max_digits=12, decimal_places=2)
    terlambat = models.DecimalField(max_digits=12, decimal_places=2,default=0)
    denda = models.DecimalField(max_digits=12, decimal_places=2)
    bea_jasa = models.DecimalField(max_digits=12, decimal_places=2)
    gerai = models.ForeignKey (Tbl_Cabang)
    ###kendaraan
    jenis_barang= models.CharField(max_length=20 ,null=True, blank=True)
    terlambat_kendaraan = models.DecimalField(max_digits=12, decimal_places=2,default=0,null=True, blank=True)
    nilai_lebih = models.DecimalField(max_digits=12, decimal_places=2,default=0,null=True, blank=True)
    denda_kendaraan = models.DecimalField(max_digits=12, decimal_places=2,blank=True,null=True)
    bea_jasa_kendaraan = models.DecimalField(max_digits=12, decimal_places=2,default=0,blank=True,null=True)
    nocoa_titipan = models.CharField(max_length=15,blank=True,null=True)
    nocoa_kas = models.CharField(max_length=15,blank=True,null=True)
    val = models.CharField(max_length=3,blank=True,null=True)
    cu = models.ForeignKey(User, related_name='c_pelunasan', editable=False, null=True, blank=True)
    mu = models.ForeignKey(User, related_name='m_pelunasan', editable=False, null=True, blank=True)
    cdate = models.DateTimeField(auto_now_add=True)
    mdate = models.DateTimeField(auto_now=True)
    #nilai = models.DecimalField(max_digits=12, decimal_places=2,default=0,null=True, blank=True)
    status_kwlunas = models.CharField(max_length=10,blank=True,null=True)
    comment = models.CharField(max_length=100,blank=True,null=True)
    status = models.CharField(max_length=10,choices=STATUS_OTORISASI,blank=True,null=True)
    sts_plns = models.CharField(max_length=10,choices=STS_PLNS,blank=True,null=True)
    
    def __unicode__(self):
        return '%s %s' % (self.pelunasan, self.tanggal)
        
    class Meta:
        db_table ="pelunasan"
        verbose_name= "Pelunasan"
        verbose_name_plural = verbose_name
        get_latest_by = 'tanggal'
        ordering = ['-tanggal']

    def get_bea_jasa_total(self):
        return self.bea_jasa + self.bea_jasa_kendaraan   
    total_jasa_plns = property(get_bea_jasa_total) 

    def denda_total_filter(self):
        return self.denda + self.denda_kendaraan
    total_denda_filter = property(denda_total_filter)
        
    def kwlunas_validasi(self):
        return "KL %s %s %s %s %s WIB %s" % ((self.pelunasan.norek()),self.nocoa_titipan,self.nilai,self.nocoa_kas,self.pelunasan.mdate,(str(self.pelunasan.gerai.init_cabang))) 
        
    def total_terima_bersih_plns(self):
        return self.denda_all() + self.bea_jasa_total+ self.nilaimas

    def get_absolute_url(self):
        return "/akadgadai/%s/show/" % self.pelunasan.id
    
    def cekkasirgerai(self):
        try:
            s = self.kasirgerai
            ret = s.status=='1'
        except KasirGerai.DoesNotExist:
            ret = False
        return ret
    
    def denda_all(self):
        if self.jenis_barang == u'1':
            return (self.denda) + (self.bea_jasa)
        else:
            return (self.denda_kendaraan) + (self.bea_jasa_kendaraan)

    def denda_all_rekap(self):
        if self.jenis_barang == u'1':
            return (self.denda)
        else:
            return (self.denda_kendaraan)
    
    def jasa_all(self):
        if self.jenis_barang == u'1':
            return self.bea_jasa
        else:
            return self.bea_jasa_kendaraan

    def akumulasi_jasa_denda(self):
        return self.denda_all() + self.jasa_all()

     ####JUMLAH BEA JASA & DENDA####
    def get_jasa_denda(self):
        D = decimal.Decimal
        return  self.bea_jasa + self.denda + D(self.bea_jasa_kendaraan) + self.denda_kendaraan
    jasa_denda = property(get_jasa_denda)
    
    def get_jasa_denda_kendaraan(self):
        return  self.bea_jasa_kendaraan + self.denda_kendaraan
    jasa_denda_kendaraan = property(get_jasa_denda_kendaraan)
    
    ###18 april 2013
    @property
    def bea_jasa_total(self):
        return self.bea_jasa + self.bea_jasa_kendaraan
    
    @property
    def denda_total(self):
        return self.denda + self.denda_kendaraan
    ####rekap haraian gerai
    @property
    def tot_jasa_denda_plns(self):
        return self.bea_jasa_total + self.denda_total
    ###18 april 2013

    ####TOTAL PELUNASAN####
    def get_jumlah_pelunasan(self):
        return self.nilai + self.jasa_denda
    jumlah_pelunasan = property(get_jumlah_pelunasan)

    def get_jumlah_pelunasan_kendaraan(self):
        return ((self.nilai)) + self.get_jasa_denda_kendaraan()
    jumlah_pelunasan_kendaraan = property(get_jumlah_pelunasan_kendaraan)
    
    def norek(self):
        return "%s.%s.%s" % (str(self.gerai.kode_cabang).zfill(2),str(self.tanggal.year).zfill(1),str(self.id).zfill(6))
  
STATUS_MANOP_PELUNASAN =(
    ('1','OTORISAI'),
    ('2','OTORISAI OK')
)

ITEM_JURNAL=(
    ('parkir','PARKIR'),('bbm','BBM'),('materai','MATERAI'),('fotocopy','FOTO COPY'),('lingkungan','LINGKUNGAN'),
    ('sumbangan','SUMBANGAN'),('perlengkapan','PERLENGKAPAN'),('konsumsi','KONSUMSI'),('majalah','MAJALAH'),('listrik','LISTRIK'),
    ('telepon','TELEPON'),('pdam','PDAM'),('sewa','SEWA'),('gaji','GAJI'),('transport','TRANSPORT'),
    ('peralkantor','PERALKANTOR'),('adm_bank','ADM BANK'),('pengiriman','PENGIRIMAN'),
    ('penjualan_materai','PENJUALAN MATERAI'),('pembelian_materai','Pembelian Materai'),
)

class BiayaMapper(models.Model):
    item = models.CharField(max_length=50,null=True,blank=True,choices=ITEM_JURNAL)
    cabang = models.ForeignKey(Tbl_Cabang)
    coa_debet = models.ForeignKey(Tbl_Akun,related_name="+",blank=True,null=True)
    coa = models.ForeignKey(Tbl_Akun,related_name="+",blank=True,null=True)
    coa_uk = models.ForeignKey(Tbl_Akun,related_name="+",blank=True,null=True)

    class Meta:
       db_table = 'biayamapper'

    def get_absolute_url(self):
        return "/parameterjurnal/jurnal_biaya/"


ITEM_GERAI_PUSAT=(
    ('parkir','PARKIR'),('bbm','BBM'),
    ('sumbangan','SUMBANGAN'),('listrik','LISTRIK'),
    ('telepon','TELEPON'),('pdam','PDAM'),
    ('transport','PEMELIHARAAN TRANSPORT'),('lain-lain','LAIN-LAIN'),
    ('parkir_bank','PARKIR BANK'),('bbm_bank','BBM BANK'),
    ('sumbangan_bank','SUMBANGAN BANK'),('listrik_bank','LISTRIK BANK'),
    ('telepon_bank','TELEPON BANK'),('pdam_bank','PDAM BANK'),
    ('transport_bank','PEMELIHARAAN TRANSPORT BANK'),('lain-lain_bank','LAIN-LAIN BANK')
)

class BiayaMapperdiBayarPusat(models.Model):
    item = models.CharField(max_length=50,null=True,blank=True,choices=ITEM_GERAI_PUSAT)
    cabang = models.ForeignKey(Tbl_Cabang)
    coa_debet_pusat = models.ForeignKey(Tbl_Akun,related_name="+",blank=True,null=True)
    coa_kredit_pusat = models.ForeignKey(Tbl_Akun,related_name="+",blank=True,null=True)
    coa_debet_gerai = models.ForeignKey(Tbl_Akun,related_name="+",blank=True,null=True)
    coa_kredit_gerai = models.ForeignKey(Tbl_Akun,related_name="+",blank=True,null=True)

    class Meta:
       db_table = 'biayamapperdibayarpusat'

CHOICES_PRODUK=(
    ('1','BULANAN'),
    ('2','MINGGUAN'),
    ('3','HARIAN'),
    )

CHOICES_AKTIFASI=(
    ('1','AKTIF'),
    ('2','NON AKTIF'),    
    )

JENIS_TRANSAKSI_PARAMETER=(
    ('1','Elektronik'),
    ('2','Motor'),
    ('3','Mobil'),
)
JENIS_KREDIT=(
    ('300','PJB'),
    ('301','MF'),
    ('302','KRESUN'),
)
class ParameterProduk(models.Model):
    jenis_kredit = models.CharField(max_length=50,null=True,blank=True,choices=JENIS_KREDIT)
    jenis = models.CharField(max_length=50,null=True,blank=True,choices=CHOICES_PRODUK_PARAM)
    jenis_transaksi = models.CharField(max_length=20 ,choices=JENIS_TRANSAKSI_PARAMETER, null=True, blank=True)
    aktif = models.CharField(max_length=50,null=True,blank=True,choices=CHOICES_AKTIFASI)
    tanggal = models.DateField(null=True,blank=True)
    jasa = models.DecimalField(max_digits=12, decimal_places=2,null=True,blank=True,default=0)
    denda = models.DecimalField(max_digits=12, decimal_places=2,null=True,blank=True,default=0)
    denda_terlambat = models.DecimalField(max_digits=12, decimal_places=2,null=True,blank=True,default=0)
    adm = models.DecimalField(max_digits=12, decimal_places=2,null=True,blank=True,default=0)
    provisi = models.DecimalField(max_digits=12, decimal_places=2,null=True,blank=True,default=0)
    asuransi = models.DecimalField(max_digits=12, decimal_places=2,null=True,blank=True,default=0)
    biayasimpan = models.DecimalField(max_digits=12, decimal_places=2,null=True,blank=True,default=0)
    materai = models.DecimalField(max_digits=12, decimal_places=2,null=True,blank=True,default=0)
    jenis_barang = models.CharField(max_length=4 ,choices=JENIS_AGUNAN, null =True, blank=True,default=0)
    jw = models.CharField(max_length=4 , null =True, blank=True)
    pembagi = models.CharField(max_length=4 , null =True, blank=True)
        
    class Meta:
       db_table = 'parameterproduk'

class RakPusatMapper(models.Model):
    cabang = models.ForeignKey(Tbl_Cabang)
    coa_rak_cabang = models.ForeignKey(Tbl_Akun,related_name="+",blank=True,null=True)
    coa_rak_pusat = models.ForeignKey(Tbl_Akun,related_name="+",blank=True,null=True)
    class Meta:
       db_table = 'rakpusatmapper'

    def get_absolute_url(self):
        return "/parameterjurnal/rak_pusat/"

JENIS_BIAYA_PUSAT =(
    ('1','Kas'),
    ('2','Uang Muka'),
)

class BiayaPusatMapper(models.Model):
    item = models.CharField(max_length=50,null=True,blank=True,choices=ITEM_JURNAL)
    cabang = models.ForeignKey(Tbl_Cabang)
    jenis = models.CharField(max_length=50,null=True,blank=True,choices=JENIS_BIAYA_PUSAT)
    cabang_tuju = models.ForeignKey(Tbl_Cabang,related_name="+",blank=True,null=True)
    coa_debet = models.ForeignKey(Tbl_Akun,related_name="+",blank=True,null=True)    
    coa = models.ForeignKey(Tbl_Akun,related_name="+",blank=True,null=True)
    coa_uk = models.ForeignKey(Tbl_Akun,related_name="+",blank=True,null=True)
    coa_debet_tuju = models.ForeignKey(Tbl_Akun,related_name="+",blank=True,null=True)
    coa_kredit_tuju = models.ForeignKey(Tbl_Akun,related_name="+",blank=True,null=True)

    class Meta:
       db_table = 'biayapusatmapper'

    def get_absolute_url(self):
        return "/parameterjurnal/biaya_pusat/"

ITEM_UANGMUKA_NEW=(
    ('1','PENGAMBILAN UANG MUKA'),
    ('2','PENGEMBALIAN UANG MUKA'),
)

class UangMukaGeraiMapper(models.Model):
    item = models.CharField(max_length=50,null=True,blank=True,choices=ITEM_UANGMUKA_NEW)
    cabang = models.ForeignKey(Tbl_Cabang)
    debet_pengembalian_uk = models.ForeignKey(Tbl_Akun,related_name="+",null = True,blank=True)
    kredit_pengembalian_uk = models.ForeignKey(Tbl_Akun,related_name="+",null = True,blank=True)
    debet_pengambilan_uk  = models.ForeignKey(Tbl_Akun,related_name="+",null = True,blank=True)
    kredit_pengambilan_uk  = models.ForeignKey(Tbl_Akun,related_name="+",null = True,blank=True)

    class Meta:
       db_table = 'uangmukageraimapper'

    def get_absolute_url(self):
        return "/parameterjurnal/uangmuka_gerai/"



PELUNASAN_KASIR=(
    ('1','Jurnal pelunasan Bank lebih'),
    ('2','Jurnal Pelunasan Bank Nilai sama'),      
    ('3','Jurnal Pelunasan Bank Nilai kurang'),     
    ('4','Jurnal Pelunasan Kas Nilai lebih'),
    ('5','Jurnal Pelunasan Kas Nilai sama'),
    ('6','Jurnal Pelunasan Kas Nilai kurang'), 
    ('7','Jurnal Pelunasan Kas Nilai Titipan Kas'),
    ('8','Jurnal Pelunasan Kas Nilai Titipan Bank'), 
    ('9','Jurnal Pelunasan Bank Pendapatan'),
    ('10','Jurnal Pelunasan Bank Titipan Kelebihan'),
    ('11','Jurnal Pelunasan Bank Pendapatan Titipan Kelebihan'),
)

JENIS_TRANS =(
    ('1','Bank'),
    ('2','Kas'),
)

class KasirPelunasanMapper(models.Model):
    item = models.CharField(max_length=50,null=True,blank=True,choices=PELUNASAN_KASIR)
    jenis = models.CharField(max_length=50,null=True,blank=True,choices=JENIS_TRANS)
    cabang = models.ForeignKey(Tbl_Cabang,related_name="+",blank=True,null=True)
    ke_cabang = models.ForeignKey(Tbl_Cabang,blank=True,null=True,related_name="+")
    coa_1 = models.ForeignKey(Tbl_Akun,related_name="+",null=True,blank=True)
    coa_2 = models.ForeignKey(Tbl_Akun,related_name="+",null=True,blank=True)
    coa_3 = models.ForeignKey(Tbl_Akun,related_name="+",null=True,blank=True)
    coa_4 = models.ForeignKey(Tbl_Akun,related_name="+",null=True,blank=True)
    coa_5 = models.ForeignKey(Tbl_Akun,related_name="+",null=True,blank=True)
    #debet_rak_cabang= models.ForeignKey(Tbl_Akun,blank=True,null=True,related_name="+")
    #kredit_rak_pusat= models.ForeignKey(Tbl_Akun,blank=True,null=True,related_name="+")
    #tanggal = models.DateField(null=True,blank=True)

    class Meta:
       db_table = 'kasirpelunasanmapper'

JENIS_RAK=(
     ('1','RAK PUSAT'),
)

class KasirPelunasanRakMapper(models.Model):
    item = models.CharField(max_length=50,null=True,blank=True,choices=JENIS_RAK)
    jenis = models.CharField(max_length=50,null=True,blank=True,choices=JENIS_TRANS)
    cabang = models.ForeignKey(Tbl_Cabang,related_name="+",blank=True,null=True)
    ke_cabang = models.ForeignKey(Tbl_Cabang,blank=True,null=True,related_name="+")
    coa_1 = models.ForeignKey(Tbl_Akun,related_name="+",null=True,blank=True)
    coa_2 = models.ForeignKey(Tbl_Akun,related_name="+",null=True,blank=True)
    coa_3 = models.ForeignKey(Tbl_Akun,related_name="+",null=True,blank=True)
    coa_4 = models.ForeignKey(Tbl_Akun,related_name="+",null=True,blank=True)
    debet_rak_cabang= models.ForeignKey(Tbl_Akun,blank=True,null=True,related_name="+")
    kredit_rak_pusat= models.ForeignKey(Tbl_Akun,blank=True,null=True,related_name="+")
    rak_debet_pusat1= models.ForeignKey(Tbl_Akun,blank=True,null=True,related_name="+")
    rak_kredit_pusat2= models.ForeignKey(Tbl_Akun,blank=True,null=True,related_name="+")

    class Meta:
       db_table = 'kasirpelunasanrakmapper'

ITEM_K_PENCAIRAN=(
    ('pencairan_kas_sama','Pencairan Kas Sama'),('pencairan_kas_nilai_kecil','Pencairan Kas Nilai Kecil'),
    ('pencairan_kas_nilai_besar','Pencairan Kas Nilai Besar'),
    )

class KasirPencairanMapper(models.Model):
    tanggal = models.DateField()
    item = models.CharField(max_length=50,null=True,blank=True,choices=ITEM_K_PENCAIRAN)
    cabang = models.ForeignKey(Tbl_Cabang)
    coa_debet = models.ForeignKey(Tbl_Akun,related_name="+",null=True,blank=True)
    coa_debet_satu = models.ForeignKey(Tbl_Akun,related_name="+",null=True,blank=True)
    coa_kredit = models.ForeignKey(Tbl_Akun,related_name="+",null=True,blank=True)
    coa_kredit_satu = models.ForeignKey(Tbl_Akun,related_name="+",null=True,blank=True)

    class Meta:
       db_table = 'kasirpencairanmapper'
       ordering = ['-tanggal']

ITEM_BANK_PENCAIRAN=(
    ('pencairan_bank_sama','Pencairan Bank Sama'),('pencairan_bank_nilai_kecil','Pencairan Bank Nilai Kecil'),
    ('pencairan_bank_nilai_besar','Pencairan Bank Nilai Besar'),
    )

class KasirPencairanBankMapper(models.Model):####BANK
    tanggal = models.DateField()
    item = models.CharField(max_length=50,null=True,blank=True,choices=ITEM_BANK_PENCAIRAN)
    cabang = models.ForeignKey(Tbl_Cabang)
    coa_debet = models.ForeignKey(Tbl_Akun,related_name="+" ,null=True,blank=True)
    coa_debet_satu = models.ForeignKey(Tbl_Akun,related_name="+" ,null=True,blank=True)
    coa_kredit = models.ForeignKey(Tbl_Akun,related_name="+" ,null=True,blank=True)
    coa_kredit_satu = models.ForeignKey(Tbl_Akun,related_name="+" ,null=True,blank=True)

    class Meta:
       db_table = 'kasirpencairanbankmapper'
       ordering = ['-tanggal']


ITEM_GULANG=(
    ('pinjaman_sama_bayar_sama','Pinjaman sama Bayar sama'),
    ('pinjaman_sama_bayar_lebih','Pinjaman Sama Bayar Lebih'),
    ('pinjaman_sama_bayar_kurang','Pinjaman Sama Bayar Kurang'),
    #('pinjaman_kurang_bayar_lebih','Pinjaman Kurang Bayar Lebih'),
    ('pinjaman_lebih_bayar_sama','Pinjaman Lebih Bayar Sama'),
    ('pinjaman_lebih_bayar_kurang','Pinjaman Lebih Bayar Kurang'),
    ('pinjaman_lebih_bayar_lebih','Pinjaman Lebih Bayar Lebih'),####pinjaman lebih Bayar lebih belum    

    ('jurnal_bank_gu_nilai_sama','Pinjaman sama bayar sama(Bank)'),
    ('jurnal_bank_gu_nilai_lebih','Pinjaman sama bayar lebih(Bank)'),
    ('jurnal_bank_gu_nilai_kurang','Pinjaman sama bayar kurang (Bank)'),
    ('jurnal_bank_gu_nilai_lebih_pinjaman_lebih','Pinjaman Kurang bayar lebih(Bank)'),
    ('jurnal_bank_jkt_gu_nilai_sama_pinjaman_lebih','Pinjaman lebih bayar sama(Bank)'),
    ('jurnal_bank_jkt_gu_nilai_lebih_pinjaman_lebih','Pinjaman lebih bayar lebih(Bank)'),####pinjaman lebih Bayar lebih belum
    ('jurnal_bank_jkt_gu_nilai_kurang_pinjaman_lebih','Pinjaman lebih bayar kurang(Bank)'),
    ########tambahan Sepur
    ('jurnal_bank_gu_nilai_lebih_titipan','Pinjaman sama bayar lebih Titipan Kelebihan(Bank)'),
    ('jurnal_bank_gu_nilai_lebih_pendapatan','Pinjaman sama bayar lebih Pendapatan (Bank)'),
    ('jurnal_bank_gu_nilai_lebih_pendapatan_titipan','Pinjaman sama bayar lebih Pendapatan Titipan Kelebihan (Bank)'),

)

ITEM_KEMBALI_TITIP=(
    ('1','Kembali Kas'),
    ('2','Kembali Bank'),
)

class PengembalianTitipanMapper(models.Model):
    tanggal = models.DateField()
    item = models.CharField(max_length=50,choices=ITEM_KEMBALI_TITIP)
    cabang = models.ForeignKey(Tbl_Cabang)
    coa_1 = models.ForeignKey(Tbl_Akun,related_name="+",blank=True,null=True)
    coa_2 = models.ForeignKey(Tbl_Akun,related_name="+",blank=True,null=True)

    cu = models.ForeignKey(User, related_name='+', editable=False, null=True, blank=True)
    mu = models.ForeignKey(User, related_name='+', editable=False, null=True, blank=True)
    
    class Meta:
       db_table = 'pengembaliantitipanmapper'

class PengembalianTitipanGadaiUlangMapper(models.Model):
    tanggal = models.DateField()
    item = models.CharField(max_length=50,choices=ITEM_KEMBALI_TITIP)
    cabang = models.ForeignKey(Tbl_Cabang)
    coa_1 = models.ForeignKey(Tbl_Akun,related_name="+",blank=True,null=True)
    coa_2 = models.ForeignKey(Tbl_Akun,related_name="+",blank=True,null=True)

    cu = models.ForeignKey(User, related_name='+', editable=False, null=True, blank=True)
    mu = models.ForeignKey(User, related_name='+', editable=False, null=True, blank=True)
    
    class Meta:
       db_table = 'pengembaliantitipangadaiulangmapper'  

class GadaiUlangMapper(models.Model):
    tanggal = models.DateField()
    item = models.CharField(max_length=50,choices=ITEM_GULANG)
    cabang = models.ForeignKey(Tbl_Cabang)
    coa_titipan_pelunasan = models.ForeignKey(Tbl_Akun,related_name="+")
    coa_kas = models.ForeignKey(Tbl_Akun,related_name="+",blank=True,null=True)
    coa_pendapatan_lainnya = models.ForeignKey(Tbl_Akun,related_name="+",blank=True,null=True)
    coa_beban = models.ForeignKey(Tbl_Akun,related_name="+",blank=True,null=True)
    coa_titipan_kelebihan = models.ForeignKey(Tbl_Akun,related_name="+",blank=True,null=True)
    cu = models.ForeignKey(User, related_name='+', editable=False, null=True, blank=True)
    mu = models.ForeignKey(User, related_name='+', editable=False, null=True, blank=True)
    
    class Meta:
       db_table = 'gadaiulangmapper'
       ordering = ['-tanggal']

PUSAT_KAS_BANK =(
    ('1','Penerimaan Bank'),
    ('2','Penerimaan kas'),
    ('3','Pengeluaran Bank'),
    ('4','Pengeluaran Kas'),
)

class PusatKasBankMapper(models.Model):
    item = models.CharField(max_length=50,null=True,blank=True,choices=PUSAT_KAS_BANK)
    cabang = models.ForeignKey(Tbl_Cabang,related_name="pst_cbg")
    ke_cabang = models.ForeignKey(Tbl_Cabang,blank=True,null=True,related_name="pst_lwn_cbg")
    coa = models.ForeignKey(Tbl_Akun,related_name="pst_bank")
    coa_kredit = models.ForeignKey(Tbl_Akun,related_name="pst_bank_krd")
    coa_lawan_debet = models.ForeignKey(Tbl_Akun,blank=True,null=True,related_name="pst_lwn")
    coa_lawan_kredit = models.ForeignKey(Tbl_Akun,blank=True,null=True,related_name="pst_kredit")
    debet_rak_cabang= models.ForeignKey(Tbl_Akun,blank=True,null=True,related_name="+")
    kredit_rak_pusat= models.ForeignKey(Tbl_Akun,blank=True,null=True,related_name="+")
    class Meta:
       db_table = 'pusatkasbankmapper'

    #def get_absolute_url(self):
        #return "/parameterjurnal/jurnal_biaya/"

PENJUALAN_BARANG_GERAI =(
    ('1','Non Anggota Lelang Lebih'),
    ('2','Non Anggota Lelang Pas'),
    ('3','Non Anggota Lelang Kurang'),
    ('6','Anggota Lelang Lebih'),
    ('7','Anggota Lelang Pas'),
    ('8','Anggota Lelang Kurang'),
    ('4','Lelang Kasir Kas'),
    ('5','Lelang kasir Bank'),
    ('9','Ayda Anggota'),
    ('10','Ayda Non Anggota')
)

class GeraiPenjualanMapper(models.Model):
    item = models.CharField(max_length=50,null=True,blank=True,choices=PENJUALAN_BARANG_GERAI)
    cabang = models.ForeignKey(Tbl_Cabang,related_name="+",blank=True,null=True,)
    coa1 = models.ForeignKey(Tbl_Akun,related_name="+",blank=True,null=True,)
    coa2 = models.ForeignKey(Tbl_Akun,related_name="+",blank=True,null=True,)
    coa3 = models.ForeignKey(Tbl_Akun,related_name="+",blank=True,null=True,)
    coa4 = models.ForeignKey(Tbl_Akun,related_name="+",blank=True,null=True,)
    ke_cabang = models.ForeignKey(Tbl_Cabang,related_name="+",blank=True,null=True,)
    class Meta:
       db_table = 'geraipenjualanmapper'


PENAMBAHAN_JURNAL=(
    ('penambahan_saldo_debet_bank','PENERIMAAN DARI GERAI MELALUI BANK'),
    ('penambahan_saldo_debet_kas','PENERIMAAN DARI GERAI MELALUI KAS'),
    ('pengembalian_saldo_antarbank_bank','PENGELUARAN GERAI DARI BANK'),
    #('pengembalian_saldo_antarbank_bank_ke_gerai','PENGELUARAN GERAI DARI BANK (KE GERAI)'),
    ('pengembalian_saldo_antarbank_kas','PENGELUARAN GERAI DARI KAS'),
)

JENIS_PENAMBAHAN=(
    ('BANK','BANK'),('KAS','KAS'),
)

class PenKasBankMapper(models.Model):####PENAMBAHAN  PENGAMBILAN SALDO KAS BANK
    item = models.CharField(max_length=50,null=True,blank=True,choices=PENAMBAHAN_JURNAL)
    jenis = models.CharField(max_length=50,null=True,blank=True,choices=JENIS_PENAMBAHAN)
    cabang = models.ForeignKey(Tbl_Cabang,related_name="+",null=True,blank=True,)
    ke_cabang = models.ForeignKey(Tbl_Cabang,null=True,blank=True,related_name="+")
    coa = models.ForeignKey(Tbl_Akun,related_name="+",null=True,blank=True,)
    coa_kredit = models.ForeignKey(Tbl_Akun,null=True,blank=True,related_name="+")
    coa_lawan = models.ForeignKey(Tbl_Akun,related_name="+",null=True,blank=True)
    coa_kredit_lawan = models.ForeignKey(Tbl_Akun,null=True,blank=True,related_name="+")
    debet_rak_cabang = models.ForeignKey(Tbl_Akun,null=True,blank=True,related_name="+")
    kredit_rak_pusat = models.ForeignKey(Tbl_Akun,null=True,blank=True,related_name="+")   
    
    class Meta:
       db_table = 'penkasbankmapper'

JENIS_MATERAI_MAPPER =(
    ('1','MATERAI KAS'),('2','MATERAI BIAYA'),('3','MATERAI UANG MUKA'),
)

class MateraiMapper(models.Model):
    item = models.CharField(max_length=50,null=True,blank=True,choices=JENIS_MATERAI_MAPPER)
    cabang = models.ForeignKey(Tbl_Cabang,null=True,blank=True)
    coa1 = models.ForeignKey(Tbl_Akun,related_name="+",blank=True,null=True)
    coa2 = models.ForeignKey(Tbl_Akun,null=True,blank=True,related_name="+")
    coa3 = models.ForeignKey(Tbl_Akun,null=True,blank=True,related_name="+")
    coa4 = models.ForeignKey(Tbl_Akun,null=True,blank=True,related_name="+")

    class Meta:
       db_table = 'materaimapper'

    def get_absolute_url(self):
        return "/parameterjurnal/jurnal_materai/"

class MateraiPusatMapper(models.Model):
    item = models.CharField(max_length=50,null=True,blank=True,choices=JENIS_MATERAI_MAPPER)
    cabang = models.ForeignKey(Tbl_Cabang,null=True,blank=True)
    coa1 = models.ForeignKey(Tbl_Akun,related_name="+",blank=True,null=True)
    coa2 = models.ForeignKey(Tbl_Akun,null=True,blank=True,related_name="+")
    coa_cabang_debet = models.ForeignKey(Tbl_Akun,related_name="+",blank=True,null=True)
    coa_cabang_kredit = models.ForeignKey(Tbl_Akun,null=True,blank=True,related_name="+")

    class Meta:
       db_table = 'materaipusatmapper'

    def get_absolute_url(self):
        return "/parameterjurnal/jurnal_materai_pusat/"



AKADBARANGSAMA_ADM=(
    ('1','Jurnal Pelunasan Barang Sama Anggota (JasaAda ,Denda Ada)(1)'),
    ('2','Jurnal Pelunasan Barang Sama Anggota Lebih (JasaAda, DendaAda)(2)'),   
    ('3','Jurnal Pelunasan Barang Sama Non Anggota (JasaAda, DendaAda)(3)'),
    ('4','Jurnal Pelunasan Barang Sama Non Anggota Lebih (JasaAda, DendaAda)(4)'),
    ('9','Jurnal Pelunasan Barang Sama Anggota (NonJasa,NonDenda)-(9)'),
    ('10','Jurnal Pelunasan Barang Sama Anggota Lebih (NonJasa,NonDenda)(10)'), 
    ('11','Jurnal Pelunasan Barang Sama Non Anggota (NonJasa,Non Denda)(11)'),
    ('12','Jurnal Pelunasan Barang Sama Non Anggota Lebih (NonJasa,NonDenda)-(12)'),  

    ('13','Jurnal Pelunasan Barang Sama Anggota (JasaAda,NonDenda)(13)'),
    ('14','jurnal Pelunasan Barang Sama Anggota (NonJasa ,DendaAda)(14) '),
    ('15','Jurnal Pelunasan Barang Sama Non Anggota (NonDenda,JasaAda)(15)'),
    ('16','jurnal Pelunasan Barang Sama Non Anggota (NonJasa,DendaAda)(16)'),
    ('5','Jurnal Pencairan Barang Sama Anggota(5)'),
    ('6','Jurnal Pencairan Barang Sama Non Anggota(6)'),
    ('7','Jurnal Pencairan Barang Sama Anggota Materai(7)'),
    ('8','Jurnal Pencairan Barang Sama Non Anggota Materai(8)'),
)

class AdmGadaiUlangMapper(models.Model):
    item = models.CharField(max_length=50,null=True,blank=True,choices=AKADBARANGSAMA_ADM)
    coa = models.ForeignKey(Tbl_Akun,related_name="+",null=True,blank=True)
    coa_1 = models.ForeignKey(Tbl_Akun,related_name="+",null=True,blank=True)
    coa_2 = models.ForeignKey(Tbl_Akun,related_name="+",null=True,blank=True)
    coa_3 = models.ForeignKey(Tbl_Akun,related_name="+",null=True,blank=True)
    coa_4 = models.ForeignKey(Tbl_Akun,related_name="+",null=True,blank=True)
    coa_5 = models.ForeignKey(Tbl_Akun,related_name="+",null=True,blank=True)
    coa_6 = models.ForeignKey(Tbl_Akun,related_name="+",null=True,blank=True)
    coa_7 = models.ForeignKey(Tbl_Akun,related_name="+",null=True,blank=True)
    class Meta:
       db_table = 'admgadaiulangmapper'

PELUNASAN_ADM=(
    ('1','Pelunasan Anggota'),
    ('2','Pelunasan Non Anggota'),
    ('3','Pelunasan Anggota (Non Denda)'),
    ('4','Pelunasan Non Anggota (Non Denda)'),
    ###Tambahan
    ('5','Pelunasan Anggota PPAP'),
    ('6','Pelunasan Non Anggota PPAP'),
    ('7','Pelunasan Anggota Otorisasi (Non Jasa)'),
    ('8','Pelunasan Non Anggota Otorisasi (Non Jasa)'),
    ('9','Pelunasan Anggota Otorisasi (Non Denda)'),
    ('10','Pelunasan Non Anggota Otorisasi (Non Denda)'),
)

class AdmPelunasanMapper(models.Model):
    item = models.CharField(max_length=50,null=True,blank=True,choices=PELUNASAN_ADM)
    coa_1 = models.ForeignKey(Tbl_Akun,related_name="+",null=True,blank=True)
    coa_2 = models.ForeignKey(Tbl_Akun,related_name="+",null=True,blank=True)
    coa_3 = models.ForeignKey(Tbl_Akun,related_name="+",null=True,blank=True)
    coa_4 = models.ForeignKey(Tbl_Akun,related_name="+",null=True,blank=True)
    coa_5 = models.ForeignKey(Tbl_Akun,related_name="+",null=True,blank=True)
    coa_6 = models.ForeignKey(Tbl_Akun,related_name="+",null=True,blank=True)
    coa_7 = models.ForeignKey(Tbl_Akun,related_name="+",null=True,blank=True)
    class Meta:
       db_table = 'admpelunasanmapper'

ITEM_ADM_JURNAL =(
    ('1','Pinjaman Anggota (Materai)'),
    ('2','Pinjaman Anggota (Non Materai)'),
    ('3','Pinjaman Non Anggota (Materai)'),
    ('4','Pinjaman Non Anggota (Non Materai)'),    
)
class PencairanAdmMapper(models.Model):
    item = models.CharField(max_length=50,null=True,blank=True,choices=ITEM_ADM_JURNAL)
    cabang = models.ForeignKey(Tbl_Cabang,null=True,blank=True)
    coa1 = models.ForeignKey(Tbl_Akun,related_name="+")
    coa2 = models.ForeignKey(Tbl_Akun,null=True,blank=True,related_name="+")
    coa3 = models.ForeignKey(Tbl_Akun,null=True,blank=True,related_name="+")
    coa4 = models.ForeignKey(Tbl_Akun,null=True,blank=True,related_name="+")
    coa5 = models.ForeignKey(Tbl_Akun,null=True,blank=True,related_name="+")
    coa6 = models.ForeignKey(Tbl_Akun,null=True,blank=True,related_name="+")    
    tanggal = models.DateField()

    class Meta:
       db_table = 'pencairanadmmapper'

    def get_absolute_url(self):
        return "/parameter/pencairanadmmapper/"

class ManopPelunasan(models.Model):
    pelunasan = models.OneToOneField('AkadGadai',null=True, blank=True)
    status = models.CharField(max_length=1, choices=STATUS_MANOP_PELUNASAN)
    tanggal = models.DateField()
    cu = models.ForeignKey(User, related_name='c_manopelunasan', editable=False, null=True, blank=True)
    mu = models.ForeignKey(User, related_name='m_manopelunasan', editable=False, null=True, blank=True)
    note = models.CharField(max_length=200, null=True, blank=True)

    class Meta:
        db_table = 'manoppelunasan'
        verbose_name = 'ManopPelunasan'
        verbose_name_plural = verbose_name



class ManopPelunasanGu(models.Model):
    gu = models.OneToOneField('Pelunasan',null=True, blank=True)
    status = models.CharField(max_length=1, choices=STATUS_MANOP_PELUNASAN)
    note = models.CharField(max_length=200, null=True, blank=True)
    tanggal = models.DateField()
    nilai = models.DecimalField(max_digits=12, decimal_places=2,blank=True,null=True)########Perubahan Nilai Pelunasan
    denda = models.DecimalField(max_digits=12, decimal_places=2,blank=True,null=True)########Perubahan Nilai Pelunasan
    bea_jasa = models.DecimalField(max_digits=12, decimal_places=2,blank=True,null=True)########Perubahan Nilai Pelunasan
    denda_kendaraan = models.DecimalField(max_digits=12, decimal_places=2,blank=True,null=True)########Perubahan Nilai Pelunasan
    bea_jasa_kendaraan = models.DecimalField(max_digits=12, decimal_places=2,blank=True,null=True)########Perubahan Nilai Pelunasan
    cu = models.ForeignKey(User, related_name='+', editable=False, null=True, blank=True)
    mu = models.ForeignKey(User, related_name='+', editable=False, null=True, blank=True)

    class Meta:
        db_table = 'manoppelunasangu'
        verbose_name = 'ManopPelunasanGu'
        verbose_name_plural = verbose_name

    def tot_denda(self):
        return self.denda + self.denda_kendaraan

    def tot_jasa(self):
        return self.bea_jasa + self.bea_jasa_kendaraan

    def get_terlambat(self):
        selisih =  self.tanggal - self.gu.pelunasan.jatuhtempo
        if selisih.days < 0 :
            return 0
        else:
            return selisih.days

    def get_h_denda_plns(self):
        return int(round(((self.gu.pelunasan.nilai*0.05/30))*(self.get_terlambat())))

    def get_jasa_pel_mo(self):
        if self.gu.pelunasan.jenis_transaksi == u'1':
            return int(round((self.gu.pelunasan.nilai*0.02/7)*(self.get_terlambat())))
        else:
            return int(round((self.gu.pelunasan.nilai*0.04/30)*(self.get_terlambat())))

STATUS_TITIPAN =(
    ('1','Titipan'),
    ('2','Kelebihan'),
    ('3','Telah Di Kembalikan'),
)

class TitipanPelunasan(models.Model):
    norek = models.CharField(max_length =20)
    gerai = models.CharField(max_length =30)
    nilai = models.DecimalField(max_digits=12,decimal_places=2)
    tanggal = models.DateField()
    status = models.CharField(max_length=50,null=True,blank=True,choices=STATUS_TITIPAN)
    cu = models.ForeignKey(User, related_name='+', editable=False, null=True, blank=True)
    mu = models.ForeignKey(User, related_name='+', editable=False, null=True, blank=True)

    
    class Meta:
        db_table = 'titipanpelunasan'
        verbose_name = 'TitipanPelunasan'
        verbose_name_plural = verbose_name

    def nama(self):
        pn = 0
        a = AkadGadai.objects.filter(id = self.norek)
        for p in a:
            try:
                pn = p.agnasabah.nama
            except:
                pass
            return pn

    def akad_norek(self):
        pn = 0
        a = AkadGadai.objects.filter(id = self.norek)
        for p in a:
            try:
                pn = p.norek()
            except:
                pass
            return pn

    def akad_gerai(self):
        pn = 0
        a = AkadGadai.objects.filter(id = self.norek)
        for p in a:
            try:
                pn = p.gerai.nama_cabang
            except:
                pass
            return pn            

           
    def akad_nonas(self):
        pn = 0
        a = AkadGadai.objects.filter(id = self.norek)
        for p in a:
            try:
                pn = p.nonas()
            except:
                pass
            return pn  

    def akad_merk_barang(self):
        pn = 0
        akad = AkadGadai.objects.filter(id = self.norek)
        for p in akad:
            try:
                if p.jenis_transaksi == u'1':
                    pn = p.barang.merk
                else:
                    pn = p.barang.merk_kendaraan                   
            except:
                pass
            return pn

    def akad_type_barang(self):
        pn = 0
        akad = AkadGadai.objects.filter(id = self.norek)
        for p in akad:
            try:
                if p.jenis_transaksi == u'1':
                    pn = p.barang.type
                else:
                    pn = p.barang.type_kendaraan               
            except:
                pass
            return pn

    def akad_sn_barang(self):
        pn = 0
        akad = AkadGadai.objects.filter(id = self.norek)
        for p in akad:
            try:
                if p.jenis_transaksi == u'1':
                    pn = p.barang.sn
                else:
                    pn = p.barang.no_rangka          
            except:
                pass
            return pn            

    def akad_alamat(self):
        pn = 0
        a = AkadGadai.objects.filter(id = self.norek)
        for p in a:
            try:
                pn = p.agnasabah.alamat_ktp
            except:
                pass
            return pn        

    def akad_no_rumah(self):
        pn = 0
        a = AkadGadai.objects.filter(id = self.norek)
        for p in a:
            try:
                pn = p.agnasabah.no_rumah_ktp
            except:
                pass
            return pn 


    def akad_rt(self):
        pn = 0
        a = AkadGadai.objects.filter(id = self.norek)
        for p in a:
            try:
                pn = p.agnasabah.rt_ktp
            except:
                pass
            return pn 

    def akad_rw(self):
        pn = 0
        a = AkadGadai.objects.filter(id = self.norek)
        for p in a:
            try:
                pn = p.agnasabah.rw_ktp
            except:
                pass
            return pn 

    def akad_kelurahan_ktp(self):
        pn = 0
        a = AkadGadai.objects.filter(id = self.norek)
        for p in a:
            try:
                pn = p.agnasabah.kelurahan_ktp
            except:
                pass
            return pn

    def akad_kecamatan_ktp(self):
        pn = 0
        a = AkadGadai.objects.filter(id = self.norek)
        for p in a:
            try:
                pn = p.agnasabah.kecamatan_ktp
            except:
                pass
            return pn

    def akad_kotamadya_ktp(self):
        pn = 0
        a = AkadGadai.objects.filter(id = self.norek)
        for p in a:
            try:
                pn = p.agnasabah.kotamadya_ktp
            except:
                pass
            return pn

    def akad_kabupaten_ktp(self):
        pn = 0
        a = AkadGadai.objects.filter(id = self.norek)
        for p in a:
            try:
                pn = p.agnasabah.kabupaten_ktp
            except:
                pass
            return pn

STATUS_POSTING_GERAI =(
    ('1','Sudah Posting'),

)

class PostingGerai(models.Model):
    status_posting = models.CharField(max_length=50,null=True,blank=True,choices=STATUS_POSTING_GERAI)
    kode_cabang = models.CharField(max_length=3,null=True,blank=True)
    gerai = models.CharField(max_length =30)
    tanggal = models.DateField()
    status_posting_pusat = models.CharField(max_length=50,null=True,blank=True,choices=STATUS_POSTING_GERAI)
    cu = models.ForeignKey(User, related_name='+', editable=False, null=True, blank=True)
    mu = models.ForeignKey(User, related_name='+', editable=False, null=True, blank=True)
    
    class Meta:
        db_table = 'postinggerai'
        verbose_name = 'PostingGerai'
        verbose_name_plural = verbose_name

STATUS_OTO_TITIPAN = (
    ('1','Otorisasi'),
)

APPROVE_OTO_TITIPAN = (
    ('1','LANJUT'),
    #('2','TOLAK'),
)
class AppTitipanKeu(models.Model):
    titip_gu = models.OneToOneField('AkadGadai',null=True, blank=True)
    status_oto_gerai = models.CharField(max_length=4, choices= STATUS_OTO_TITIPAN,null=True, blank=True)
    status_oto_pusat = models.CharField(max_length=4, choices= APPROVE_OTO_TITIPAN,null=True, blank=True)
    tanggal_oto_gerai = models.DateField(null=True, blank=True)
    tanggal_oto_pusat = models.DateField(null=True, blank=True)
    nilai = models.DecimalField(max_digits=12,decimal_places=2)
    tanggal_eksekusi = models.DateField(null=True, blank=True)
    nilai_eksekusi = models.DecimalField(max_digits=12,decimal_places=2,null=True, blank=True)
    cu = models.ForeignKey(User, related_name='+', editable=False, null=True, blank=True)
    mu = models.ForeignKey(User, related_name='+', editable=False, null=True, blank=True)
    note = models.CharField(max_length=200, null=True, blank=True)
    
    class Meta:
        db_table = 'apptitipankeu'
        verbose_name = 'AppTitipanKeu'
        verbose_name_plural = verbose_name

class TitipanAkadUlang(models.Model):
    norek = models.CharField(max_length =20)
    gerai = models.CharField(max_length =30)
    nilai = models.DecimalField(max_digits=12,decimal_places=2)
    tanggal = models.DateField()
    status = models.CharField(max_length=50,null=True,blank=True,choices=STATUS_TITIPAN)
    cu = models.ForeignKey(User, related_name='+', editable=False, null=True, blank=True)
    mu = models.ForeignKey(User, related_name='+', editable=False, null=True, blank=True)

    
    class Meta:
        db_table = 'titipanakadulang'
        verbose_name = 'TitipanAkadUlang'
        verbose_name_plural = verbose_name

    def nama(self):
        pn = 0
        a = AkadGadai.objects.filter(id = self.norek)
        for p in a:
            try:
                pn = p.agnasabah.nama
            except:
                pass
            return pn

    def akad_norek(self):
        pn = 0
        a = AkadGadai.objects.filter(id = self.norek)
        for p in a:
            try:
                pn = p.norek()
            except:
                pass
            return pn

    def akad_titipan_gerai(self):
        pn = 0
        a = AkadGadai.objects.filter(id = self.norek,apptitipankeu__isnull = False)
        for p in a:
            try:
                pn = p.apptitipankeu.status_oto_gerai
            except:
                pass
            return pn

    def akad_titipan_keu(self):
        pn = 0
        a = AkadGadai.objects.filter(id = self.norek,apptitipankeu__isnull = False)
        for p in a:
            try:
                pn = p.apptitipankeu.status_oto_pusat
            except:
                pass
            return pn

    def akad_gerai(self):
        pn = 0
        a = AkadGadai.objects.filter(id = self.norek)
        for p in a:
            try:
                pn = p.gerai.nama_cabang
            except:
                pass
            return pn            

           
    def akad_nonas(self):
        pn = 0
        a = AkadGadai.objects.filter(id = self.norek)
        for p in a:
            try:
                pn = p.nonas()
            except:
                pass
            return pn  

    def akad_merk_barang(self):
        pn = 0
        akad = AkadGadai.objects.filter(id = self.norek)
        for p in akad:
            try:
                if p.jenis_transaksi == u'1':
                    pn = p.barang.merk
                else:
                    pn = p.barang.merk_kendaraan                   
            except:
                pass
            return pn

    def akad_type_barang(self):
        pn = 0
        akad = AkadGadai.objects.filter(id = self.norek)
        for p in akad:
            try:
                if p.jenis_transaksi == u'1':
                    pn = p.barang.type
                else:
                    pn = p.barang.type_kendaraan               
            except:
                pass
            return pn

    def akad_sn_barang(self):
        pn = 0
        akad = AkadGadai.objects.filter(id = self.norek)
        for p in akad:
            try:
                if p.jenis_transaksi == u'1':
                    pn = p.barang.sn
                else:
                    pn = p.barang.no_rangka          
            except:
                pass
            return pn            

    def akad_alamat(self):
        pn = 0
        a = AkadGadai.objects.filter(id = self.norek)
        for p in a:
            try:
                pn = p.agnasabah.alamat_ktp
            except:
                pass
            return pn        

    def akad_no_rumah(self):
        pn = 0
        a = AkadGadai.objects.filter(id = self.norek)
        for p in a:
            try:
                pn = p.agnasabah.no_rumah_ktp
            except:
                pass
            return pn 


    def akad_rt(self):
        pn = 0
        a = AkadGadai.objects.filter(id = self.norek)
        for p in a:
            try:
                pn = p.agnasabah.rt_ktp
            except:
                pass
            return pn 

    def akad_rw(self):
        pn = 0
        a = AkadGadai.objects.filter(id = self.norek)
        for p in a:
            try:
                pn = p.agnasabah.rw_ktp
            except:
                pass
            return pn 

    def akad_kelurahan_ktp(self):
        pn = 0
        a = AkadGadai.objects.filter(id = self.norek)
        for p in a:
            try:
                pn = p.agnasabah.kelurahan_ktp
            except:
                pass
            return pn

    def akad_kecamatan_ktp(self):
        pn = 0
        a = AkadGadai.objects.filter(id = self.norek)
        for p in a:
            try:
                pn = p.agnasabah.kecamatan_ktp
            except:
                pass
            return pn

    def akad_kotamadya_ktp(self):
        pn = 0
        a = AkadGadai.objects.filter(id = self.norek)
        for p in a:
            try:
                pn = p.agnasabah.kotamadya_ktp
            except:
                pass
            return pn

    def akad_kabupaten_ktp(self):
        pn = 0
        a = AkadGadai.objects.filter(id = self.norek)
        for p in a:
            try:
                pn = p.agnasabah.kabupaten_ktp
            except:
                pass
            return pn

class Denominasi(models.Model):
    kertas_seratusribu = models.IntegerField(null=True, blank=True)
    kertas_limapuluhribu = models.IntegerField(null=True, blank=True)
    kertas_duapuluhribu = models.IntegerField(null=True, blank=True)
    kertas_sepuluhribu = models.IntegerField(null=True, blank=True)
    kertas_limaribu = models.IntegerField(null=True, blank=True)
    kertas_duaribu = models.IntegerField(null=True, blank=True)
    kertas_seribu = models.IntegerField(null=True, blank=True)
    koin_seribu = models.IntegerField(null=True, blank=True)
    koin_limaratus = models.IntegerField(null=True, blank=True)
    koin_duaratus = models.IntegerField(null=True, blank=True)
    koin_seratus = models.IntegerField(null=True, blank=True)	
    koin_limapuluh = models.IntegerField(null=True, blank=True)
    koin_dualima = models.IntegerField(null=True, blank=True)
    
    jumlah_kertas_seratusribu = models.IntegerField(null=True, blank=True)
    jumlah_kertas_limapuluhribu = models.IntegerField(null=True, blank=True)
    jumlah_kertas_duapuluhribu = models.IntegerField(null=True, blank=True)
    jumlah_kertas_sepuluhribu = models.IntegerField(null=True, blank=True)
    jumlah_kertas_limaribu = models.IntegerField(null=True, blank=True)
    jumlah_kertas_duaribu = models.IntegerField(null=True, blank=True)
    jumlah_kertas_seribu = models.IntegerField(null=True, blank=True)
    jumlah_koin_seribu = models.IntegerField(null=True, blank=True)
    jumlah_koin_limaratus = models.IntegerField(null=True, blank=True)
    jumlah_koin_duaratus = models.IntegerField(null=True, blank=True)
    jumlah_koin_seratus = models.IntegerField(null=True, blank=True)	
    jumlah_koin_limapuluh = models.IntegerField(null=True, blank=True)
    jumlah_koin_dualima = models.IntegerField(null=True, blank=True)  
    gerai = models.CharField(max_length =30,null=True, blank=True)
    tanggal = models.DateField(null=True, blank=True)
    cu = models.ForeignKey(User, related_name='+', editable=False, null=True, blank=True)
    mu = models.ForeignKey(User, related_name='+', editable=False, null=True, blank=True)
    class Meta:
        db_table = 'denominasi'
        verbose_name = 'Denominasi'
        verbose_name_plural = verbose_name

    def sum_all_denominasi(self):
        return self.jumlah_kertas_seratusribu + self.jumlah_kertas_limapuluhribu + self.jumlah_kertas_duapuluhribu +\
            self.jumlah_kertas_sepuluhribu+ self.jumlah_kertas_limaribu + self.jumlah_kertas_duaribu +\
            self.jumlah_kertas_seribu + self.jumlah_koin_seribu + self.jumlah_koin_limaratus + self.jumlah_koin_duaratus +\
            self.jumlah_koin_seratus + self.jumlah_koin_limapuluh + self.jumlah_koin_dualima
  
class UserProfile(models.Model):
    user = models.ForeignKey(User, unique=True)
    rekening = models.CharField(max_length=20, unique=True, null=True, blank=True)
    gerai = models.ForeignKey(Tbl_Cabang, null=True, blank=True)

    class Meta:
        db_table = 'userprofile'

    def __unicode__(self):
        return self.user.username

User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])

class Visitor(models.Model):
    user = models.OneToOneField(AUTH_USER_MODEL, null=False,related_name='visitor')
    session_key = models.CharField(null=False, max_length=40)

    class Meta:
        db_table = 'visitor'

class JurnalKeuangan(models.Model):
    def number():
        kode = 1000000
        no = Jurnal.objects.all().count()
        if no == None:
            return 1
        else:
            return no + 1 + kode
    nobukti= models.CharField(max_length=35,blank=True, null=True)
    no_akad = models.IntegerField(default=number,blank=True, null=True) 
    object_id = models.IntegerField(max_length=11,blank =True,null=True)        
    diskripsi = models.CharField(max_length=200, blank=True, null=True)
    kode_cabang = models.CharField(max_length=5,blank=True,null=True)
    tgl_trans = models.DateField()
    cdate = models.DateTimeField(auto_now_add=True)
    mdate = models.DateTimeField(auto_now=True)
    cu = models.ForeignKey(User, related_name='+', null=True)
    mu = models.ForeignKey(User, related_name='+', null=True)

    def __unicode__(self):
        return '%s' % (self.id)
    
    class Meta:
        db_table = "jurnalkeuangan"

class Tbl_TransaksiKeu(models.Model):
    id_coa = models.ForeignKey(Tbl_Akun,null =True,blank=True)
    jurnal = models.ForeignKey(JurnalKeuangan)
    no_trans = models.IntegerField(max_length=6, null=True, blank=True)
    jenis = models.CharField(max_length=60)
    debet = models.IntegerField(max_length=11)
    kredit = models.IntegerField(max_length=11)
    id_cabang = models.IntegerField(max_length=3)
    id_cabang_tuju = models.IntegerField(max_length=3,null=True,blank=True)
    id_unit = models.IntegerField(max_length=3)
    id_product  = models.IntegerField(max_length=1)
    status_jurnal = models.IntegerField(max_length=1)
    user = models.ForeignKey(User, related_name='+', editable=False, null=True, blank=True)
    tgl_trans = models.DateField()
    status_posting = models.IntegerField(max_length=1,blank=True,null=True)
    deskripsi = models.CharField(max_length=500, blank=True, null=True)
    #saldo = models.IntegerField(max_length=16, blank=True, null=True)
    saldo = models.DecimalField(max_digits=20,decimal_places=2,default=0,null=True,blank=True)
    
    class Meta:
        db_table = "tbl_transaksikeu"

    def __unicode__(self):
        return '%s-%s' % ((self.id),(self.jurnal))
    
    def saldo_kas(self,start_date):
        total = 0
        for k in self.tbl_transaksikeu_set.filter(jenis='SALDOKASGERAI').filter(status_jurnal='2').filter(tgl_trans = start_date):
            #if k.saldo == None:
                #return total
            #else:
            total += int(k.saldo)
            return total

class Master_Sop(models.Model):
    judul_sop = models.CharField(max_length=500, blank=True, null=True)
    tanggal_sop = models.DateField()
    status_sop = models.CharField(null=True, blank = True,max_length=200,choices=AKTIFASI_PARAMETER)

    class Meta:
        db_table = "sop"
        verbose_name = 'sop'
        ordering = ['-id']

    def __unicode__(self):
        return '%s' % (self.judul_sop)

class BerkasSop(models.Model):
    agsop = models.ForeignKey(Master_Sop)
    gambar = models.FileField(upload_to="media/sopberkas/")
    judul = models.CharField(max_length=500, blank=True, null=True)
    deskripsi = models.CharField(max_length=500, blank=True, null=True)
    no_urut = models.IntegerField(max_length=1,blank=True,null=True)
    tanggal = models.DateField()
    status = models.CharField(null=True, blank = True,max_length=200,choices=AKTIFASI_PARAMETER)
    

    class Meta:
        db_table = "berkassop"
        verbose_name = 'berkassop'
        ordering = ['-id']

