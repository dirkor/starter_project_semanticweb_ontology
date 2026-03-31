import rdflib
import owlrl

def run_inference():
    print("Memuat ontologi...")
    g = rdflib.Graph()
    # Muat file ontologi yang baru dibuat
    g.parse("data/academic_ontology_v1.owl")

    print(f"Jumlah triple sebelum inferensi: {len(g)}")

    # Menjalankan reasoner OWLRL (simulasi inferensi OWL)
    print("\nMenjalankan reasoner OWL-RL...")
    owlrl.DeductiveClosure(owlrl.OWLRL_Semantics).expand(g)
    
    print(f"Jumlah triple setelah inferensi: {len(g)}")

    # Namespace untuk query
    BASE = rdflib.Namespace("http://example.org/akademik#")
    
    print("\n=== HASIL INFERENSI ===")
    
    # 1. Inferensi Transitive Property (memilikiPrasyarat)
    # KecerdasanBuatan -> StrukturData -> MatematikaDiskrit
    # Seharusnya KecerdasanBuatan memiliki prasyarat MatematikaDiskrit
    print("\n1. Inferensi Prasyarat Transitive (Kecerdasan Buatan):")
    for o in g.objects(BASE.KecerdasanBuatan, BASE.memilikiPrasyarat):
        print(f" - Prasyarat: {o.split('#')[-1]}")

    # 2. Inferensi Inverse Property (diampuOleh vs mengampu)
    # DosenC mengampu KecerdasanBuatan, maka KecerdasanBuatan diampuOleh DosenC
    print("\n2. Inferensi Inverse Property (Siapa yang mengampu Kecerdasan Buatan?):")
    for o in g.objects(BASE.KecerdasanBuatan, BASE.diampuOleh):
        print(f" - Diampu Oleh: {o.split('#')[-1]}")

    # 3. Inferensi SubClass (DosenTetap -> Dosen)
    # DosenC adalah DosenTetap, seharusnya DosenC juga terdeteksi sebagai Dosen
    print("\n3. Inferensi SubClass (Siapa saja yang merupakan Dosen?):")
    from rdflib.namespace import RDF
    for s in g.subjects(RDF.type, BASE.Dosen):
        print(f" - Dosen: {s.split('#')[-1]}")

if __name__ == "__main__":
    try:
        run_inference()
    except ImportError:
        print("Pastikan Anda sudah menginstall library 'owlrl'")
        print("Jalankan: pip install owlrl")
