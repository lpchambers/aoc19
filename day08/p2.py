with open('input') as f:
    line = f.read().strip()

W = 25
H = 6

# TEST
# line = "0222112222120000"
# W = 2
# H = 2

LSIZE = W * H
n_layers = int(len(line) / LSIZE)
layers = [line[x*LSIZE:(x+1)*LSIZE] for x in range(n_layers)]

image = ""
for pos in range(LSIZE):
    for layer in layers:
        if layer[pos] != "2":
            image += layer[pos]
            break

image = image.replace("1", "*").replace("0", " ")
for row in range(H):
    print(image[W*row:W*(row+1)])
