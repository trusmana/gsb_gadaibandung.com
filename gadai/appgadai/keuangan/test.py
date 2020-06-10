####Jurnal kas dari du ke Gerai dan Pusat
def jurnal_biaya_penambahan_saldo_kas_du_pusat(biaya, user):
    D = decimal.Decimal
    a_penambahan_saldo_debet = get_object_or_404(Tbl_Akun, id=610L)
    a_penambahan_saldo_kredit = get_object_or_404(Tbl_Akun, id=4L)
    jurnal = Jurnal.objects.create(
        diskripsi= 'Pengembalian KasGerai NoRek: %s ' % (biaya.ket_penambahan_saldo),
        tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_penambahan_saldo)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENAMBAHAN_PUSAT"), id_coa = a_penambahan_saldo_debet,
        kredit = 0,debet = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
     
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENAMBAHAN_PUSAT"), id_coa = a_penambahan_saldo_kredit,
        debet = 0,kredit = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
    
def jurnal_biaya_penambahan_saldo_kas_du_jakarta(biaya, user):
    D = decimal.Decimal
    a_penambahan_saldo_debet = get_object_or_404(Tbl_Akun, id=610L)
    a_penambahan_saldo_kredit = get_object_or_404(Tbl_Akun, id=7L)
    jurnal = Jurnal.objects.create(
        diskripsi= 'Pengiriman KAS Gerai ke SUCI: %s ' % (biaya.ket_penambahan_saldo),
        tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_penambahan_saldo)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENAMBAHAN_GERAI"), id_coa = a_penambahan_saldo_debet,
        kredit = 0,debet = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
     
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENAMBAHAN_GERAI"), id_coa = a_penambahan_saldo_kredit,
        debet = 0,kredit = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
    
def jurnal_biaya_penambahan_saldo_kas_du_suci(biaya, user):
    D = decimal.Decimal
    a_penambahan_saldo_debet = get_object_or_404(Tbl_Akun, id=610L)
    a_penambahan_saldo_kredit = get_object_or_404(Tbl_Akun, id=609L)
    jurnal = Jurnal.objects.create(
        diskripsi= 'Pengiriman KAS Gerai ke DU: %s ' % (biaya.ket_penambahan_saldo),
        tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_penambahan_saldo)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENAMBAHAN_GERAI"), id_coa = a_penambahan_saldo_debet,
        kredit = 0,debet = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
     
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENAMBAHAN_GERAI"), id_coa = a_penambahan_saldo_kredit,
        debet = 0,kredit = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
    
def jurnal_biaya_penambahan_saldo_kas_du_balubur(biaya, user):
    D = decimal.Decimal
    a_penambahan_saldo_debet = get_object_or_404(Tbl_Akun, id=610L)
    a_penambahan_saldo_kredit = get_object_or_404(Tbl_Akun, id=611L)
    jurnal = Jurnal.objects.create(
        diskripsi= 'Pengiriman KAS Gerai ke BALUBUR: %s ' % (biaya.ket_penambahan_saldo),
        tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_penambahan_saldo)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENAMBAHAN_GERAI"), id_coa = a_penambahan_saldo_debet,
        kredit = 0,debet = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
     
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENAMBAHAN_GERAI"), id_coa = a_penambahan_saldo_kredit,
        debet = 0,kredit = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
    
def jurnal_biaya_penambahan_saldo_kas_du_hilir(biaya, user):
    D = decimal.Decimal
    a_penambahan_saldo_debet = get_object_or_404(Tbl_Akun, id=610L)
    a_penambahan_saldo_kredit = get_object_or_404(Tbl_Akun, id=613L)
    jurnal = Jurnal.objects.create(
        diskripsi= 'Pengiriman KAS Gerai ke HILIR: %s ' % (biaya.ket_penambahan_saldo),
        tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_penambahan_saldo)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENAMBAHAN_GERAI"), id_coa = a_penambahan_saldo_debet,
        kredit = 0,debet = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
     
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENAMBAHAN_GERAI"), id_coa = a_penambahan_saldo_kredit,
        debet = 0,kredit = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)

def jurnal_biaya_penambahan_saldo_kas_du_kopo(biaya, user):
    D = decimal.Decimal
    a_penambahan_saldo_debet = get_object_or_404(Tbl_Akun, id=610L)
    a_penambahan_saldo_kredit = get_object_or_404(Tbl_Akun, id=614L)
    jurnal = Jurnal.objects.create(
        diskripsi= 'Pengiriman KAS Gerai ke KOPO: %s ' % (biaya.ket_penambahan_saldo),
        tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_penambahan_saldo)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENAMBAHAN_GERAI"), id_coa = a_penambahan_saldo_debet,
        kredit = 0,debet = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
     
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENAMBAHAN_GERAI"), id_coa = a_penambahan_saldo_kredit,
        debet = 0,kredit = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
    
def jurnal_biaya_penambahan_saldo_kas_du_cibiru(biaya, user):
    D = decimal.Decimal
    a_penambahan_saldo_debet = get_object_or_404(Tbl_Akun, id=610L)
    a_penambahan_saldo_kredit = get_object_or_404(Tbl_Akun, id=615L)
    jurnal = Jurnal.objects.create(
        diskripsi= 'Pengiriman KAS Gerai ke CIBIRU: %s ' % (biaya.ket_penambahan_saldo),
        tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_penambahan_saldo)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENAMBAHAN_GERAI"), id_coa = a_penambahan_saldo_debet,
        kredit = 0,debet = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
     
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENAMBAHAN_GERAI"), id_coa = a_penambahan_saldo_kredit,
        debet = 0,kredit = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
    
def jurnal_biaya_penambahan_saldo_kas_du_cipacing(biaya, user):
    D = decimal.Decimal
    a_penambahan_saldo_debet = get_object_or_404(Tbl_Akun, id=610L)
    a_penambahan_saldo_kredit = get_object_or_404(Tbl_Akun, id=616L)
    jurnal = Jurnal.objects.create(
        diskripsi= 'Pengiriman KAS Gerai ke CIPACING: %s ' % (biaya.ket_penambahan_saldo),
        tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_penambahan_saldo)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENAMBAHAN_GERAI"), id_coa = a_penambahan_saldo_debet,
        kredit = 0,debet = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
     
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENAMBAHAN_GERAI"), id_coa = a_penambahan_saldo_kredit,
        debet = 0,kredit = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)

def jurnal_biaya_penambahan_saldo_kas_du_jatinangor(biaya, user):
    D = decimal.Decimal
    a_penambahan_saldo_debet = get_object_or_404(Tbl_Akun, id=610L)
    a_penambahan_saldo_kredit = get_object_or_404(Tbl_Akun, id=617L)
    jurnal = Jurnal.objects.create(
        diskripsi= 'Pengiriman KAS Gerai ke JATINANGOR: %s ' % (biaya.ket_penambahan_saldo),
        tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_penambahan_saldo)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENAMBAHAN_GERAI"), id_coa = a_penambahan_saldo_debet,
        kredit = 0,debet = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
     
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENAMBAHAN_GERAI"), id_coa = a_penambahan_saldo_kredit,
        debet = 0,kredit = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
    
def jurnal_biaya_penambahan_saldo_kas_du_cimahi(biaya, user):
    D = decimal.Decimal
    a_penambahan_saldo_debet = get_object_or_404(Tbl_Akun, id=610L)
    a_penambahan_saldo_kredit = get_object_or_404(Tbl_Akun, id=618L)
    jurnal = Jurnal.objects.create(
        diskripsi= 'Pengiriman KAS Gerai ke CIMAHI: %s ' % (biaya.ket_penambahan_saldo),
        tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_penambahan_saldo)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENAMBAHAN_GERAI"), id_coa = a_penambahan_saldo_debet,
        kredit = 0,debet = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
     
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENAMBAHAN_GERAI"), id_coa = a_penambahan_saldo_kredit,
        debet = 0,kredit = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
    
def jurnal_biaya_penambahan_saldo_kas_du_bubat(biaya, user):
    D = decimal.Decimal
    a_penambahan_saldo_debet = get_object_or_404(Tbl_Akun, id=610L)
    a_penambahan_saldo_kredit = get_object_or_404(Tbl_Akun, id=619L)
    jurnal = Jurnal.objects.create(
        diskripsi= 'Pengiriman KAS Gerai ke BUBAT: %s ' % (biaya.ket_penambahan_saldo),
        tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_penambahan_saldo)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENAMBAHAN_GERAI"), id_coa = a_penambahan_saldo_debet,
        kredit = 0,debet = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
     
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENAMBAHAN_GERAI"), id_coa = a_penambahan_saldo_kredit,
        debet = 0,kredit = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)

def jurnal_biaya_penambahan_saldo_kas_du_maranatha(biaya, user):
    D = decimal.Decimal
    a_penambahan_saldo_debet = get_object_or_404(Tbl_Akun, id=610L)
    a_penambahan_saldo_kredit = get_object_or_404(Tbl_Akun, id=622L)
    jurnal = Jurnal.objects.create(
        diskripsi= 'Pengiriman KAS Gerai ke MARANATHA: %s ' % (biaya.ket_penambahan_saldo),
        tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_penambahan_saldo)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENAMBAHAN_GERAI"), id_coa = a_penambahan_saldo_debet,
        kredit = 0,debet = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
     
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENAMBAHAN_GERAI"), id_coa = a_penambahan_saldo_kredit,
        debet = 0,kredit = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
       
def jurnal_biaya_penambahan_saldo_kas_du_cirebon(biaya, user):
    D = decimal.Decimal
    a_penambahan_saldo_debet = get_object_or_404(Tbl_Akun, id=610L)
    a_penambahan_saldo_kredit = get_object_or_404(Tbl_Akun, id=624L)
    jurnal = Jurnal.objects.create(
        diskripsi= 'Pengiriman KAS Gerai ke CIREBON: %s ' % (biaya.ket_penambahan_saldo),
        tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_penambahan_saldo)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENAMBAHAN_GERAI"), id_coa = a_penambahan_saldo_debet,
        kredit = 0,debet = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
     
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENAMBAHAN_GERAI"), id_coa = a_penambahan_saldo_kredit,
        debet = 0,kredit = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)

def jurnal_biaya_penambahan_saldo_kas_du_ciumbeleuit(biaya, user):
    D = decimal.Decimal
    a_penambahan_saldo_debet = get_object_or_404(Tbl_Akun, id=610L)
    a_penambahan_saldo_kredit = get_object_or_404(Tbl_Akun, id=626L)
    jurnal = Jurnal.objects.create(
        diskripsi= 'Pengiriman KAS Gerai ke ciumbeleuit: %s ' % (biaya.ket_penambahan_saldo),
        tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_penambahan_saldo)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENAMBAHAN_GERAI"), id_coa = a_penambahan_saldo_debet,
        kredit = 0,debet = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
     
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENAMBAHAN_GERAI"), id_coa = a_penambahan_saldo_kredit,
        debet = 0,kredit = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
    
def jurnal_biaya_penambahan_saldo_kas_du_uber(biaya, user):
    D = decimal.Decimal
    a_penambahan_saldo_debet = get_object_or_404(Tbl_Akun, id=610L)
    a_penambahan_saldo_kredit = get_object_or_404(Tbl_Akun, id=627L)
    jurnal = Jurnal.objects.create(
        diskripsi= 'Pengiriman KAS Gerai ke UJUNG BERUNG: %s ' % (biaya.ket_penambahan_saldo),
        tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_penambahan_saldo)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENAMBAHAN_GERAI"), id_coa = a_penambahan_saldo_debet,
        kredit = 0,debet = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
     
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENAMBAHAN_GERAI"), id_coa = a_penambahan_saldo_kredit,
        debet = 0,kredit = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
    
def jurnal_biaya_penambahan_saldo_kas_du_ciwastra(biaya, user):
    D = decimal.Decimal
    a_penambahan_saldo_debet = get_object_or_404(Tbl_Akun, id=610L)
    a_penambahan_saldo_kredit = get_object_or_404(Tbl_Akun, id=628L)
    jurnal = Jurnal.objects.create(
        diskripsi= 'Pengiriman KAS Gerai ke CIWASTRA: %s ' % (biaya.ket_penambahan_saldo),
        tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_penambahan_saldo)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENAMBAHAN_GERAI"), id_coa = a_penambahan_saldo_debet,
        kredit = 0,debet = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENAMBAHAN_GERAI"), id_coa = a_penambahan_saldo_kredit,
        debet = 0,kredit = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)

####Jurnal kas dari Balubur ke pusat 
def jurnal_biaya_penambahan_saldo_kas_balubur_pusat(biaya, user):
    D = decimal.Decimal
    a_penambahan_saldo_debet = get_object_or_404(Tbl_Akun, id=611L)
    a_penambahan_saldo_kredit = get_object_or_404(Tbl_Akun, id=4L)
    jurnal = Jurnal.objects.create(
        diskripsi= 'Pengembalian KasGerai NoRek: %s ' % (biaya.ket_penambahan_saldo),
        tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_penambahan_saldo)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENAMBAHAN_PUSAT"), id_coa = a_penambahan_saldo_debet,
        kredit = 0,debet = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
     
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENAMBAHAN_PUSAT"), id_coa = a_penambahan_saldo_kredit,
        debet = 0,kredit = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
    
def jurnal_biaya_penambahan_saldo_kas_balubur_jakarta(biaya, user):
    D = decimal.Decimal
    a_penambahan_saldo_debet = get_object_or_404(Tbl_Akun, id=611L)
    a_penambahan_saldo_kredit = get_object_or_404(Tbl_Akun, id=7L)
    jurnal = Jurnal.objects.create(
        diskripsi= 'Pengiriman KAS Gerai ke SUCI: %s ' % (biaya.ket_penambahan_saldo),
        tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_penambahan_saldo)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENAMBAHAN_GERAI"), id_coa = a_penambahan_saldo_debet,
        kredit = 0,debet = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
     
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENAMBAHAN_GERAI"), id_coa = a_penambahan_saldo_kredit,
        debet = 0,kredit = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
    
def jurnal_biaya_penambahan_saldo_kas_balubur_du(biaya, user):
    D = decimal.Decimal
    a_penambahan_saldo_debet = get_object_or_404(Tbl_Akun, id=611L)
    a_penambahan_saldo_kredit = get_object_or_404(Tbl_Akun, id=610L)
    jurnal = Jurnal.objects.create(
        diskripsi= 'Pengiriman KAS Gerai ke DU: %s ' % (biaya.ket_penambahan_saldo),
        tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_penambahan_saldo)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENAMBAHAN_GERAI"), id_coa = a_penambahan_saldo_debet,
        kredit = 0,debet = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
     
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENAMBAHAN_GERAI"), id_coa = a_penambahan_saldo_kredit,
        debet = 0,kredit = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
    
def jurnal_biaya_penambahan_saldo_kas_balubur_suci(biaya, user):
    D = decimal.Decimal
    a_penambahan_saldo_debet = get_object_or_404(Tbl_Akun, id=611L)
    a_penambahan_saldo_kredit = get_object_or_404(Tbl_Akun, id=609L)
    jurnal = Jurnal.objects.create(
        diskripsi= 'Pengiriman KAS Gerai ke BALUBUR: %s ' % (biaya.ket_penambahan_saldo),
        tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_penambahan_saldo)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENAMBAHAN_GERAI"), id_coa = a_penambahan_saldo_debet,
        kredit = 0,debet = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
     
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENAMBAHAN_GERAI"), id_coa = a_penambahan_saldo_kredit,
        debet = 0,kredit = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
    
def jurnal_biaya_penambahan_saldo_kas_balubur_hilir(biaya, user):
    D = decimal.Decimal
    a_penambahan_saldo_debet = get_object_or_404(Tbl_Akun, id=611L)
    a_penambahan_saldo_kredit = get_object_or_404(Tbl_Akun, id=613L)
    jurnal = Jurnal.objects.create(
        diskripsi= 'Pengiriman KAS Gerai ke HILIR: %s ' % (biaya.ket_penambahan_saldo),
        tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_penambahan_saldo)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENAMBAHAN_GERAI"), id_coa = a_penambahan_saldo_debet,
        kredit = 0,debet = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
     
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENAMBAHAN_GERAI"), id_coa = a_penambahan_saldo_kredit,
        debet = 0,kredit = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)

def jurnal_biaya_penambahan_saldo_kas_balubur_kopo(biaya, user):
    D = decimal.Decimal
    a_penambahan_saldo_debet = get_object_or_404(Tbl_Akun, id=611L)
    a_penambahan_saldo_kredit = get_object_or_404(Tbl_Akun, id=614L)
    jurnal = Jurnal.objects.create(
        diskripsi= 'Pengiriman KAS Gerai ke KOPO: %s ' % (biaya.ket_penambahan_saldo),
        tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_penambahan_saldo)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENAMBAHAN_GERAI"), id_coa = a_penambahan_saldo_debet,
        kredit = 0,debet = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
     
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENAMBAHAN_GERAI"), id_coa = a_penambahan_saldo_kredit,
        debet = 0,kredit = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
    
def jurnal_biaya_penambahan_saldo_kas_balubur_cibiru(biaya, user):
    D = decimal.Decimal
    a_penambahan_saldo_debet = get_object_or_404(Tbl_Akun, id=611L)
    a_penambahan_saldo_kredit = get_object_or_404(Tbl_Akun, id=615L)
    jurnal = Jurnal.objects.create(
        diskripsi= 'Pengiriman KAS Gerai ke CIBIRU: %s ' % (biaya.ket_penambahan_saldo),
        tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_penambahan_saldo)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENAMBAHAN_GERAI"), id_coa = a_penambahan_saldo_debet,
        kredit = 0,debet = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
     
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENAMBAHAN_GERAI"), id_coa = a_penambahan_saldo_kredit,
        debet = 0,kredit = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
    
def jurnal_biaya_penambahan_saldo_kas_balubur_cipacing(biaya, user):
    D = decimal.Decimal
    a_penambahan_saldo_debet = get_object_or_404(Tbl_Akun, id=611L)
    a_penambahan_saldo_kredit = get_object_or_404(Tbl_Akun, id=616L)
    jurnal = Jurnal.objects.create(
        diskripsi= 'Pengiriman KAS Gerai ke CIPACING: %s ' % (biaya.ket_penambahan_saldo),
        tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_penambahan_saldo)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENAMBAHAN_GERAI"), id_coa = a_penambahan_saldo_debet,
        kredit = 0,debet = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
     
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENAMBAHAN_GERAI"), id_coa = a_penambahan_saldo_kredit,
        debet = 0,kredit = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)

