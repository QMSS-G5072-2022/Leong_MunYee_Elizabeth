from cipher_ml4837 import cipher_ml4837

def test_cipher_a(self):
    assert cipher_ml4837.cipher("Good", 1) == "Hppe", "Should be Hppe"

def test_cipher_b(self):
    assert cipher_ml4837.cipher("Good", -1) == "Fnnc", "Should be Fnnc"

def test_cipher_c(self):
    assert cipher_ml4837.cipher("Good!283", 1) == "Hppe!283", "Should be Hppe!283"
