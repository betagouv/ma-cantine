# run this with python field_gen.py > ../notes/whatever.py
# in response to https://github.com/betagouv/ma-cantine/issues/1509

# model
labels = [
    ("BIO", "Bio"),
    ("LABEL_ROUGE", "Label rouge"),
    ("AOCAOP_IGP_STG", "AOC / AOP / IGP / STG"),
    ("HVE", "Haute valeur environnementale"),
    ("PECHE_DURABLE", "Pêche durable"),
    ("RUP", "Région ultrapériphérique"),
    ("FERMIER", "Fermier"),
    (
        "EXTERNALITES",
        "Produit prenant en compte les coûts imputés aux externalités environnementales pendant son cycle de vie",
    ),
    ("COMMERCE_EQUITABLE", "Commerce équitable"),
    ("PERFORMANCE", "Produits acquis sur la base de leurs performances en matière environnementale"),
    ("EQUIVALENTS", "Produits équivalents"),
    ("FRANCE", "Provenance France"),
    ("SHORT_DISTRIBUTION", "Circuit-court"),
    ("LOCAL", "Produit local"),
]
families = [
    ("VIANDES_VOLAILLES", "Viandes et volailles fraîches et surgelées"),
    ("PRODUITS_DE_LA_MER", "Produits aquatiques frais et surgelés"),
    ("FRUITS_ET_LEGUMES", "Fruits et légumes frais et surgelés"),
    ("CHARCUTERIE", "Charcuterie"),
    ("PRODUITS_LAITIERS", "BOF (Produits laitiers, beurre et œufs)"),
    ("BOULANGERIE", "Boulangerie/Pâtisserie fraîches"),
    ("BOISSONS", "Boissons"),
    ("AUTRES", "Autres produits frais, surgelés et d’épicerie"),
]
labels = [(label[0].lower(), label[1]) for label in labels]
families = [(f[0].lower(), f[1]) for f in families]
fields = []
for label in labels:
    for family in families:
        fields.append({"fieldname": f"{family[0]}_{label[0]}", "description": f"{family[1]}, {label[1]}"})

print(f"# will generate {len(fields)} fields")
for f in fields:
    print(f"{f['fieldname']} = models.DecimalField(")
    print("    max_digits=20,")
    print("    decimal_places=2,")
    print("    blank=True,")
    print("    null=True,")
    print(f"    verbose_name=\"{f['description']}\",")
    print(")")

print("\n# properties")
print("\n# TODO: define label_sum and family_sum methods")
for label in labels:
    print("@property")
    print(f"def total_label_{label[0]}(self):")
    print(f'    return self.label_sum("{label[0]}")')
for family in families:
    print("@property")
    print(f"def total_family_{family[0]}(self):")
    print(f'    return self.family_sum("{family[0]}")')

# factory
print("\n# factory")
for f in fields:
    print(f"{f['fieldname']} = factory.Faker(\"random_int\", min=0, max=200)")

# serializer
print("\n# serializer, admin")
for f in fields:
    print(f"\"{f['fieldname']}\",")
print("\n# properties")
labels_and_families = [*labels, *families]
for t in labels_and_families:
    print(f'"{t[0]}",')

# lists
print("\n# misc")
print("[", end="")
for f in fields:
    print(f"\"{f['fieldname']}\"", end=", ")
for t in labels_and_families:
    print(f'"{t[0]}"', end=", ")
print("]")
print("[", end="")
for t in labels:
    print(f'"{t[0]}"', end=", ")
print("]")
print("[", end="")
for t in families:
    print(f'"{t[0]}"', end=", ")
print("]")

# importer
print("\n# CSV")
for f in fields:
    print(f"\"{f['description'].replace(',', ' -')}\"", end=",")
print("")
for f in fields:
    print("10", end=",")
print("")
# TODO: code for importer view
# TODO: can make nicer column names

# test
print("\n# diagnostic api test")
for f in fields:
    print(f"\"{f['fieldname']}\": 10,")
print("")
for label in labels:
    print(f"self.assertEqual(diagnostic.total_label_{label[0]}, {10 * len(families)})")
for family in families:
    print(f"self.assertEqual(diagnostic.total_family_{family[0]}, {10 * len(labels)})")