def jurnal_biaya_penambahan_saldo_kas_balubur_jatinangor(biaya, user):
    D = decimal.Decimal
    a_penambahan_saldo_debet = get_object_or_404(Tbl_Akun, id=611L)
    a_penambahan_saldo_kredit = get_object_or_404(Tbl_Akun, id=617L)
    jurnal = Jurnal.objects.create(
        diskripsi= 'Pengiriman KAS Gerai ke JATINANGOR: %s ' % (biaya.ket_penambahan_saldo),
        tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_penambahan_saldo)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENAMBAHAN_GERAI"), id_coa = a_penambahan_saldo_debet,
        kredit = 0,debet = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
     
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENAMBAHAN_GERAI"), id_coa = a_penambahan_saldo_kredit,
        debet = 0,kredit = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
    
def jurnal_biaya_penambahan_saldo_kas_balubur_cimahi(biaya, user):
    D = decimal.Decimal
    a_penambahan_saldo_debet = get_object_or_404(Tbl_Akun, id=611L)
    a_penambahan_saldo_kredit = get_object_or_404(Tbl_Akun, id=618L)
    jurnal = Jurnal.objects.create(
        diskripsi= 'Pengiriman KAS Gerai ke CIMAHI: %s ' % (biaya.ket_penambahan_saldo),
        tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_penambahan_saldo)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENAMBAHAN_GERAI"), id_coa = a_penambahan_saldo_debet,
        kredit = 0,debet = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
     
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENAMBAHAN_GERAI"), id_coa = a_penambahan_saldo_kredit,
        debet = 0,kredit = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
    
def jurnal_biaya_penambahan_saldo_kas_balubur_bubat(biaya, user):
    D = decimal.Decimal
    a_penambahan_saldo_debet = get_object_or_404(Tbl_Akun, id=611L)
    a_penambahan_saldo_kredit = get_object_or_404(Tbl_Akun, id=619L)
    jurnal = Jurnal.objects.create(
        diskripsi= 'Pengiriman KAS Gerai ke BUBAT: %s ' % (biaya.ket_penambahan_saldo),
        tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_penambahan_saldo)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENAMBAHAN_GERAI"), id_coa = a_penambahan_saldo_debet,
        kredit = 0,debet = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
     
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENAMBAHAN_GERAI"), id_coa = a_penambahan_saldo_kredit,
        debet = 0,kredit = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)

def jurnal_biaya_penambahan_saldo_kas_balubur_maranatha(biaya, user):
    D = decimal.Decimal
    a_penambahan_saldo_debet = get_object_or_404(Tbl_Akun, id=611L)
    a_penambahan_saldo_kredit = get_object_or_404(Tbl_Akun, id=622L)
    jurnal = Jurnal.objects.create(
        diskripsi= 'Pengiriman KAS Gerai ke MARANATHA: %s ' % (biaya.ket_penambahan_saldo),
        tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_penambahan_saldo)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENAMBAHAN_GERAI"), id_coa = a_penambahan_saldo_debet,
        kredit = 0,debet = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
     
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENAMBAHAN_GERAI"), id_coa = a_penambahan_saldo_kredit,
        debet = 0,kredit = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
       
def jurnal_biaya_penambahan_saldo_kas_balubur_cirebon(biaya, user):
    D = decimal.Decimal
    a_penambahan_saldo_debet = get_object_or_404(Tbl_Akun, id=611L)
    a_penambahan_saldo_kredit = get_object_or_404(Tbl_Akun, id=624L)
    jurnal = Jurnal.objects.create(
        diskripsi= 'Pengiriman KAS Gerai ke CIREBON: %s ' % (biaya.ket_penambahan_saldo),
        tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_penambahan_saldo)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENAMBAHAN_GERAI"), id_coa = a_penambahan_saldo_debet,
        kredit = 0,debet = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
     
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENAMBAHAN_GERAI"), id_coa = a_penambahan_saldo_kredit,
        debet = 0,kredit = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)

def jurnal_biaya_penambahan_saldo_kas_balubur_ciumbeleuit(biaya, user):
    D = decimal.Decimal
    a_penambahan_saldo_debet = get_object_or_404(Tbl_Akun, id=611L)
    a_penambahan_saldo_kredit = get_object_or_404(Tbl_Akun, id=626L)
    jurnal = Jurnal.objects.create(
        diskripsi= 'Pengiriman KAS Gerai ke ciumbeleuit: %s ' % (biaya.ket_penambahan_saldo),
        tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_penambahan_saldo)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENAMBAHAN_GERAI"), id_coa = a_penambahan_saldo_debet,
        kredit = 0,debet = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
     
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENAMBAHAN_GERAI"), id_coa = a_penambahan_saldo_kredit,
        debet = 0,kredit = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
    
def jurnal_biaya_penambahan_saldo_kas_balubur_uber(biaya, user):
    D = decimal.Decimal
    a_penambahan_saldo_debet = get_object_or_404(Tbl_Akun, id=611L)
    a_penambahan_saldo_kredit = get_object_or_404(Tbl_Akun, id=627L)
    jurnal = Jurnal.objects.create(
        diskripsi= 'Pengiriman KAS Gerai ke UJUNG BERUNG: %s ' % (biaya.ket_penambahan_saldo),
        tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_penambahan_saldo)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENAMBAHAN_GERAI"), id_coa = a_penambahan_saldo_debet,
        kredit = 0,debet = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
     
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENAMBAHAN_GERAI"), id_coa = a_penambahan_saldo_kredit,
        debet = 0,kredit = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
    
def jurnal_biaya_penambahan_saldo_kas_balubur_ciwastra(biaya, user):
    D = decimal.Decimal
    a_penambahan_saldo_debet = get_object_or_404(Tbl_Akun, id=611L)
    a_penambahan_saldo_kredit = get_object_or_404(Tbl_Akun, id=628L)
    jurnal = Jurnal.objects.create(
        diskripsi= 'Pengiriman KAS Gerai ke CIWASTRA: %s ' % (biaya.ket_penambahan_saldo),
        tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_penambahan_saldo)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENAMBAHAN_GERAI"), id_coa = a_penambahan_saldo_debet,
        kredit = 0,debet = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENAMBAHAN_GERAI"), id_coa = a_penambahan_saldo_kredit,
        debet = 0,kredit = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
    
###Jurnal kas dari Hilir ke pusat 
def jurnal_biaya_penambahan_saldo_kas_hilir_pusat(biaya, user):
    D = decimal.Decimal
    a_penambahan_saldo_debet = get_object_or_404(Tbl_Akun, id=613L)
    a_penambahan_saldo_kredit = get_object_or_404(Tbl_Akun, id=4L)
    jurnal = Jurnal.objects.create(
        diskripsi= 'Pengembalian KasGerai NoRek: %s ' % (biaya.ket_penambahan_saldo),
        tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_penambahan_saldo)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_PUSAT"), id_coa = a_penambahan_saldo_debet,
        kredit = 0,debet = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
     
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_PUSAT"), id_coa = a_penambahan_saldo_kredit,
        debet = 0,kredit = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
    
def jurnal_biaya_penambahan_saldo_kas_hilir_jakarta(biaya, user):
    D = decimal.Decimal
    a_penambahan_saldo_debet = get_object_or_404(Tbl_Akun, id=613L)
    a_penambahan_saldo_kredit = get_object_or_404(Tbl_Akun, id=7L)
    jurnal = Jurnal.objects.create(
        diskripsi= 'Pengiriman KAS Gerai ke SUCI: %s ' % (biaya.ket_penambahan_saldo),
        tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_penambahan_saldo)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_debet,
        kredit = 0,debet = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
     
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_kredit,
        debet = 0,kredit = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
    
def jurnal_biaya_penambahan_saldo_kas_hilir_du(biaya, user):
    D = decimal.Decimal
    a_penambahan_saldo_debet = get_object_or_404(Tbl_Akun, id=613L)
    a_penambahan_saldo_kredit = get_object_or_404(Tbl_Akun, id=610L)
    jurnal = Jurnal.objects.create(
        diskripsi= 'Pengiriman KAS Gerai ke DU: %s ' % (biaya.ket_penambahan_saldo),
        tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_penambahan_saldo)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_debet,
        kredit = 0,debet = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
     
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_kredit,
        debet = 0,kredit = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
    
def jurnal_biaya_penambahan_saldo_kas_hilir_suci(biaya, user):
    D = decimal.Decimal
    a_penambahan_saldo_debet = get_object_or_404(Tbl_Akun, id=613L)
    a_penambahan_saldo_kredit = get_object_or_404(Tbl_Akun, id=609L)
    jurnal = Jurnal.objects.create(
        diskripsi= 'Pengiriman KAS Gerai ke Suci: %s ' % (biaya.ket_penambahan_saldo),
        tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_penambahan_saldo)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_debet,
        kredit = 0,debet = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
     
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_kredit,
        debet = 0,kredit = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
    
def jurnal_biaya_penambahan_saldo_kas_hilir_balubur(biaya, user):
    D = decimal.Decimal
    a_penambahan_saldo_debet = get_object_or_404(Tbl_Akun, id=613L)
    a_penambahan_saldo_kredit = get_object_or_404(Tbl_Akun, id=611L)
    jurnal = Jurnal.objects.create(
        diskripsi= 'Pengiriman KAS Gerai ke Balubur: %s ' % (biaya.ket_penambahan_saldo),
        tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_penambahan_saldo)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_debet,
        kredit = 0,debet = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
     
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_kredit,
        debet = 0,kredit = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)

def jurnal_biaya_penambahan_saldo_kas_hilir_kopo(biaya, user):
    D = decimal.Decimal
    a_penambahan_saldo_debet = get_object_or_404(Tbl_Akun, id=613L)
    a_penambahan_saldo_kredit = get_object_or_404(Tbl_Akun, id=614L)
    jurnal = Jurnal.objects.create(
        diskripsi= 'Pengiriman KAS Gerai ke KOPO: %s ' % (biaya.ket_penambahan_saldo),
        tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_penambahan_saldo)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_debet,
        kredit = 0,debet = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
     
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_kredit,
        debet = 0,kredit = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
    
def jurnal_biaya_penambahan_saldo_kas_hilir_cibiru(biaya, user):
    D = decimal.Decimal
    a_penambahan_saldo_debet = get_object_or_404(Tbl_Akun, id=613L)
    a_penambahan_saldo_kredit = get_object_or_404(Tbl_Akun, id=615L)
    jurnal = Jurnal.objects.create(
        diskripsi= 'Pengiriman KAS Gerai ke CIBIRU: %s ' % (biaya.ket_penambahan_saldo),
        tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_penambahan_saldo)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_debet,
        kredit = 0,debet = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
     
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_kredit,
        debet = 0,kredit = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
    
def jurnal_biaya_penambahan_saldo_kas_hilir_cipacing(biaya, user):
    D = decimal.Decimal
    a_penambahan_saldo_debet = get_object_or_404(Tbl_Akun, id=613L)
    a_penambahan_saldo_kredit = get_object_or_404(Tbl_Akun, id=616L)
    jurnal = Jurnal.objects.create(
        diskripsi= 'Pengiriman KAS Gerai ke CIPACING: %s ' % (biaya.ket_penambahan_saldo),
        tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_penambahan_saldo)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_debet,
        kredit = 0,debet = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
     
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_kredit,
        debet = 0,kredit = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)

def jurnal_biaya_penambahan_saldo_kas_hilir_jatinangor(biaya, user):
    D = decimal.Decimal
    a_penambahan_saldo_debet = get_object_or_404(Tbl_Akun, id=613L)
    a_penambahan_saldo_kredit = get_object_or_404(Tbl_Akun, id=617L)
    jurnal = Jurnal.objects.create(
        diskripsi= 'Pengiriman KAS Gerai ke JATINANGOR: %s ' % (biaya.ket_penambahan_saldo),
        tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_penambahan_saldo)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_debet,
        kredit = 0,debet = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
     
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_kredit,
        debet = 0,kredit = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
    
def jurnal_biaya_penambahan_saldo_kas_hilir_cimahi(biaya, user):
    D = decimal.Decimal
    a_penambahan_saldo_debet = get_object_or_404(Tbl_Akun, id=613L)
    a_penambahan_saldo_kredit = get_object_or_404(Tbl_Akun, id=618L)
    jurnal = Jurnal.objects.create(
        diskripsi= 'Pengiriman KAS Gerai ke CIMAHI: %s ' % (biaya.ket_penambahan_saldo),
        tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_penambahan_saldo)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_debet,
        kredit = 0,debet = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
     
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_kredit,
        debet = 0,kredit = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
    
def jurnal_biaya_penambahan_saldo_kas_hilir_bubat(biaya, user):
    D = decimal.Decimal
    a_penambahan_saldo_debet = get_object_or_404(Tbl_Akun, id=613L)
    a_penambahan_saldo_kredit = get_object_or_404(Tbl_Akun, id=619L)
    jurnal = Jurnal.objects.create(
        diskripsi= 'Pengiriman KAS Gerai ke BUBAT: %s ' % (biaya.ket_penambahan_saldo),
        tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_penambahan_saldo)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_debet,
        kredit = 0,debet = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
     
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_kredit,
        debet = 0,kredit = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)

def jurnal_biaya_penambahan_saldo_kas_hilir_maranatha(biaya, user):
    D = decimal.Decimal
    a_penambahan_saldo_debet = get_object_or_404(Tbl_Akun, id=613L)
    a_penambahan_saldo_kredit = get_object_or_404(Tbl_Akun, id=622L)
    jurnal = Jurnal.objects.create(
        diskripsi= 'Pengiriman KAS Gerai ke MARANATHA: %s ' % (biaya.ket_penambahan_saldo),
        tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_penambahan_saldo)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_debet,
        kredit = 0,debet = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
     
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_kredit,
        debet = 0,kredit = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
       
def jurnal_biaya_penambahan_saldo_kas_hilir_cirebon(biaya, user):
    D = decimal.Decimal
    a_penambahan_saldo_debet = get_object_or_404(Tbl_Akun, id=613L)
    a_penambahan_saldo_kredit = get_object_or_404(Tbl_Akun, id=624L)
    jurnal = Jurnal.objects.create(
        diskripsi= 'Pengiriman KAS Gerai ke CIREBON: %s ' % (biaya.ket_penambahan_saldo),
        tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_penambahan_saldo)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_debet,
        kredit = 0,debet = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
     
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_kredit,
        debet = 0,kredit = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)

def jurnal_biaya_penambahan_saldo_kas_hilir_ciumbeleuit(biaya, user):
    D = decimal.Decimal
    a_penambahan_saldo_debet = get_object_or_404(Tbl_Akun, id=613L)
    a_penambahan_saldo_kredit = get_object_or_404(Tbl_Akun, id=626L)
    jurnal = Jurnal.objects.create(
        diskripsi= 'Pengiriman KAS Gerai ke ciumbeleuit: %s ' % (biaya.ket_penambahan_saldo),
        tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_penambahan_saldo)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_debet,
        kredit = 0,debet = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
     
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_kredit,
        debet = 0,kredit = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
    
def jurnal_biaya_penambahan_saldo_kas_hilir_uber(biaya, user):
    D = decimal.Decimal
    a_penambahan_saldo_debet = get_object_or_404(Tbl_Akun, id=613L)
    a_penambahan_saldo_kredit = get_object_or_404(Tbl_Akun, id=627L)
    jurnal = Jurnal.objects.create(
        diskripsi= 'Pengiriman KAS Gerai ke UJUNG BERUNG: %s ' % (biaya.ket_penambahan_saldo),
        tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_penambahan_saldo)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_debet,
        kredit = 0,debet = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
     
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_kredit,
        debet = 0,kredit = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
    
def jurnal_biaya_penambahan_saldo_kas_hilir_ciwastra(biaya, user):
    D = decimal.Decimal
    a_penambahan_saldo_debet = get_object_or_404(Tbl_Akun, id=613L)
    a_penambahan_saldo_kredit = get_object_or_404(Tbl_Akun, id=628L)
    jurnal = Jurnal.objects.create(
        diskripsi= 'Pengiriman KAS Gerai ke CIWASTRA: %s ' % (biaya.ket_penambahan_saldo),
        tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_penambahan_saldo)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_debet,
        kredit = 0,debet = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_kredit,
        debet = 0,kredit = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)

###Jurnal kas dari Kopo ke pusat 
def jurnal_biaya_penambahan_saldo_kas_kopo_pusat(biaya, user):
    D = decimal.Decimal
    a_penambahan_saldo_debet = get_object_or_404(Tbl_Akun, id=614L)
    a_penambahan_saldo_kredit = get_object_or_404(Tbl_Akun, id=4L)
    jurnal = Jurnal.objects.create(
        diskripsi= 'Pengembalian KasGerai NoRek: %s ' % (biaya.ket_penambahan_saldo),
        tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_penambahan_saldo)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_PUSAT"), id_coa = a_penambahan_saldo_debet,
        kredit = 0,debet = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
     
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_PUSAT"), id_coa = a_penambahan_saldo_kredit,
        debet = 0,kredit = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
    
def jurnal_biaya_penambahan_saldo_kas_kopo_jakarta(biaya, user):
    D = decimal.Decimal
    a_penambahan_saldo_debet = get_object_or_404(Tbl_Akun, id=614L)
    a_penambahan_saldo_kredit = get_object_or_404(Tbl_Akun, id=7L)
    jurnal = Jurnal.objects.create(
        diskripsi= 'Pengiriman KAS Gerai ke SUCI: %s ' % (biaya.ket_penambahan_saldo),
        tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_penambahan_saldo)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_debet,
        kredit = 0,debet = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
     
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_kredit,
        debet = 0,kredit = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
    
