from django.contrib import admin
import datetime
from gadai.appgadai.models import *
from gadai.appkeuangan.models import *
from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportMixin, ExportActionModelAdmin

class MenuAdmin(ImportExportMixin,admin.ModelAdmin):
    list_display = ['id']
    search_fields = ['id']
admin.site.register(Menu, MenuAdmin)

class MenuItemAdmin(ImportExportMixin,admin.ModelAdmin):
    list_display = ['id','link_url','judul']
    search_fields = ['id']
admin.site.register(MenuItem, MenuItemAdmin)


class TeguranAdmin(ImportExportMixin,admin.ModelAdmin):
    list_display = ['id']
    search_fields = ['id']
admin.site.register(Teguran, TeguranAdmin)

class UploadPkAdmin(ImportExportMixin,admin.ModelAdmin):
    raw_id_fields = ['upload']
    list_display = ['id','upload']
    search_fields = ['id']
admin.site.register(UploadPk, UploadPkAdmin)

class AppTitipanKeuAdmin(ImportExportMixin,admin.ModelAdmin):
    list_display = ['id','status_oto_gerai']
    search_fields = ['id']
    raw_id_fields = ['titip_gu']
admin.site.register(AppTitipanKeu, AppTitipanKeuAdmin)

class HistoryLapurAdmin(ImportExportMixin, admin.ModelAdmin):
    raw_id_fields = ['aglapur']
    list_display=('id','tanggal')
    #exclude = ['aglapur']
    search_fields =['id']
admin.site.register(HistoryLapur,HistoryLapurAdmin)

class AdmGadaiUlangMapperAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display=('id',)
    search_fields =['id']
admin.site.register(AdmGadaiUlangMapper,AdmGadaiUlangMapperAdmin)

class PencairanAdmMapperAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display=('id',)
    search_fields =['id']
admin.site.register(PencairanAdmMapper,PencairanAdmMapperAdmin)

class AdmPelunasanMapperAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display=('id',)
    search_fields =['id']
admin.site.register(AdmPelunasanMapper,AdmPelunasanMapperAdmin)

class Master_SopAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display=('id','judul_sop','tanggal_sop','status_sop')
    search_fields =['id','judul_sop','tanggal_sop','status_sop']
    #exclude = ['pelunasan']
admin.site.register(Master_Sop,Master_SopAdmin)

class BerkasSopAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display=('id','gambar','judul','deskripsi','no_urut','tanggal','status')
    search_fields =['id','gambar','judul','deskripsi','no_urut','tanggal','status']
admin.site.register(BerkasSop,BerkasSopAdmin)


class BiayaMapperdiBayarPusatAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display=('id','item',)
    search_fields =['id']
    #exclude = ['pelunasan']
admin.site.register(BiayaMapperdiBayarPusat,BiayaMapperdiBayarPusatAdmin)

class PostingGeraiAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display=('id','status_posting','kode_cabang','gerai','tanggal','cu','mu')
    search_fields =['id','status_posting','kode_cabang','gerai','tanggal','cu','mu']
admin.site.register(PostingGerai,PostingGeraiAdmin)

class Limit_PetyCashAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display=('nilai','tanggal','status')
    search_fields =['id','tanggal']
admin.site.register(Limit_PetyCash,Limit_PetyCashAdmin)

class TitipanAkadUlangAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display=('norek','gerai','nilai','tanggal','status')
    search_fields =['id','norek']
admin.site.register(TitipanAkadUlang,TitipanAkadUlangAdmin)

#class HistoryBarangAdmin(ImportExportMixin, admin.ModelAdmin):
    #list_display = ('agbarang')
    #search_fields = ['agbarang']
#admin.site.register(HistoryBarang ,HistoryBarangAdmin)

class PengembalianTitipanGadaiUlangMapperAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display=('item','cabang','coa_1','coa_2')
    search_fields =['id','item']
admin.site.register(PengembalianTitipanGadaiUlangMapper,PengembalianTitipanGadaiUlangMapperAdmin)

class PengembalianTitipanMapperAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display=('item','cabang','coa_1','coa_2')
    search_fields =['id','item']
admin.site.register(PengembalianTitipanMapper,PengembalianTitipanMapperAdmin)

class HistoryAkadUlangAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display=('id','nama')
    search_fields =['id']
admin.site.register(HistoryAkadUlang, HistoryAkadUlangAdmin)


class ParameterAkadUlangAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display=('id','jml_akad','aktif','tanggal','jenis_transaksi','jangka_waktu_kendaraan','jangka_waktu')
    #exclude = ('pelunasan',)
    search_fields =['id']
admin.site.register(ParameterAkadUlang, ParameterAkadUlangAdmin)

class BiayaPusatMapperAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display =['id','item','cabang','jenis','cabang_tuju','coa_debet','coa','coa_uk','coa_debet_tuju','coa_kredit_tuju']
    search_fields =['id','item']
admin.site.register(BiayaPusatMapper, BiayaPusatMapperAdmin)

class KasirPencairanBankMapperAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display =['id','tanggal','item','cabang','coa_debet','coa_debet_satu','coa_kredit','coa_kredit_satu']
    search_fields =['id','item']
admin.site.register(KasirPencairanBankMapper, KasirPencairanBankMapperAdmin)

class MateraiPusatMapperAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display =['id','item','cabang','coa1','coa2',]
    search_fields =['id','item']
admin.site.register(MateraiPusatMapper, MateraiPusatMapperAdmin)

class KasirPelunasanRakMapperAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display =['id','item','jenis','cabang','ke_cabang','coa_1','coa_2','coa_3','coa_4','debet_rak_cabang','kredit_rak_pusat','rak_debet_pusat1','rak_kredit_pusat2']
    search_fields =['id','item']
admin.site.register(KasirPelunasanRakMapper, KasirPelunasanRakMapperAdmin)

class KasirPelunasanMapperAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display =['id','item','jenis','cabang','ke_cabang','coa_1','coa_2','coa_3','coa_4']
    search_fields =['id','item']
admin.site.register(KasirPelunasanMapper, KasirPelunasanMapperAdmin) 

class UangMukaGeraiMapperAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display=('id','item','cabang','debet_pengembalian_uk','kredit_pengembalian_uk','debet_pengambilan_uk','kredit_pengambilan_uk')
    search_fields =['id']
admin.site.register(UangMukaGeraiMapper,UangMukaGeraiMapperAdmin)

class RakPusatMapperAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display=('id','cabang','coa_rak_cabang','coa_rak_pusat')
    search_fields =['id']
admin.site.register(RakPusatMapper,RakPusatMapperAdmin)

class ParameterProdukAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display =['id','jenis_kredit','jenis','tanggal','aktif','jasa','denda','denda_terlambat','adm','provisi','asuransi','biayasimpan','materai','jenis_transaksi']
    search_fields =['id','item']
admin.site.register(ParameterProduk, ParameterProdukAdmin)

class JurnalKeuanganAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display =['id','nobukti','kode_cabang','tgl_trans','no_akad']
    search_fields =['id','nobukti','no_akad']
admin.site.register(JurnalKeuangan, JurnalKeuanganAdmin)

class Tbl_TransaksiKeuAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display =['id','id_coa','tgl_trans','deskripsi','id_cabang','saldo','jurnal']
    search_fields =['id','id_cabang','jenis','id_coa__coa']
    raw_id_fields = ('id_coa','jurnal',)
admin.site.register(Tbl_TransaksiKeu, Tbl_TransaksiKeuAdmin)

class AydaMapperAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display =['id','item']
    search_fields =['id','cabang','item']
admin.site.register(AydaMapper, AydaMapperAdmin)


class DenominasiAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display =['id','gerai']
    search_fields =['id','gerai']
admin.site.register(Denominasi, DenominasiAdmin)

class Jurnal_HistoryAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display =['id','tgl_trans']
    search_fields =['id','tgl_trans']
admin.site.register(Jurnal_History, Jurnal_HistoryAdmin)

class Tbl_Transaksi_HistoryAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display =['id','id_coa','tgl_trans','deskripsi','id_cabang']
    search_fields =['id','id_cabang']
admin.site.register(Tbl_Transaksi_History, Tbl_Transaksi_HistoryAdmin)

class ManopPelunasanGuAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display=('id',)
    search_fields =['id',]
admin.site.register(ManopPelunasanGu,ManopPelunasanGuAdmin)

class GeraiPenjualanMapperAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display=('item','cabang','coa1','coa2','coa3')
    search_fields =['id','item']
admin.site.register(GeraiPenjualanMapper,GeraiPenjualanMapperAdmin)

class TitipanPelunasanAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display=('norek','gerai','nilai','tanggal')
    search_fields =['id','norek']
admin.site.register(TitipanPelunasan,TitipanPelunasanAdmin)

class KasirPencairanMapperAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display=('id','tanggal','item')
    search_fields =['id']
admin.site.register(KasirPencairanMapper,KasirPencairanMapperAdmin)

class KasirGeraiPelunasanAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display=('id',)
    raw_id_fields = ('kasir_lunas',)
    #exclude =['kasir_lunas',]
    search_fields =['id']
admin.site.register(KasirGeraiPelunasan,KasirGeraiPelunasanAdmin)

class GadaiUlangMapperAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display=('id','tanggal','item')
    search_fields =['id']
admin.site.register(GadaiUlangMapper,GadaiUlangMapperAdmin)

class KeuanganPusatAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display=('id',)
    search_fields =['id']
admin.site.register(KeuanganPusat,KeuanganPusatAdmin)

class BiayaPusatAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display=('id',)
    search_fields =['id']
admin.site.register(BiayaPusat,BiayaPusatAdmin)

class ManopPelunasanAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display=('id','pelunasan')
    search_fields =['id']
    raw_id_fields = ('pelunasan',)
    #exclude = ['pelunasan']
admin.site.register(ManopPelunasan,ManopPelunasanAdmin)


class PusatKasBankMapperAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display=('id','item','cabang','ke_cabang')
    search_fields =['id']
admin.site.register(PusatKasBankMapper,PusatKasBankMapperAdmin)

class MateraiMapperAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display=('id','item','cabang',)
    search_fields =['id']
admin.site.register(MateraiMapper,MateraiMapperAdmin)

class PenKasBankMapperAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display=('id','item','jenis','coa','coa_kredit','cabang','ke_cabang',)
    search_fields =['id']
    #exclude = ['pelunasan']
admin.site.register(PenKasBankMapper,PenKasBankMapperAdmin)

class BiayaMapperAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display=('id','item',)
    search_fields =['id']
    #exclude = ['pelunasan']
admin.site.register(BiayaMapper,BiayaMapperAdmin)

class Biaya_MateraiAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display=('id','gerai','nilai')
    search_fields =['id']
admin.site.register(Biaya_Materai,Biaya_MateraiAdmin)


class Biaya_Materai_CabAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display=('id','gerai','nilai','norek')
    search_fields =['id','norek']
admin.site.register(Biaya_Materai_Cab,Biaya_Materai_CabAdmin)
    

class PelunasanAdmin(ImportExportMixin, admin.ModelAdmin):
    raw_id_fields = ('pelunasan',)
    list_display=('id','tanggal','nilai','gerai')
    search_fields =['id']
admin.site.register(Pelunasan,PelunasanAdmin)


class AkadGadaiAdmin(ImportExportMixin, admin.ModelAdmin):
    #list_filter = ['agnasabah','gerai']
    raw_id_fields = ['barang','taksir']
    exclude = ['agnasabah']
    list_display =('id','tanggal','agnasabah','gerai')
    search_fields =['id']

class BarangAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display =('id','merk','barang_masuk','barang_keluar','no_rak')
    search_fields = ['id']


class TaksirAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display=('id','spesifikasi','harga_baru','harga_pasar','maxpinjaman')
    search_fields =['id']

class TaksirHistoryAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display=('id','spesifikasi','harga_baru','harga_pasar','maxpinjaman')
    search_fields =['id']
    
class Tbl_UnitAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display =('id','kode_unit',)
    search_fields =['id']
    
class Tbl_CabangAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ['id', 'kode_cabang','nama_cabang','parent','kode_unit','nama_unit','id_lama','status_aktif']
    fieldsets = (
        (None, {
            'fields': ('kode_cabang','nama_cabang','parent','kode_unit','nama_unit','nama_kasir','id_lama','status_aktif')}),
        ('Isian Lanjut', {
            'classes': ('collapse',),
            'fields': ('alamat','no_telp','nama_admin','init_cabang','nama_kg')
        }),
    )

class Tbl_AkunAdmin(ImportExportMixin,admin.ModelAdmin):
    list_display =('id','coa','header_parent','kode_guna','deskripsi','status','jenis','view_unit','view_cabang')
    search_fields =['id','coa']
    
