with open('input') as f:
    line = f.read().strip()

W = 25
H = 6

LSIZE = W * H
n_layers = int(len(line) / LSIZE)
layers = [line[x*LSIZE:(x+1)*LSIZE] for x in range(n_layers)]

min_layer = min(layers, key=lambda x: x.count("0"))

print(min_layer)
print(min_layer.count("1") * min_layer.count("2"))