def jurnal_biaya_penambahan_saldo_kas_kopo_du(biaya, user):
    D = decimal.Decimal
    a_penambahan_saldo_debet = get_object_or_404(Tbl_Akun, id=614L)
    a_penambahan_saldo_kredit = get_object_or_404(Tbl_Akun, id=610L)
    jurnal = Jurnal.objects.create(
        diskripsi= 'Pengiriman KAS Gerai ke DU: %s ' % (biaya.ket_penambahan_saldo),
        tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_penambahan_saldo)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_debet,
        kredit = 0,debet = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
     
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_kredit,
        debet = 0,kredit = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
    
def jurnal_biaya_penambahan_saldo_kas_kopo_suci(biaya, user):
    D = decimal.Decimal
    a_penambahan_saldo_debet = get_object_or_404(Tbl_Akun, id=614L)
    a_penambahan_saldo_kredit = get_object_or_404(Tbl_Akun, id=609L)
    jurnal = Jurnal.objects.create(
        diskripsi= 'Pengiriman KAS Gerai ke Suci: %s ' % (biaya.ket_penambahan_saldo),
        tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_penambahan_saldo)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_debet,
        kredit = 0,debet = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
     
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_kredit,
        debet = 0,kredit = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
    
def jurnal_biaya_penambahan_saldo_kas_kopo_balubur(biaya, user):
    D = decimal.Decimal
    a_penambahan_saldo_debet = get_object_or_404(Tbl_Akun, id=614L)
    a_penambahan_saldo_kredit = get_object_or_404(Tbl_Akun, id=611L)
    jurnal = Jurnal.objects.create(
        diskripsi= 'Pengiriman KAS Gerai ke Balubur: %s ' % (biaya.ket_penambahan_saldo),
        tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_penambahan_saldo)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_debet,
        kredit = 0,debet = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
     
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_kredit,
        debet = 0,kredit = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)

def jurnal_biaya_penambahan_saldo_kas_kopo_hilir (biaya, user):
    D = decimal.Decimal
    a_penambahan_saldo_debet = get_object_or_404(Tbl_Akun, id=614L)
    a_penambahan_saldo_kredit = get_object_or_404(Tbl_Akun, id=613L)
    jurnal = Jurnal.objects.create(
        diskripsi= 'Pengiriman KAS Gerai ke KOPO: %s ' % (biaya.ket_penambahan_saldo),
        tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_penambahan_saldo)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_debet,
        kredit = 0,debet = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
     
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_kredit,
        debet = 0,kredit = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
    
def jurnal_biaya_penambahan_saldo_kas_kopo_cibiru(biaya, user):
    D = decimal.Decimal
    a_penambahan_saldo_debet = get_object_or_404(Tbl_Akun, id=614L)
    a_penambahan_saldo_kredit = get_object_or_404(Tbl_Akun, id=615L)
    jurnal = Jurnal.objects.create(
        diskripsi= 'Pengiriman KAS Gerai ke CIBIRU: %s ' % (biaya.ket_penambahan_saldo),
        tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_penambahan_saldo)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_debet,
        kredit = 0,debet = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
     
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_kredit,
        debet = 0,kredit = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
    
def jurnal_biaya_penambahan_saldo_kas_kopo_cipacing(biaya, user):
    D = decimal.Decimal
    a_penambahan_saldo_debet = get_object_or_404(Tbl_Akun, id=614L)
    a_penambahan_saldo_kredit = get_object_or_404(Tbl_Akun, id=616L)
    jurnal = Jurnal.objects.create(
        diskripsi= 'Pengiriman KAS Gerai ke CIPACING: %s ' % (biaya.ket_penambahan_saldo),
        tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_penambahan_saldo)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_debet,
        kredit = 0,debet = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
     
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_kredit,
        debet = 0,kredit = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)

def jurnal_biaya_penambahan_saldo_kas_kopo_jatinangor(biaya, user):
    D = decimal.Decimal
    a_penambahan_saldo_debet = get_object_or_404(Tbl_Akun, id=614L)
    a_penambahan_saldo_kredit = get_object_or_404(Tbl_Akun, id=617L)
    jurnal = Jurnal.objects.create(
        diskripsi= 'Pengiriman KAS Gerai ke JATINANGOR: %s ' % (biaya.ket_penambahan_saldo),
        tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_penambahan_saldo)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_debet,
        kredit = 0,debet = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
     
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_kredit,
        debet = 0,kredit = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
    
def jurnal_biaya_penambahan_saldo_kas_kopo_cimahi(biaya, user):
    D = decimal.Decimal
    a_penambahan_saldo_debet = get_object_or_404(Tbl_Akun, id=614L)
    a_penambahan_saldo_kredit = get_object_or_404(Tbl_Akun, id=618L)
    jurnal = Jurnal.objects.create(
        diskripsi= 'Pengiriman KAS Gerai ke CIMAHI: %s ' % (biaya.ket_penambahan_saldo),
        tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_penambahan_saldo)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_debet,
        kredit = 0,debet = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
     
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_kredit,
        debet = 0,kredit = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
    
def jurnal_biaya_penambahan_saldo_kas_kopo_bubat(biaya, user):
    D = decimal.Decimal
    a_penambahan_saldo_debet = get_object_or_404(Tbl_Akun, id=614L)
    a_penambahan_saldo_kredit = get_object_or_404(Tbl_Akun, id=619L)
    jurnal = Jurnal.objects.create(
        diskripsi= 'Pengiriman KAS Gerai ke BUBAT: %s ' % (biaya.ket_penambahan_saldo),
        tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_penambahan_saldo)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_debet,
        kredit = 0,debet = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
     
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_kredit,
        debet = 0,kredit = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)

def jurnal_biaya_penambahan_saldo_kas_kopo_maranatha(biaya, user):
    D = decimal.Decimal
    a_penambahan_saldo_debet = get_object_or_404(Tbl_Akun, id=614L)
    a_penambahan_saldo_kredit = get_object_or_404(Tbl_Akun, id=622L)
    jurnal = Jurnal.objects.create(
        diskripsi= 'Pengiriman KAS Gerai ke MARANATHA: %s ' % (biaya.ket_penambahan_saldo),
        tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_penambahan_saldo)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_debet,
        kredit = 0,debet = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
     
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_kredit,
        debet = 0,kredit = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
       
def jurnal_biaya_penambahan_saldo_kas_kopo_cirebon(biaya, user):
    D = decimal.Decimal
    a_penambahan_saldo_debet = get_object_or_404(Tbl_Akun, id=614L)
    a_penambahan_saldo_kredit = get_object_or_404(Tbl_Akun, id=624L)
    jurnal = Jurnal.objects.create(
        diskripsi= 'Pengiriman KAS Gerai ke CIREBON: %s ' % (biaya.ket_penambahan_saldo),
        tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_penambahan_saldo)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_debet,
        kredit = 0,debet = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
     
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_kredit,
        debet = 0,kredit = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)

def jurnal_biaya_penambahan_saldo_kas_kopo_ciumbeleuit(biaya, user):
    D = decimal.Decimal
    a_penambahan_saldo_debet = get_object_or_404(Tbl_Akun, id=614L)
    a_penambahan_saldo_kredit = get_object_or_404(Tbl_Akun, id=626L)
    jurnal = Jurnal.objects.create(
        diskripsi= 'Pengiriman KAS Gerai ke ciumbeleuit: %s ' % (biaya.ket_penambahan_saldo),
        tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_penambahan_saldo)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_debet,
        kredit = 0,debet = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
     
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_kredit,
        debet = 0,kredit = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
    
def jurnal_biaya_penambahan_saldo_kas_kopo_uber(biaya, user):
    D = decimal.Decimal
    a_penambahan_saldo_debet = get_object_or_404(Tbl_Akun, id=614L)
    a_penambahan_saldo_kredit = get_object_or_404(Tbl_Akun, id=627L)
    jurnal = Jurnal.objects.create(
        diskripsi= 'Pengiriman KAS Gerai ke UJUNG BERUNG: %s ' % (biaya.ket_penambahan_saldo),
        tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_penambahan_saldo)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_debet,
        kredit = 0,debet = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
     
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_kredit,
        debet = 0,kredit = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
    
def jurnal_biaya_penambahan_saldo_kas_kopo_ciwastra(biaya, user):
    D = decimal.Decimal
    a_penambahan_saldo_debet = get_object_or_404(Tbl_Akun, id=614L)
    a_penambahan_saldo_kredit = get_object_or_404(Tbl_Akun, id=628L)
    jurnal = Jurnal.objects.create(
        diskripsi= 'Pengiriman KAS Gerai ke CIWASTRA: %s ' % (biaya.ket_penambahan_saldo),
        tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_penambahan_saldo)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_debet,
        kredit = 0,debet = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_kredit,
        debet = 0,kredit = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
    
###Jurnal kas dari Cibiru ke pusat 
def jurnal_biaya_penambahan_saldo_kas_cibiru_pusat(biaya, user):
    D = decimal.Decimal
    a_penambahan_saldo_debet = get_object_or_404(Tbl_Akun, id=615L)
    a_penambahan_saldo_kredit = get_object_or_404(Tbl_Akun, id=4L)
    jurnal = Jurnal.objects.create(
        diskripsi= 'Pengembalian KasGerai NoRek: %s ' % (biaya.ket_penambahan_saldo),
        tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_penambahan_saldo)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_PUSAT"), id_coa = a_penambahan_saldo_debet,
        kredit = 0,debet = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
     
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_PUSAT"), id_coa = a_penambahan_saldo_kredit,
        debet = 0,kredit = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
    
def jurnal_biaya_penambahan_saldo_kas_cibiru_jakarta(biaya, user):
    D = decimal.Decimal
    a_penambahan_saldo_debet = get_object_or_404(Tbl_Akun, id=615L)
    a_penambahan_saldo_kredit = get_object_or_404(Tbl_Akun, id=7L)
    jurnal = Jurnal.objects.create(
        diskripsi= 'Pengiriman KAS Gerai ke Jakarta %s ' % (biaya.ket_penambahan_saldo),
        tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_penambahan_saldo)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_debet,
        kredit = 0,debet = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
     
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_kredit,
        debet = 0,kredit = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
    
def jurnal_biaya_penambahan_saldo_kas_cibiru_du(biaya, user):
    D = decimal.Decimal
    a_penambahan_saldo_debet = get_object_or_404(Tbl_Akun, id=615L)
    a_penambahan_saldo_kredit = get_object_or_404(Tbl_Akun, id=610L)
    jurnal = Jurnal.objects.create(
        diskripsi= 'Pengiriman KAS Gerai ke DU: %s ' % (biaya.ket_penambahan_saldo),
        tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_penambahan_saldo)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_debet,
        kredit = 0,debet = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
     
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_kredit,
        debet = 0,kredit = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
    
def jurnal_biaya_penambahan_saldo_kas_cibiru_suci(biaya, user):
    D = decimal.Decimal
    a_penambahan_saldo_debet = get_object_or_404(Tbl_Akun, id=615L)
    a_penambahan_saldo_kredit = get_object_or_404(Tbl_Akun, id=609L)
    jurnal = Jurnal.objects.create(
        diskripsi= 'Pengiriman KAS Gerai ke Suci: %s ' % (biaya.ket_penambahan_saldo),
        tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_penambahan_saldo)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_debet,
        kredit = 0,debet = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
     
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_kredit,
        debet = 0,kredit = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
    
def jurnal_biaya_penambahan_saldo_kas_cibiru_balubur(biaya, user):
    D = decimal.Decimal
    a_penambahan_saldo_debet = get_object_or_404(Tbl_Akun, id=615L)
    a_penambahan_saldo_kredit = get_object_or_404(Tbl_Akun, id=611L)
    jurnal = Jurnal.objects.create(
        diskripsi= 'Pengiriman KAS Gerai ke Balubur: %s ' % (biaya.ket_penambahan_saldo),
        tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_penambahan_saldo)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_debet,
        kredit = 0,debet = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
     
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_kredit,
        debet = 0,kredit = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)

def jurnal_biaya_penambahan_saldo_kas_cibiru_hilir (biaya, user):
    D = decimal.Decimal
    a_penambahan_saldo_debet = get_object_or_404(Tbl_Akun, id=615L)
    a_penambahan_saldo_kredit = get_object_or_404(Tbl_Akun, id=613L)
    jurnal = Jurnal.objects.create(
        diskripsi= 'Pengiriman KAS Gerai ke Hilir: %s ' % (biaya.ket_penambahan_saldo),
        tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_penambahan_saldo)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_debet,
        kredit = 0,debet = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
     
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_kredit,
        debet = 0,kredit = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
    
def jurnal_biaya_penambahan_saldo_kas_cibiru_kopo(biaya, user):
    D = decimal.Decimal
    a_penambahan_saldo_debet = get_object_or_404(Tbl_Akun, id=615L)
    a_penambahan_saldo_kredit = get_object_or_404(Tbl_Akun, id=614L)
    jurnal = Jurnal.objects.create(
        diskripsi= 'Pengiriman KAS Gerai ke Kopo: %s ' % (biaya.ket_penambahan_saldo),
        tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_penambahan_saldo)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_debet,
        kredit = 0,debet = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
     
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_kredit,
        debet = 0,kredit = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
    
def jurnal_biaya_penambahan_saldo_kas_cibiru_cipacing(biaya, user):
    D = decimal.Decimal
    a_penambahan_saldo_debet = get_object_or_404(Tbl_Akun, id=615L)
    a_penambahan_saldo_kredit = get_object_or_404(Tbl_Akun, id=616L)
    jurnal = Jurnal.objects.create(
        diskripsi= 'Pengiriman KAS Gerai ke CIPACING: %s ' % (biaya.ket_penambahan_saldo),
        tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_penambahan_saldo)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_debet,
        kredit = 0,debet = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
     
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_kredit,
        debet = 0,kredit = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)

def jurnal_biaya_penambahan_saldo_kas_cibiru_jatinangor(biaya, user):
    D = decimal.Decimal
    a_penambahan_saldo_debet = get_object_or_404(Tbl_Akun, id=615L)
    a_penambahan_saldo_kredit = get_object_or_404(Tbl_Akun, id=617L)
    jurnal = Jurnal.objects.create(
        diskripsi= 'Pengiriman KAS Gerai ke JATINANGOR: %s ' % (biaya.ket_penambahan_saldo),
        tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_penambahan_saldo)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_debet,
        kredit = 0,debet = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
     
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_kredit,
        debet = 0,kredit = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
    
def jurnal_biaya_penambahan_saldo_kas_cibiru_cimahi(biaya, user):
    D = decimal.Decimal
    a_penambahan_saldo_debet = get_object_or_404(Tbl_Akun, id=615L)
    a_penambahan_saldo_kredit = get_object_or_404(Tbl_Akun, id=618L)
    jurnal = Jurnal.objects.create(
        diskripsi= 'Pengiriman KAS Gerai ke CIMAHI: %s ' % (biaya.ket_penambahan_saldo),
        tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_penambahan_saldo)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_debet,
        kredit = 0,debet = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
     
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_kredit,
        debet = 0,kredit = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
    
def jurnal_biaya_penambahan_saldo_kas_cibiru_bubat(biaya, user):
    D = decimal.Decimal
    a_penambahan_saldo_debet = get_object_or_404(Tbl_Akun, id=615L)
    a_penambahan_saldo_kredit = get_object_or_404(Tbl_Akun, id=619L)
    jurnal = Jurnal.objects.create(
        diskripsi= 'Pengiriman KAS Gerai ke BUBAT: %s ' % (biaya.ket_penambahan_saldo),
        tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_penambahan_saldo)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_debet,
        kredit = 0,debet = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
     
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_kredit,
        debet = 0,kredit = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)

def jurnal_biaya_penambahan_saldo_kas_cibiru_maranatha(biaya, user):
    D = decimal.Decimal
    a_penambahan_saldo_debet = get_object_or_404(Tbl_Akun, id=615L)
    a_penambahan_saldo_kredit = get_object_or_404(Tbl_Akun, id=622L)
    jurnal = Jurnal.objects.create(
        diskripsi= 'Pengiriman KAS Gerai ke MARANATHA: %s ' % (biaya.ket_penambahan_saldo),
        tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_penambahan_saldo)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_debet,
        kredit = 0,debet = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
     
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_kredit,
        debet = 0,kredit = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
       
def jurnal_biaya_penambahan_saldo_kas_cibiru_cirebon(biaya, user):
    D = decimal.Decimal
    a_penambahan_saldo_debet = get_object_or_404(Tbl_Akun, id=615L)
    a_penambahan_saldo_kredit = get_object_or_404(Tbl_Akun, id=624L)
    jurnal = Jurnal.objects.create(
        diskripsi= 'Pengiriman KAS Gerai ke CIREBON: %s ' % (biaya.ket_penambahan_saldo),
        tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_penambahan_saldo)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_debet,
        kredit = 0,debet = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
     
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_kredit,
        debet = 0,kredit = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)

def jurnal_biaya_penambahan_saldo_kas_cibiru_ciumbeleuit(biaya, user):
    D = decimal.Decimal
    a_penambahan_saldo_debet = get_object_or_404(Tbl_Akun, id=615L)
    a_penambahan_saldo_kredit = get_object_or_404(Tbl_Akun, id=626L)
    jurnal = Jurnal.objects.create(
        diskripsi= 'Pengiriman KAS Gerai ke ciumbeleuit: %s ' % (biaya.ket_penambahan_saldo),
        tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_penambahan_saldo)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_debet,
        kredit = 0,debet = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
     
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_kredit,
        debet = 0,kredit = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
    
def jurnal_biaya_penambahan_saldo_kas_cibiru_uber(biaya, user):
    D = decimal.Decimal
    a_penambahan_saldo_debet = get_object_or_404(Tbl_Akun, id=615L)
    a_penambahan_saldo_kredit = get_object_or_404(Tbl_Akun, id=627L)
    jurnal = Jurnal.objects.create(
        diskripsi= 'Pengiriman KAS Gerai ke UJUNG BERUNG: %s ' % (biaya.ket_penambahan_saldo),
        tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_penambahan_saldo)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_debet,
        kredit = 0,debet = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
     
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_kredit,
        debet = 0,kredit = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
    
def jurnal_biaya_penambahan_saldo_kas_cibiru_ciwastra(biaya, user):
    D = decimal.Decimal
    a_penambahan_saldo_debet = get_object_or_404(Tbl_Akun, id=615L)
    a_penambahan_saldo_kredit = get_object_or_404(Tbl_Akun, id=628L)
    jurnal = Jurnal.objects.create(
        diskripsi= 'Pengiriman KAS Gerai ke CIWASTRA: %s ' % (biaya.ket_penambahan_saldo),
        tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_penambahan_saldo)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_debet,
        kredit = 0,debet = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_kredit,
        debet = 0,kredit = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)

