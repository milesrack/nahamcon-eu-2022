from Crypto.Cipher import AES
import base64

key = bytes.fromhex("e2761a8eb2264abee2567aee1286aa1e")

ct = base64.b64decode("pNUmvTZxrIlgqNwa3IVysgB6lG/ZcfQcXhVsMeugJxV62P61P5KHC0OjpsV7SF2aguTRGhbbp/uX\
qa03+zTHCpem5pzZQVh8et/BvOWRE6LGyhE9EfrzK90vdjewhHDtbavPMa35YKi03cscIt8bMkZT\
rUHq7f2qELPmXr5a7lKdLbPwWrh96zqBMSQJ7QJorF6Rv1F1YpQVIXI/LYJzpZizDukOAPBLdxFr\
YBj+Ndch/rihIMLHayg/MFcKlpLQ3rQX6qwKmJv21Gu51BWqFkUJMfhpUWeG7bB9AgUdCI+ecpqF\
9fHM34TkdSKzKCmbffq/0ZkxGZZgqrpV3wnZZKCvgGtVUh9c1LKB4bWenUnjyB5275pGCSLMUk7V\
Wo9q")

aes = AES.new(key, AES.MODE_CBC)
pt = aes.decrypt(ct)
print(pt)