admin.site.register(Tbl_Akun, Tbl_AkunAdmin)
admin.site.register(Tbl_Cabang,Tbl_CabangAdmin)
admin.site.register(Tbl_Unit, Tbl_UnitAdmin)    
admin.site.register(Taksir,TaksirAdmin)
admin.site.register(Barang,BarangAdmin)
admin.site.register(AkadGadai, AkadGadaiAdmin)
admin.site.register(TaksirHistory,TaksirHistoryAdmin)


class NasabahAdmin(ImportExportMixin,admin.ModelAdmin):
    list_display = ['id','nama',]
    search_fields = ['id','nama', 'alamat_domisili']
admin.site.register(Nasabah,NasabahAdmin)

class AdmGudangAdmin(ImportExportMixin,admin.ModelAdmin):
    list_display = ['id','status','tanggal',]
    raw_id_fields = ['adm']
    search_fields = ['id','status', 'tanggal']
admin.site.register(AdmGudang,AdmGudangAdmin)


class LunasTerjualAdmin(ImportExportMixin,admin.ModelAdmin):
    list_display =('id','aglunas')
    raw_id_fields = ['aglunas']
    search_fields = ['id']
admin.site.register(LunasTerjual,LunasTerjualAdmin)

class KepalaGeraiAdmin(ImportExportMixin,admin.ModelAdmin):
    list_display = ['id','status']
    search_fields = ['id']
    raw_id_fields = ['kepala_gerai']
admin.site.register(KepalaGerai, KepalaGeraiAdmin)

class KplGeraiAdmin(ImportExportMixin,admin.ModelAdmin):
    list_display = ['id','status']
    search_fields = ['id']
admin.site.register(KplGerai, KplGeraiAdmin)

class BerkasGadaiAdmin(ImportExportMixin,admin.ModelAdmin):
    list_display = ['id','upload']
    search_fields = ['id']
admin.site.register(BerkasGadai, BerkasGadaiAdmin)

class ManopKeuAdmin(admin.ModelAdmin):
    list_display = ['id','status']
    search_fields = ['id']
admin.site.register(ManopKeu, ManopKeuAdmin)


class JurnalAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display =['id','nobukti','kode_cabang','no_akad','tgl_trans']
    search_fields =['id','nobukti','no_akad',]
admin.site.register(Jurnal, JurnalAdmin)

class Tbl_TransaksiAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display =['id','id_coa','tgl_trans','deskripsi','id_cabang','saldo']
    search_fields =['id','id_cabang','id_coa__coa']
admin.site.register(Tbl_Transaksi, Tbl_TransaksiAdmin)


class Tbl_ProductAdmin(admin.ModelAdmin):
    list_display =('id','kode_produk',)
    search_fields =['id']
admin.site.register(Tbl_Product, Tbl_ProductAdmin)

class KasirGeraiAdmin(ImportExportMixin,admin.ModelAdmin):
    list_display =('id',)
    raw_id_fields = ('kasir','kasir_lunas')
    search_fields =['id']
admin.site.register(KasirGerai, KasirGeraiAdmin)

class ManopGadaiAdmin(ImportExportMixin,admin.ModelAdmin):
    list_display =('id','tanggal','manop')
    raw_id_fields = ('manop','pelunasan')
    search_fields =['id']
admin.site.register(ManopGadai, ManopGadaiAdmin)


class BarangLelangAdmin(ImportExportMixin,admin.ModelAdmin):
    list_display = ('id','aglelang','tgl_lelang','harga_jual')
    raw_id_fields = ('aglelang',)
    search_fields = ['id']
admin.site.register(BarangLelang,BarangLelangAdmin)

class BiayaAdmin(ImportExportMixin,admin.ModelAdmin):
    list_display=('id','gerai','tanggal')
    search_fields =['id']
admin.site.register(Biaya,BiayaAdmin)

class LapurAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display=('id','tanggal')
    exclude = ['aglapur']
    search_fields =['id']
admin.site.register(Lapur,LapurAdmin)


class UserProfileAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display=('id','user','rekening','gerai')
    search_fields = ['id','user__username']
admin.site.register(UserProfile,UserProfileAdmin)
''' Untuk IMPORT ExPORT USER
class UserResource(resources.ModelResource):
    class Meta:
        model = User
        #fields = ('first_name', 'last_name', 'email')

class UserAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display=('id','username','first_name', 'last_name', 'email','password','is_active',)
    resource_class = UserResource
    pass

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
'''