###Jurnal kas dari CIpacing ke pusat 
def jurnal_biaya_penambahan_saldo_kas_cipacing_pusat(biaya, user):
    D = decimal.Decimal
    a_penambahan_saldo_debet = get_object_or_404(Tbl_Akun, id=616L)
    a_penambahan_saldo_kredit = get_object_or_404(Tbl_Akun, id=4L)
    jurnal = Jurnal.objects.create(
        diskripsi= 'Pengembalian KasGerai NoRek: %s ' % (biaya.ket_penambahan_saldo),
        tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_penambahan_saldo)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_PUSAT"), id_coa = a_penambahan_saldo_debet,
        kredit = 0,debet = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
     
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_PUSAT"), id_coa = a_penambahan_saldo_kredit,
        debet = 0,kredit = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
    
def jurnal_biaya_penambahan_saldo_kas_cipacing_jakarta(biaya, user):
    D = decimal.Decimal
    a_penambahan_saldo_debet = get_object_or_404(Tbl_Akun, id=616L)
    a_penambahan_saldo_kredit = get_object_or_404(Tbl_Akun, id=7L)
    jurnal = Jurnal.objects.create(
        diskripsi= 'Pengiriman KAS Gerai ke Jakarta %s ' % (biaya.ket_penambahan_saldo),
        tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_penambahan_saldo)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_debet,
        kredit = 0,debet = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
     
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_kredit,
        debet = 0,kredit = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
    
def jurnal_biaya_penambahan_saldo_kas_cipacing_du(biaya, user):
    D = decimal.Decimal
    a_penambahan_saldo_debet = get_object_or_404(Tbl_Akun, id=616L)
    a_penambahan_saldo_kredit = get_object_or_404(Tbl_Akun, id=610L)
    jurnal = Jurnal.objects.create(
        diskripsi= 'Pengiriman KAS Gerai ke DU: %s ' % (biaya.ket_penambahan_saldo),
        tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_penambahan_saldo)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_debet,
        kredit = 0,debet = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
     
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_kredit,
        debet = 0,kredit = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
    
def jurnal_biaya_penambahan_saldo_kas_cipacing_suci(biaya, user):
    D = decimal.Decimal
    a_penambahan_saldo_debet = get_object_or_404(Tbl_Akun, id=616L)
    a_penambahan_saldo_kredit = get_object_or_404(Tbl_Akun, id=609L)
    jurnal = Jurnal.objects.create(
        diskripsi= 'Pengiriman KAS Gerai ke Suci: %s ' % (biaya.ket_penambahan_saldo),
        tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_penambahan_saldo)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_debet,
        kredit = 0,debet = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
     
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_kredit,
        debet = 0,kredit = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
    
def jurnal_biaya_penambahan_saldo_kas_cipacing_balubur(biaya, user):
    D = decimal.Decimal
    a_penambahan_saldo_debet = get_object_or_404(Tbl_Akun, id=616L)
    a_penambahan_saldo_kredit = get_object_or_404(Tbl_Akun, id=611L)
    jurnal = Jurnal.objects.create(
        diskripsi= 'Pengiriman KAS Gerai ke Balubur: %s ' % (biaya.ket_penambahan_saldo),
        tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_penambahan_saldo)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_debet,
        kredit = 0,debet = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
     
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_kredit,
        debet = 0,kredit = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)

def jurnal_biaya_penambahan_saldo_kas_cipacing_hilir (biaya, user):
    D = decimal.Decimal
    a_penambahan_saldo_debet = get_object_or_404(Tbl_Akun, id=616L)
    a_penambahan_saldo_kredit = get_object_or_404(Tbl_Akun, id=613L)
    jurnal = Jurnal.objects.create(
        diskripsi= 'Pengiriman KAS Gerai ke Hilir: %s ' % (biaya.ket_penambahan_saldo),
        tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_penambahan_saldo)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_debet,
        kredit = 0,debet = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
     
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_kredit,
        debet = 0,kredit = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
    
def jurnal_biaya_penambahan_saldo_kas_cipacing_kopo(biaya, user):
    D = decimal.Decimal
    a_penambahan_saldo_debet = get_object_or_404(Tbl_Akun, id=616L)
    a_penambahan_saldo_kredit = get_object_or_404(Tbl_Akun, id=614L)
    jurnal = Jurnal.objects.create(
        diskripsi= 'Pengiriman KAS Gerai ke Kopo: %s ' % (biaya.ket_penambahan_saldo),
        tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_penambahan_saldo)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_debet,
        kredit = 0,debet = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
     
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_kredit,
        debet = 0,kredit = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
    
def jurnal_biaya_penambahan_saldo_kas_cipacing_cibiru(biaya, user):
    D = decimal.Decimal
    a_penambahan_saldo_debet = get_object_or_404(Tbl_Akun, id=616L)
    a_penambahan_saldo_kredit = get_object_or_404(Tbl_Akun, id=615L)
    jurnal = Jurnal.objects.create(
        diskripsi= 'Pengiriman KAS Gerai ke CIBIRU: %s ' % (biaya.ket_penambahan_saldo),
        tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_penambahan_saldo)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_debet,
        kredit = 0,debet = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
     
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_kredit,
        debet = 0,kredit = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)

def jurnal_biaya_penambahan_saldo_kas_cipacing_jatinangor(biaya, user):
    D = decimal.Decimal
    a_penambahan_saldo_debet = get_object_or_404(Tbl_Akun, id=616L)
    a_penambahan_saldo_kredit = get_object_or_404(Tbl_Akun, id=617L)
    jurnal = Jurnal.objects.create(
        diskripsi= 'Pengiriman KAS Gerai ke JATINANGOR: %s ' % (biaya.ket_penambahan_saldo),
        tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_penambahan_saldo)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_debet,
        kredit = 0,debet = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
     
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_kredit,
        debet = 0,kredit = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
    
def jurnal_biaya_penambahan_saldo_kas_cipacing_cimahi(biaya, user):
    D = decimal.Decimal
    a_penambahan_saldo_debet = get_object_or_404(Tbl_Akun, id=616L)
    a_penambahan_saldo_kredit = get_object_or_404(Tbl_Akun, id=618L)
    jurnal = Jurnal.objects.create(
        diskripsi= 'Pengiriman KAS Gerai ke CIMAHI: %s ' % (biaya.ket_penambahan_saldo),
        tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_penambahan_saldo)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_debet,
        kredit = 0,debet = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
     
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_kredit,
        debet = 0,kredit = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
    
def jurnal_biaya_penambahan_saldo_kas_cipacing_bubat(biaya, user):
    D = decimal.Decimal
    a_penambahan_saldo_debet = get_object_or_404(Tbl_Akun, id=616L)
    a_penambahan_saldo_kredit = get_object_or_404(Tbl_Akun, id=619L)
    jurnal = Jurnal.objects.create(
        diskripsi= 'Pengiriman KAS Gerai ke BUBAT: %s ' % (biaya.ket_penambahan_saldo),
        tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_penambahan_saldo)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_debet,
        kredit = 0,debet = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
     
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_kredit,
        debet = 0,kredit = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)

def jurnal_biaya_penambahan_saldo_kas_cipacing_maranatha(biaya, user):
    D = decimal.Decimal
    a_penambahan_saldo_debet = get_object_or_404(Tbl_Akun, id=616L)
    a_penambahan_saldo_kredit = get_object_or_404(Tbl_Akun, id=622L)
    jurnal = Jurnal.objects.create(
        diskripsi= 'Pengiriman KAS Gerai ke MARANATHA: %s ' % (biaya.ket_penambahan_saldo),
        tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_penambahan_saldo)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_debet,
        kredit = 0,debet = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
     
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_kredit,
        debet = 0,kredit = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
       
def jurnal_biaya_penambahan_saldo_kas_cipacing_cirebon(biaya, user):
    D = decimal.Decimal
    a_penambahan_saldo_debet = get_object_or_404(Tbl_Akun, id=616L)
    a_penambahan_saldo_kredit = get_object_or_404(Tbl_Akun, id=624L)
    jurnal = Jurnal.objects.create(
        diskripsi= 'Pengiriman KAS Gerai ke CIREBON: %s ' % (biaya.ket_penambahan_saldo),
        tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_penambahan_saldo)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_debet,
        kredit = 0,debet = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
     
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_kredit,
        debet = 0,kredit = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)

def jurnal_biaya_penambahan_saldo_kas_cipacing_ciumbeleuit(biaya, user):
    D = decimal.Decimal
    a_penambahan_saldo_debet = get_object_or_404(Tbl_Akun, id=616L)
    a_penambahan_saldo_kredit = get_object_or_404(Tbl_Akun, id=626L)
    jurnal = Jurnal.objects.create(
        diskripsi= 'Pengiriman KAS Gerai ke ciumbeleuit: %s ' % (biaya.ket_penambahan_saldo),
        tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_penambahan_saldo)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_debet,
        kredit = 0,debet = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
     
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_kredit,
        debet = 0,kredit = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
    
def jurnal_biaya_penambahan_saldo_kas_cipacing_uber(biaya, user):
    D = decimal.Decimal
    a_penambahan_saldo_debet = get_object_or_404(Tbl_Akun, id=616L)
    a_penambahan_saldo_kredit = get_object_or_404(Tbl_Akun, id=627L)
    jurnal = Jurnal.objects.create(
        diskripsi= 'Pengiriman KAS Gerai ke UJUNG BERUNG: %s ' % (biaya.ket_penambahan_saldo),
        tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_penambahan_saldo)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_debet,
        kredit = 0,debet = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
     
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_kredit,
        debet = 0,kredit = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
    
def jurnal_biaya_penambahan_saldo_kas_cipacing_ciwastra(biaya, user):
    D = decimal.Decimal
    a_penambahan_saldo_debet = get_object_or_404(Tbl_Akun, id=616L)
    a_penambahan_saldo_kredit = get_object_or_404(Tbl_Akun, id=628L)
    jurnal = Jurnal.objects.create(
        diskripsi= 'Pengiriman KAS Gerai ke CIWASTRA: %s ' % (biaya.ket_penambahan_saldo),
        tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_penambahan_saldo)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_debet,
        kredit = 0,debet = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_kredit,
        debet = 0,kredit = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
    
###Jurnal kas dari Jatinangor ke pusat 
def jurnal_biaya_penambahan_saldo_kas_jatinangor_pusat(biaya, user):
    D = decimal.Decimal
    a_penambahan_saldo_debet = get_object_or_404(Tbl_Akun, id=617L)
    a_penambahan_saldo_kredit = get_object_or_404(Tbl_Akun, id=4L)
    jurnal = Jurnal.objects.create(
        diskripsi= 'Pengembalian KasGerai NoRek: %s ' % (biaya.ket_penambahan_saldo),
        tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_penambahan_saldo)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_PUSAT"), id_coa = a_penambahan_saldo_debet,
        kredit = 0,debet = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
     
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_PUSAT"), id_coa = a_penambahan_saldo_kredit,
        debet = 0,kredit = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
    
def jurnal_biaya_penambahan_saldo_kas_jatinangor_jakarta(biaya, user):
    D = decimal.Decimal
    a_penambahan_saldo_debet = get_object_or_404(Tbl_Akun, id=617L)
    a_penambahan_saldo_kredit = get_object_or_404(Tbl_Akun, id=7L)
    jurnal = Jurnal.objects.create(
        diskripsi= 'Pengiriman KAS Gerai ke Jakarta %s ' % (biaya.ket_penambahan_saldo),
        tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_penambahan_saldo)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_debet,
        kredit = 0,debet = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
     
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_kredit,
        debet = 0,kredit = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
    
def jurnal_biaya_penambahan_saldo_kas_jatinangor_du(biaya, user):
    D = decimal.Decimal
    a_penambahan_saldo_debet = get_object_or_404(Tbl_Akun, id=617L)
    a_penambahan_saldo_kredit = get_object_or_404(Tbl_Akun, id=610L)
    jurnal = Jurnal.objects.create(
        diskripsi= 'Pengiriman KAS Gerai ke DU: %s ' % (biaya.ket_penambahan_saldo),
        tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_penambahan_saldo)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_debet,
        kredit = 0,debet = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
     
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_kredit,
        debet = 0,kredit = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
    
def jurnal_biaya_penambahan_saldo_kas_jatinangor_suci(biaya, user):
    D = decimal.Decimal
    a_penambahan_saldo_debet = get_object_or_404(Tbl_Akun, id=617L)
    a_penambahan_saldo_kredit = get_object_or_404(Tbl_Akun, id=609L)
    jurnal = Jurnal.objects.create(
        diskripsi= 'Pengiriman KAS Gerai ke Suci: %s ' % (biaya.ket_penambahan_saldo),
        tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_penambahan_saldo)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_debet,
        kredit = 0,debet = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
     
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_kredit,
        debet = 0,kredit = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
    
def jurnal_biaya_penambahan_saldo_kas_jatinangor_balubur(biaya, user):
    D = decimal.Decimal
    a_penambahan_saldo_debet = get_object_or_404(Tbl_Akun, id=617L)
    a_penambahan_saldo_kredit = get_object_or_404(Tbl_Akun, id=611L)
    jurnal = Jurnal.objects.create(
        diskripsi= 'Pengiriman KAS Gerai ke Balubur: %s ' % (biaya.ket_penambahan_saldo),
        tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_penambahan_saldo)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_debet,
        kredit = 0,debet = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
     
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_kredit,
        debet = 0,kredit = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)

def jurnal_biaya_penambahan_saldo_kas_jatinangor_hilir (biaya, user):
    D = decimal.Decimal
    a_penambahan_saldo_debet = get_object_or_404(Tbl_Akun, id=617L)
    a_penambahan_saldo_kredit = get_object_or_404(Tbl_Akun, id=613L)
    jurnal = Jurnal.objects.create(
        diskripsi= 'Pengiriman KAS Gerai ke Hilir: %s ' % (biaya.ket_penambahan_saldo),
        tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_penambahan_saldo)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_debet,
        kredit = 0,debet = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
     
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_kredit,
        debet = 0,kredit = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
    
def jurnal_biaya_penambahan_saldo_kas_jatinangor_kopo(biaya, user):
    D = decimal.Decimal
    a_penambahan_saldo_debet = get_object_or_404(Tbl_Akun, id=617L)
    a_penambahan_saldo_kredit = get_object_or_404(Tbl_Akun, id=614L)
    jurnal = Jurnal.objects.create(
        diskripsi= 'Pengiriman KAS Gerai ke Kopo: %s ' % (biaya.ket_penambahan_saldo),
        tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_penambahan_saldo)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_debet,
        kredit = 0,debet = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
     
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_kredit,
        debet = 0,kredit = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
    
def jurnal_biaya_penambahan_saldo_kas_jatinangor_cibiru(biaya, user):
    D = decimal.Decimal
    a_penambahan_saldo_debet = get_object_or_404(Tbl_Akun, id=617L)
    a_penambahan_saldo_kredit = get_object_or_404(Tbl_Akun, id=615L)
    jurnal = Jurnal.objects.create(
        diskripsi= 'Pengiriman KAS Gerai ke CIBIRU: %s ' % (biaya.ket_penambahan_saldo),
        tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_penambahan_saldo)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_debet,
        kredit = 0,debet = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
     
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_kredit,
        debet = 0,kredit = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)

def jurnal_biaya_penambahan_saldo_kas_jatinangor_cipacing(biaya, user):
    D = decimal.Decimal
    a_penambahan_saldo_debet = get_object_or_404(Tbl_Akun, id=617L)
    a_penambahan_saldo_kredit = get_object_or_404(Tbl_Akun, id=616L)
    jurnal = Jurnal.objects.create(
        diskripsi= 'Pengiriman KAS Gerai ke JATINANGOR: %s ' % (biaya.ket_penambahan_saldo),
        tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_penambahan_saldo)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_debet,
        kredit = 0,debet = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
     
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_kredit,
        debet = 0,kredit = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
    
def jurnal_biaya_penambahan_saldo_kas_jatinangor_cimahi(biaya, user):
    D = decimal.Decimal
    a_penambahan_saldo_debet = get_object_or_404(Tbl_Akun, id=617L)
    a_penambahan_saldo_kredit = get_object_or_404(Tbl_Akun, id=618L)
    jurnal = Jurnal.objects.create(
        diskripsi= 'Pengiriman KAS Gerai ke CIMAHI: %s ' % (biaya.ket_penambahan_saldo),
        tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_penambahan_saldo)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_debet,
        kredit = 0,debet = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
     
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_kredit,
        debet = 0,kredit = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
    
def jurnal_biaya_penambahan_saldo_kas_jatinangor_bubat(biaya, user):
    D = decimal.Decimal
    a_penambahan_saldo_debet = get_object_or_404(Tbl_Akun, id=617L)
    a_penambahan_saldo_kredit = get_object_or_404(Tbl_Akun, id=619L)
    jurnal = Jurnal.objects.create(
        diskripsi= 'Pengiriman KAS Gerai ke BUBAT: %s ' % (biaya.ket_penambahan_saldo),
        tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_penambahan_saldo)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_debet,
        kredit = 0,debet = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
     
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_kredit,
        debet = 0,kredit = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)

def jurnal_biaya_penambahan_saldo_kas_jatinangor_maranatha(biaya, user):
    D = decimal.Decimal
    a_penambahan_saldo_debet = get_object_or_404(Tbl_Akun, id=617L)
    a_penambahan_saldo_kredit = get_object_or_404(Tbl_Akun, id=622L)
    jurnal = Jurnal.objects.create(
        diskripsi= 'Pengiriman KAS Gerai ke MARANATHA: %s ' % (biaya.ket_penambahan_saldo),
        tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_penambahan_saldo)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_debet,
        kredit = 0,debet = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
     
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_kredit,
        debet = 0,kredit = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
       
