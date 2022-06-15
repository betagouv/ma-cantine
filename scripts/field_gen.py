# run this with python field_gen.py > ../notes/whatever.py

# model
labels = ["bio", "label_rouge", "aocaop_igp", "hve"]
families = ["viandes_volailles", "produits_de_la_mer", "produits_laitiers", "boissons", "boulangerie", "autres"]
fields = []
for label in labels:
    for family in families:
        fields.append({"fieldname": f"{label}_{family}", "description": f"{label}, {family}"})

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
    print(f"def total_label_{label}(self):")
    print(f'    return label_sum(self, "{label}")')
for family in families:
    print("@property")
    print(f"def total_family_{family}(self):")
    print(f'    return family_sum(self, "{family}")')

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
    print(f'"{t}",')

# lists
print("\n# misc")
print("[", end="")
for f in fields:
    print(f"\"{f['fieldname']}\"", end=", ")
for t in labels_and_families:
    print(f'"{t}"', end=", ")
print("]")

# importer
print("\n# CSV")
for f in fields:
    print(f"\"{f['description'].replace(',', '')}\"", end=",")
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
for label in labels:
    print(f"self.assertEqual(diagnostic.total_label_{label}, {10 * len(families)})")
for family in families:
    print(f"self.assertEqual(diagnostic.total_family_{family}, {10 * len(labels)})")
