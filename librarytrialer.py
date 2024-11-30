from librarytrial import morphological_pipeline

# Custom transformations and data
data = ["quantum", "morph"]
transformations = [
    lambda x: x[::-1].upper(),
    lambda x: x[::-1].upper()
]
energy_func = lambda x: len(x)

# Process the data
result, (high_energy, low_energy) = morphological_pipeline(
    data, transformations, energy_func
)

for item in result:
    if not energy_func == energy_func(item):
        print(item)
    else:
        print("Decoherent item: ", item)