def jurnal_biaya_penambahan_saldo_kas_jatinangor_cirebon(biaya, user):
    D = decimal.Decimal
    a_penambahan_saldo_debet = get_object_or_404(Tbl_Akun, id=617L)
    a_penambahan_saldo_kredit = get_object_or_404(Tbl_Akun, id=624L)
    jurnal = Jurnal.objects.create(
        diskripsi= 'Pengiriman KAS Gerai ke CIREBON: %s ' % (biaya.ket_penambahan_saldo),
        tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_penambahan_saldo)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_debet,
        kredit = 0,debet = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
     
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_kredit,
        debet = 0,kredit = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)

def jurnal_biaya_penambahan_saldo_kas_jatinangor_ciumbeleuit(biaya, user):
    D = decimal.Decimal
    a_penambahan_saldo_debet = get_object_or_404(Tbl_Akun, id=617L)
    a_penambahan_saldo_kredit = get_object_or_404(Tbl_Akun, id=626L)
    jurnal = Jurnal.objects.create(
        diskripsi= 'Pengiriman KAS Gerai ke ciumbeleuit: %s ' % (biaya.ket_penambahan_saldo),
        tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_penambahan_saldo)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_debet,
        kredit = 0,debet = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
     
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_kredit,
        debet = 0,kredit = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
    
def jurnal_biaya_penambahan_saldo_kas_jatinangor_uber(biaya, user):
    D = decimal.Decimal
    a_penambahan_saldo_debet = get_object_or_404(Tbl_Akun, id=617L)
    a_penambahan_saldo_kredit = get_object_or_404(Tbl_Akun, id=627L)
    jurnal = Jurnal.objects.create(
        diskripsi= 'Pengiriman KAS Gerai ke UJUNG BERUNG: %s ' % (biaya.ket_penambahan_saldo),
        tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_penambahan_saldo)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_debet,
        kredit = 0,debet = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
     
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_kredit,
        debet = 0,kredit = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
    
def jurnal_biaya_penambahan_saldo_kas_jatinangor_ciwastra(biaya, user):
    D = decimal.Decimal
    a_penambahan_saldo_debet = get_object_or_404(Tbl_Akun, id=617L)
    a_penambahan_saldo_kredit = get_object_or_404(Tbl_Akun, id=628L)
    jurnal = Jurnal.objects.create(
        diskripsi= 'Pengiriman KAS Gerai ke CIWASTRA: %s ' % (biaya.ket_penambahan_saldo),
        tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_penambahan_saldo)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_debet,
        kredit = 0,debet = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_kredit,
        debet = 0,kredit = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
    
###Jurnal kas dari Cimahi ke pusat 
def jurnal_biaya_penambahan_saldo_kas_cimahi_pusat(biaya, user):
    D = decimal.Decimal
    a_penambahan_saldo_debet = get_object_or_404(Tbl_Akun, id=618L)
    a_penambahan_saldo_kredit = get_object_or_404(Tbl_Akun, id=4L)
    jurnal = Jurnal.objects.create(
        diskripsi= 'Pengembalian KasGerai NoRek: %s ' % (biaya.ket_penambahan_saldo),
        tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_penambahan_saldo)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_PUSAT"), id_coa = a_penambahan_saldo_debet,
        kredit = 0,debet = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
     
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_PUSAT"), id_coa = a_penambahan_saldo_kredit,
        debet = 0,kredit = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
    
def jurnal_biaya_penambahan_saldo_kas_cimahi_jakarta(biaya, user):
    D = decimal.Decimal
    a_penambahan_saldo_debet = get_object_or_404(Tbl_Akun, id=618L)
    a_penambahan_saldo_kredit = get_object_or_404(Tbl_Akun, id=7L)
    jurnal = Jurnal.objects.create(
        diskripsi= 'Pengiriman KAS Gerai ke Jakarta %s ' % (biaya.ket_penambahan_saldo),
        tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_penambahan_saldo)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_debet,
        kredit = 0,debet = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
     
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_kredit,
        debet = 0,kredit = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
    
def jurnal_biaya_penambahan_saldo_kas_cimahi_du(biaya, user):
    D = decimal.Decimal
    a_penambahan_saldo_debet = get_object_or_404(Tbl_Akun, id=618L)
    a_penambahan_saldo_kredit = get_object_or_404(Tbl_Akun, id=610L)
    jurnal = Jurnal.objects.create(
        diskripsi= 'Pengiriman KAS Gerai ke DU: %s ' % (biaya.ket_penambahan_saldo),
        tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_penambahan_saldo)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_debet,
        kredit = 0,debet = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
     
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_kredit,
        debet = 0,kredit = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
    
def jurnal_biaya_penambahan_saldo_kas_cimahi_suci(biaya, user):
    D = decimal.Decimal
    a_penambahan_saldo_debet = get_object_or_404(Tbl_Akun, id=618L)
    a_penambahan_saldo_kredit = get_object_or_404(Tbl_Akun, id=609L)
    jurnal = Jurnal.objects.create(
        diskripsi= 'Pengiriman KAS Gerai ke Suci: %s ' % (biaya.ket_penambahan_saldo),
        tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_penambahan_saldo)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_debet,
        kredit = 0,debet = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
     
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_kredit,
        debet = 0,kredit = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
    
def jurnal_biaya_penambahan_saldo_kas_cimahi_balubur(biaya, user):
    D = decimal.Decimal
    a_penambahan_saldo_debet = get_object_or_404(Tbl_Akun, id=618L)
    a_penambahan_saldo_kredit = get_object_or_404(Tbl_Akun, id=611L)
    jurnal = Jurnal.objects.create(
        diskripsi= 'Pengiriman KAS Gerai ke Balubur: %s ' % (biaya.ket_penambahan_saldo),
        tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_penambahan_saldo)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_debet,
        kredit = 0,debet = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
     
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_kredit,
        debet = 0,kredit = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)

def jurnal_biaya_penambahan_saldo_kas_cimahi_hilir (biaya, user):
    D = decimal.Decimal
    a_penambahan_saldo_debet = get_object_or_404(Tbl_Akun, id=618L)
    a_penambahan_saldo_kredit = get_object_or_404(Tbl_Akun, id=613L)
    jurnal = Jurnal.objects.create(
        diskripsi= 'Pengiriman KAS Gerai ke Hilir: %s ' % (biaya.ket_penambahan_saldo),
        tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_penambahan_saldo)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_debet,
        kredit = 0,debet = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
     
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_kredit,
        debet = 0,kredit = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
    
def jurnal_biaya_penambahan_saldo_kas_cimahi_kopo(biaya, user):
    D = decimal.Decimal
    a_penambahan_saldo_debet = get_object_or_404(Tbl_Akun, id=618L)
    a_penambahan_saldo_kredit = get_object_or_404(Tbl_Akun, id=614L)
    jurnal = Jurnal.objects.create(
        diskripsi= 'Pengiriman KAS Gerai ke Kopo: %s ' % (biaya.ket_penambahan_saldo),
        tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_penambahan_saldo)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_debet,
        kredit = 0,debet = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
     
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_kredit,
        debet = 0,kredit = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
    
def jurnal_biaya_penambahan_saldo_kas_cimahi_cibiru(biaya, user):
    D = decimal.Decimal
    a_penambahan_saldo_debet = get_object_or_404(Tbl_Akun, id=618L)
    a_penambahan_saldo_kredit = get_object_or_404(Tbl_Akun, id=615L)
    jurnal = Jurnal.objects.create(
        diskripsi= 'Pengiriman KAS Gerai ke CIBIRU: %s ' % (biaya.ket_penambahan_saldo),
        tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_penambahan_saldo)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_debet,
        kredit = 0,debet = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
     
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_kredit,
        debet = 0,kredit = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)

def jurnal_biaya_penambahan_saldo_kas_cimahi_cipacing(biaya, user):
    D = decimal.Decimal
    a_penambahan_saldo_debet = get_object_or_404(Tbl_Akun, id=618L)
    a_penambahan_saldo_kredit = get_object_or_404(Tbl_Akun, id=616L)
    jurnal = Jurnal.objects.create(
        diskripsi= 'Pengiriman KAS Gerai ke JATINANGOR: %s ' % (biaya.ket_penambahan_saldo),
        tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_penambahan_saldo)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_debet,
        kredit = 0,debet = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
     
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_kredit,
        debet = 0,kredit = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
    
def jurnal_biaya_penambahan_saldo_kas_cimahi_jatinangor(biaya, user):
    D = decimal.Decimal
    a_penambahan_saldo_debet = get_object_or_404(Tbl_Akun, id=618L)
    a_penambahan_saldo_kredit = get_object_or_404(Tbl_Akun, id=617L)
    jurnal = Jurnal.objects.create(
        diskripsi= 'Pengiriman KAS Gerai ke Jatinangor : %s ' % (biaya.ket_penambahan_saldo),
        tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_penambahan_saldo)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_debet,
        kredit = 0,debet = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
     
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_kredit,
        debet = 0,kredit = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
    
def jurnal_biaya_penambahan_saldo_kas_cimahi_bubat(biaya, user):
    D = decimal.Decimal
    a_penambahan_saldo_debet = get_object_or_404(Tbl_Akun, id=618L)
    a_penambahan_saldo_kredit = get_object_or_404(Tbl_Akun, id=619L)
    jurnal = Jurnal.objects.create(
        diskripsi= 'Pengiriman KAS Gerai ke BUBAT: %s ' % (biaya.ket_penambahan_saldo),
        tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_penambahan_saldo)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_debet,
        kredit = 0,debet = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
     
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_kredit,
        debet = 0,kredit = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)

def jurnal_biaya_penambahan_saldo_kas_cimahi_maranatha(biaya, user):
    D = decimal.Decimal
    a_penambahan_saldo_debet = get_object_or_404(Tbl_Akun, id=618L)
    a_penambahan_saldo_kredit = get_object_or_404(Tbl_Akun, id=622L)
    jurnal = Jurnal.objects.create(
        diskripsi= 'Pengiriman KAS Gerai ke MARANATHA: %s ' % (biaya.ket_penambahan_saldo),
        tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_penambahan_saldo)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_debet,
        kredit = 0,debet = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
     
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_kredit,
        debet = 0,kredit = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
       
def jurnal_biaya_penambahan_saldo_kas_cimahi_cirebon(biaya, user):
    D = decimal.Decimal
    a_penambahan_saldo_debet = get_object_or_404(Tbl_Akun, id=618L)
    a_penambahan_saldo_kredit = get_object_or_404(Tbl_Akun, id=624L)
    jurnal = Jurnal.objects.create(
        diskripsi= 'Pengiriman KAS Gerai ke CIREBON: %s ' % (biaya.ket_penambahan_saldo),
        tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_penambahan_saldo)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_debet,
        kredit = 0,debet = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
     
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_kredit,
        debet = 0,kredit = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)

def jurnal_biaya_penambahan_saldo_kas_cimahi_ciumbeleuit(biaya, user):
    D = decimal.Decimal
    a_penambahan_saldo_debet = get_object_or_404(Tbl_Akun, id=618L)
    a_penambahan_saldo_kredit = get_object_or_404(Tbl_Akun, id=626L)
    jurnal = Jurnal.objects.create(
        diskripsi= 'Pengiriman KAS Gerai ke ciumbeleuit: %s ' % (biaya.ket_penambahan_saldo),
        tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_penambahan_saldo)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_debet,
        kredit = 0,debet = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
     
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_kredit,
        debet = 0,kredit = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
    
def jurnal_biaya_penambahan_saldo_kas_cimahi_uber(biaya, user):
    D = decimal.Decimal
    a_penambahan_saldo_debet = get_object_or_404(Tbl_Akun, id=618L)
    a_penambahan_saldo_kredit = get_object_or_404(Tbl_Akun, id=627L)
    jurnal = Jurnal.objects.create(
        diskripsi= 'Pengiriman KAS Gerai ke UJUNG BERUNG: %s ' % (biaya.ket_penambahan_saldo),
        tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_penambahan_saldo)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_debet,
        kredit = 0,debet = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
     
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_kredit,
        debet = 0,kredit = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
    
def jurnal_biaya_penambahan_saldo_kas_cimahi_ciwastra(biaya, user):
    D = decimal.Decimal
    a_penambahan_saldo_debet = get_object_or_404(Tbl_Akun, id=618L)
    a_penambahan_saldo_kredit = get_object_or_404(Tbl_Akun, id=628L)
    jurnal = Jurnal.objects.create(
        diskripsi= 'Pengiriman KAS Gerai ke CIWASTRA: %s ' % (biaya.ket_penambahan_saldo),
        tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_penambahan_saldo)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_debet,
        kredit = 0,debet = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_kredit,
        debet = 0,kredit = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)

###Jurnal kas dari Buah Batu ke pusat 
def jurnal_biaya_penambahan_saldo_kas_bubat_pusat(biaya, user):
    D = decimal.Decimal
    a_penambahan_saldo_debet = get_object_or_404(Tbl_Akun, id=619L)
    a_penambahan_saldo_kredit = get_object_or_404(Tbl_Akun, id=4L)
    jurnal = Jurnal.objects.create(
        diskripsi= 'Pengembalian KasGerai NoRek: %s ' % (biaya.ket_penambahan_saldo),
        tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_penambahan_saldo)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_PUSAT"), id_coa = a_penambahan_saldo_debet,
        kredit = 0,debet = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
     
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_PUSAT"), id_coa = a_penambahan_saldo_kredit,
        debet = 0,kredit = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
    
def jurnal_biaya_penambahan_saldo_kas_bubat_jakarta(biaya, user):
    D = decimal.Decimal
    a_penambahan_saldo_debet = get_object_or_404(Tbl_Akun, id=619L)
    a_penambahan_saldo_kredit = get_object_or_404(Tbl_Akun, id=7L)
    jurnal = Jurnal.objects.create(
        diskripsi= 'Pengiriman KAS Gerai ke Jakarta %s ' % (biaya.ket_penambahan_saldo),
        tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_penambahan_saldo)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_debet,
        kredit = 0,debet = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
     
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_kredit,
        debet = 0,kredit = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
    
def jurnal_biaya_penambahan_saldo_kas_bubat_du(biaya, user):
    D = decimal.Decimal
    a_penambahan_saldo_debet = get_object_or_404(Tbl_Akun, id=619L)
    a_penambahan_saldo_kredit = get_object_or_404(Tbl_Akun, id=610L)
    jurnal = Jurnal.objects.create(
        diskripsi= 'Pengiriman KAS Gerai ke DU: %s ' % (biaya.ket_penambahan_saldo),
        tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_penambahan_saldo)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_debet,
        kredit = 0,debet = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
     
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_kredit,
        debet = 0,kredit = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
    
def jurnal_biaya_penambahan_saldo_kas_bubat_suci(biaya, user):
    D = decimal.Decimal
    a_penambahan_saldo_debet = get_object_or_404(Tbl_Akun, id=619L)
    a_penambahan_saldo_kredit = get_object_or_404(Tbl_Akun, id=609L)
    jurnal = Jurnal.objects.create(
        diskripsi= 'Pengiriman KAS Gerai ke Suci: %s ' % (biaya.ket_penambahan_saldo),
        tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_penambahan_saldo)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_debet,
        kredit = 0,debet = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
     
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_kredit,
        debet = 0,kredit = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
    
def jurnal_biaya_penambahan_saldo_kas_bubat_balubur(biaya, user):
    D = decimal.Decimal
    a_penambahan_saldo_debet = get_object_or_404(Tbl_Akun, id=619L)
    a_penambahan_saldo_kredit = get_object_or_404(Tbl_Akun, id=611L)
    jurnal = Jurnal.objects.create(
        diskripsi= 'Pengiriman KAS Gerai ke Balubur: %s ' % (biaya.ket_penambahan_saldo),
        tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_penambahan_saldo)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_debet,
        kredit = 0,debet = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
     
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_kredit,
        debet = 0,kredit = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)

def jurnal_biaya_penambahan_saldo_kas_bubat_hilir (biaya, user):
    D = decimal.Decimal
    a_penambahan_saldo_debet = get_object_or_404(Tbl_Akun, id=619L)
    a_penambahan_saldo_kredit = get_object_or_404(Tbl_Akun, id=613L)
    jurnal = Jurnal.objects.create(
        diskripsi= 'Pengiriman KAS Gerai ke Hilir: %s ' % (biaya.ket_penambahan_saldo),
        tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_penambahan_saldo)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_debet,
        kredit = 0,debet = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
     
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_kredit,
        debet = 0,kredit = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
    
def jurnal_biaya_penambahan_saldo_kas_bubat_kopo(biaya, user):
    D = decimal.Decimal
    a_penambahan_saldo_debet = get_object_or_404(Tbl_Akun, id=619L)
    a_penambahan_saldo_kredit = get_object_or_404(Tbl_Akun, id=614L)
    jurnal = Jurnal.objects.create(
        diskripsi= 'Pengiriman KAS Gerai ke Kopo: %s ' % (biaya.ket_penambahan_saldo),
        tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_penambahan_saldo)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_debet,
        kredit = 0,debet = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
     
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_kredit,
        debet = 0,kredit = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
    
def jurnal_biaya_penambahan_saldo_kas_bubat_cibiru(biaya, user):
    D = decimal.Decimal
    a_penambahan_saldo_debet = get_object_or_404(Tbl_Akun, id=619L)
    a_penambahan_saldo_kredit = get_object_or_404(Tbl_Akun, id=615L)
    jurnal = Jurnal.objects.create(
        diskripsi= 'Pengiriman KAS Gerai ke CIBIRU: %s ' % (biaya.ket_penambahan_saldo),
        tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_penambahan_saldo)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_debet,
        kredit = 0,debet = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
     
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_kredit,
        debet = 0,kredit = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)

def jurnal_biaya_penambahan_saldo_kas_bubat_cipacing(biaya, user):
    D = decimal.Decimal
    a_penambahan_saldo_debet = get_object_or_404(Tbl_Akun, id=619L)
    a_penambahan_saldo_kredit = get_object_or_404(Tbl_Akun, id=616L)
    jurnal = Jurnal.objects.create(
        diskripsi= 'Pengiriman KAS Gerai ke JATINANGOR: %s ' % (biaya.ket_penambahan_saldo),
        tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_penambahan_saldo)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_debet,
        kredit = 0,debet = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
     
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_kredit,
        debet = 0,kredit = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
    
def jurnal_biaya_penambahan_saldo_kas_bubat_jatinangor(biaya, user):
    D = decimal.Decimal
    a_penambahan_saldo_debet = get_object_or_404(Tbl_Akun, id=619L)
    a_penambahan_saldo_kredit = get_object_or_404(Tbl_Akun, id=617L)
    jurnal = Jurnal.objects.create(
        diskripsi= 'Pengiriman KAS Gerai ke Jatinangor : %s ' % (biaya.ket_penambahan_saldo),
        tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_penambahan_saldo)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_debet,
        kredit = 0,debet = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
     
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_kredit,
        debet = 0,kredit = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
    
def jurnal_biaya_penambahan_saldo_kas_bubat_cimahi(biaya, user):
    D = decimal.Decimal
    a_penambahan_saldo_debet = get_object_or_404(Tbl_Akun, id=619L)
    a_penambahan_saldo_kredit = get_object_or_404(Tbl_Akun, id=618L)
    jurnal = Jurnal.objects.create(
        diskripsi= 'Pengiriman KAS Gerai ke CIMAHI: %s ' % (biaya.ket_penambahan_saldo),
        tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_penambahan_saldo)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_debet,
        kredit = 0,debet = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
     
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_kredit,
        debet = 0,kredit = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)

def jurnal_biaya_penambahan_saldo_kas_bubat_maranatha(biaya, user):
    D = decimal.Decimal
    a_penambahan_saldo_debet = get_object_or_404(Tbl_Akun, id=619L)
    a_penambahan_saldo_kredit = get_object_or_404(Tbl_Akun, id=622L)
    jurnal = Jurnal.objects.create(
        diskripsi= 'Pengiriman KAS Gerai ke MARANATHA: %s ' % (biaya.ket_penambahan_saldo),
        tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_penambahan_saldo)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_debet,
        kredit = 0,debet = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
     
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_kredit,
        debet = 0,kredit = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
       
def jurnal_biaya_penambahan_saldo_kas_bubat_cirebon(biaya, user):
    D = decimal.Decimal
    a_penambahan_saldo_debet = get_object_or_404(Tbl_Akun, id=619L)
    a_penambahan_saldo_kredit = get_object_or_404(Tbl_Akun, id=624L)
    jurnal = Jurnal.objects.create(
        diskripsi= 'Pengiriman KAS Gerai ke CIREBON: %s ' % (biaya.ket_penambahan_saldo),
        tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_penambahan_saldo)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_debet,
        kredit = 0,debet = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
     
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_kredit,
        debet = 0,kredit = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)

def jurnal_biaya_penambahan_saldo_kas_bubat_ciumbeleuit(biaya, user):
    D = decimal.Decimal
    a_penambahan_saldo_debet = get_object_or_404(Tbl_Akun, id=619L)
    a_penambahan_saldo_kredit = get_object_or_404(Tbl_Akun, id=626L)
    jurnal = Jurnal.objects.create(
        diskripsi= 'Pengiriman KAS Gerai ke ciumbeleuit: %s ' % (biaya.ket_penambahan_saldo),
        tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_penambahan_saldo)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_debet,
        kredit = 0,debet = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
     
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_kredit,
        debet = 0,kredit = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
    
def jurnal_biaya_penambahan_saldo_kas_bubat_uber(biaya, user):
    D = decimal.Decimal
    a_penambahan_saldo_debet = get_object_or_404(Tbl_Akun, id=619L)
    a_penambahan_saldo_kredit = get_object_or_404(Tbl_Akun, id=627L)
    jurnal = Jurnal.objects.create(
        diskripsi= 'Pengiriman KAS Gerai ke UJUNG BERUNG: %s ' % (biaya.ket_penambahan_saldo),
        tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_penambahan_saldo)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_debet,
        kredit = 0,debet = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
     
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_kredit,
        debet = 0,kredit = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
    
def jurnal_biaya_penambahan_saldo_kas_bubat_ciwastra(biaya, user):
    D = decimal.Decimal
    a_penambahan_saldo_debet = get_object_or_404(Tbl_Akun, id=619L)
    a_penambahan_saldo_kredit = get_object_or_404(Tbl_Akun, id=628L)
    jurnal = Jurnal.objects.create(
        diskripsi= 'Pengiriman KAS Gerai ke CIWASTRA: %s ' % (biaya.ket_penambahan_saldo),
        tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_penambahan_saldo)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_debet,
        kredit = 0,debet = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_kredit,
        debet = 0,kredit = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
    
###Jurnal kas dari Maranatha ke pusat 
def jurnal_biaya_penambahan_saldo_kas_maranatha_pusat(biaya, user):
    D = decimal.Decimal
    a_penambahan_saldo_debet = get_object_or_404(Tbl_Akun, id=622L)
    a_penambahan_saldo_kredit = get_object_or_404(Tbl_Akun, id=4L)
    jurnal = Jurnal.objects.create(
        diskripsi= 'Pengembalian KasGerai NoRek: %s ' % (biaya.ket_penambahan_saldo),
        tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_penambahan_saldo)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_PUSAT"), id_coa = a_penambahan_saldo_debet,
        kredit = 0,debet = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
     
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_PUSAT"), id_coa = a_penambahan_saldo_kredit,
        debet = 0,kredit = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
    
def jurnal_biaya_penambahan_saldo_kas_maranatha_jakarta(biaya, user):
    D = decimal.Decimal
    a_penambahan_saldo_debet = get_object_or_404(Tbl_Akun, id=622L)
    a_penambahan_saldo_kredit = get_object_or_404(Tbl_Akun, id=7L)
    jurnal = Jurnal.objects.create(
        diskripsi= 'Pengiriman KAS Gerai ke Jakarta %s ' % (biaya.ket_penambahan_saldo),
        tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_penambahan_saldo)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_debet,
        kredit = 0,debet = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
     
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_kredit,
        debet = 0,kredit = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
    
def jurnal_biaya_penambahan_saldo_kas_maranatha_du(biaya, user):
    D = decimal.Decimal
    a_penambahan_saldo_debet = get_object_or_404(Tbl_Akun, id=622L)
    a_penambahan_saldo_kredit = get_object_or_404(Tbl_Akun, id=610L)
    jurnal = Jurnal.objects.create(
        diskripsi= 'Pengiriman KAS Gerai ke DU: %s ' % (biaya.ket_penambahan_saldo),
        tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_penambahan_saldo)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_debet,
        kredit = 0,debet = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
     
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_kredit,
        debet = 0,kredit = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
    
def jurnal_biaya_penambahan_saldo_kas_maranatha_suci(biaya, user):
    D = decimal.Decimal
    a_penambahan_saldo_debet = get_object_or_404(Tbl_Akun, id=622L)
    a_penambahan_saldo_kredit = get_object_or_404(Tbl_Akun, id=609L)
    jurnal = Jurnal.objects.create(
        diskripsi= 'Pengiriman KAS Gerai ke Suci: %s ' % (biaya.ket_penambahan_saldo),
        tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_penambahan_saldo)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_debet,
        kredit = 0,debet = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
     
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_kredit,
        debet = 0,kredit = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
    
def jurnal_biaya_penambahan_saldo_kas_maranatha_balubur(biaya, user):
    D = decimal.Decimal
    a_penambahan_saldo_debet = get_object_or_404(Tbl_Akun, id=622L)
    a_penambahan_saldo_kredit = get_object_or_404(Tbl_Akun, id=611L)
    jurnal = Jurnal.objects.create(
        diskripsi= 'Pengiriman KAS Gerai ke Balubur: %s ' % (biaya.ket_penambahan_saldo),
        tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_penambahan_saldo)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_debet,
        kredit = 0,debet = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
     
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_kredit,
        debet = 0,kredit = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)

def jurnal_biaya_penambahan_saldo_kas_maranatha_hilir (biaya, user):
    D = decimal.Decimal
    a_penambahan_saldo_debet = get_object_or_404(Tbl_Akun, id=622L)
    a_penambahan_saldo_kredit = get_object_or_404(Tbl_Akun, id=613L)
    jurnal = Jurnal.objects.create(
        diskripsi= 'Pengiriman KAS Gerai ke Hilir: %s ' % (biaya.ket_penambahan_saldo),
        tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_penambahan_saldo)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_debet,
        kredit = 0,debet = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
     
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_kredit,
        debet = 0,kredit = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
    
def jurnal_biaya_penambahan_saldo_kas_maranatha_kopo(biaya, user):
    D = decimal.Decimal
    a_penambahan_saldo_debet = get_object_or_404(Tbl_Akun, id=622L)
    a_penambahan_saldo_kredit = get_object_or_404(Tbl_Akun, id=614L)
    jurnal = Jurnal.objects.create(
        diskripsi= 'Pengiriman KAS Gerai ke Kopo: %s ' % (biaya.ket_penambahan_saldo),
        tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_penambahan_saldo)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_debet,
        kredit = 0,debet = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
     
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_kredit,
        debet = 0,kredit = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
    
def jurnal_biaya_penambahan_saldo_kas_maranatha_cibiru(biaya, user):
    D = decimal.Decimal
    a_penambahan_saldo_debet = get_object_or_404(Tbl_Akun, id=622L)
    a_penambahan_saldo_kredit = get_object_or_404(Tbl_Akun, id=615L)
    jurnal = Jurnal.objects.create(
        diskripsi= 'Pengiriman KAS Gerai ke CIBIRU: %s ' % (biaya.ket_penambahan_saldo),
        tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_penambahan_saldo)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_debet,
        kredit = 0,debet = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
     
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_kredit,
        debet = 0,kredit = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)

def jurnal_biaya_penambahan_saldo_kas_maranatha_cipacing(biaya, user):
    D = decimal.Decimal
    a_penambahan_saldo_debet = get_object_or_404(Tbl_Akun, id=622L)
    a_penambahan_saldo_kredit = get_object_or_404(Tbl_Akun, id=616L)
    jurnal = Jurnal.objects.create(
        diskripsi= 'Pengiriman KAS Gerai ke JATINANGOR: %s ' % (biaya.ket_penambahan_saldo),
        tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_penambahan_saldo)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_debet,
        kredit = 0,debet = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
     
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_kredit,
        debet = 0,kredit = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
    
def jurnal_biaya_penambahan_saldo_kas_maranatha_jatinangor(biaya, user):
    D = decimal.Decimal
    a_penambahan_saldo_debet = get_object_or_404(Tbl_Akun, id=622L)
    a_penambahan_saldo_kredit = get_object_or_404(Tbl_Akun, id=617L)
    jurnal = Jurnal.objects.create(
        diskripsi= 'Pengiriman KAS Gerai ke Jatinangor : %s ' % (biaya.ket_penambahan_saldo),
        tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_penambahan_saldo)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_debet,
        kredit = 0,debet = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
     
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_kredit,
        debet = 0,kredit = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
    
def jurnal_biaya_penambahan_saldo_kas_maranatha_cimahi(biaya, user):
    D = decimal.Decimal
    a_penambahan_saldo_debet = get_object_or_404(Tbl_Akun, id=622L)
    a_penambahan_saldo_kredit = get_object_or_404(Tbl_Akun, id=618L)
    jurnal = Jurnal.objects.create(
        diskripsi= 'Pengiriman KAS Gerai ke CIMAHI: %s ' % (biaya.ket_penambahan_saldo),
        tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_penambahan_saldo)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_debet,
        kredit = 0,debet = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
     
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_kredit,
        debet = 0,kredit = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)

def jurnal_biaya_penambahan_saldo_kas_maranatha_bubat(biaya, user):
    D = decimal.Decimal
    a_penambahan_saldo_debet = get_object_or_404(Tbl_Akun, id=622L)
    a_penambahan_saldo_kredit = get_object_or_404(Tbl_Akun, id=619L)
    jurnal = Jurnal.objects.create(
        diskripsi= 'Pengiriman KAS Gerai ke BUAH BATU: %s ' % (biaya.ket_penambahan_saldo),
        tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_penambahan_saldo)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_debet,
        kredit = 0,debet = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
     
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_kredit,
        debet = 0,kredit = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
       
def jurnal_biaya_penambahan_saldo_kas_maranatha_cirebon(biaya, user):
    D = decimal.Decimal
    a_penambahan_saldo_debet = get_object_or_404(Tbl_Akun, id=622L)
    a_penambahan_saldo_kredit = get_object_or_404(Tbl_Akun, id=624L)
    jurnal = Jurnal.objects.create(
        diskripsi= 'Pengiriman KAS Gerai ke CIREBON: %s ' % (biaya.ket_penambahan_saldo),
        tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_penambahan_saldo)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_debet,
        kredit = 0,debet = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
     
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_kredit,
        debet = 0,kredit = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)

def jurnal_biaya_penambahan_saldo_kas_maranatha_ciumbeleuit(biaya, user):
    D = decimal.Decimal
    a_penambahan_saldo_debet = get_object_or_404(Tbl_Akun, id=622L)
    a_penambahan_saldo_kredit = get_object_or_404(Tbl_Akun, id=626L)
    jurnal = Jurnal.objects.create(
        diskripsi= 'Pengiriman KAS Gerai ke ciumbeleuit: %s ' % (biaya.ket_penambahan_saldo),
        tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_penambahan_saldo)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_debet,
        kredit = 0,debet = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
     
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_kredit,
        debet = 0,kredit = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
    
def jurnal_biaya_penambahan_saldo_kas_maranatha_uber(biaya, user):
    D = decimal.Decimal
    a_penambahan_saldo_debet = get_object_or_404(Tbl_Akun, id=622L)
    a_penambahan_saldo_kredit = get_object_or_404(Tbl_Akun, id=627L)
    jurnal = Jurnal.objects.create(
        diskripsi= 'Pengiriman KAS Gerai ke UJUNG BERUNG: %s ' % (biaya.ket_penambahan_saldo),
        tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_penambahan_saldo)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_debet,
        kredit = 0,debet = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
     
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_kredit,
        debet = 0,kredit = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
    
def jurnal_biaya_penambahan_saldo_kas_maranatha_ciwastra(biaya, user):
    D = decimal.Decimal
    a_penambahan_saldo_debet = get_object_or_404(Tbl_Akun, id=622L)
    a_penambahan_saldo_kredit = get_object_or_404(Tbl_Akun, id=628L)
    jurnal = Jurnal.objects.create(
        diskripsi= 'Pengiriman KAS Gerai ke CIWASTRA: %s ' % (biaya.ket_penambahan_saldo),
        tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_penambahan_saldo)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_debet,
        kredit = 0,debet = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_kredit,
        debet = 0,kredit = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
    
###Jurnal kas dari Cirebon ke pusat 
def jurnal_biaya_penambahan_saldo_kas_cirebon_pusat(biaya, user):
    D = decimal.Decimal
    a_penambahan_saldo_debet = get_object_or_404(Tbl_Akun, id=624L)
    a_penambahan_saldo_kredit = get_object_or_404(Tbl_Akun, id=4L)
    jurnal = Jurnal.objects.create(
        diskripsi= 'Pengembalian KasGerai NoRek: %s ' % (biaya.ket_penambahan_saldo),
        tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_penambahan_saldo)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_PUSAT"), id_coa = a_penambahan_saldo_debet,
        kredit = 0,debet = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
     
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_PUSAT"), id_coa = a_penambahan_saldo_kredit,
        debet = 0,kredit = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
    
def jurnal_biaya_penambahan_saldo_kas_cirebon_jakarta(biaya, user):
    D = decimal.Decimal
    a_penambahan_saldo_debet = get_object_or_404(Tbl_Akun, id=624L)
    a_penambahan_saldo_kredit = get_object_or_404(Tbl_Akun, id=7L)
    jurnal = Jurnal.objects.create(
        diskripsi= 'Pengiriman KAS Gerai ke Jakarta %s ' % (biaya.ket_penambahan_saldo),
        tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_penambahan_saldo)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_debet,
        kredit = 0,debet = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
     
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_kredit,
        debet = 0,kredit = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
    
def jurnal_biaya_penambahan_saldo_kas_cirebon_du(biaya, user):
    D = decimal.Decimal
    a_penambahan_saldo_debet = get_object_or_404(Tbl_Akun, id=624L)
    a_penambahan_saldo_kredit = get_object_or_404(Tbl_Akun, id=610L)
    jurnal = Jurnal.objects.create(
        diskripsi= 'Pengiriman KAS Gerai ke DU: %s ' % (biaya.ket_penambahan_saldo),
        tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_penambahan_saldo)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_debet,
        kredit = 0,debet = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
     
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_kredit,
        debet = 0,kredit = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
    
def jurnal_biaya_penambahan_saldo_kas_cirebon_suci(biaya, user):
    D = decimal.Decimal
    a_penambahan_saldo_debet = get_object_or_404(Tbl_Akun, id=624L)
    a_penambahan_saldo_kredit = get_object_or_404(Tbl_Akun, id=609L)
    jurnal = Jurnal.objects.create(
        diskripsi= 'Pengiriman KAS Gerai ke Suci: %s ' % (biaya.ket_penambahan_saldo),
        tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_penambahan_saldo)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_debet,
        kredit = 0,debet = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
     
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_kredit,
        debet = 0,kredit = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
    
def jurnal_biaya_penambahan_saldo_kas_cirebon_balubur(biaya, user):
    D = decimal.Decimal
    a_penambahan_saldo_debet = get_object_or_404(Tbl_Akun, id=624L)
    a_penambahan_saldo_kredit = get_object_or_404(Tbl_Akun, id=611L)
    jurnal = Jurnal.objects.create(
        diskripsi= 'Pengiriman KAS Gerai ke Balubur: %s ' % (biaya.ket_penambahan_saldo),
        tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_penambahan_saldo)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_debet,
        kredit = 0,debet = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
     
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_kredit,
        debet = 0,kredit = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)

def jurnal_biaya_penambahan_saldo_kas_cirebon_hilir (biaya, user):
    D = decimal.Decimal
    a_penambahan_saldo_debet = get_object_or_404(Tbl_Akun, id=624L)
    a_penambahan_saldo_kredit = get_object_or_404(Tbl_Akun, id=613L)
    jurnal = Jurnal.objects.create(
        diskripsi= 'Pengiriman KAS Gerai ke Hilir: %s ' % (biaya.ket_penambahan_saldo),
        tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_penambahan_saldo)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_debet,
        kredit = 0,debet = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
     
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_kredit,
        debet = 0,kredit = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
    
def jurnal_biaya_penambahan_saldo_kas_cirebon_kopo(biaya, user):
    D = decimal.Decimal
    a_penambahan_saldo_debet = get_object_or_404(Tbl_Akun, id=624L)
    a_penambahan_saldo_kredit = get_object_or_404(Tbl_Akun, id=614L)
    jurnal = Jurnal.objects.create(
        diskripsi= 'Pengiriman KAS Gerai ke Kopo: %s ' % (biaya.ket_penambahan_saldo),
        tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_penambahan_saldo)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_debet,
        kredit = 0,debet = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
     
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_kredit,
        debet = 0,kredit = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
    
def jurnal_biaya_penambahan_saldo_kas_cirebon_cibiru(biaya, user):
    D = decimal.Decimal
    a_penambahan_saldo_debet = get_object_or_404(Tbl_Akun, id=624L)
    a_penambahan_saldo_kredit = get_object_or_404(Tbl_Akun, id=615L)
    jurnal = Jurnal.objects.create(
        diskripsi= 'Pengiriman KAS Gerai ke CIBIRU: %s ' % (biaya.ket_penambahan_saldo),
        tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_penambahan_saldo)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_debet,
        kredit = 0,debet = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
     
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_kredit,
        debet = 0,kredit = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)

def jurnal_biaya_penambahan_saldo_kas_cirebon_cipacing(biaya, user):
    D = decimal.Decimal
    a_penambahan_saldo_debet = get_object_or_404(Tbl_Akun, id=624L)
    a_penambahan_saldo_kredit = get_object_or_404(Tbl_Akun, id=616L)
    jurnal = Jurnal.objects.create(
        diskripsi= 'Pengiriman KAS Gerai ke JATINANGOR: %s ' % (biaya.ket_penambahan_saldo),
        tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_penambahan_saldo)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_debet,
        kredit = 0,debet = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
     
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_kredit,
        debet = 0,kredit = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
    
def jurnal_biaya_penambahan_saldo_kas_cirebon_jatinangor(biaya, user):
    D = decimal.Decimal
    a_penambahan_saldo_debet = get_object_or_404(Tbl_Akun, id=624L)
    a_penambahan_saldo_kredit = get_object_or_404(Tbl_Akun, id=617L)
    jurnal = Jurnal.objects.create(
        diskripsi= 'Pengiriman KAS Gerai ke Jatinangor : %s ' % (biaya.ket_penambahan_saldo),
        tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_penambahan_saldo)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_debet,
        kredit = 0,debet = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
     
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_kredit,
        debet = 0,kredit = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
    
def jurnal_biaya_penambahan_saldo_kas_cirebon_cimahi(biaya, user):
    D = decimal.Decimal
    a_penambahan_saldo_debet = get_object_or_404(Tbl_Akun, id=624L)
    a_penambahan_saldo_kredit = get_object_or_404(Tbl_Akun, id=618L)
    jurnal = Jurnal.objects.create(
        diskripsi= 'Pengiriman KAS Gerai ke CIMAHI: %s ' % (biaya.ket_penambahan_saldo),
        tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_penambahan_saldo)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_debet,
        kredit = 0,debet = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
     
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_kredit,
        debet = 0,kredit = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)

def jurnal_biaya_penambahan_saldo_kas_cirebon_bubat(biaya, user):
    D = decimal.Decimal
    a_penambahan_saldo_debet = get_object_or_404(Tbl_Akun, id=624L)
    a_penambahan_saldo_kredit = get_object_or_404(Tbl_Akun, id=619L)
    jurnal = Jurnal.objects.create(
        diskripsi= 'Pengiriman KAS Gerai ke BUAH BATU: %s ' % (biaya.ket_penambahan_saldo),
        tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_penambahan_saldo)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_debet,
        kredit = 0,debet = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
     
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_kredit,
        debet = 0,kredit = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
       
def jurnal_biaya_penambahan_saldo_kas_cirebon_maranatha(biaya, user):
    D = decimal.Decimal
    a_penambahan_saldo_debet = get_object_or_404(Tbl_Akun, id=624L)
    a_penambahan_saldo_kredit = get_object_or_404(Tbl_Akun, id=622L)
    jurnal = Jurnal.objects.create(
        diskripsi= 'Pengiriman KAS Gerai ke MARANATHA %s ' % (biaya.ket_penambahan_saldo),
        tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_penambahan_saldo)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_debet,
        kredit = 0,debet = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
     
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_kredit,
        debet = 0,kredit = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)

def jurnal_biaya_penambahan_saldo_kas_cirebon_ciumbeleuit(biaya, user):
    D = decimal.Decimal
    a_penambahan_saldo_debet = get_object_or_404(Tbl_Akun, id=624L)
    a_penambahan_saldo_kredit = get_object_or_404(Tbl_Akun, id=626L)
    jurnal = Jurnal.objects.create(
        diskripsi= 'Pengiriman KAS Gerai ke ciumbeleuit: %s ' % (biaya.ket_penambahan_saldo),
        tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_penambahan_saldo)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_debet,
        kredit = 0,debet = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
     
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_kredit,
        debet = 0,kredit = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
    
def jurnal_biaya_penambahan_saldo_kas_cirebon_uber(biaya, user):
    D = decimal.Decimal
    a_penambahan_saldo_debet = get_object_or_404(Tbl_Akun, id=624L)
    a_penambahan_saldo_kredit = get_object_or_404(Tbl_Akun, id=627L)
    jurnal = Jurnal.objects.create(
        diskripsi= 'Pengiriman KAS Gerai ke UJUNG BERUNG: %s ' % (biaya.ket_penambahan_saldo),
        tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_penambahan_saldo)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_debet,
        kredit = 0,debet = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
     
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_kredit,
        debet = 0,kredit = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
    
def jurnal_biaya_penambahan_saldo_kas_cirebon_ciwastra(biaya, user):
    D = decimal.Decimal
    a_penambahan_saldo_debet = get_object_or_404(Tbl_Akun, id=624L)
    a_penambahan_saldo_kredit = get_object_or_404(Tbl_Akun, id=628L)
    jurnal = Jurnal.objects.create(
        diskripsi= 'Pengiriman KAS Gerai ke CIWASTRA: %s ' % (biaya.ket_penambahan_saldo),
        tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_penambahan_saldo)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_debet,
        kredit = 0,debet = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_kredit,
        debet = 0,kredit = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)  

###Jurnal kas dari Ciumbeleuit ke pusat 
def jurnal_biaya_penambahan_saldo_kas_ciumbeleuit_pusat(biaya, user):
    D = decimal.Decimal
    a_penambahan_saldo_debet = get_object_or_404(Tbl_Akun, id=626L)
    a_penambahan_saldo_kredit = get_object_or_404(Tbl_Akun, id=4L)
    jurnal = Jurnal.objects.create(
        diskripsi= 'Pengembalian KasGerai NoRek: %s ' % (biaya.ket_penambahan_saldo),
        tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_penambahan_saldo)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_PUSAT"), id_coa = a_penambahan_saldo_debet,
        kredit = 0,debet = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
     
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_PUSAT"), id_coa = a_penambahan_saldo_kredit,
        debet = 0,kredit = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
    
def jurnal_biaya_penambahan_saldo_kas_ciumbeleuit_jakarta(biaya, user):
    D = decimal.Decimal
    a_penambahan_saldo_debet = get_object_or_404(Tbl_Akun, id=626L)
    a_penambahan_saldo_kredit = get_object_or_404(Tbl_Akun, id=7L)
    jurnal = Jurnal.objects.create(
        diskripsi= 'Pengiriman KAS Gerai ke Jakarta %s ' % (biaya.ket_penambahan_saldo),
        tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_penambahan_saldo)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_debet,
        kredit = 0,debet = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
     
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_kredit,
        debet = 0,kredit = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
    
def jurnal_biaya_penambahan_saldo_kas_ciumbeleuit_du(biaya, user):
    D = decimal.Decimal
    a_penambahan_saldo_debet = get_object_or_404(Tbl_Akun, id=626L)
    a_penambahan_saldo_kredit = get_object_or_404(Tbl_Akun, id=610L)
    jurnal = Jurnal.objects.create(
        diskripsi= 'Pengiriman KAS Gerai ke DU: %s ' % (biaya.ket_penambahan_saldo),
        tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_penambahan_saldo)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_debet,
        kredit = 0,debet = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
     
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_kredit,
        debet = 0,kredit = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
    
def jurnal_biaya_penambahan_saldo_kas_ciumbeleuit_suci(biaya, user):
    D = decimal.Decimal
    a_penambahan_saldo_debet = get_object_or_404(Tbl_Akun, id=626L)
    a_penambahan_saldo_kredit = get_object_or_404(Tbl_Akun, id=609L)
    jurnal = Jurnal.objects.create(
        diskripsi= 'Pengiriman KAS Gerai ke Suci: %s ' % (biaya.ket_penambahan_saldo),
        tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_penambahan_saldo)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_debet,
        kredit = 0,debet = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
     
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_kredit,
        debet = 0,kredit = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
    
def jurnal_biaya_penambahan_saldo_kas_ciumbeleuit_balubur(biaya, user):
    D = decimal.Decimal
    a_penambahan_saldo_debet = get_object_or_404(Tbl_Akun, id=626L)
    a_penambahan_saldo_kredit = get_object_or_404(Tbl_Akun, id=611L)
    jurnal = Jurnal.objects.create(
        diskripsi= 'Pengiriman KAS Gerai ke Balubur: %s ' % (biaya.ket_penambahan_saldo),
        tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_penambahan_saldo)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_debet,
        kredit = 0,debet = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
     
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_kredit,
        debet = 0,kredit = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)

def jurnal_biaya_penambahan_saldo_kas_ciumbeleuit_hilir (biaya, user):
    D = decimal.Decimal
    a_penambahan_saldo_debet = get_object_or_404(Tbl_Akun, id=626L)
    a_penambahan_saldo_kredit = get_object_or_404(Tbl_Akun, id=613L)
    jurnal = Jurnal.objects.create(
        diskripsi= 'Pengiriman KAS Gerai ke Hilir: %s ' % (biaya.ket_penambahan_saldo),
        tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_penambahan_saldo)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_debet,
        kredit = 0,debet = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
     
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_kredit,
        debet = 0,kredit = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
    
def jurnal_biaya_penambahan_saldo_kas_ciumbeleuit_kopo(biaya, user):
    D = decimal.Decimal
    a_penambahan_saldo_debet = get_object_or_404(Tbl_Akun, id=626L)
    a_penambahan_saldo_kredit = get_object_or_404(Tbl_Akun, id=614L)
    jurnal = Jurnal.objects.create(
        diskripsi= 'Pengiriman KAS Gerai ke Kopo: %s ' % (biaya.ket_penambahan_saldo),
        tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_penambahan_saldo)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_debet,
        kredit = 0,debet = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
     
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_kredit,
        debet = 0,kredit = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
    
def jurnal_biaya_penambahan_saldo_kas_ciumbeleuit_cibiru(biaya, user):
    D = decimal.Decimal
    a_penambahan_saldo_debet = get_object_or_404(Tbl_Akun, id=626L)
    a_penambahan_saldo_kredit = get_object_or_404(Tbl_Akun, id=615L)
    jurnal = Jurnal.objects.create(
        diskripsi= 'Pengiriman KAS Gerai ke CIBIRU: %s ' % (biaya.ket_penambahan_saldo),
        tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_penambahan_saldo)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_debet,
        kredit = 0,debet = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
     
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_kredit,
        debet = 0,kredit = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)

def jurnal_biaya_penambahan_saldo_kas_ciumbeleuit_cipacing(biaya, user):
    D = decimal.Decimal
    a_penambahan_saldo_debet = get_object_or_404(Tbl_Akun, id=626L)
    a_penambahan_saldo_kredit = get_object_or_404(Tbl_Akun, id=616L)
    jurnal = Jurnal.objects.create(
        diskripsi= 'Pengiriman KAS Gerai ke JATINANGOR: %s ' % (biaya.ket_penambahan_saldo),
        tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_penambahan_saldo)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_debet,
        kredit = 0,debet = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
     
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_kredit,
        debet = 0,kredit = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
    
def jurnal_biaya_penambahan_saldo_kas_ciumbeleuit_jatinangor(biaya, user):
    D = decimal.Decimal
    a_penambahan_saldo_debet = get_object_or_404(Tbl_Akun, id=626L)
    a_penambahan_saldo_kredit = get_object_or_404(Tbl_Akun, id=617L)
    jurnal = Jurnal.objects.create(
        diskripsi= 'Pengiriman KAS Gerai ke Jatinangor : %s ' % (biaya.ket_penambahan_saldo),
        tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_penambahan_saldo)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_debet,
        kredit = 0,debet = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
     
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_kredit,
        debet = 0,kredit = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
    
def jurnal_biaya_penambahan_saldo_kas_ciumbeleuit_cimahi(biaya, user):
    D = decimal.Decimal
    a_penambahan_saldo_debet = get_object_or_404(Tbl_Akun, id=626L)
    a_penambahan_saldo_kredit = get_object_or_404(Tbl_Akun, id=618L)
    jurnal = Jurnal.objects.create(
        diskripsi= 'Pengiriman KAS Gerai ke CIMAHI: %s ' % (biaya.ket_penambahan_saldo),
        tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_penambahan_saldo)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_debet,
        kredit = 0,debet = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
     
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_kredit,
        debet = 0,kredit = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)

def jurnal_biaya_penambahan_saldo_kas_ciumbeleuit_bubat(biaya, user):
    D = decimal.Decimal
    a_penambahan_saldo_debet = get_object_or_404(Tbl_Akun, id=626L)
    a_penambahan_saldo_kredit = get_object_or_404(Tbl_Akun, id=619L)
    jurnal = Jurnal.objects.create(
        diskripsi= 'Pengiriman KAS Gerai ke BUAH BATU: %s ' % (biaya.ket_penambahan_saldo),
        tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_penambahan_saldo)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_debet,
        kredit = 0,debet = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
     
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_kredit,
        debet = 0,kredit = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
       
def jurnal_biaya_penambahan_saldo_kas_ciumbeleuit_maranatha(biaya, user):
    D = decimal.Decimal
    a_penambahan_saldo_debet = get_object_or_404(Tbl_Akun, id=626L)
    a_penambahan_saldo_kredit = get_object_or_404(Tbl_Akun, id=622L)
    jurnal = Jurnal.objects.create(
        diskripsi= 'Pengiriman KAS Gerai ke MARANATHA %s ' % (biaya.ket_penambahan_saldo),
        tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_penambahan_saldo)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_debet,
        kredit = 0,debet = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
     
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_kredit,
        debet = 0,kredit = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)

def jurnal_biaya_penambahan_saldo_kas_ciumbeleuit_cirebon(biaya, user):
    D = decimal.Decimal
    a_penambahan_saldo_debet = get_object_or_404(Tbl_Akun, id=626L)
    a_penambahan_saldo_kredit = get_object_or_404(Tbl_Akun, id=624L)
    jurnal = Jurnal.objects.create(
        diskripsi= 'Pengiriman KAS Gerai ke ciumbeleuit: %s ' % (biaya.ket_penambahan_saldo),
        tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_penambahan_saldo)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_debet,
        kredit = 0,debet = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
     
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_kredit,
        debet = 0,kredit = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
    
def jurnal_biaya_penambahan_saldo_kas_ciumbeleuit_uber(biaya, user):
    D = decimal.Decimal
    a_penambahan_saldo_debet = get_object_or_404(Tbl_Akun, id=626L)
    a_penambahan_saldo_kredit = get_object_or_404(Tbl_Akun, id=627L)
    jurnal = Jurnal.objects.create(
        diskripsi= 'Pengiriman KAS Gerai ke UJUNG BERUNG: %s ' % (biaya.ket_penambahan_saldo),
        tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_penambahan_saldo)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_debet,
        kredit = 0,debet = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
     
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_kredit,
        debet = 0,kredit = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
    
def jurnal_biaya_penambahan_saldo_kas_ciumbeleuit_ciwastra(biaya, user):
    D = decimal.Decimal
    a_penambahan_saldo_debet = get_object_or_404(Tbl_Akun, id=626L)
    a_penambahan_saldo_kredit = get_object_or_404(Tbl_Akun, id=628L)
    jurnal = Jurnal.objects.create(
        diskripsi= 'Pengiriman KAS Gerai ke CIWASTRA: %s ' % (biaya.ket_penambahan_saldo),
        tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_penambahan_saldo)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_debet,
        kredit = 0,debet = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_kredit,
        debet = 0,kredit = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)  

###Jurnal kas dari Ujungberung ke pusat 
def jurnal_biaya_penambahan_saldo_kas_uber_pusat(biaya, user):
    D = decimal.Decimal
    a_penambahan_saldo_debet = get_object_or_404(Tbl_Akun, id=627L)
    a_penambahan_saldo_kredit = get_object_or_404(Tbl_Akun, id=4L)
    jurnal = Jurnal.objects.create(
        diskripsi= 'Pengembalian KasGerai NoRek: %s ' % (biaya.ket_penambahan_saldo),
        tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_penambahan_saldo)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_PUSAT"), id_coa = a_penambahan_saldo_debet,
        kredit = 0,debet = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
     
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_PUSAT"), id_coa = a_penambahan_saldo_kredit,
        debet = 0,kredit = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
    
def jurnal_biaya_penambahan_saldo_kas_uber_jakarta(biaya, user):
    D = decimal.Decimal
    a_penambahan_saldo_debet = get_object_or_404(Tbl_Akun, id=627L)
    a_penambahan_saldo_kredit = get_object_or_404(Tbl_Akun, id=7L)
    jurnal = Jurnal.objects.create(
        diskripsi= 'Pengiriman KAS Gerai ke Jakarta %s ' % (biaya.ket_penambahan_saldo),
        tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_penambahan_saldo)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_debet,
        kredit = 0,debet = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
     
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_kredit,
        debet = 0,kredit = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
    
def jurnal_biaya_penambahan_saldo_kas_uber_du(biaya, user):
    D = decimal.Decimal
    a_penambahan_saldo_debet = get_object_or_404(Tbl_Akun, id=627L)
    a_penambahan_saldo_kredit = get_object_or_404(Tbl_Akun, id=610L)
    jurnal = Jurnal.objects.create(
        diskripsi= 'Pengiriman KAS Gerai ke DU: %s ' % (biaya.ket_penambahan_saldo),
        tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_penambahan_saldo)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_debet,
        kredit = 0,debet = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
     
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_kredit,
        debet = 0,kredit = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
    
def jurnal_biaya_penambahan_saldo_kas_uber_suci(biaya, user):
    D = decimal.Decimal
    a_penambahan_saldo_debet = get_object_or_404(Tbl_Akun, id=627L)
    a_penambahan_saldo_kredit = get_object_or_404(Tbl_Akun, id=609L)
    jurnal = Jurnal.objects.create(
        diskripsi= 'Pengiriman KAS Gerai ke Suci: %s ' % (biaya.ket_penambahan_saldo),
        tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_penambahan_saldo)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_debet,
        kredit = 0,debet = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
     
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_kredit,
        debet = 0,kredit = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
    
def jurnal_biaya_penambahan_saldo_kas_uber_balubur(biaya, user):
    D = decimal.Decimal
    a_penambahan_saldo_debet = get_object_or_404(Tbl_Akun, id=627L)
    a_penambahan_saldo_kredit = get_object_or_404(Tbl_Akun, id=611L)
    jurnal = Jurnal.objects.create(
        diskripsi= 'Pengiriman KAS Gerai ke Balubur: %s ' % (biaya.ket_penambahan_saldo),
        tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_penambahan_saldo)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_debet,
        kredit = 0,debet = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
     
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_kredit,
        debet = 0,kredit = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)

def jurnal_biaya_penambahan_saldo_kas_uber_hilir (biaya, user):
    D = decimal.Decimal
    a_penambahan_saldo_debet = get_object_or_404(Tbl_Akun, id=627L)
    a_penambahan_saldo_kredit = get_object_or_404(Tbl_Akun, id=613L)
    jurnal = Jurnal.objects.create(
        diskripsi= 'Pengiriman KAS Gerai ke Hilir: %s ' % (biaya.ket_penambahan_saldo),
        tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_penambahan_saldo)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_debet,
        kredit = 0,debet = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
     
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_kredit,
        debet = 0,kredit = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
    
def jurnal_biaya_penambahan_saldo_kas_uber_kopo(biaya, user):
    D = decimal.Decimal
    a_penambahan_saldo_debet = get_object_or_404(Tbl_Akun, id=627L)
    a_penambahan_saldo_kredit = get_object_or_404(Tbl_Akun, id=614L)
    jurnal = Jurnal.objects.create(
        diskripsi= 'Pengiriman KAS Gerai ke Kopo: %s ' % (biaya.ket_penambahan_saldo),
        tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_penambahan_saldo)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_debet,
        kredit = 0,debet = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
     
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_kredit,
        debet = 0,kredit = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
    
def jurnal_biaya_penambahan_saldo_kas_uber_cibiru(biaya, user):
    D = decimal.Decimal
    a_penambahan_saldo_debet = get_object_or_404(Tbl_Akun, id=627L)
    a_penambahan_saldo_kredit = get_object_or_404(Tbl_Akun, id=615L)
    jurnal = Jurnal.objects.create(
        diskripsi= 'Pengiriman KAS Gerai ke CIBIRU: %s ' % (biaya.ket_penambahan_saldo),
        tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_penambahan_saldo)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_debet,
        kredit = 0,debet = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
     
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_kredit,
        debet = 0,kredit = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)

def jurnal_biaya_penambahan_saldo_kas_uber_cipacing(biaya, user):
    D = decimal.Decimal
    a_penambahan_saldo_debet = get_object_or_404(Tbl_Akun, id=627L)
    a_penambahan_saldo_kredit = get_object_or_404(Tbl_Akun, id=616L)
    jurnal = Jurnal.objects.create(
        diskripsi= 'Pengiriman KAS Gerai ke JATINANGOR: %s ' % (biaya.ket_penambahan_saldo),
        tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_penambahan_saldo)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_debet,
        kredit = 0,debet = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
     
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_kredit,
        debet = 0,kredit = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
    
def jurnal_biaya_penambahan_saldo_kas_uber_jatinangor(biaya, user):
    D = decimal.Decimal
    a_penambahan_saldo_debet = get_object_or_404(Tbl_Akun, id=627L)
    a_penambahan_saldo_kredit = get_object_or_404(Tbl_Akun, id=617L)
    jurnal = Jurnal.objects.create(
        diskripsi= 'Pengiriman KAS Gerai ke Jatinangor : %s ' % (biaya.ket_penambahan_saldo),
        tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_penambahan_saldo)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_debet,
        kredit = 0,debet = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
     
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_kredit,
        debet = 0,kredit = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
    
def jurnal_biaya_penambahan_saldo_kas_uber_cimahi(biaya, user):
    D = decimal.Decimal
    a_penambahan_saldo_debet = get_object_or_404(Tbl_Akun, id=627L)
    a_penambahan_saldo_kredit = get_object_or_404(Tbl_Akun, id=618L)
    jurnal = Jurnal.objects.create(
        diskripsi= 'Pengiriman KAS Gerai ke CIMAHI: %s ' % (biaya.ket_penambahan_saldo),
        tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_penambahan_saldo)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_debet,
        kredit = 0,debet = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
     
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_kredit,
        debet = 0,kredit = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)

def jurnal_biaya_penambahan_saldo_kas_uber_bubat(biaya, user):
    D = decimal.Decimal
    a_penambahan_saldo_debet = get_object_or_404(Tbl_Akun, id=627L)
    a_penambahan_saldo_kredit = get_object_or_404(Tbl_Akun, id=619L)
    jurnal = Jurnal.objects.create(
        diskripsi= 'Pengiriman KAS Gerai ke BUAH BATU: %s ' % (biaya.ket_penambahan_saldo),
        tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_penambahan_saldo)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_debet,
        kredit = 0,debet = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
     
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_kredit,
        debet = 0,kredit = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
       
def jurnal_biaya_penambahan_saldo_kas_uber_maranatha(biaya, user):
    D = decimal.Decimal
    a_penambahan_saldo_debet = get_object_or_404(Tbl_Akun, id=627L)
    a_penambahan_saldo_kredit = get_object_or_404(Tbl_Akun, id=622L)
    jurnal = Jurnal.objects.create(
        diskripsi= 'Pengiriman KAS Gerai ke MARANATHA %s ' % (biaya.ket_penambahan_saldo),
        tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_penambahan_saldo)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_debet,
        kredit = 0,debet = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
     
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_kredit,
        debet = 0,kredit = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)

def jurnal_biaya_penambahan_saldo_kas_uber_cirebon(biaya, user):
    D = decimal.Decimal
    a_penambahan_saldo_debet = get_object_or_404(Tbl_Akun, id=627L)
    a_penambahan_saldo_kredit = get_object_or_404(Tbl_Akun, id=624L)
    jurnal = Jurnal.objects.create(
        diskripsi= 'Pengiriman KAS Gerai ke uber: %s ' % (biaya.ket_penambahan_saldo),
        tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_penambahan_saldo)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_debet,
        kredit = 0,debet = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
     
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_kredit,
        debet = 0,kredit = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
    
def jurnal_biaya_penambahan_saldo_kas_uber_ciumbeleuit(biaya, user):
    D = decimal.Decimal
    a_penambahan_saldo_debet = get_object_or_404(Tbl_Akun, id=627L)
    a_penambahan_saldo_kredit = get_object_or_404(Tbl_Akun, id=626L)
    jurnal = Jurnal.objects.create(
        diskripsi= 'Pengiriman KAS Gerai ke UJUNG BERUNG: %s ' % (biaya.ket_penambahan_saldo),
        tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_penambahan_saldo)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_debet,
        kredit = 0,debet = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
     
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_kredit,
        debet = 0,kredit = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
    
def jurnal_biaya_penambahan_saldo_kas_uber_ciwastra(biaya, user):
    D = decimal.Decimal
    a_penambahan_saldo_debet = get_object_or_404(Tbl_Akun, id=627L)
    a_penambahan_saldo_kredit = get_object_or_404(Tbl_Akun, id=628L)
    jurnal = Jurnal.objects.create(
        diskripsi= 'Pengiriman KAS Gerai ke CIWASTRA: %s ' % (biaya.ket_penambahan_saldo),
        tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_penambahan_saldo)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_debet,
        kredit = 0,debet = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_kredit,
        debet = 0,kredit = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
    
###Jurnal kas dari Ciwastra ke pusat 
def jurnal_biaya_penambahan_saldo_kas_ciwastra_pusat(biaya, user):
    D = decimal.Decimal
    a_penambahan_saldo_debet = get_object_or_404(Tbl_Akun, id=628L)
    a_penambahan_saldo_kredit = get_object_or_404(Tbl_Akun, id=4L)
    jurnal = Jurnal.objects.create(
        diskripsi= 'Pengembalian KasGerai NoRek: %s ' % (biaya.ket_penambahan_saldo),
        tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_penambahan_saldo)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_PUSAT"), id_coa = a_penambahan_saldo_debet,
        kredit = 0,debet = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
     
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_PUSAT"), id_coa = a_penambahan_saldo_kredit,
        debet = 0,kredit = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
    
def jurnal_biaya_penambahan_saldo_kas_ciwastra_jakarta(biaya, user):
    D = decimal.Decimal
    a_penambahan_saldo_debet = get_object_or_404(Tbl_Akun, id=628L)
    a_penambahan_saldo_kredit = get_object_or_404(Tbl_Akun, id=7L)
    jurnal = Jurnal.objects.create(
        diskripsi= 'Pengiriman KAS Gerai ke Jakarta %s ' % (biaya.ket_penambahan_saldo),
        tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_penambahan_saldo)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_debet,
        kredit = 0,debet = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
     
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_kredit,
        debet = 0,kredit = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
    
def jurnal_biaya_penambahan_saldo_kas_ciwastra_du(biaya, user):
    D = decimal.Decimal
    a_penambahan_saldo_debet = get_object_or_404(Tbl_Akun, id=628L)
    a_penambahan_saldo_kredit = get_object_or_404(Tbl_Akun, id=610L)
    jurnal = Jurnal.objects.create(
        diskripsi= 'Pengiriman KAS Gerai ke DU: %s ' % (biaya.ket_penambahan_saldo),
        tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_penambahan_saldo)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_debet,
        kredit = 0,debet = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
     
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_kredit,
        debet = 0,kredit = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
    
def jurnal_biaya_penambahan_saldo_kas_ciwastra_suci(biaya, user):
    D = decimal.Decimal
    a_penambahan_saldo_debet = get_object_or_404(Tbl_Akun, id=628L)
    a_penambahan_saldo_kredit = get_object_or_404(Tbl_Akun, id=609L)
    jurnal = Jurnal.objects.create(
        diskripsi= 'Pengiriman KAS Gerai ke Suci: %s ' % (biaya.ket_penambahan_saldo),
        tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_penambahan_saldo)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_debet,
        kredit = 0,debet = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
     
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_kredit,
        debet = 0,kredit = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
    
def jurnal_biaya_penambahan_saldo_kas_ciwastra_balubur(biaya, user):
    D = decimal.Decimal
    a_penambahan_saldo_debet = get_object_or_404(Tbl_Akun, id=628L)
    a_penambahan_saldo_kredit = get_object_or_404(Tbl_Akun, id=611L)
    jurnal = Jurnal.objects.create(
        diskripsi= 'Pengiriman KAS Gerai ke Balubur: %s ' % (biaya.ket_penambahan_saldo),
        tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_penambahan_saldo)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_debet,
        kredit = 0,debet = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
     
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_kredit,
        debet = 0,kredit = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)

def jurnal_biaya_penambahan_saldo_kas_ciwastra_hilir (biaya, user):
    D = decimal.Decimal
    a_penambahan_saldo_debet = get_object_or_404(Tbl_Akun, id=628L)
    a_penambahan_saldo_kredit = get_object_or_404(Tbl_Akun, id=613L)
    jurnal = Jurnal.objects.create(
        diskripsi= 'Pengiriman KAS Gerai ke Hilir: %s ' % (biaya.ket_penambahan_saldo),
        tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_penambahan_saldo)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_debet,
        kredit = 0,debet = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
     
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_kredit,
        debet = 0,kredit = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
    
def jurnal_biaya_penambahan_saldo_kas_ciwastra_kopo(biaya, user):
    D = decimal.Decimal
    a_penambahan_saldo_debet = get_object_or_404(Tbl_Akun, id=628L)
    a_penambahan_saldo_kredit = get_object_or_404(Tbl_Akun, id=614L)
    jurnal = Jurnal.objects.create(
        diskripsi= 'Pengiriman KAS Gerai ke Kopo: %s ' % (biaya.ket_penambahan_saldo),
        tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_penambahan_saldo)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_debet,
        kredit = 0,debet = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
     
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_kredit,
        debet = 0,kredit = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
    
def jurnal_biaya_penambahan_saldo_kas_ciwastra_cibiru(biaya, user):
    D = decimal.Decimal
    a_penambahan_saldo_debet = get_object_or_404(Tbl_Akun, id=628L)
    a_penambahan_saldo_kredit = get_object_or_404(Tbl_Akun, id=615L)
    jurnal = Jurnal.objects.create(
        diskripsi= 'Pengiriman KAS Gerai ke CIBIRU: %s ' % (biaya.ket_penambahan_saldo),
        tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_penambahan_saldo)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_debet,
        kredit = 0,debet = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
     
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_kredit,
        debet = 0,kredit = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)

def jurnal_biaya_penambahan_saldo_kas_ciwastra_cipacing(biaya, user):
    D = decimal.Decimal
    a_penambahan_saldo_debet = get_object_or_404(Tbl_Akun, id=628L)
    a_penambahan_saldo_kredit = get_object_or_404(Tbl_Akun, id=616L)
    jurnal = Jurnal.objects.create(
        diskripsi= 'Pengiriman KAS Gerai ke JATINANGOR: %s ' % (biaya.ket_penambahan_saldo),
        tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_penambahan_saldo)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_debet,
        kredit = 0,debet = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
     
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_kredit,
        debet = 0,kredit = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
    
def jurnal_biaya_penambahan_saldo_kas_ciwastra_jatinangor(biaya, user):
    D = decimal.Decimal
    a_penambahan_saldo_debet = get_object_or_404(Tbl_Akun, id=628L)
    a_penambahan_saldo_kredit = get_object_or_404(Tbl_Akun, id=617L)
    jurnal = Jurnal.objects.create(
        diskripsi= 'Pengiriman KAS Gerai ke Jatinangor : %s ' % (biaya.ket_penambahan_saldo),
        tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_penambahan_saldo)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_debet,
        kredit = 0,debet = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
     
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_kredit,
        debet = 0,kredit = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
    
def jurnal_biaya_penambahan_saldo_kas_ciwastra_cimahi(biaya, user):
    D = decimal.Decimal
    a_penambahan_saldo_debet = get_object_or_404(Tbl_Akun, id=628L)
    a_penambahan_saldo_kredit = get_object_or_404(Tbl_Akun, id=618L)
    jurnal = Jurnal.objects.create(
        diskripsi= 'Pengiriman KAS Gerai ke CIMAHI: %s ' % (biaya.ket_penambahan_saldo),
        tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_penambahan_saldo)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_debet,
        kredit = 0,debet = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
     
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_kredit,
        debet = 0,kredit = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)

def jurnal_biaya_penambahan_saldo_kas_ciwastra_bubat(biaya, user):
    D = decimal.Decimal
    a_penambahan_saldo_debet = get_object_or_404(Tbl_Akun, id=628L)
    a_penambahan_saldo_kredit = get_object_or_404(Tbl_Akun, id=619L)
    jurnal = Jurnal.objects.create(
        diskripsi= 'Pengiriman KAS Gerai ke BUAH BATU: %s ' % (biaya.ket_penambahan_saldo),
        tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_penambahan_saldo)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_debet,
        kredit = 0,debet = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
     
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_kredit,
        debet = 0,kredit = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
       
def jurnal_biaya_penambahan_saldo_kas_ciwastra_maranatha(biaya, user):
    D = decimal.Decimal
    a_penambahan_saldo_debet = get_object_or_404(Tbl_Akun, id=628L)
    a_penambahan_saldo_kredit = get_object_or_404(Tbl_Akun, id=622L)
    jurnal = Jurnal.objects.create(
        diskripsi= 'Pengiriman KAS Gerai ke MARANATHA %s ' % (biaya.ket_penambahan_saldo),
        tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_penambahan_saldo)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_debet,
        kredit = 0,debet = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
     
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_kredit,
        debet = 0,kredit = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)

def jurnal_biaya_penambahan_saldo_kas_ciwastra_cirebon(biaya, user):
    D = decimal.Decimal
    a_penambahan_saldo_debet = get_object_or_404(Tbl_Akun, id=628L)
    a_penambahan_saldo_kredit = get_object_or_404(Tbl_Akun, id=624L)
    jurnal = Jurnal.objects.create(
        diskripsi= 'Pengiriman KAS Gerai ke ciwastra: %s ' % (biaya.ket_penambahan_saldo),
        tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_penambahan_saldo)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_debet,
        kredit = 0,debet = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
     
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_kredit,
        debet = 0,kredit = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
    
def jurnal_biaya_penambahan_saldo_kas_ciwastra_ciumbeleuit(biaya, user):
    D = decimal.Decimal
    a_penambahan_saldo_debet = get_object_or_404(Tbl_Akun, id=628L)
    a_penambahan_saldo_kredit = get_object_or_404(Tbl_Akun, id=626L)
    jurnal = Jurnal.objects.create(
        diskripsi= 'Pengiriman KAS Gerai ke UJUNG BERUNG: %s ' % (biaya.ket_penambahan_saldo),
        tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_penambahan_saldo)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_debet,
        kredit = 0,debet = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
     
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_kredit,
        debet = 0,kredit = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
    
def jurnal_biaya_penambahan_saldo_kas_ciwastra_uber(biaya, user):
    D = decimal.Decimal
    a_penambahan_saldo_debet = get_object_or_404(Tbl_Akun, id=628L)
    a_penambahan_saldo_kredit = get_object_or_404(Tbl_Akun, id=627L)
    jurnal = Jurnal.objects.create(
        diskripsi= 'Pengiriman KAS Gerai ke Ujungberung: %s ' % (biaya.ket_penambahan_saldo),
        tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_penambahan_saldo)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_debet,
        kredit = 0,debet = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_GERAI"), id_coa = a_penambahan_saldo_kredit,
        debet = 0,kredit = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='0',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)  
